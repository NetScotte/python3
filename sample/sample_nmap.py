# -*- coding: utf-8 -*-
"""
功能：
设计：
参数：
作者: netliu
时间：
"""

import nmap
from pprint import pprint
scanner = nmap.PortScanner()
# result = scanner.scan(hosts="172.20.10.1", arguments="-sn")
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

result = scanner.scan(hosts="172.20.10.1", arguments="-sS")
"""
 'scan': {'172.20.10.3': {'addresses': {'ipv4': '172.20.10.3'},
                          'hostnames': [{'name': '', 'type': ''}],
                          'status': {'reason': 'localhost-response',
                                     'state': 'up'},
                          'tcp': {22: {'conf': '3',
                                       'cpe': '',
                                       'extrainfo': '',
                                       'name': 'ssh',
                                       'product': '',
                                       'reason': 'syn-ack',
                                       'state': 'open',
                                       'version': ''},
                                  10000: {'conf': '3',
                                          'cpe': '',
                                          'extrainfo': '',
                                          'name': 'snet-sensor-mgmt',
                                          'product': '',
                                          'reason': 'syn-ack',
                                          'state': 'open',
                                          'version': ''}},
                          'vendor': {}}}
"""

# result = scanner.scan(hosts="172.20.10.1", arguments="-O")
pprint(result)


