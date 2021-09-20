# -*- coding: utf-8 -*-
"""
功能：
设计：
参数：
作者: netliu
时间：
"""
import nmap


def get_alive_hosts(hosts):
    """

    :param hosts:
    :return:
    """
    assert isinstance(hosts, str), "params hosts should be str"
    scannner = nmap.PortScanner()
    result = scannner.scan(hosts=hosts, arguments="-sn").get("scan", {})
    custom_result = {}
    """
    {'nmap': {'command_line': 'nmap -oX - -sn 172.20.10.3',
          'scaninfo': {},
          'scanstats': {'downhosts': '0',
                        'elapsed': '0.01',
                        'timestr': 'Sun Apr 28 11:22:00 2019',
                        'totalhosts': '1',
                        'uphosts': '1'}},
    'scan': {'172.20.10.3': {'addresses': {'ipv4': '172.20.10.3'},
                          'hostnames': [{'name': '', 'type': ''}],
                          'status': {'reason': 'conn-refused', 'state': 'up'},
                          'vendor': {}}}}
    """
    for ip in result:
        custom_result[ip] = result[ip].get("status", {}).get("state")
    return custom_result


def get_basic_info(hosts):
    """

    :param hosts:
    :return:
    custom_result = {"172.20.10.3":
        {
            "hostname": "",
            "os": "windows",
            "service": {22: "ssh"},
            "uptime": "0"
        }
    }
    """
    assert isinstance(hosts, list), "params host should be alive hosts list"
    scannner = nmap.PortScanner()
    result = scannner.scan(hosts=" ".join(hosts), arguments="-O").get("scan", {})
    custom_result = {}
    for ip in result:
        custom_result[ip] = {}
        # 获取操作系统信息
        if len(result[ip].get("osmatch", [])) > 0:
            custom_result[ip]["os"] = result[ip]["osmatch"][0].get("name", "")
        else:
            custom_result[ip]["os"] = ""
        # 获取服务信息
        custom_result[ip]["services"] = {}
        if "tcp" in result[ip]:
            for port in result[ip]["tcp"]:
                custom_result[ip]["services"][port] = result[ip]["tcp"][port].get("name", "")
        # 获取开机时间
        custom_result[ip]["uptime"] = result[ip].get("uptime", {}).get("seconds", "0")
        # 获取主机名
        if len(result[ip].get("hostnames", [])) > 0:
            custom_result[ip]["hostname"] = result[ip].get("hostnames", [])[0].get("name", "0")
        else:
            custom_result[ip]["hostname"] = ""
        # 获取操作系统的mac地址
        custom_result[ip]["mac"] = result[ip].get("addresses", {}).get("mac", "")
    return custom_result


if __name__ == "__main__":
    print(get_basic_info(["172.16.18.3"]))




