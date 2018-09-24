from django.shortcuts import render

# Create your views here.
import json,os,uuid,datetime
from django.views import View
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.http import StreamingHttpResponse
from django.db import connection

from utils.get_sources import get_source, get_source_by_id
from utils.tuling_answer import get_tuling_answer
from .models import SourcesCore
from .serializers import SourcesCoreSerializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,mixins,generics,viewsets,filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication
from rest_framework.throttling import AnonRateThrottle,UserRateThrottle

from aip import AipOcr
from  helloD2.settings import BAIDU_APP_ID,BAIDU_API_KEY,BAIDU_SECRET_KEY

import pandas as pd


class WechatTalk(View):
    def get(self, request):
        return render(request, "sources/talk.html", {})


class QueryWechat(View):
    def get(self, request):
        return render(request, "sources/talk.html", {})

    def post(self, request):
        source = request.POST.get("msg")
        num_id = int(request.POST.get("num_id", -1))
        content = []
        if num_id != -1:
            data_dict = get_source_by_id(num_id)
            for k, v in data_dict.items():
                this_value = "{0}的百度云盘<a href={1}>{2}</a>".format(v["sourcename"], v["sourceurl"], v["sourcedesc"])
                content.append(this_value)
        else:
            data_count, data_dict = get_source(source)
            if data_count > 1:
                content.append("相关类似资源如下：<br>")
                for k, v in data_dict.items():
                    this_value = "<a  href='#'  class='source_answer' onclick=showAsk({0},'{1}')>{2}</a></br>".format(
                        v["id"], v["sourcename"], v["sourcename"])
                    content.append(this_value)
            elif data_count == 1:
                for k, v in data_dict.items():
                    this_value = "{0}的百度云盘<a href={1}>{2}</a>".format(v["sourcename"], v["sourceurl"], v["sourcedesc"])
                    content.append(this_value)
            else:
                tuling_answer = get_tuling_answer(source)
                content.append(tuling_answer)
        content = '\n'.join(content)
        try:
            reginfs = {
                "code": 200,
                "message": "success",
                "data": content
            }
        except:
            reginfs = {
                "code": 400,
                "message": "failed",
                "data": "失败"
            }
        return JsonResponse(reginfs, content_type='application/json')


