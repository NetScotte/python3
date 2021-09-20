# -*- coding: utf-8 -*-
"""
功能：练习paramiko功能
设计：
    执行命令
    上传文件
    下载文件
    作为服务端
备注：
时间：
"""
import paramiko
import os


class MyParamiko:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.client = None

    def connect(self, host=None, user=None, password=None):
        if not host:
            host = self.host
        if not user:
            user = self.user
        if not password:
            password = self.password

        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        self.client.connect(host, username=user, password=password)
        return self.client

    def exec_command(self, command):
        self.connect()
        stdin, stdout, stderr = self.client.exec_command(command)
        error_info = self.__b2s(stderr.read())
        out_info = self.__b2s(stdout.read())
        self.client.close()
        if error_info:
            raise Exception(error_info)
        else:
            return out_info

    def __b2s(self, obj):
        return obj.decode("utf-8") if isinstance(obj, bytes) else obj

    def __s2b(self, obj):
        return obj.encode("utf-8") if isinstance(obj, str) else obj

    def download_file(self, remote, local=None, binary=False):
        if not local:
            local = os.path.basename(remote)
        self.connect()
        sftp_client = self.client.open_sftp()
        with open(local, "wb") as localfile:
            with sftp_client.file(remote, "r") as remotefile:
                if binary:
                    localfile.write(remotefile.read())
                else:
                    localfile.write(self.__b2s(remotefile.read()))
        self.client.close()

    def upload_file(self, local, remote, binary=False):
        if not os.path.isfile(local):
            raise Exception("no such file: {}".format(local))
        self.connect()
        sftp_client = self.client.open_sftp()
        with open(local, "rb") as localfile:
            with sftp_client.file(remote, "w") as remotefile:
                if binary:
                    remotefile.write(localfile.read())
                else:
                    remotefile.write(self.__s2b(localfile.read()))
        self.client.close()


if __name__ == "__main__":
    myparamiko = MyParamiko("192.168.56.101", "root", "123lloi")
    for command in ["hostname", "netstat", "ls -al /root"]:
        print(myparamiko.exec_command(command))



