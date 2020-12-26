import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
# from DjangoUeditor.models import UEditorField

from utils.replay_email import common_reply_email


# Create your models here.
class UserProfile(AbstractUser):
    """
    user information
    """
    LOGIN_TYPE = (
        (0, "未登录"),
        (1, "未人脸认证"),
        (2, "已人脸认证"),
    )
    faceid = models.TextField(verbose_name='用户唯一值', null=True, blank=True)
    user_name = models.TextField(verbose_name='用户名', null=True, blank=True)
    knowfacecode = models.TextField(verbose_name='用户人脸矩阵',default='',null=True, blank=True)
    login_type = models.IntegerField(choices=LOGIN_TYPE, verbose_name="登录类型", help_text="登录类型", default=0)
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name='姓名')
    birthday = models.DateField(null=True, blank=True, verbose_name='出生年月')
    mobile = models.CharField(null=True, blank=True, max_length=11, verbose_name='电话号码')
    gender = models.CharField(max_length=6, choices=(('male', '男'), ('female', '女')), default='male', verbose_name='性别')
    email = models.CharField(max_length=100, null=True, blank=True, verbose_name='邮箱')

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name="验证码")
    email = models.EmailField(max_length=50, verbose_name="邮件")
    type_code = models.CharField(choices=(("register", u"register"), ("forget", u"forget")), max_length=10)
    send_time = models.DateField(default=datetime.datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = "邮件验证码"
        verbose_name_plural = verbose_name


# class Banner(models.Model):
#     title = models.CharField(max_length=100, verbose_name="title")
#     image = models.ImageField(upload_to="banner/%Y/%m", verbose_name="lunbo", max_length=100)
#     url = models.URLField(max_length=200, verbose_name="url")
#     index = models.IntegerField(default=100, verbose_name="index")
#     add_time = models.DateField(default=datetime.datetime.now, verbose_name="time")

#     class Meta:
#         verbose_name = "banner"
#         verbose_name_plural = verbose_name


class Suggestion(models.Model):
    SUGGEST_TYPE = (
        (1, "已答复"),
        (0, "未答复"),
    )
    suggest_name = models.CharField(max_length=100, verbose_name="用户名", null=True, blank=True)
    suggest_content = models.TextField(verbose_name="建议内容", null=False, blank=False)
    email = models.EmailField(max_length=50, verbose_name="邮件地址", null=False, blank=False)
    suggest_type = models.IntegerField(choices=SUGGEST_TYPE, verbose_name="回复类型", help_text="回复类型", default=0)
    reply_content = models.TextField(verbose_name='回复内容', default="", null=True, blank=True)
    add_time = models.DateField(default=datetime.datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户建议"
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        if self.suggest_type == 0:
            pass
        else:
            common_reply_email(self.email, self.suggest_content, self.reply_content)
        # return super(Suggestion, self).delete(*args, **kwargs)
        return super(Suggestion, self).save(*args, **kwargs)

    def __str__(self):
        return self.email


class FaceUser(models.Model):
    id = models.IntegerField(primary_key=True)
    faceid = models.TextField(verbose_name='用户唯一值')
    username = models.TextField(verbose_name='用户名')
    knowfacecode = models.TextField(verbose_name='用户人脸矩阵')

    class Meta:
        verbose_name = "用户人脸"
        verbose_name_plural = verbose_name
