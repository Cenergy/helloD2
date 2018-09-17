from django.db import models

# Create your models here.
import datetime


class SourcesCore(models.Model):
    SOURCES_TYPE = (
        (1, "视频资源"),
        (2, "专业资源"),
        (3, "软件资源"),
        (0, "其他资源"),
    )
    id=models.IntegerField(primary_key=True,verbose_name="资源ID")
    sourcename=models.CharField(max_length=100,verbose_name='资源名称')
    sourceurl=models.URLField(verbose_name="资源地址",null=True,blank=True)
    code=models.CharField(max_length=20,verbose_name="提取码",null=True,blank=True)
    sourcedesc = models.CharField(max_length=200, null=True,blank=True,verbose_name='综合描述')
    question_type = models.IntegerField(choices=SOURCES_TYPE, verbose_name="资源类型", help_text="资源类型", default=0)
    send_time=models.DateField(default=datetime.datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name="资源集合"
        verbose_name_plural=verbose_name