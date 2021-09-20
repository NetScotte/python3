# -*- coding: utf-8 -*-
"""
功能：docker练习
设计：docker相关的功能
备注：
    http://docker-py.readthedocs.io/en/stable/
    https://docs.docker.com/reference/
时间：
"""
import docker
from docker import models
import logging
import os
logging.basicConfig(format="[%(asctime)s %(funcName)s %(levelname)s] %(message)s", level=logging.DEBUG)


class MyDocker:
    def __init__(self, environment):
        # 可以通过client获得configs, containers, images, networks, plugins, secrets, services, swarm,
        # volumes类
        self.client = docker.from_env(environment=environment)
        self.logger = logging.getLogger("MyDocker")

    def get_networkinfo(self):
        networks = self.client.networks.list()
        networkinfo = []
        for network in networks:
            tempdict = {}
            tempdict['id'] = network.id
            tempdict['name'] = network.name
            tempdict['containers'] = network.containers
            networkinfo.append(tempdict)
        return networkinfo

    def run_container(self, image, detach=True):
        """
        运行一个容器
        :return:
        """
        # self.client.containers.run("nginx")
        # self.client.containers.run("nginx", ["echo", "hello", "world"])
        self.client.containers.run(image, detach=detach)

    def get_containers(self):
        containers = self.client.containers.list()
        return containers

    def get_container(self, containerId):
        container = self.client.container.get(containerId)
        return container

    def stop_container(self, containerId=None, all=False):
        if all:
            containers = self.get_containers()
            for container in containers:
                container.stop()
        else:
            containers = self.get_containers()
            for container in containers:
                if container.id == containerId:
                    container.stop()
                    break

    def get_images(self):
        images = self.client.images.list()
        return images

    def get_image(self, imageId):
        image = self.client.images.get(imageId)
        return image

    def build_image(self, fileobj):
        # 对于tar包应该传递encoding: gzip, custom_context=True, fileobj
        # 默认放置于/var/lib/docker/tmp/docker-builder992899633/
        if isinstance(fileobj, str) and os.path.isdir(fileobj):
            images = self.client.images.build(path=fileobj, tag="myapp:latest", rm=True, quiet=False)
        else:
            images = self.client.images.build(fileobj=fileobj, custom_context=True, encoding="gzip")
        return images

    def pull_image(self, imageName, tag="latest"):
        image = self.client.images.pull(repository=imageName, tag=tag)
        return image

    def remove_image(self, image):
        self.client.images.remove(image)

    def close(self):
        self.client.close()

    def get_service(self, service_id=None, service_name=None):
        """
        获取service信息，服务的信息包括id, name, version, attr
        :param service_id: 可选，服务id
        :param service_name: 可选，服务名称
        :return: 服务对象列表，
        """
        if service_id:
            service_list = [self.client.services.get(service_id=service_id)]
        else:
            service_list = self.client.services.list()
            if service_name:
                for service in service_list:
                    if service.name == service_name:
                        service_list = [service]
        return service_list

    def create_service(self, image, command=None, **kwargs):
        """
        创建服务
        :param image: 镜像名
        :param command: 启动镜像时的执行命令
        :param kwargs: 其他参数，参考https://docker-py.readthedocs.io/en/stable/services.html#
        :return:
        Example:
        create_service(image="netscotte/started_daemon:v1.0",
                        name="web", networks=["my-overlay"],
                        mode={"replicated": {"replicas": 2}},
                        endpoint_spec={"ports": [{"TargetPort": 80, "PublishedPort": 8080}]}
                        )
        """
        # Todo: 如果创建的服务很快down掉，是否会无限次创建，如何解决
        # 答： 也会直接返回，
        new_service = self.client.services.create(image, command, **kwargs)
        return new_service

    def update_obj(self, service_name, **kwargs):
        """
        更新资源对象，容易失败，故这里会在失败的时候再尝试三遍
        :param service: 服务对象
        :param kwargs: 参考create_service中的参数
        :return:
        """
        service = self.get_service(service_name=service_name)[0]
        # update容易失败，故这里尝试几次
        try:
            service.update(**kwargs)
            return None
        except Exception as e:
            self.logger.error("update service {} error: {}".format(service.name, e))
        tries = 0
        while tries < 3:
            self.logger.warning("retry to update service: {} tries: {}".format(service.name, tries))
            try:
                service.update()
                self.logger.info("update service: {} success after tries: {}".format(service.name, tries))
                return None
            except Exception as e:
                self.logger.error("update service: {} error {} tries {}".format(service.name, e, tries))
        raise Exception("update service: {} failed".format(service.name))

    def remove_service(self, service_name):
        """
        删除资源，
        :param service: 服务名称。
        :return:
        """
        service = self.get_service(service_name=service_name)[0]
        service.remove()


if __name__ == "__main__":
    environment = {
        "DOCKER_HOST": "tcp://192.168.199.244:2375",
    }
    mydocker = MyDocker(environment=environment)
    mydocker.create_service(image="netscotte/started_daemon:v1.0", name="web", networks=["my-overlay"],
                            mode={"replicated": {"replicas": 2}},
                            endpoint_spec={"ports": [{"TargetPort": 80, "PublishedPort": 8080}]},
                            mounts=["/etc/hosts:/tmp/hosts:"])
