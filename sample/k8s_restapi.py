# -*- coding: utf-8 -*-
"""
功能：基于k8s rest api的一些常见方法
设计：
参数：
作者: netliu
时间：
"""
import requests
from urllib.parse import urljoin
import unittest


class K8SApi:
    def __init__(self, token, endpoint):
        self.authorization_value = "Bearer {}".format(token)
        self.endpoint = endpoint

    def easyrequest(self, method, **kwargs):
        method = method.upper()
        self.headers = {
            "Authorization": self.authorization_value
        }
        if method == "GET":
            response = requests.get(headers=self.headers, timeout=30, **kwargs)
        elif method == "POST":
            response = requests.post(headers=self.headers, timeout=30, **kwargs)
        elif method == "PUT":
            response = requests.put(headers=self.headers, timeout=30, **kwargs)
        elif method == "DELETE":
            response = requests.delete(headers=self.headers, timeout=30, **kwargs)
        else:
            raise Exception("unsupported request method")
        if response.status_code == 200:
            return response.content
        else:
            raise Exception(
                "{} {} status: {}, message: {}".format(method, response.url, response.status_code, response.content))

    def get_pods(self, namespace=None):
        if namespace:
            uri = "/api/v1/namespaces/{namespace}/pods".format(namespace=namespace)
        else:
            uri = "/api/v1/pods"
        url = urljoin(self.endpoint, uri)
        response = self.easyrequest("get", url=url, verify=False)
        return response


class K8SApi_test(unittest.TestCase):
    def setUp(self):
        self.token = "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUN5RENDQWJDZ0F3SUJBZ0lCQURBTkJna3Foa2lHOXcwQkFRc0ZBREFWTVJNd0VRWURWUVFERXdwcmRXSmwKY201bGRHVnpNQjRYRFRJd01EVXhOakUwTURnMU9Gb1hEVE13TURVeE5ERTBNRGcxT0Zvd0ZURVRNQkVHQTFVRQpBeE1LYTNWaVpYSnVaWFJsY3pDQ0FTSXdEUVlKS29aSWh2Y05BUUVCQlFBRGdnRVBBRENDQVFvQ2dnRUJBSzk0CjlvcUxzM1RaVnhnazJHbm5TQlIvYTduYWM3SmlQZlhReEtMc3VKS2ZSNTkzZ3lwK2FTcE1wMDA2NDhhTUtyWFMKcDdPUDNUeU10dUpVbDRISGIyWW5yYjB4WXZWWVlvb3ppcTVrZVNRNTlwdTE1dEFlNUhEZXZuWVFyUXJHb3RDTApaM0krZlNpLzdMK2p3OWRsSzVva2tHMkk5U0kveFNDT0trNStEL3hDc2pQZUFRM1UvTzlCMUN1RHFFY0Rjb0M3CmpVOWxmaDRwV2krdWpqL2FuSjZTWThqQmg3SHBPeXU2WlY2SzZCMmFTeTRBQk5yMnRlWGRIenZQc1Q2cDZ0OEkKM2ZlT0l3NjFZdWN0QkNRQk9SL0h5Uis4SlpTa2ZEUEFXMkFPQ2pla0Z0aDg3RHQzb3lZSUNPbDNYQUx5aGJLegpuVzVQdytLZ2JUODcvdktTbnFVQ0F3RUFBYU1qTUNFd0RnWURWUjBQQVFIL0JBUURBZ0trTUE4R0ExVWRFd0VCCi93UUZNQU1CQWY4d0RRWUpLb1pJaHZjTkFRRUxCUUFEZ2dFQkFHa0UvMFFFMW5XcGNDY0pLRHI4THEzdW5HaG0KaitzaXg4aXZTL3A5dzN2RVhZaVV0VnRQY2EyaUVzMjI3MWJ2YXVheGZKQWJaMEN3dlJCUFZ6SG1Tamw4S0M5dwpIZi94UHVPMkVCWFFlczlpZyt5a0J2VFVuWmNnVmdEUHk3dEtDUUFDdVUxUnRoOEZRZ2dDZkZITGsySnRQank3CnJ1M2hmcVFNZnJ6SjBtOHFic2RJUlhyL3NWYVJ6cmZCaU1pQ3JHcXJZUTdxb3BKRDNZU21jS21rM2JBRk10eE4KK2pXSitxbEhUVjIvUk5nT1dNdy94R1FqSFNRaHNuRmR4bnF4bnM3NEV3clFzdWdvYXhZbDRidEl5T3owVkgrZAo5UmVtUXFoR2w2L3MzNnRtYzJwZmFNbHg4MDVqbExhdVo0bHpQdmxMMGhvWkhLZy83bzFRMm05VFZoZz0KLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLQo="
        self.endpoint = "https://192.168.100.192:6443"
        self.api = K8SApi(self.token, self.endpoint)

    def test_get_pods(self):
        pods = self.api.get_pods()
        print(pods)
