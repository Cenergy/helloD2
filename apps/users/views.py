import os, json, uuid, base64, datetime, random, string
import platform as plat

import pandas as pd
import numpy as np
from django.shortcuts import render, render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from .models import UserProfile, EmailVerifyRecord, Suggestion, FaceUser
from django.db.models import Q
from django.views.generic.base import View
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm
from django.contrib.auth.hashers import make_password
from utils.email_send import register_send_email, common_send_email
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.db import connection

from rest_framework import permissions, renderers, viewsets

from utils.voices import towords
import face_recognition


# custom_error404
def page_not_found(request):
    return render(request, '404.html')


# custom_error500
def page_error(request):
    return render(request, '500.html')


# custom_error403
def permission_denied(request):
    return render(request, '403.html')


def test(request):
    from utils.word_get_pic import getIntPages
    dataList = getIntPages("蔬菜", 1)
    return render(request, "users/test.html", locals())


def map(request):
    return render(request, "users/map.html")


class CustomBackend(ModelBackend):
    """
    custom authenticate
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class IndexView(View):
    def get(self, request):
        user_name = request.session.get("user_name", " ")
        if user_name == " ":
            login_type = 0
        else:
            login_sql = "select * from users_userprofile where email='{email}'".format(email=user_name)
            login_data = pd.read_sql(login_sql, connection)
            login_type = login_data["knowfacecode"][0]
            if login_type == '':
                login_type = 1
            else:
                login_type = 2
        # 判断apide时间有效性
        query_sql = "select * from sources_sourcelimit where id={abc}".format(abc=1)
        all_data = pd.read_sql(query_sql, connection)
        today = datetime.date.today().strftime('%Y-%m-%d')
        if str(all_data["limit_time"][0]) == str(today):
            pass
        else:
            sub_one_sql = "UPDATE 'sources_sourcelimit' SET num_count=50,limit_time='%s'" % today
            sub_one_cursor = connection.cursor()
            sub_one_cursor.execute(sub_one_sql)
        num_count = all_data["num_count"][0]
        return render(request, "users/index.html", locals())


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/#hello_django')


class LoginView(View):
    renderer_classes = [renderers.TemplateHTMLRenderer]
    template_name = "users/login.html"

    def get(self, request):
        return render(request, "users/login.html", locals())

    def post(self, request):
        login_form = LoginForm(request.POST)
        username = request.POST.get("username", "")
        username = username.lower()
        password = request.POST.get("password", "")
        if login_form.is_valid():
            # request.session["username"] = username
            # username = request.session.get("username", " ")

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    request.session["user_name"] = username
                    pre_url = request.session.get("pre_url_path", "/")
                    return redirect(pre_url)
                    # return HttpResponseRedirect('/')
                    # return render(request, "users/index.html", locals())
                else:
                    return render(request, "users/login.html", {"msg": "用户未激活！"})
            else:
                msg = "密码错误!"
                return render(request, "users/login.html", locals())
        else:
            login_form = login_form
            return render(request, "users/login.html", locals())


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "users/register.html", locals())

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = request.POST.get("email", "")
            username = username.lower()
            url_strs = HttpRequest.get_host(request)
            if UserProfile.objects.filter(email=username, is_active=True):
                msg = "邮箱已被注册！！"
                return render(request, "users/register.html", locals())
            elif UserProfile.objects.filter(email=username, is_active=False):
                msg = "请激活您的邮箱"
                send_type = "register"
                register_send_email(username,url_strs,send_type)
                return render(request, "users/register.html", locals())
            password = request.POST.get("password", "")
            user_proflie = UserProfile()
            user_proflie.username = username
            user_proflie.email = username
            user_proflie.is_active = False
            user_proflie.password = make_password(password)
            user_proflie.save()
            send_type = "register"
            register_send_email(username,url_strs,send_type)
            return render(request, "users/send_success.html", locals())
        else:
            return render(request, "users/register.html", locals())


class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                email = email.lower()
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
            return render(request, "users/login.html", locals())
        else:
            return render(request, "users/active_fail.html", locals())


class ForgetPwdView(View):
    def get(self, request):
        username = ""
        forget_form = ForgetForm()
        return render(request, "users/forgetpwd.html", locals())

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        username = request.POST.get("email", "")
        username = username.lower()
        if forget_form.is_valid():
            if UserProfile.objects.filter(email=username):
                email = request.POST.get("email", "")
                if UserProfile.objects.filter(email=username)[0].is_active == 0:
                    msg = "邮箱未被激活"
                    return render(request, "users/forgetpwd.html", locals())
                else:
                    send_type = "forget"
                    url_strs = HttpRequest.get_host(request)
                    register_send_email(email,url_strs,send_type)
                    return render(request, "users/send_success.html", locals())
            else:
                msg = "邮箱未被注册"
                return render(request, "users/forgetpwd.html", locals())
        else:
            return render(request, "users/forgetpwd.html", locals())


class ResetPwdView(View):
    def get(self, request, reset_code):
        all_records = EmailVerifyRecord.objects.filter(code=reset_code)
        if all_records:
            for record in all_records:
                email = record.email
                email = email.lower()
                return render(request, "users/password_reset.html", locals())
        else:
            return render(request, "users/active_fail.html", locals())


class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            email = email.lower()
            if pwd1 != pwd2:
                msg = "两次密码不一致"
                return render(request, "users/password_reset.html", locals())
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            return HttpResponseRedirect("/login/")
        else:
            email = request.POST.get("email", "")
            return render(request, "users/password_reset.html", locals())


class UserinfoView(View):
    def get(self, request):
        return render(request, "users/usercenter-info.html")


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
        print(userid)
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
            print("voice:", voice_words)
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
            common_send_email("673598118@qq.com", suggest_email, suggest_message)
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


class FaceRegView(View):
    def get(self, request):
        return render(request, "users/facereg.html", locals())


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
            login_sql = "select * from users_userprofile where email='{email}'".format(email=user_name)
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
            unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
            results = list(face_recognition.compare_faces(known_faces, unknown_face_encoding, tolerance=0.39))
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
            known_face_encoding = face_recognition.face_encodings(unknown_image)[0]
            ran_name = ''.join(random.sample(string.ascii_letters, 6))
            faceid = (str(uuid.uuid1())).replace("-", "")
            # newimgpath = sysfile + '/media/face/faceLibrary/'
            # randimgname = newimgpath + faceid + '/' + ran_name + '.jpg'
            # os.renames(uknownimgpath, randimgname)
            #FaceUser.objects.create(username=ran_name, faceid=faceid, knowfacecode=known_face_encoding)
            request.session["userfaceid"] = faceid
            request.session["username"] = ran_name
            user_name = request.session.get("user_name", '')
            request.session["face_code"] = str(known_face_encoding)
            # 库里没脸，分登陆情况
            # 1.未登录，识别到人脸 login_type==0
            if login_type==0:
                abcs = {
                    "code": 404040,
                    "message": "未登录，识别到人脸",
                    "data": {"usename": "hhh1", "facename": ran_name}
                }
            # 2.登陆，但人脸库中没有login_type==1
            elif login_type==1:
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
            if login_type==0:
                abcs = {
                    "code": 404020,
                    "message": "帮忙登陆?",
                    "data": {"usename": "hhh1", "facename": face_name}
                }
            # 2.已登陆，但人脸库中有，login_type==1,这种情况好像是别人的脸
            elif login_type==1:
                abcs = {
                    "code": 202024,
                    "message": "库里有脸识别到别的脸，切换到别的",
                    "data": {"usename": "hhh1", "facename": face_name}
                }
            # 3.登陆，人脸库中也有,判断是不是同一张脸？不是的话，是否切换账号？login_type==2
            else:
                user_name = request.session.get("user_name", '')
                if face_name==user_name:
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

class FaceLink(View):
    def get(self,request):
        pass
    def post(self,request):
        face_code=str(request.session.get("face_code",'1024'))
        user_name = request.session.get("user_name", '')
        face_id=(str(uuid.uuid1())).replace("-", "")
        ran_name = ''.join(random.sample(string.ascii_letters, 6))
        login_type=2
        if face_code!='1024'and user_name!='':
            update_face_sql = "UPDATE 'users_userprofile' SET knowfacecode='{0}',faceid='{1}',user_name='{2}',login_type=2 where  username='{3}'".format(face_code,face_id,ran_name,user_name)
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

class FaceLoginView(View):
    renderer_classes = [renderers.TemplateHTMLRenderer]
    template_name = "users/login.html"

    def get(self, request):
        return render(request, "users/login.html", locals())

    def post(self, request):
        login_form = LoginForm(request.POST)
        username = request.POST.get("username", "")
        username = username.lower()
        password = request.POST.get("password", "")
        if login_form.is_valid():
            # request.session["username"] = username
            # username = request.session.get("username", " ")

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    request.session["user_name"] = username
                    pre_url = request.session.get("pre_url_path", "/")
                    abcs = {
                        "code": 200,
                        "message": "登陆成功",
                        "data": {"reurl": pre_url}
                    }
                else:
                    abcs = {
                        "code": 401,
                        "message": "用户未激活",
                        "data": {"reurl": "/login/"}
                    }
            else:
                msg = "密码错误!"
                abcs = {
                    "code": 401,
                    "message": "密码错误",
                    "data": {"reurl": "/login/"}
                }
        else:
            login_form = login_form
            abcs = {
                "code": 401,
                "message": "登陆失败",
                "data": {"reurl": "/login/"}
            }
        return HttpResponse(json.dumps(abcs), content_type='application/json')

# 删除人脸

class DeleteFaceView(View):
    def get(self,request):
        pass
    def post(self,request):
        login_form = LoginForm(request.POST)
        username = request.POST.get("username", "")
        username = username.lower()
        password = request.POST.get("password", "")
        if login_form.is_valid():
            user = authenticate(username=username, password=password)
            if user is not None:
                delete_face_sql="UPDATE users_userprofile SET knowfacecode = '',faceid='',login_type=0 WHERE username = '{0}'".format(username)
                delete_face_cursor = connection.cursor()
                delete_face_cursor.execute(delete_face_sql)
                abcs = {
                    "code": 200,
                    "message": "删除成功",
                    "data": {"reurl": '../'}
                }
            else:
                abcs = {
                    "code": 401,
                    "message": "密码错误",
                    "data": {"reurl": "/login/"}
                }
        else:
            login_form = login_form
            abcs = {
                "code": 401,
                "message": "删除失败",
                "data": {"reurl": "/login/"}
            }
        return HttpResponse(json.dumps(abcs), content_type='application/json')