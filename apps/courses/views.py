import datetime, base64, uuid, os, datetime

from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.http import StreamingHttpResponse
from django.http import HttpRequest, HttpResponse, JsonResponse
from helloD5.settings import BAIDU_APP_ID, BAIDU_API_KEY, BAIDU_SECRET_KEY
import pandas as pd

from .models import Blog, BlogType

from aip import AipOcr


class OrgView(View):
    def get(self, request):
        return render(request, "courses/org_list.html", {})


# 图像表格转excel

class ImagetoExcel(View):
    def get_file_content(self, filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    def get_excel_url(self, image):
        aipOcr = AipOcr(BAIDU_APP_ID, BAIDU_API_KEY, BAIDU_SECRET_KEY)
        image = self.get_file_content(image)
        hhh = aipOcr.tableRecognitionAsync(image)
        picUrl = "图片中的表格未能识别或者未知错误"
        starttime = datetime.datetime.now()
        while True:
            try:
                requestId = hhh["result"][0]["request_id"]
                aaa = aipOcr.getTableRecognitionResult(requestId)
                picUrl = aaa["result"]["result_data"]
                if picUrl != '':
                    break
            except:
                pass
            endtime = datetime.datetime.now()
            if (endtime - starttime).seconds > 20:
                picUrl = "图片中的表格未能识别或者未知错误"
                break
        return picUrl

    def file_iterator(self, file_name, chunk_size=512):  # 用于形成二进制数据
        with open(file_name, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    def get(self, req):
        pass

    def post(self, request):
        imgbase64 = request.POST.get("imgbase64")
        img = base64.b64decode(imgbase64.split(',')[-1])

        sysfile = os.path.abspath('.')
        unknown_img_uuid = (str(uuid.uuid1())).replace("-", "")
        unknownimgpath = sysfile + '/media/images/' + unknown_img_uuid
        unknownimages = unknownimgpath + '.jpg'
        unknownexcel = unknownimgpath + '.xls'
        with open(unknownimgpath, 'wb') as f:
            f.write(img)
        picRes = self.get_excel_url(unknownimgpath)
        if picRes == "图片中的表格未能识别或者未知错误":
            pass
        else:
            abc = pd.read_excel(picRes, header=1)
            abc.to_excel(unknownexcel)
        the_file_name = unknownexcel
        response = StreamingHttpResponse(self.file_iterator(the_file_name))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)

        return response
def blog(request):
    return render(request, "courses/blog.html", locals())
