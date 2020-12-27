from django.db import models

# Create your models here.
from users.models import UserProfile

# from DjangoUeditor.models import UEditorField
from utils import renameImg



class BlogType(models.Model):
    type_name=models.CharField(max_length=15)

    class Meta:
        verbose_name="文章类型"
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.type_name


class Blog(models.Model):
    title=models.CharField(max_length=50)
    blog_type=models.ForeignKey(BlogType,on_delete=models.DO_NOTHING)
    content=models.TextField(verbose_name='文章', default="", null=True, blank=True)
    author=models.ForeignKey(UserProfile,on_delete=models.DO_NOTHING)
    source_img = models.ImageField(null=True, blank=True, upload_to="blog/images/",
                                   default="blog/images/default.png", storage=renameImg.ImageStorage(),
                                   verbose_name="封面图片")
    created_time=models.DateTimeField(auto_now_add=True)
    last_update_time=models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name="文章"
        verbose_name_plural=verbose_name

    def __str__(self):
        return "<Blog: %s>"%self.title