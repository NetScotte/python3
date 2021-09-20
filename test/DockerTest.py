# -*- coding: utf-8 -*-
"""
功能：
设计：
备注：
时间：
"""
import logging
import unittest
from sample.sample_docker import MyDocker

class DockerTest(unittest.TestCase):
    """
    MyDocker的测试
    """
    def setUp(self):
        self.logger = logging.getLogger("DockerTest")
        self.logger.info("start to test...")
        self.testimage = "nginx"
        environment={
            "DOCKER_HOST": "tcp://192.168.56.101:2375",
        }
        self.docker = MyDocker(environment=environment)

    def test_get_containers(self):
        containers = self.docker.get_containers()
        self.assertIsInstance(containers, list)
        self.logger.info("get containers:\n {}".format(containers))

    def test_pull_image(self):
        self.docker.pull_image(self.testimage)

    def test_get_images(self):
        images = self.docker.get_images()
        self.assertIsInstance(images, list)
        self.logger.info("get images:\n {}".format(images))

    def test_remove_image(self):
        self.docker.remove_image(self.testimage)

    def tearDown(self):
        self.logger.info("end test")
        self.docker.close()