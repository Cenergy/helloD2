from django.shortcuts import render

# Create your views here.
import json,os,uuid,base64
from django.views import View
from django.http import  HttpResponse



from rest_framework.views import APIView
from rest_framework.response import Response


from aip import AipOcr
from  helloD2.settings import BAIDU_APP_ID,BAIDU_API_KEY,BAIDU_SECRET_KEY

sysfile = os.path.abspath('.')

class  SourcesUpload(APIView):
    def get(self, request):
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
        return Response(reginfs)

    def post(self, request):
        # 上传图片的处理
        try:
            stick_img=request.POST.get("stick_img",False)
            upload_img_uuid = (str(uuid.uuid1())).replace("-", "")
            upload_img_path = sysfile + '/static/img2word/' + upload_img_uuid + '.jpg'
            if stick_img:
                img_path = base64.b64decode(stick_img.split(',')[-1])
                with open(upload_img_path, 'wb') as f:
                    f.write(img_path)
                reginfs = {
                    "code": 200,
                    "message": "success",
                    "data": {
                        "id":upload_img_uuid
                    }
                }
            else:
                f = request.FILES["file"]
                with open(upload_img_path, 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)
                reginfs = {
                    "code": 200,
                    "message": "success",
                    "data": {
                        "id": upload_img_uuid
                    }
                }
        except Exception as e:
            reginfs = {
                "code": 400,
                "message": "failed",
                "data": str(e)
            }
        return Response(reginfs)

class ImgtoWords(APIView):
    def get(self, request):
        img_uuid = request.query_params.get("id", None)
        if img_uuid==None:
            reginfs = {
                "code": 400,
                "message": "failed",
                "data": "失败"
            }
        else:
            relative_img_path='/static/img2word/' + img_uuid + '.jpg'
            try:
                options = {
                    'detect_direction': 'true',
                    'language_type': 'CHN_ENG',
                }
                img_target_path = sysfile + relative_img_path
                aipOcr = AipOcr(BAIDU_APP_ID, BAIDU_API_KEY, BAIDU_SECRET_KEY)
                result = aipOcr.webImage(self.get_file_content(img_target_path), options)
                statusCode=200
                if result["words_result_num"] == 0:
                    vector_word = "图中没有文字或未能识别"
                else:
                    pic_words = [i["words"] for i in result["words_result"]]
                    pic_word_data = [(i + '<br>') for i in pic_words]
                    vector_word = ''.join(pic_word_data)
            except:
                statusCode = 204
                vector_word = "不支持的该格式的文字识别！"
            imginfo = {}
            imginfo["vector_words"] = vector_word
            imginfo["img_uuid"] = img_uuid
            imginfo["img_path"]=relative_img_path
            reginfs = {
                "code": statusCode,
                "message": "success",
                "data": imginfo
            }
        return Response(reginfs)

    def delete(self,request):
        img_uuid = request.query_params.get("id", None)
        if img_uuid==None:
            reginfs = {
                "code": 400,
                "message": "failed",
                "data": "失败"
            }
        else:
            relative_img_path='/static/img2word/' + img_uuid + '.jpg'
            delete_img_path = sysfile + relative_img_path
            try:
                os.remove(delete_img_path)
                reginfs = {
                    "code": 200,
                    "message": "success",
                    "data": "success"
                }
            except:
                reginfs = {
                    "code": 400,
                    "message": "failed",
                    "data": "失败"
                }
        return Response(reginfs)

    def get_file_content(self,filepath):
        with open(filepath, 'rb') as fp:
            return fp.read()