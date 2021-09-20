# -*- coding: utf-8 -*-
"""
功能：
设计：
备注：
时间：
"""
import kafka
import logging


class KafkaHandler(logging.Handler):
    def __init__(self, host, topic=None):
        logging.Handler.__init__(self)
        self.producer = kafka.KafkaProducer(bootstrap_servers=host)
        self.topic = topic if topic else "log"

    def emit(self, record):
        if record.name == "daemon":
            return
        try:
            msg = self.format(record)
            print(msg)
            self.producer.send(topic=self.topic, value=msg)
        except Exception as e:
            print(e)
            self.handle(record)

    def close(self):
        self.producer.close(timeout=10)
        logging.Handler.close(self)

