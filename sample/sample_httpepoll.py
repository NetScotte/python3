#!/usr/bin/python3.5
# -*- coding: utf-8 -*-
import socket
import re
import select


def http_sever(new_socket, recv_data):

    recv_data_list = recv_data.splitlines()
    ret = re.match(r"[^/]+(/[^ ]*)",recv_data_list[0])

    file_name = ""
    if ret:
        file_name = ret.group(1)
        if file_name == "/":
            file_name = "/index.html"

    http_header = ""
    http_body = ""

    try:
        f = open("./html" + file_name, "rb")
    except:
        http_header = "HTTP/1.1 404 NOT FOUND\r\n\r\n"
        http_body = "<h1>Sorry not found</h1>".encode("utf-8")
    else:
        http_body = f.read()
        f.close()
        http_header = "HTTP/1.1 200 OK\r\n\r\n"

    new_socket.send(http_header.encode("utf-8"))
    new_socket.send(http_body)
    new_socket.close()


def main():
    tcp_sever_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sever_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_sever_socket.bind(("",7890))
    tcp_sever_socket.listen(128)
    # 创建epoll对象
    epl = select.poll()

    # 将tcp_sever_socket注册到epoll中
    epl.register(tcp_sever_socket.fileno(), select.POLLIN)

    fd_even_dict = dict()

    while True:
        fd_even_list = epl.poll()  # 默认会堵塞，直到套接字进来
        # 套接字进来,遍历列表获得fd和even.
        for fd, even in fd_even_list:
            # 如果fd和tcp_sever_socket的fd一样,就accept()
            if fd == tcp_sever_socket.fileno():
                new_socket, new_add = tcp_sever_socket.accept()
                # 将新的套接字注册到epl中
                epl.register(new_socket.fileno(), select.POLLIN)
                # 将这个键值对添加到字典中
                fd_even_dict[new_socket.fileno()] = new_socket

            elif even == select.POLLIN:
                # 判断是否发送了数据过来
                recv_data = fd_even_dict[fd].recv(1024).decode("utf-8")
                if recv_data:
                    http_sever(fd_even_dict[fd], recv_data)
                else:
                    fd_even_dict[fd].close()
                    # 从epl中删除
                    epl.unregister(fd)
                    # 从字典中删除键值对
                    del fd_even_dict[fd]


if __name__ == '__main__':
    main()