import time  # 设置时间
import requests  # 导入requests库，
import sys  # 导入系统库
import numpy as np
import socket
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
from helloD2.settings import BAIDU_APP_ID, BAIDU_API_KEY, BAIDU_SECRET_KEY, BAIDU_MAP_KEY

sysfile = os.path.abspath('.')

ty = sys.getfilesystemencoding()  # 这个可以获取文件系统的编码形式
timeout = 20


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
        img_uuid = request.query_params.get("id", None)
        if img_uuid == None:
            reginfs = {
                "code": 400,
                "message": "failed",
                "data": "失败"
            }
        else:
            try:
                imgpath = sysfile + '/static/img2word/' + img_uuid + '.jpg'
                excel_name = sysfile + "/static/img2word/" + img_uuid + ".xls"
                os.remove(imgpath)
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
                # sub_one_sql = "UPDATE 'sources_sourcelimit' SET num_count=num_count-1"
                # sub_one_cursor = connection.cursor()
                # sub_one_cursor.execute(sub_one_sql)
                while True:
                    try:
                        requestId = result["result"][0]["request_id"]
                        aaa = aipOcr.getTableRecognitionResult(
                            requestId, options)
                        picUrl = aaa["result"]
                        percent=picUrl["percent"]
                        if picUrl != '' and percent==100:
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
                    picUrl["imgPath"]= unknownimgpath
                    reginfs = {
                            "code": 200,
                            "message": "success",
                            "data": picUrl
                        }
            except:
                picUrl = "error"
                os.remove(unknownimgpath)
                reginfs = {
                    "code": 400,
                    "message": "fail3",
                    "data": "fail"
                }
            return HttpResponse(json.dumps(reginfs), content_type='application/json')

    def get_file_content(self, filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()


def getdata(url):
    try:
        socket.setdefaulttimeout(timeout)
        html = requests.get(url)
        data = html.json()
        if data['results'] != None:
            return data['results']
        return  []
        # time.sleep(1)
    except:
        getdata(url)


class POIbyName(APIView):

    def get(self, request):
        name = request.query_params.get("name", None)
        city = request.query_params.get("city", None)
        print(name,city,"====")
        urls = []  # 声明一个数组列表
        for i in range(0, 20):
            page_num = str(i)
            url = 'http://api.map.baidu.com/place/v2/search?query='+name+'&region=' + \
                city+'&page_size=20&page_num='+str(page_num)+'&output=json&ak='+BAIDU_MAP_KEY
            urls.append(url)
        print('url列表读取完成')

        results=[]
        for url in urls:
            res=getdata(url)
            if res!=[]:
                results+=res
        df = pd.DataFrame(results)
        excel_uuid = (str(uuid.uuid1())).replace("-", "")
        relative_excel_path = "/static/img2word/" + excel_uuid + ".xls"
        excel_path = sysfile+"/static/img2word/" + excel_uuid + ".xls"
        # df['coord'] = ["[{},{}]".format(res["location"]["lng"],res["location"]["lat"]) for res in results]
        df.to_excel(excel_path)

        excel_json={}
        excel_json["excelpath"] = relative_excel_path
        excel_json["id"] = excel_uuid
        excel_json["data"] = results

        reginfs = {
            "code": 200,
            "message": "success",
            "data": excel_json
        }
        return Response(reginfs)

    def post(self, request):
        reginfs = {
            "code": 400,
            "message": "failed",
            "data": str(e)
        }
        return Response(reginfs)


class POIbyRegion(APIView):
    def get(self, request):
        name = request.query_params.get("name", None)
        minLng = request.query_params.get("minLng", None)
        minLat = request.query_params.get("minLat", None)
        maxLng = request.query_params.get("maxLng", None)
        maxLat = request.query_params.get("maxLat", None)

        lng_c=float(maxLng)-float(minLng)
        lat_c=float(maxLat)-float(minLat)

        lng_num=int(lng_c/0.1)+1
        lat_num=int(lat_c/0.1)+1
        # minLng, minLat, maxLng, maxLat
        arr=np.zeros((lat_num+1,lng_num+1,2))
        for lat in range(0,lat_num+1):
            for lng in range(0,lng_num+1):
                arr[lat][lng]=[float(minLng)+lng*0.1,float(minLat)+lat*0.1]

        urls=[]


        bounds='{},{},{},{}'.format(minLat,minLng,maxLat, maxLng)
        for lat in range(0,lat_num):
            for lng in range(0,lng_num):    
                for b in range(0,20):
                    page_num=str(b)
                    url='http://api.map.baidu.com/place/v2/search?query='+name+'&bounds='+bounds+'&page_size=20&page_num='+str(page_num)+'&coord_type=2&output=json&ak='+BAIDU_MAP_KEY
                    urls.append(url)

        results=[]
        for url in urls:
            res=getdata(url)
            if res!=[]:
                results+=res
        df = pd.DataFrame(results)
        excel_uuid = (str(uuid.uuid1())).replace("-", "")
        relative_excel_path = "/static/img2word/" + excel_uuid + ".xls"
        excel_path = sysfile+"/static/img2word/" + excel_uuid + ".xls"
        # df['coord'] = ["[{},{}]".format(res["location"]["lng"],res["location"]["lat"]) for res in results]
        df.to_excel(excel_path)

        excel_json={}
        excel_json["excelpath"] = relative_excel_path
        excel_json["id"] = excel_uuid
        excel_json["data"] = results

        reginfs = {
            "code": 200,
            "message": "success",
            "data": excel_json
        }
        return Response(reginfs)

    def post(self, request):
        reginfs = {
            "code": 400,
            "message": "failed",
            "data": str(e)
        }
        return Response(reginfs)
