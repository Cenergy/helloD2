from django.shortcuts import render

# Create your views here.
import json
import os
import uuid
import base64
import datetime
import pandas as pd
from django.views import View
from django.http import HttpResponse


from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection


from aip import AipOcr
from helloD2.settings import BAIDU_APP_ID, BAIDU_API_KEY, BAIDU_SECRET_KEY

sysfile = os.path.abspath('.')


class SourcesUpload(APIView):
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
            stick_img = request.POST.get("stick_img", False)
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
                        "id": upload_img_uuid
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


class ImageUpload(APIView):
    def get(self, request):
        try:
            reginfs = {
                "code": 200,
                "message": "success",
                "data": "hello"
            }
        except:
            reginfs = {
                "code": 400,
                "message": "failed",
                "data": "注册失败"
            }
        return Response(reginfs)

    def post(self, request):
        # 上传图片的处理
        try:
            stick_img = request.data.get("stick_img", None)
            if stick_img:
                upload_img_uuid = (str(uuid.uuid1())).replace("-", "")
                upload_img_path = sysfile + '/static/img2word/' + upload_img_uuid + '.jpg'
                img_path = base64.b64decode(stick_img.split(',')[-1])
                with open(upload_img_path, 'wb') as f:
                    f.write(img_path)
                reginfs = {
                    "code": 200,
                    "message": "success",
                    "data": {
                        "id": upload_img_uuid
                    }
                }
            else:
                reginfs = {
                    "code": 400,
                    "message": "failed",
                    "data": '上传失败!!'
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
        if img_uuid == None:
            reginfs = {
                "code": 400,
                "message": "failed",
                "data": "失败"
            }
        else:
            relative_img_path = '/static/img2word/' + img_uuid + '.jpg'
            try:
                options = {
                    'detect_direction': 'true',
                    'language_type': 'CHN_ENG',
                }
                img_target_path = sysfile + relative_img_path
                aipOcr = AipOcr(BAIDU_APP_ID, BAIDU_API_KEY, BAIDU_SECRET_KEY)
                result = aipOcr.webImage(
                    self.get_file_content(img_target_path), options)
                statusCode = 200
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
            imginfo["img_path"] = relative_img_path
            reginfs = {
                "code": statusCode,
                "message": "success",
                "data": imginfo
            }
        return Response(reginfs)

    def delete(self, request):
        img_uuid = request.query_params.get("id", None)
        if img_uuid == None:
            reginfs = {
                "code": 400,
                "message": "failed",
                "data": "失败"
            }
        else:
            relative_img_path = '/static/img2word/' + img_uuid + '.jpg'
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

    def get_file_content(self, filepath):
        with open(filepath, 'rb') as fp:
            return fp.read()


class ImgtoExcel(APIView):
    def delete(self, request):
        try:
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

    def get(self, request):
        # 图片的处理
        # h获取图片的路径

        img_uuid = request.query_params.get("id", None)
        if img_uuid == None:
            reginfs = {
                "code": 400,
                "message": "failed",
                "data": "失败"
            }
        else:
            relative_img_path = '/static/img2word/' + img_uuid + '.jpg'
            unknownimgpath = sysfile + relative_img_path
            options = {
                'detect_direction': 'true',
                'language_type': 'CHN_ENG',
            }
            picUrl = "error"
            try:
                aipOcr = AipOcr(BAIDU_APP_ID, BAIDU_API_KEY, BAIDU_SECRET_KEY)
                result = aipOcr.tableRecognitionAsync(
                    self.get_file_content(unknownimgpath), options)
                starttime = datetime.datetime.now()
                # api-1
                sub_one_sql = "UPDATE 'sources_sourcelimit' SET num_count=num_count-1"
                sub_one_cursor = connection.cursor()
                sub_one_cursor.execute(sub_one_sql)
                while True:
                    try:
                        requestId = result["result"][0]["request_id"]
                        aaa = aipOcr.getTableRecognitionResult(
                            requestId, options)
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
                    excel_json = {}
                    excel_source = pd.read_excel(picUrl)
                    relative_excel_path = "/static/img2word/" + img_uuid + ".xls"
                    excel_name = sysfile+"/static/img2word/" + img_uuid + ".xls"
                    excel_source.to_excel(excel_name)
                    excel_html = excel_source.to_html(classes='layui-table')
                    excel_json["excel_html"] = excel_html
                    excel_json["img_uuid"] = img_uuid
                    excel_json["imgpath"] = relative_img_path
                    excel_json["excelpath"] = relative_excel_path
                    row, col = excel_source.shape
                    if row == 0 or col == 0:
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

    def get_file_content(self, filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()
