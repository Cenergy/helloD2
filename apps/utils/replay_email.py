# -*-coding:utf-8 -*-
__author__ = 'Cenergy'
__date__ = '30/9/18 上午11:58'

import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 第三方 SMTP 服务
mail_host = "smtp.qq.com"  # 设置服务器
mail_user = "aigiser@foxmail.com"  # 用户名
mail_pass = "jmpfewnbvyscfjcd"  # 口令,QQ邮箱是输入授权码，在qq邮箱设置 里用验证过的手机发送短信获得，不含空格
sender = 'aigiser@foxmail.com'

def  common_reply_email(email,suggest,content):
    email_body= "<h3>关于您提出的<span style='color:blue'>"+suggest+"</span>的相关建议或意见，回复如下：<p>"+content+"</p><p>有空常来<a href='https://www.aigisss.com/'>https://www.aigisss.com</a></p><p>感谢您的支持</p></h3>"
    message = MIMEText(email_body, 'html', 'utf-8')
    message['From'] = Header("AIGIS网", 'utf-8')
    try:
        subject = 'AIGIS网'
        message['Subject'] = Header(subject, 'utf-8')
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, [email], message.as_string())
        smtpObj.quit()
    except smtplib.SMTPException as e:
        print(e)