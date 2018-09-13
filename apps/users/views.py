import os,json,uuid,base64
import platform as plat

from django.shortcuts import render, render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from .models import UserProfile, EmailVerifyRecord
from django.db.models import Q
from django.views.generic.base import View
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm
from django.contrib.auth.hashers import make_password
from utils.email_send import register_send_email
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response


from utils.voices import towords


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
    return render(request, "users/test.html", {})

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
        return render(request, "users/index.html", locals())


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/#hello_django')


class LoginView(View):
    def get(self, request):
        return render(request, "users/login.html", locals())

    def post(self, request):
        login_form = LoginForm(request.POST)
        username = request.POST.get("username", "")
        username=username.lower()
        password = request.POST.get("password", "")
        if login_form.is_valid():
            # request.session["username"] = username
            # username = request.session.get("username", " ")

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    request.session["user_name"] = username
                    return HttpResponseRedirect('/')
                    # return render(request, "users/index.html", locals())
                else:
                    return render(request, "users/login.html", {"msg": "用户未激活！"})
            else:
                msg = "密码错误"
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
            username=username.lower()
            if UserProfile.objects.filter(email=username,is_active=True):
                msg = "邮箱已被注册！！"
                return render(request, "users/register.html", locals())
            elif UserProfile.objects.filter(email=username,is_active=False):
                msg = "请激活您的邮箱"
                send_type = "register"
                register_send_email(username, send_type)
                return render(request, "users/register.html", locals())
            password = request.POST.get("password", "")
            user_proflie = UserProfile()
            user_proflie.username = username
            user_proflie.email = username
            user_proflie.is_active = False
            user_proflie.password = make_password(password)
            user_proflie.save()
            send_type = "register"
            register_send_email(username, send_type)
            return render(request, "users/send_success.html", locals())
        else:
            return render(request, "users/register.html", locals())


class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                email=email.lower()
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
        username=username.lower()
        if forget_form.is_valid():
            if UserProfile.objects.filter(email=username):
                email = request.POST.get("email", "")
                if UserProfile.objects.filter(email=username)[0].is_active == 0:
                    msg = "邮箱未被激活"
                    return render(request, "users/forgetpwd.html", locals())
                else:
                    send_type = "forget"
                    register_send_email(email, send_type)
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
                email=email.lower()
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
            email=email.lower()
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
        if True:
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
                "data": voice_words

            }
        else:
            abc = {
                "code": 400,
                "message": "fail!",
                "data": "网络错误"

            }
        try:
            os.remove(voice_path)
        except:
            pass
        return HttpResponse(json.dumps(abc), content_type='application/json')
