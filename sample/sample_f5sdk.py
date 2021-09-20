# -*- coding: utf-8 -*-
"""
功能：
    f5功能测试
设计：
备注：
时间：
"""
import requests
requests.packages.urllib3.disable_warnings()
import re
from f5.bigip import ManagementRoot


class MyBigIp:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.__connect()

    def __connect(self):
        self.bigip = ManagementRoot(self.host, self.user, self.password)

    def get_obj_attr(self, obj):
        return dir(obj)

    def get_organizing_collection_attr(self, org):
        assert org in ["ltm", "gtm", "asm", "net", "sys"], print("no such organizing collection: {}".format(org))
        realobj = eval("self.bigip.cm.{}".format(org))
        for collection in realobj.get_collection():
            url = collection['reference']['link']
            content = re.findall("/(.*)\?", url)[0]

            print(content.split("/")[-1])
        exit(0)
        collections = {collection.name: dir(collection) for collection in realobj.get_collection()}
        return collections

    def get_colelctions_attr(self, supercollection, chilccollection):
        realobj = eval("self.bigip.tm.{}.{}".format(supercollection, chilccollection))
        collections = {collection.name: dir(collection) for collection in realobj.get_collection}
        return collections

    def create_obj(self, obj, data):
        if not self.exists_obj(obj, data):
            obj.create(**data)

    def update_obj(self, obj):
        obj.update()

    def refresh_obj(self, obj):
        obj.refresh()

    def delete_obj(self, obj):
        if self.exists_obj(obj):
            obj.delete()

    def load_obj(self, obj, data):
        return obj.load(data)

    def exists_obj(self, obj, data):
        assert isinstance(data, dict)
        return obj.exists(**data)


if __name__ == "__main__":
    bigip = ManagementRoot(hostname="192.168.110.84", username="admin", password="f5bigip")
    tm_collection = []
    for collection in bigip.tm.ltm.get_collection():
        print(collection)
        collection = collection['link'].split("/")
        if len(collection) < 6:
            continue
        collection = collection[5]
        if collection not in tm_collection:
            tm_collection.append(collection)
    print(tm_collection)
