from django.db import models

# Create your models here.
import datetime

from utils import renameImg


class SourcesCore(models.Model):
    SOURCES_TYPE = (
        (1, "视频资源"),
        (2, "专业资源"),
        (3, "软件资源"),
        (0, "其他资源"),
    )
    id=models.IntegerField(primary_key=True,verbose_name="资源ID")
    sourcename=models.CharField(max_length=100,verbose_name='资源名称')
    sourceurl=models.URLField(verbose_name="资源地址",null=True,blank=True,help_text="可不填，会自动从资源描述里读取")
    code=models.CharField(max_length=20,verbose_name="提取码",null=True,blank=True,help_text="可不填，会自动从资源描述里读取")
    sourcedesc = models.CharField(max_length=200, null=True,blank=True,verbose_name='综合描述', help_text="默认是百度云的资源，如果不是，上面两个请填写")
    question_type = models.IntegerField(choices=SOURCES_TYPE, verbose_name="资源类型", help_text="资源类型", default=0)
    source_img=models.ImageField(null=True,blank=True,upload_to="sources/images/",default="sources/images/default.png",storage=renameImg.ImageStorage(),verbose_name="资源图片")
    send_time=models.DateField(default=datetime.datetime.now,verbose_name='添加时间')

    def save(self, *args, **kwargs):
        if self.sourceurl is None:
            abc = self.sourcedesc.split()
            urllink = abc[0].split("链接:")
            urlcode = abc[-1].split("密码:")
            self.sourceurl=urllink[-1]
            self.code=urlcode[-1]
        else:
            pass
        return super(SourcesCore, self).save(*args, **kwargs)

    class Meta:
        verbose_name="资源集合"
        verbose_name_plural=verbose_name
# 因为有API有次数限制
class SourceLimit(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name="ID")
    num_count=models.IntegerField(default=50,verbose_name="次数")
    limit_time=models.DateField(default=datetime.date.today,verbose_name='有效时间')

    class Meta:
        verbose_name="次数管理"
        verbose_name_plural=verbose_name