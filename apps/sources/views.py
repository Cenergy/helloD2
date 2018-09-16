from django.shortcuts import render

# Create your views here.

from django.views import View
from django.http import HttpRequest, HttpResponse, JsonResponse


from utils.get_sources import get_source
from utils.tuling_answer import get_tuling_answer

class WechatTalk(View):
    def get(self,request):
        return render(request,"sources/talk.html",{})

class QueryWechat(View):
    def get(self,request):
        return render(request,"sources/talk.html",{})
    def post(self,request):
        source = request.POST.get("msg")
        content=[]
        data_count, data_dict = get_source(source)
        if data_count > 1:
            content.append("相关类似资源如下：<br>")
            for k, v in data_dict.items():
                this_value = "<a href='{0}?key={1}' onclick=showAsk({2})>{3}</a></br>".format("http://127.0.0.1:8000/sources/wxtalk/",
                                                                        v["sourcename"],  v["sourcename"],v["sourcename"])
                content.append(this_value)
        elif data_count == 1:
            for k, v in data_dict.items():
                this_value = "{0}的百度云盘<a href={1}>{2}</a>".format(v["sourcename"], v["sourceurl"],v["sourcedesc"])
                content.append(this_value)
        else:
            tuling_answer = get_tuling_answer(source)
            content.append(tuling_answer)
        content = '\n'.join(content)
        try:
            reginfs = {
                "code": 400,
                "message": "success",
                "data": content
            }
        except:
            reginfs = {
                "code": 200,
                "message": "failed",
                "data": "注册失败"
            }
        return JsonResponse(reginfs, content_type='application/json')