class SourcesUpload(View):
    def get(self, request):
        print(request.GET)
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

    def post(self, request):
        # 上传图片的处理
        try:
            f = request.FILES["file"]
            sysfile = os.path.abspath('.')
            unknown_img_uuid = (str(uuid.uuid1())).replace("-", "")
            imgpath=unknown_img_uuid
            unknownimgpath = sysfile + '/static/img2word/' + imgpath+'.jpg'
            with open(unknownimgpath, 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
            request.session["imgpath"] = imgpath
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
class ImgtoWords(View):
    def get(self, request):
        try:
            sysfile = os.path.abspath('.')
            imgpath = request.session.get("imgpath")
            unknownimgpath = sysfile + '/static/img2word/' + imgpath + '.jpg'
            os.remove(unknownimgpath)
            reginfs = {
                "code": 444,
                "message": "success",
                "data": "hello"
            }
        except:
            reginfs = {
                "code": 222,
                "message": "failed",
                "data": "失败"
            }
        return HttpResponse(json.dumps(reginfs), content_type='application/json')
    def post(self, request):
        # 图片的处理
        # h获取图片的路径
        imgpath = request.session.get("imgpath")
        sysfile = os.path.abspath('.')
        unknownimgpath = sysfile + '/static/img2word/' + imgpath + '.jpg'
        options = {
            'detect_direction': 'true',
            'language_type': 'CHN_ENG',
        }
        try:
            aipOcr = AipOcr(BAIDU_APP_ID, BAIDU_API_KEY, BAIDU_SECRET_KEY)
            result = aipOcr.webImage(self.get_file_content(unknownimgpath), options)
            if result["words_result_num"] == 0:
                vector_word = "图中没有文字或未能识别"
            else:
                pic_words = []
                for i in result["words_result"]:
                    pic_words.append(i["words"])
                pic_words=[('<p>'+i+'</p>') for i in pic_words]
                vector_word = ''.join(pic_words)
        except:
            vector_word = "图中没有文字或未能识别"
        imginfo={}
        imginfo["vector_words"] = vector_word
        imginfo["imgpath"]='/static/img2word/' + imgpath + '.jpg'
        try:
            reginfs = {
                "code": 400,
                "message": "success",
                "data": imginfo
            }
        except:
            reginfs = {
                "code": 200,
                "message": "failed",
                "data": "失败"
            }
        return HttpResponse(json.dumps(reginfs), content_type='application/json')

    def get_file_content(self,filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()
def img2wordRes(request):
    return render(request, "sources/img2wordRes.html", {})

class ImgtoExcel(View):
    def get(self, request):
        try:
            sysfile = os.path.abspath('.')
            imgpath = request.session.get("imgpath")
            print(imgpath)
            unknownimgpath = sysfile + '/static/img2word/' + imgpath + '.jpg'
            excel_name = sysfile + "/static/img2word/" + imgpath + ".xls"
            os.remove(unknownimgpath)
            os.remove(excel_name)
            reginfs = {
                "code": 444,
                "message": "success",
                "data": "hello"
            }
        except:
            reginfs = {
                "code": 222,
                "message": "failed",
                "data": "失败"
            }
        return HttpResponse(json.dumps(reginfs), content_type='application/json')
    def post(self, request):
        # 图片的处理
        # h获取图片的路径
        imgpath = request.session.get("imgpath")
        sysfile = os.path.abspath('.')
        unknownimgpath = sysfile + '/static/img2word/' + imgpath + '.jpg'
        options = {
            'detect_direction': 'true',
            'language_type': 'CHN_ENG',
        }
        picUrl = "error"
        try:
            aipOcr = AipOcr(BAIDU_APP_ID, BAIDU_API_KEY, BAIDU_SECRET_KEY)
            result = aipOcr.tableRecognitionAsync(self.get_file_content(unknownimgpath), options)
            starttime = datetime.datetime.now()
            #api-1
            sub_one_sql = "UPDATE 'sources_sourcelimit' SET num_count=num_count-1"
            sub_one_cursor = connection.cursor()
            sub_one_cursor.execute(sub_one_sql)
            while True:
                try:
                    requestId = result["result"][0]["request_id"]
                    aaa = aipOcr.getTableRecognitionResult(requestId, options)
                    picUrl = aaa["result"]["result_data"]
                    if picUrl != '':
                        break
                except:
                    picUrl = "error"
                endtime = datetime.datetime.now()
                if (endtime - starttime).seconds > 20:
                    picUrl = "error"
                    break
            if picUrl == "error":
                os.remove(unknownimgpath)
                reginfs = {
                    "code": 200,
                    "message": "fail1",
                    "data": "fail"
                }
            else:
                excel_json={}
                excel_source = pd.read_excel(picUrl)
                excel_name = sysfile+"/static/img2word/" + imgpath + ".xls"
                excel_source.to_excel(excel_name)
                excel_html=excel_source.to_html(classes='layui-table')
                excel_json["excel_html"]=excel_html
                excel_json["imgpath"]=imgpath
                row,col=excel_source.shape
                if row==0:
                    os.remove(unknownimgpath)
                    os.remove(excel_name)
                    reginfs = {
                        "code": 200,
                        "message": "fail2",
                        "data": "fail"
                    }
                else:
                    reginfs = {
                        "code": 400,
                        "message": "success",
                        "data": excel_json
                    }
        except:
            picUrl = "error"
            os.remove(unknownimgpath)
            reginfs = {
                "code": 200,
                "message": "fail3",
                "data": "fail"
            }
        return HttpResponse(json.dumps(reginfs), content_type='application/json')

    def get_file_content(self,filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

def excel_download(request):
    """
    sql 文件下载
    :param request:
    :return:
    """
    sysfile = os.path.abspath('.')
    imgpath = request.session.get("imgpath")
    the_file_name = imgpath + '.xls'
    filename = sysfile+'/static/img2word/{}'.format(the_file_name)  # 要下载的文件路径
    response = StreamingHttpResponse(readFile(filename))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
    return response


def readFile(filename, chunk_size=512):
    """
    缓冲流下载文件方法
    :param filename:
    :param chunk_size:
    :return:
    """
    with open(filename, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break

#资源获取的restful api接口
class SourcesCoreViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):

    """
    list：商品的分类列表数据
    """
    queryset = SourcesCore.objects.all()
    serializer_class=SourcesCoreSerializers

from rest_framework.views import APIView
from rest_framework.response import Response


class SnippetList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        snippets = SourcesCore.objects.all()
        serializer = SourcesCoreSerializers(snippets, many=True)
        return Response(serializer.data)


