from django.test import TestCase

# Create your tests here.

import smtplib
from email.mime.text import MIMEText
from email.header import Header
import random
from users.models import EmailVerifyRecord

# 第三方 SMTP 服务
mail_host = "smtp.qq.com"  # 设置服务器
mail_user = "673598118@qq.com"  # 用户名
mail_pass = "olxthuaragspbfic"  # 口令,QQ邮箱是输入授权码，在qq邮箱设置 里用验证过的手机发送短信获得，不含空格
sender = 'cenergy@foxmail.com'



def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def  register_send_email(email,type_code="register"):
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.type_code = type_code
    email_record.save()
    if type_code == "register":
        email_body= "<h3>请点击下面的链接激活你的账号:<p>" \
                    "<a>http://localhost:8000/active/"+code+"</a></p></h3>"
        message = MIMEText(email_body, 'html', 'utf-8')
        message['From'] = Header("AIGIS网", 'utf-8')
        try:
            subject = 'AIGIS账户激活链接'
            message['Subject'] = Header(subject, 'utf-8')
            smtpObj = smtplib.SMTP_SSL(mail_host, 465)
            smtpObj.login(mail_user, mail_pass)
            smtpObj.sendmail(sender, [email], message.as_string())
            smtpObj.quit()
        except smtplib.SMTPException as e:
            print(e)
    elif type_code == "forget":
        email_body = "<h3>大侠，密码太多容易忘记? 点击以下链接，再战江湖！----------><p>" \
                     "<a>http://localhost:8000/reset/" + code + "</a></p></h3>"
        message = MIMEText(email_body, 'html', 'utf-8')
        message['From'] = Header("AIGIS网", 'utf-8')
        try:
            subject = 'AIGIS账户密码重置密码'
            message['Subject'] = Header(subject, 'utf-8')
            smtpObj = smtplib.SMTP_SSL(mail_host, 465)
            smtpObj.login(mail_user, mail_pass)
            smtpObj.sendmail(sender, [email], message.as_string())
            smtpObj.quit()
        except smtplib.SMTPException as e:
            print(e)

if __name__ == '__main__':
    register_send_email('673598118@qq.com',type_code ="forget")