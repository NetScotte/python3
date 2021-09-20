#  -*- coding:utf-8-*-
import os
import requests
from scrapy import Spider, Request
from contextlib import closing
import json
from LightupScrapy.utils import middleware_utils
from urllib.parse import unquote
from microservice import feignclient
from LightupScrapy.rabbitmq import send
import time


class DouYinSpider(Spider):
    name = "DouYinID"
    allowed_domains = ['*']
    start_urls = ['https://aweme.snssdk.com/aweme/v1/discover/search/?']

    keyword = None
    search_id = None
    proxy = None
    user_agent = None

    def __init__(self, keyword=None, search_id=None, *args, **kwargs):
        super(DouYinSpider, self).__init__(*args, **kwargs)
        if keyword:
            self.keyword = keyword
        if search_id:
            self.search_id = search_id

        self.logger.debug('keyword is : ' + unquote(self.keyword, encoding='UTF-8'))
        # self.logger.debug('search_id is :' + self.search_id)

        """
        if kwargs:
            print('kwargs is : ' + str(kwargs))
            self.keyword = kwargs.get('keyword')
            self.search_id = kwargs.get('search_id')
        """

        self.proxy = middleware_utils.get_random_proxy()
        self.user_agent = middleware_utils.get_random_user_agent()
        self.headers = {
            "User-Agent": "Aweme/2.8.0 (iPhone; iOS 11.0; Scale/2.00)",
        }

        self.API = "https://api.appsign.vip:2688"
        self.APPINFO = {
            "version_code": "2.9.1",
            "app_version": "2.9.1",
            "channel": "App Stroe",
            "app_name": "aweme",
            "build_number": "29101",
            "aid": "1128",
        }
        self.cover_img_list = list()
        self.url_list = list()
        self.orm_list = list()
        self.dada_list = list()

    # 获取Token       有效期60分钟
    def GetToken(self):
        resp = requests.get(self.API + "/token/douyin/version/2.7.0").json()
        token = resp['token']
        return token

    # 获取新的设备信息  有效期60分钟永久
    def GetDevice(self):
        resp = requests.get(self.API + "/douyin/device/new/version/2.7.0").json()
        device_info = resp['data']
        return device_info

    # 拼装参数
    def params2str(self, params):
        query = ""
        for k, v in params.items():
            query += "%s=%s&" % (k, v)
        query = query.strip("&")
        return query

    # 使用拼装参数签名
    def GetSign(self, token, query):
        if isinstance(query, dict):
            query = self.params2str(query)
        resp = requests.post(self.API + "/sign", json={"token": token, "query": query}).json()
        sign = resp['data']
        return sign

    # 视频下载
    def Video_Downloader(self, video_url, video_name):
        size = 0
        with closing(requests.get(video_url, headers=self.headers, stream=True)) as response:
            chunk_size = 1024
            if response.status_code == 200:
                try:
                    with open(video_name, 'wb') as file:
                        for data in response.iter_content(chunk_size=chunk_size):
                            file.write(data)
                            size += len(data)
                            file.flush()
                except Exception as e:
                    pass

    # 封面下载
    def Img_Downloader(self, img_url, img_nme):
        headers = {
            "User-Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 69.0.3497.92Safari / 537.36"
        }
        r = requests.get(img_url, headers=headers)
        with open(img_nme, 'wb') as f:
            f.write(r.content)

    # 文件上传
    # def upload(self, path):
    #     client = feignclient.FeignClient('192.168.0.212', '8500', 'cdn-service')
    #     result = client.upload('/cdn/upload', file=path)
    #     return result

    # 获得视频和封面的链接
    def get_video_cover_list(self, uid):
        os.chdir('F:\shipin\知名抖音ID')
        if self.keyword not in os.listdir():
            os.mkdir(self.keyword)
        has_more = 1
        token = self.GetToken()
        device_info = self.GetDevice()
        params = {
            "iid": device_info['iid'],
            "idfa": device_info['idfa'],
            "vid": device_info['vid'],
            "device_id": device_info['device_id'],
            "openudid": device_info['openudid'],
            "device_type": device_info['device_type'],
            "os_version": device_info['os_version'],
            "os_api": device_info['os_api'],
            "screen_width": device_info['screen_width'],
            "device_platform": device_info['device_platform'],
            "version_code": self.APPINFO['version_code'],
            "channel": self.APPINFO['channel'],
            "app_name": self.APPINFO['app_name'],
            "build_number": self.APPINFO['build_number'],
            "app_version": self.APPINFO['app_version'],
            "aid": self.APPINFO['aid'],
            "ac": "WIFI",
            "pass-region": "1",
            "count": "12",
            "max_cursor": "0",
            "user_id": uid,
        }
        while has_more:
            sign = self.GetSign(token, params)
            params['mas'] = sign['mas']
            params['as'] = sign['as']
            params['ts'] = sign['ts']
            url = 'https://api.amemv.com/aweme/v1/aweme/post/?'
            for key, value in params.items():
                query = '{}={}&'.format(key, value)
                url += query
            response = requests.get(url, headers=self.headers)
            self.dada_list.append(response.text)
            data = json.loads(response.text)
            has_more = data['has_more']
            aweme_list = data['aweme_list']
            print(len(self.url_list))
            for aweme in aweme_list:
                try:
                    video_url = aweme['video']['download_addr']['url_list'][0]
                    cover_img_url = aweme['video']['cover']['url_list'][0]
                    self.url_list.append(video_url)
                    self.cover_img_list.append(cover_img_url)
                except Exception as e:
                    pass

            if not has_more:
                text_name = self.keyword + '.txt'
                file_path = os.path.join(self.keyword, text_name)
                with open(file_path, 'w', encoding='GB18030') as f:
                    f.write(str(self.dada_list))

            params['max_cursor'] = data['max_cursor']

    # 下载和上传
    def download_upload(self):
        print(len(self.url_list))
        for video_url in self.url_list:
            index = self.url_list.index(video_url)
            img_url = self.cover_img_list[index]
            img_name = str(index + 1) + '.jpg'
            video_name = str(index + 1) + '.mp4'
            print(os.path.join(self.keyword, video_name))
            if os.path.isfile(os.path.join(self.keyword, video_name)):
                pass
            else:
                self.Video_Downloader(video_url, os.path.join(self.keyword, video_name))
                self.Img_Downloader(img_url, os.path.join(self.keyword, img_name))
                # video_result = self.upload(os.path.join(self.keyword, video_name))
                # video_result = json.loads(video_result)
                # video_url_return = video_result['url']
                # 
                # img_result = self.upload(os.path.join(self.keyword, img_name))
                # img_result = json.loads(img_result)
                # img_url_return = img_result['url']
                # 
                # data = {'video': video_url_return, 'posterUrl': img_url_return}
                # send.send('THIRD_VIDEO', str(data))
                # orm_dict = str({video_name: video_url_return, img_name: img_url_return}) + "\n"
                # orm_text = "orm.text"
                # text_path = os.path.join(self.keyword, orm_text)
                # with open(text_path, 'a', encoding='GB18030') as f:
                #     with open(text_path, 'r') as foo:
                #         if orm_dict not in foo.readlines():
                #             f.write(orm_dict)

    def start_requests(self):
        print('start request ... ')
        # meta = {'proxy': self.proxy}
        print('proxy is : ' + str(self.proxy))

        token = self.GetToken()
        device_info = self.GetDevice()
        params = {
            "iid": device_info['iid'],
            "idfa": device_info['idfa'],
            "vid": device_info['vid'],
            "device_id": device_info['device_id'],
            "openudid": device_info['openudid'],
            "device_type": device_info['device_type'],
            "os_version": device_info['os_version'],
            "os_api": device_info['os_api'],
            "screen_width": device_info['screen_width'],
            "device_platform": device_info['device_platform'],
            "version_code": self.APPINFO['version_code'],
            "channel": self.APPINFO['channel'],
            "app_name": self.APPINFO['app_name'],
            "build_number": self.APPINFO['build_number'],
            "app_version": self.APPINFO['app_version'],
            "aid": self.APPINFO['aid'],
            "ac": "WIFI",
            "pass-region": "1",
            "count": "20",
            "cursor": "0",
            "is_pull_refresh": "0",
            "search_source": "discover",
            "type": "1",
            "hot_search": "0",
            "keyword": self.keyword,
        }

        sign = self.GetSign(token, params)
        params['mas'] = sign['mas']
        params['as'] = sign['as']
        params['ts'] = sign['ts']
        url = 'https://aweme.snssdk.com/aweme/v1/discover/search/?'
        for key, value in params.items():
            query = '{}={}&'.format(key, value)
            url += query
        yield Request(url, headers=self.headers)

    def parse(self, response):
        data = json.loads(response.text)
        uid = data['user_list'][0]['user_info']['uid']
        self.get_video_cover_list(uid)
        self.download_upload()
