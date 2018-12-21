# 此模块用于验证微博登陆

import requests
import json


# 创建微博调用类
class OAuthWB:
    def __init__(self, client_id, client_key, redirect_url):
        self.client_id = client_id
        self.client_key = client_key
        self.redirect_url = redirect_url

    def get_access_token(self, code): # 获取用户token和uid
        # 该url用于POST querystring数据
        url = "https://api.weibo.com/oauth2/access_token"
        querystring = {
            'client_id': self.client_id,
            'client_secret': self.client_key,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirect_url
        }
        # 需要post过去的数据
        response = requests.request("POST", url, params=querystring)
        # 微博返回数据
        # {
        #     "access_token": "ACCESS_TOKEN",
        #     "expires_in": 1234,
        #     "remind_in": "798114",
        #     "uid": "12341234"
        # }
        return json.loads(response.text)

    def get_user_info(self, access_token_data):
        url = 'https://api.weibo.com/2/users/show.json'

        querystring = {
            'uid': access_token_data['uid'],
            'access_token':access_token_data['access_token']
        }

        response = requests.request('GET', url, params=querystring)
        return json.loads(response.text)


