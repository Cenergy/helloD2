import os
import json
import uuid
import base64
import datetime
import random
import string
import platform as plat

from django.views.generic.base import View
import numpy as np
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import login, authenticate, logout
from rest_framework import status
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth.hashers import make_password
from django.db import connection
import face_recognition
import pandas as pd
from rest_framework import permissions, renderers, viewsets
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView

from utils.email_send import register_send_email, common_send_email, identity_send_email
from .models import UserProfile, EmailVerifyRecord, Suggestion, FaceUser
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm
from utils.voices import towords
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


def page_not_found_view(request,exception,template_name='404.html'):
    return render(request,template_name,status=404)


def server_error_view(request, template_name='500.html'):
    return render(request, template_name,status=500)


def permission_denied_view(request,exception,template_name='403.html'):
    return render(request, template_name, status=403)


class VuePageView(TemplateView):
    template_name = "index.html"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['latest_articles'] = 1
    #     return context


class CustomBackend(ModelBackend):
    """
    custom authenticate
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(
                Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')


class UserRegisterView(APIView):
    def post(self, request):
        """
        参数为图片转为 base64 的字符串
        :param request:
        :return json:
        """
        username = (request.POST.get("email", "")).lower()
        password = request.POST.get("password", "")
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            url_strs = HttpRequest.get_host(request)
            if UserProfile.objects.filter(email=username, is_active=True):
                result = {
                    "code": 214,
                    "message": "邮箱已被注册！！",
                }
                return Response(result)
            elif UserProfile.objects.filter(email=username, is_active=False):
                send_type = "register"
                register_send_email(username, url_strs, send_type)
                result = {
                    "code": 224,
                    "message": "邮箱还没有被激活",
                }
                return Response(result)
            user_proflie = UserProfile()
            user_proflie.username = username
            user_proflie.email = username
            user_proflie.is_active = False
            user_proflie.password = make_password(password)
            user_proflie.save()
            send_type = "register"
            register_send_email(username, url_strs, send_type)
            result = {
                "code": 200,
                "message": "请前往注册邮箱激活",
            }
            return Response(result)
        else:
            result = {
                "code": 211,
                "message": "未知错误",
            }
            return Response(result)


@csrf_exempt
def get_voices(request):
    if request.method == "POST":
        userid = (str(uuid.uuid1())).replace("-", "")
        request.session["userid"] = userid
        url_str = request.POST.get("webmasterfile")
        hello = base64.b64decode(url_str.split(',')[-1])
        voice_path = "./media/voice/" + userid + ".wav"
        with open(voice_path, "wb") as f:
            f.write(hello)
        try:
            reginfs = {
                "code": 400,
                "message": "success",
                "data": "hello"
            }
        except:
            reginfs = {
                "code": 200,
                "message": "failed",
                "data": "注册失败"
            }
        return HttpResponse(json.dumps(reginfs), content_type='application/json')


@csrf_exempt
def BANAJAX(request):
    if request.method == "POST":
        userid = request.session.get("userid")
        voice_path = "./media/voice/" + userid + ".wav"
        system_type = plat.system()
        try:
            if (system_type == 'Linux'):
                from utils.voices import stt
                voice_words = stt.XF_text(voice_path, 16000)
            elif (system_type == 'Windows'):
                from utils.voices import stt_windows
                voice_words = stt_windows.XF_text(voice_path, 16000)
            else:
                voice_words = towords.main(voice_path)
            abc = {
                "code": 200,
                "message": "successs!!",
                "datas": voice_words
            }
        except:
            abc = {
                "code": 400,
                "message": "fail!",
                "data": "网络错误"

            }
        try:
            os.remove(voice_path)
        except:
            pass
        return JsonResponse(abc, content_type='application/json')


# 用户建议或者意见
class UserSuggestion(View):
    def get(self, request):
        pass

    def post(self, request):
        try:
            suggest_email = request.POST.get("suggest_email", "")
            suggest_user = request.POST.get("suggest_user", " ")
            suggest_message = request.POST.get("suggest_message", "")
            suggest_data = Suggestion()
            suggest_data.email = suggest_email
            suggest_data.suggest_name = suggest_user
            suggest_data.suggest_content = suggest_message
            suggest_data.save()
            # 发邮件回复用户已收到
            common_send_email("673598118@qq.com",
                              suggest_email, suggest_message)
            reginfs = {
                "code": 202,
                "message": "success",
                "data": "hello"
            }
        except:
            reginfs = {
                "code": 400,
                "message": "failed",
                "data": "注册失败"
            }
        return HttpResponse(json.dumps(reginfs), content_type='application/json')


# 人脸识别

class RegImage(View):
    def get(self, request):
        pass

    def post(self, request):
        faceid = request.POST.get("faceid")
        user_name = request.session.get("user_name", " ")
        if user_name == " ":
            login_type = 0
        else:
            login_sql = "select * from users_userprofile where email='{email}'".format(
                email=user_name)
            login_data = pd.read_sql(login_sql, connection)
            login_type = login_data["knowfacecode"][0]
            if login_type == '':
                login_type = 1
            else:
                login_type = 2
        sysfile = os.path.abspath('.')
        img = base64.b64decode(faceid.split(',')[-1])
        unknown_img_uuid = (str(uuid.uuid1())).replace("-", "")
        uknownimgpath = sysfile + '/media/face/' + unknown_img_uuid + '.jpg'
        with open(uknownimgpath, 'wb') as f:
            f.write(img)
        faceuser_sql = "SELECT * from 'users_userprofile'"
        all_face_users = pd.read_sql(faceuser_sql, connection)
        all_face_user = all_face_users[all_face_users["knowfacecode"] != ""]
        user_count = len(all_face_user)
        known_faces = all_face_user["knowfacecode"].values
        user_index = list(all_face_user["id"].values)
        fff = [eval(','.join(i.split())) for i in known_faces]
        known_faces = []
        for i in fff:
            known_faces.append(np.array(i))
        # # unkonw的
        face_id = ""
        try:
            unknown_image = face_recognition.load_image_file(uknownimgpath)
            unknown_face_encoding = face_recognition.face_encodings(unknown_image)[
                0]
            results = list(face_recognition.compare_faces(
                known_faces, unknown_face_encoding, tolerance=0.39))
            for i, j in zip(results, user_index):
                if i == True:
                    that_sql = "SELECT * from 'users_userprofile' where id=%d" % j
                    user_result = pd.read_sql(that_sql, connection)
                    face_name = user_result["username"].values[0]
                    match_index = j
                    face_id = user_result["faceid"].values[0]
                    break
                else:
                    face_name = "Unknown"
        except:
            face_name, match_index = "noFace", "notMatch"
        if face_name == "Unknown":
            known_image = face_recognition.load_image_file(uknownimgpath)
            known_face_encoding = face_recognition.face_encodings(unknown_image)[
                0]
            ran_name = ''.join(random.sample(string.ascii_letters, 6))
            faceid = (str(uuid.uuid1())).replace("-", "")
            # newimgpath = sysfile + '/media/face/faceLibrary/'
            # randimgname = newimgpath + faceid + '/' + ran_name + '.jpg'
            # os.renames(uknownimgpath, randimgname)
            # FaceUser.objects.create(username=ran_name, faceid=faceid, knowfacecode=known_face_encoding)
            request.session["userfaceid"] = faceid
            request.session["username"] = ran_name
            user_name = request.session.get("user_name", '')
            request.session["face_code"] = str(known_face_encoding)
            # 库里没脸，分登陆情况
            # 1.未登录，识别到人脸 login_type==0
            if login_type == 0:
                abcs = {
                    "code": 404040,
                    "message": "未登录，识别到人脸",
                    "data": {"usename": "hhh1", "facename": ran_name}
                }
            # 2.登陆，但人脸库中没有login_type==1
            elif login_type == 1:
                abcs = {
                    "code": 204040,
                    "message": "登陆，但人脸库中没有，将进行人脸关联",
                    "data": {"usename": "hhh1", "facename": user_name}
                }
            else:

                # 3.登陆，人脸库中没有,所以这是新的人脸？login_type==2
                abcs = {
                    "code": 202040,
                    "message": "更新人脸？",
                    "data": {"usename": "hhh1", "facename": user_name}
                }
        elif face_name == "noFace":
            abcs = {
                "code": 400,
                "message": "未识别到脸",
                "data": {"usename": "hhh", "error": "不能认别到人脸，请重新拍照"}
            }
        else:
            request.session["userfaceid"] = face_id
            request.session["username"] = face_name
            # 库里有脸，分登陆情况
            # 1.未登录，识别到某个人脸，帮忙登陆 login_type==0
            if login_type == 0:
                abcs = {
                    "code": 404020,
                    "message": "帮忙登陆?",
                    "data": {"usename": "hhh1", "facename": face_name}
                }
            # 2.已登陆，但人脸库中有，login_type==1,这种情况好像是别人的脸
            elif login_type == 1:
                abcs = {
                    "code": 202024,
                    "message": "库里有脸识别到别的脸，切换到别的",
                    "data": {"usename": "hhh1", "facename": face_name}
                }
            # 3.登陆，人脸库中也有,判断是不是同一张脸？不是的话，是否切换账号？login_type==2
            else:
                user_name = request.session.get("user_name", '')
                if face_name == user_name:
                    abcs = {
                        "code": 202020,
                        "message": "库里有脸识别到脸已登录",
                        "data": {"usename": "hhh1", "facename": face_name}
                    }
                else:

                    # face_name = user_result["username"].values[0]
                    abcs = {
                        "code": 202024,
                        "message": "库里有脸识别到别的脸，切换到别的",
                        "data": {"usename": "hhh1", "facename": face_name}
                    }
        try:
            os.remove(uknownimgpath)
        except:
            pass
        return HttpResponse(json.dumps(abcs), content_type='application/json')


# 关联与更新人脸
class FaceLink(View):
    def get(self, request):
        pass

    def post(self, request):
        face_code = str(request.session.get("face_code", '1024'))
        user_name = request.session.get("user_name", '')
        face_id = (str(uuid.uuid1())).replace("-", "")
        ran_name = ''.join(random.sample(string.ascii_letters, 6))
        login_type = 2
        if face_code != '1024' and user_name != '':
            update_face_sql = "UPDATE 'users_userprofile' SET knowfacecode='{0}',faceid='{1}',user_name='{2}',login_type=2 where  username='{3}'".format(
                face_code, face_id, ran_name, user_name)
            update_face_cursor = connection.cursor()
            update_face_cursor.execute(update_face_sql)
            abcs = {
                "code": 200,
                "message": "人脸关联成功",
                "data": {"usename": "hhh1"}
            }
        else:
            abcs = {
                "code": 400,
                "message": "人脸关联失败",
                "data": {"usename": "hhh1"}
            }
        return HttpResponse(json.dumps(abcs), content_type='application/json')


class DeleteFaceView(APIView):
    def get(self, request):
        pass

    def post(self, request):
        login_form = LoginForm(request.POST)
        username = request.POST.get("username", "")
        username = username.lower()
        password = request.POST.get("password", "")
        if login_form.is_valid():
            user = authenticate(username=username, password=password)
            if user is not None:
                delete_face_sql = "UPDATE users_userprofile SET knowfacecode = '',faceid='',login_type=0 WHERE username = '{0}'".format(
                    username)
                delete_face_cursor = connection.cursor()
                delete_face_cursor.execute(delete_face_sql)
                abcs = {
                    "code": 200,
                    "message": "删除成功"
                }
            else:
                abcs = {
                    "code": 401,
                    "message": "密码错误"
                }
        else:
            login_form = login_form
            abcs = {
                "code": 401,
                "message": "删除失败"
            }
        return HttpResponse(json.dumps(abcs), content_type='application/json')


class JwtLoginView(APIView):
    authentication_classes = []
    throttle_classes = []
    # permission_classes = (AllowAny,)

    def post(self, request):
        origin_username = request.data.get("username", "")
        username = origin_username.lower()
        password = request.data.get("password", "")
        login_form = LoginForm(request.data)
        if login_form.is_valid():
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:

                    return Response({
                        "code": 200,
                        "token": "%s" % TokenObtainPairSerializer.get_token(user),
                        "message": "成功登录",
                        "username": user.username,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "code": 400,
                        "message": "用户未激活！"
                    }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "code": 400,
                    "message": "用户名或者密码错误!"
                }, status=status.HTTP_200_OK)
        else:
            return Response({
                "code": 400,
                "message": "无效的表单!"
            }, status=status.HTTP_200_OK)


class JwtRegisterView(APIView):
    def post(self, request):
        """
        参数为图片转为 base64 的字符串
        :param request:
        :return json:
        """
        email = (request.data.get("email", "")).lower()
        username = (request.data.get("username", "")).lower()
        password = request.data.get("password", "")
        origin = request.data.get("origin", "")
        register_form = RegisterForm(request.data)
        if register_form.is_valid():
            if UserProfile.objects.filter(username=username):
                result = {
                    "code": 400,
                    "message": "用户名已被注册！！",
                }
                return Response(result)
            if UserProfile.objects.filter(email=email, is_active=True):
                result = {
                    "code": 400,
                    "message": "邮箱已被激活！！",
                }
                return Response(result)
            elif UserProfile.objects.filter(email=email, is_active=False):
                send_type = "register"
                identity_send_email(email, origin, send_type)
                result = {
                    "code": 200,
                    "message": "邮箱已被注册但未被激活",
                }
                return Response(result)

            user_proflie = UserProfile()
            user_proflie.username = username
            user_proflie.email = email
            user_proflie.is_active = False
            user_proflie.password = make_password(password)
            user_proflie.save()
            send_type = "register"
            identity_send_email(email, origin, send_type)
            result = {
                "code": 200,
                "message": "请前往注册邮箱激活",
            }
            return Response(result)
        else:
            result = {
                "code": 400,
                "message": "表单错误",
            }
            return Response(result)


class JwtForgetPwdView(APIView):
    def post(self, request):
        forget_form = ForgetForm(request.data)
        email = (request.data.get("email", "")).lower()
        origin = request.data.get("origin", "")
        if forget_form.is_valid():
            users_object = UserProfile.objects.filter(email=email)
            if users_object:
                if users_object.filter(is_active=False):
                    result = {
                        "code": 400,
                        "message": "邮箱未被激活"
                    }
                    return Response(result)
                else:
                    send_type = "forget"
                    identity_send_email(email, origin, send_type)
                    result = {
                        "code": 200,
                        "message": "修改密码的链接已发送至您邮箱，请注意查收！"
                    }
                    return Response(result)
            else:
                result = {
                    "code": 400,
                    "message": "邮箱未被注册"
                }
                return Response(result)
        else:
            result = {
                "code": 400,
                "message": "无效的表单 ！！！"
            }
            return Response(result)


class JwtActivatePwdView(APIView):
    def post(self, request):
        email = (request.data.get("email", "")).lower()
        code = request.data.get("code", "")
        all_records = EmailVerifyRecord.objects.filter(code=code, email=email)
        if all_records:
            record = all_records.first()
            email = record.email.lower()
            user = UserProfile.objects.get(email=email)
            user.is_active = True
            user.save()
            result = {
                "code": 200,
                "message": "激活成功"
            }
            return Response(result)
        else:
            exist_user = UserProfile.objects.filter(email=email)
            if exist_user:
                result = {
                    "code": 400,
                    "message": "核验码错误"
                }
            else:
                result = {
                    "code": 400,
                    "message": "邮箱未被注册"
                }
            return Response(result)


class JwtOrderView(APIView):
    def get(self, request):

        return Response({"a": 1})


class JwtResetPwdView(APIView):
    def post(self, request):
        email = (request.data.get("email", "")).lower()
        code = request.data.get("code", "")
        pwd1 = request.data.get("password1", "")
        pwd2 = request.data.get("password2", "")

        if pwd1 != pwd2:
            result = {
                "code": 400,
                "message": "两次密码不一致!"
            }
            return Response(result)
        all_records = EmailVerifyRecord.objects.filter(code=code, email=email)
        if all_records.exists():
            email = email.lower()
            user = UserProfile.objects.get(email=email)
            if not user.is_active:
                user.is_active = True
            user.password = make_password(pwd2)
            user.save()
            result = {
                "code": 200,
                "message": "修改密码成功"
            }
            return Response(result)
        else:
            result = {
                "code": 400,
                "message": "无效的表单！"
            }
            return Response(result)
