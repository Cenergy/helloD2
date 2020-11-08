from django.shortcuts import render
import requests
import json
import urllib.parse

from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
clientID = '3b6ace8e2d74edce65bd'
clientSecret = '21ac92ec25d136bc5d628923da40e35e24d1b178'


def github_token(client_id, client_secret, code):
    """
    通过传入的 code 参数，带上client_id、client_secret、和code请求GitHub，以获取access_token
    :param code: 重定向获取到的code参数
    :param client_id: 重定向获取到的client_id参数
    :param client_secret: 重定向获取到的client_secret参数
    :return: 成功返回acces_token；失败返回None；
    """
    token_url = 'https://github.com/login/oauth/access_token?' \
                'client_id={}&client_secret={}&code={}'
    token_url = token_url.format(client_id, client_secret, code) # 这里的client_id、client_secret修改为自己的真实ID与Secret
    header = {
        'accept': 'application/json'
    }
    res = requests.post(token_url, headers = header)
    if res.status_code == 200:
        res_dict = res.json()
        print(res_dict)
        return res_dict['access_token']
    return None


def github_user(access_token):
    """
    通过传入的access_token，带上access_token参数，向GitHub用户API发送请求以获取用户信息；
    :param access_token: 用于访问API的token
    :return: 成功返回用户信息，失败返回None
    """
    user_url = 'https://api.github.com/user'
    access_token = 'token {}'.format(access_token)
    headers = {
        'accept': 'application/json',
        'Authorization': access_token
    }
    res = requests.get(user_url, headers=headers)
    if res.status_code == 200:
        user_info = res.json()
        print(user_info)
        user_name = user_info.get('name', None)
        return user_info
    return None


class SourcesUpload(APIView):
    def get(self, request):
        print(request.query_params,"================")
        code=request.query_params.get("code", None)

        try:
            access_token = github_token(clientID, clientSecret, code)
        except QQErrorExcept:
            return Response({"message": "QQ登录异常，获取授权信息失败"}, status=status.HTTP_400_BAD_REQUEST)
        if access_token:
            user_info = github_user(access_token)  # 向GitHub用户API发送请求获取信息
            if user_info:
                user_name = user_info.get('name', None)
                print(user_name,"=================")
                try:
                    reginfs = {
                        "code": 400,
                        "message": "success",
                        "data": user_name
                    }
                except:
                    reginfs = {
                        "code": 200,
                        "message": "failed",
                        "data": "注册失败"
                    }
                return Response(reginfs)

