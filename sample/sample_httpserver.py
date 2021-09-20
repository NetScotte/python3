# -*- coding: utf-8 -*-
"""
功能：一个最简单的httpserver，包含一些常见的http处理
设计：
    基本的http服务器
    包含了GET方法的处理
    包含了处理请求头
    包含了发送数据
    包含了POST方法的处理
    包含了解析post的数据
参数：
作者: netliu
时间：2019/05/04
备注:
    BaseHTTPRequestHandler带有很多参数
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime
import sys

SERVER_NAME = datetime.now().strftime("%H-%M-%S")


class BaseHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        message = "server: {} provice service\n".format(SERVER_NAME)
        # 获取请求的头部信息
        username = self.headers.get("User", "known")
        print("get username from header: {}".format(username))

        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(message, "utf-8"))

    def do_POST(self):
        print(self.path)
        # 解析数据
        data = self.rfile.read(int(self.headers.get("Content-Length", "0")))
        print(data)
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()


def run(port):
    server_address = ("", port)
    httpd = HTTPServer(server_address, BaseHandler)
    print("listen on {}...".format(server_address))
    httpd.serve_forever()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 8080
    run(port)