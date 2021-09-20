# -*- coding: utf-8 -*-
"""
功能：
设计：
备注：
时间：
"""
from kubernetes import client, config


class MyKubernetes:
    def __init__(self, configfile):
        config.load_kube_config(configfile)

    def get_deployment(self):
        appsv1 = client.AppsV1Api()
        ret = appsv1.list_deployment_for_all_namespaces()
        return ret.items

    def get_pod(self):
        corev1 = client.CoreV1Api()
        ret = corev1.list_pod_for_all_namespaces()
        return ret.items

    def get_service(self):
        corev1 = client.CoreV1Api()
        ret = corev1.list_service_for_all_namespaces()
        return ret.items


if __name__ == "__main__":
    mk = MyKubernetes("../files/config")
    print("name, namespace")
    for deployment in mk.get_deployment():
        print(deployment.metadata.name, deployment.metadata.namespace)