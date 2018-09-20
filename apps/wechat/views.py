from django.shortcuts import render

# Create your views here.
import logging
import hashlib
import time
import uuid
import os
import requests
import xml.etree.ElementTree as ET

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from aip import AipOcr
from  helloD2.settings import BAIDU_APP_ID,BAIDU_API_KEY,BAIDU_SECRET_KEY

from utils.get_sources import get_source
from utils.tuling_answer import get_tuling_answer



# django默认开启csrf防护，这里使用@csrf_exempt去掉防护
@csrf_exempt
def weixin_main(request):
    if request.method == "GET":
        # 接收微信服务器get请求发过来的参数
        try:
            signature = request.GET.get('signature', None)
            timestamp = request.GET.get('timestamp', None)
            nonce = request.GET.get('nonce', None)
            echostr = request.GET.get('echostr', None)
            # 服务器配置中的token = 'hello'
            token = "helloworld"
            # 把参数放到list中排序后合成一个字符串，
            # 再用sha1加密得到新的字符串与微信发来的signature对比，
            # 如果相同就返回echostr给服务器，校验通过
            list = [token, timestamp, nonce]
            list.sort()
            list = ''.join(list)
            hashcode = hashlib.sha1(list.encode("utf-8")).hexdigest()
            # 官方文档中的hashlib部分出错
            # list = [token, timestamp, nonce]
            # list.sort()
            # sha1 = hashlib.sha1()
            # map(sha1.update, list)
            # hashcode = sha1.hexdigest()
            if hashcode == signature:
                logging.error(hashcode)
                return HttpResponse(echostr)
            else:
                return HttpResponse("field")
        except Exception as e:
            logging.error('%s' % e)
            return HttpResponse(echostr)
    else:
        webData = request.body
        xmlData = ET.fromstring(webData)
        othercontent = autoreply(request)
        return HttpResponse(othercontent)



#微信服务器推送消息是xml的，根据利用ElementTree来解析出的不同xml内容返回不同的回复信息，
# 就实现了基本的自动回复功能了，也可以按照需求用其他的XML解析方法
def autoreply(request):
    if True:
        webData = request.body
        xmlData = ET.fromstring(webData)
        msg_type = xmlData.find('MsgType').text
        ToUserName = xmlData.find('ToUserName').text
        FromUserName = xmlData.find('FromUserName').text
        CreateTime = xmlData.find('CreateTime').text
        # MsgType = xmlData.find('MsgType').text
        #MsgId = xmlData.find('MsgId').text
        toUser = FromUserName
        fromUser = ToUserName
        print(msg_type)
        if msg_type == 'text':
            MsgContent = xmlData.find('Content').text
            content=get_content(MsgContent)
            content = '\n'.join(content)
            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()
        elif msg_type == 'event':
            MsgEvent = xmlData.find('Event').text
            if MsgEvent=="subscribe":
                content = "终于等到你，小g已在此恭候多时。\n" \
                          "这是一个gis与ai的公众号，您可以输入关键词搜索资源。" \
                          "如输入'arcgis'，小g会为你提供关于arcgis的各种资源。\n" \
                          "您也可以通过语音输入搜索。\n" \
                          "除此之外，小g还能将您发送的图片中的文字读取出来哦。\n" \
                          "最后附上\n <a href='https://www.aigisss.com'>👉 👉 👉 个人小网站👈 👈 👈</a>👈 👈 👈"

            else:
                content = "感谢您的陪伴，请别离开我，告诉我，我改还不行吗[皱眉][皱眉]"
            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()

        elif msg_type == 'image':
            PicUrl=xmlData.find('PicUrl').text
            sysfile = os.path.abspath('.')
            unknown_img_uuid = (str(uuid.uuid1())).replace("-", "")
            unknownimgpath = sysfile + '/media/images/' + unknown_img_uuid + '.jpg'

            img = requests.get(PicUrl)
            with open(unknownimgpath, 'ab') as f:
                f.write(img.content)
            # 初始化文字百度识别分类器
            aipOcr = AipOcr(BAIDU_APP_ID, BAIDU_API_KEY, BAIDU_SECRET_KEY)
            # 定义参数变量
            options = {
                'detect_direction': 'true',
                'language_type': 'CHN_ENG',
            }
            try:
                result = aipOcr.webImage(get_file_content(unknownimgpath), options)
                print(result)
                if result["words_result_num"]==0:
                    vector_word = "图中没有文字或未能识别"
                else:
                    pic_words = []
                    for i in result["words_result"]:
                        pic_words.append(i["words"])
                    pic_words = [('<p>' + i + '</p>') for i in pic_words]
                    vector_word = ''.join(pic_words)
            except:
                vector_word = "图中没有文字或未能识别"
            vector_words = vector_word
            os.remove(unknownimgpath)
            replyMsg = TextMsg(toUser, fromUser, vector_words)
            return replyMsg.send()
        elif msg_type == 'voice':
            content = "语音已收到,谢谢"
            VoiceContent = xmlData.find('Recognition').text
            if VoiceContent is not None:
                voiceContent=["您的语音是：{0}".format(VoiceContent)]
                VoiceContent=VoiceContent.replace('。','')
                content0 = get_content(VoiceContent)
                voiceRes2=voiceContent+content0
                content = '\n'.join(voiceRes2)
                replyMsg = TextMsg(toUser, fromUser, content)
            else:
                replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()
        elif msg_type == 'video':
            content = "视频已收到,谢谢"
            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()
        elif msg_type == 'shortvideo':
            content = "小视频已收到,谢谢"
            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()
        elif msg_type == 'location':
            content = "位置已收到,谢谢"
            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()
        else:
            #msg_type == 'link'
            content = "链接已收到,谢谢"
            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()
    #except Exception as Argment:
    else:
        return "123"


class Msg(object):
    def __init__(self, xmlData):
        self.ToUserName = xmlData.find('ToUserName').text
        self.FromUserName = xmlData.find('FromUserName').text
        self.CreateTime = xmlData.find('CreateTime').text
        self.MsgType = xmlData.find('MsgType').text
        self.MsgId = xmlData.find('MsgId').text


class TextMsg(Msg):
    def __init__(self, toUserName, fromUserName, content):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['Content'] = content

    def send(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{Content}]]></Content>
        </xml>
        """
        return XmlForm.format(**self.__dict)

def get_content(MsgContent):
    content = []
    data_count, data_dict = get_source(MsgContent)
    if data_count > 1:
        content.append("相关类似资源如下：")
        for k, v in data_dict.items():
            this_value = "<a href='{0}?key={1}'>{2}</a>".format("https://www.aigisss.com/sources/wxtalk/",
                                                                v["sourcename"], v["sourcename"])
            content.append(this_value)
    elif data_count == 1:
        for k, v in data_dict.items():
            this_value = "{0}的百度云盘{1}".format(v["sourcename"], v["sourcedesc"])
            content.append(this_value)
    else:
        tuling_answer = get_tuling_answer(MsgContent)
        content.append(tuling_answer)
    return content


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()