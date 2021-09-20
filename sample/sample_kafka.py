# -*- coding: utf-8 -*-
"""
功能： kafka示例代码
设计：
备注：
1. 假如没有这个topic会如何

时间：
"""
import kafka
from kafka.client import KafkaClient
import json
import logging
logging.basicConfig(format='[%(asctime)s %(funcName)s %(levelname)s] %(message)s', level=logging.INFO,
                    filename="../log/default.log", filemode='w')


class KafkaDaemon:
    def __init__(self, host, topic):
        """
        kafkaproducer参数
        value_serializer    使用json处理后发送
        key, value,     发送键值对
        compression_type    压缩方式, 例如: gzip
        :param host:
        """
        self.host = host
        self.topic = topic
        self.logger = logging.getLogger(".KafkaDaemon")
        self.logger.info("init kafkadaemon...")

        self.logger.info("init producer")
        self.producer = kafka.KafkaProducer(bootstrap_servers=self.host, value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        self.logger.info("init consumer")
        self.consumer = kafka.KafkaConsumer(self.topic, bootstrap_servers=self.host, group_id="python_test", fetch_max_wait_ms=2000)

    def send(self, message):
        if not message:
            return None
        self.producer.send(topic=self.topic, value=message)

    def get(self):
        for msg in self.consumer:
            recv = "%s:%d:%d: key=%s value=%s" %(msg.topic,msg.partition,msg.offset,msg.key,msg.value)
            yield recv

    def info(self):
        client = KafkaClient(bootstrap_servers=self.host)
        cluster = client.cluster
        print("topics: ", cluster.topics())
        print("topic test's partition: ", cluster.available_partitions_for_topic("test"))
        print("brokers: ", cluster.brokers())
        print("broker 0's metadata: ", cluster.broker_metadata(0))

        print("kafka version: ", client.check_version())


if __name__ == "__main__":
    mykafka = KafkaDaemon("172.31.7.24.9092", "Eoi_cmdb")
    mykafka.get()






