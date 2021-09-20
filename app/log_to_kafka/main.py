# -*- coding: utf-8 -*-
"""
功能：
设计：
备注：
时间：
"""
import logging.config

logging.config.fileConfig("logger.config")
logger = logging.getLogger("daemon")
for i in range(10):
    logger.info("hello, I'am producer in python and transport by KafkaHandler")