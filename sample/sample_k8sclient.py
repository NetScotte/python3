# -*- coding: utf-8 -*-
from kubernetes import client, config
import unittest
import datetime
import json
import copy
import yaml
# # Configs can be set in Configuration class directly or using helper utility
# config.load_kube_config(config_file="/Users/net/admin.conf")
#
# v1 = client.CoreV1Api()
# print("Listing pods with their IPs:")
# ret = v1.list_pod_for_all_namespaces(watch=False)
# for i in ret.items:
#     print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))


class EasyK8S:
    def __init__(self, configFile):
        config.load_kube_config(config_file=configFile)
        self.kube_config = configFile
        self.v1 = client.CoreV1Api()
        self.apps = client.AppsV1Api()
        self.batch_v1_beta = client.BatchV1beta1Api()
        self.storage_v1 = client.StorageV1Api()
        self.network_v1 = client.NetworkingV1beta1Api()

    def get_cluster(self, configFile=None):
        if not configFile:
            configFile = self.kube_config
        with open(configFile, "r") as f:
            content = yaml.safe_load(f)
        results = []
        for cluster in content.get("clusters", []):
            results.append({
                "name": cluster["server"],
                "host": cluster["server"]
            })
        return results

    def __serialize_resource(self, obj):
        '''not available'''
        newobj = copy.deepcopy(obj)
        if isinstance(obj, dict):
            for key in newobj:
                if isinstance(newobj[key], dict):
                    newobj[key] = self.__serialize_resource(newobj[key])
                elif isinstance(newobj[key], datetime.datetime):
                    newobj[key] = newobj[key].strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(newobj, list):
            newlist = []
            for item in newobj:
                if isinstance(item, dict):
                    item = self.__serialize_resource(item)
                elif isinstance(item, datetime.datetime):
                    item = item.strftime('%Y-%m-%d %H:%M:%S')
                newlist.append(item)
            newobj = newlist
        return json.dumps(newobj)


    def get_namespace(self):
        obj = self.v1.list_namespace()
        namespaces = obj.to_dict()
        custom_namespace = []
        for item in namespaces.get("items", {}):
            custom_namespace.append({
                "name": item["metadata"]["name"],
                "status": item["status"]["phase"],
                "create": item["metadata"]["creation_timestamp"].strftime('%Y-%m-%d %H:%M:%S') if isinstance(item["metadata"]["creation_timestamp"], datetime.datetime) else "",
            })
        return custom_namespace


    def get_service(self):
        obj = self.v1.list_service_for_all_namespaces()
        services = obj.to_dict()
        custom_services = []
        for item in services["items"]:
            custom_services.append({
                "name": item["metadata"]["name"],
                "namespace": item["metadata"]["namespace"],
                "create": item["metadata"]["creation_timestamp"].strftime('%Y-%m-%d %H:%M:%S') if isinstance(item["metadata"]["creation_timestamp"], datetime.datetime) else "",
                "type": item["spec"]["type"],
                "cluster_ip": item["spec"]["cluster_ip"],
                "external_i_ps": item["spec"]["external_i_ps"],
                "ports": item["spec"]["ports"],
                "selector": item["spec"]["selector"]
            })
        return custom_services

    def get_deployments(self):
        obj = self.apps.list_deployment_for_all_namespaces()
        deployments = obj.to_dict()
        custom_deployments = []
        for item in deployments["items"]:
            custom_deployments.append({
                "name": item["metadata"]["name"],
                "namespace": item["metadata"]["namespace"],
                "create": item["metadata"]["creation_timestamp"].strftime('%Y-%m-%d %H:%M:%S') if isinstance(item["metadata"]["creation_timestamp"], datetime.datetime) else "",
                "available_replicas": item["status"]["available_replicas"],
                "replicas": item["status"]["replicas"],
                "ready_replicas": item["status"]["ready_replicas"],
                "labels": item["metadata"]["labels"]
            })

        return deployments

    def get_stateful_set(self):
        obj = self.apps.list_stateful_set_for_all_namespaces()
        stateful_sets = obj.to_dict()
        custom_stateful_sets = []
        for item in stateful_sets["items"]:
            custom_stateful_sets.append({
                "name": item["metadata"]["name"],
                "namespace": item["metadata"]["namespace"],
                "create": item["metadata"]["creation_timestamp"].strftime('%Y-%m-%d %H:%M:%S') if isinstance(item["metadata"]["creation_timestamp"], datetime.datetime) else "",
            })
        return custom_stateful_sets

    def get_daemon_set(self):
        obj = self.apps.list_daemon_set_for_all_namespaces()
        stateful_sets = obj.to_dict()
        custom_stateful_sets = []
        for item in stateful_sets["items"]:
            custom_stateful_sets.append({
                "name": item["metadata"]["name"],
                "namespace": item["metadata"]["namespace"],
                "create": item["metadata"]["creation_timestamp"].strftime('%Y-%m-%d %H:%M:%S') if isinstance(item["metadata"]["creation_timestamp"], datetime.datetime) else "",
            })
        return custom_stateful_sets

    def get_cron_jobs(self):
        obj = self.batch_v1_beta.list_cron_job_for_all_namespaces()
        stateful_sets = obj.to_dict()
        custom_results = []
        for item in stateful_sets["items"]:
            custom_results.append({
                "name": item["metadata"]["name"],
                "namespace": item["metadata"]["namespace"],
                "create": item["metadata"]["creation_timestamp"].strftime('%Y-%m-%d %H:%M:%S') if isinstance(item["metadata"]["creation_timestamp"], datetime.datetime) else "",
            })
        return custom_results

    def get_config_map(self):
        obj = self.v1.list_config_map_for_all_namespaces()
        results = obj.to_dict()
        custom_results = []
        for item in results["items"]:
            custom_results.append({
                "name": item["metadata"]["name"],
                "namespace": item["metadata"]["namespace"],
                "create": item["metadata"]["creation_timestamp"].strftime('%Y-%m-%d %H:%M:%S') if isinstance(item["metadata"]["creation_timestamp"], datetime.datetime) else "",
            })
        return custom_results

    def get_pvc(self):
        obj = self.v1.list_persistent_volume_claim_for_all_namespaces()
        results = obj.to_dict()
        custom_results = []
        for item in results["items"]:
            custom_results.append({
                "name": item["metadata"]["name"],
                "namespace": item["metadata"]["namespace"],
                "create": item["metadata"]["creation_timestamp"].strftime('%Y-%m-%d %H:%M:%S') if isinstance(item["metadata"]["creation_timestamp"], datetime.datetime) else "",
                "access_modes": item["spec"]["access_modes"]
            })
        return custom_results

    def get_resource_quota(self):
        obj = self.v1.list_resource_quota_for_all_namespaces()
        results = obj.to_dict()
        custom_results = []
        for item in results["items"]:
            custom_results.append({
                "name": item["metadata"]["name"],
                "namespace": item["metadata"]["namespace"],
                "create": item["metadata"]["creation_timestamp"].strftime('%Y-%m-%d %H:%M:%S') if isinstance(item["metadata"]["creation_timestamp"], datetime.datetime) else "",
            })
        return custom_results


    def get_storage_class(self):
        obj = self.storage_v1.list_storage_class()
        results = obj.to_dict()
        custom_results = []
        for item in results["items"]:
            custom_results.append({
                "name": item["metadata"]["name"],
                "namespace": item["metadata"]["namespace"],
                "create": item["metadata"]["creation_timestamp"].strftime('%Y-%m-%d %H:%M:%S') if isinstance(item["metadata"]["creation_timestamp"], datetime.datetime) else "",
            })
        return custom_results

    def get_secret(self):
        obj = self.v1.list_secret_for_all_namespaces()
        results = obj.to_dict()
        custom_results = []
        for item in results["items"]:
            custom_results.append({
                "name": item["metadata"]["name"],
                "namespace": item["metadata"]["namespace"],
                "create": item["metadata"]["creation_timestamp"].strftime('%Y-%m-%d %H:%M:%S') if isinstance(item["metadata"]["creation_timestamp"], datetime.datetime) else "",
            })
        return custom_results

    def get_storage_class_provisioner(self):
        return []

    def get_ingress(self):
        obj = self.network_v1.list_ingress_for_all_namespaces()
        results = obj.to_dict()
        custom_results = []
        for item in results["items"]:
            custom_results.append({
                "name": item["metadata"]["name"],
                "namespace": item["metadata"]["namespace"],
                "create": item["metadata"]["creation_timestamp"].strftime('%Y-%m-%d %H:%M:%S') if isinstance(item["metadata"]["creation_timestamp"], datetime.datetime) else "",
            })
        return custom_results

    def get_pod(self):
        obj = self.v1.list_pod_for_all_namespaces()
        results = obj.to_dict()
        custom_results = []
        for item in results["items"]:
            custom_results.append({
                "name": item["metadata"]["name"],
                "namespace": item["metadata"]["namespace"],
                "create": item["metadata"]["creation_timestamp"].strftime('%Y-%m-%d %H:%M:%S') if isinstance(item["metadata"]["creation_timestamp"], datetime.datetime) else "",
            })
        return custom_results


class EasyK8S_test(unittest.TestCase):
    def setUp(self):
        adminConf = "/Users/net/admin.conf"
        self.k8s = EasyK8S(configFile=adminConf)

    def test_all(self):
        # self.k8s.get_cluster()
        # self.k8s.get_namespace()
        self.k8s.get_service()
        self.k8s.get_deployments()
        #
        # self.k8s.get_stateful_set()
        # self.k8s.get_daemon_set()
        # self.k8s.get_cron_jobs()
        # self.k8s.get_pvc()


if __name__ == "__main__":
    unittest.main()



