# -*-coding:utf-8 -*-
__author__ = 'Cenergy'
__date__ = '4/8/18 下午12:57'



import  random
import string

from users.models import EmailVerifyRecord
from  django.core.mail import send_mail
from helloD2.settings import EMAIL_FROM



def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str
def  register_send_email(email,type_code="register"):
    email_record=EmailVerifyRecord()
    code=random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.type_code = type_code
    email_record.save()
    email_title=""
    email_body=""
    if type_code=="register":
        email_title = "AIGIS账户激活链接"
        email_body = "请点击下面的链接激活你的账号: http://localhost:8000/active/{0}".format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif type_code=="forget":
        email_title = "AIGIS账户密码重置密码"
        email_body = "大侠，密码太多容易忘记? 点击以下链接，再战江湖！---------->  http://localhost:8000/reset/{0}".format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass



















