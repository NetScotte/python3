# -*- coding: utf-8 -*-
from puresnmp import walk
from puresnmp.api.raw import walk as raw_walk
from puresnmp.x690.types import OctetString

IP = "172.30.37.100"
COMMUNITY = 'ZXD2000RO'
OID = ".1.3.6.1.4.1.9.9.289.1.1.5.1.2"

result = raw_walk(ip=IP, community=COMMUNITY, oid=OID)
for i, k in result:
    print(type(k))
    print(k.pythonic())

