# -*- coding: utf-8 -*-
"""
功能：
设计：
参数：
    cim_class: IBMTSSVC_Cluster、IBMTSSVC_BackendVolumeStatistics、IBMTSSVC_NodeStatistics、IBMTSSVC_StorageVolumeStatistics、IBMTSSVC_DiskDriveStatistics
    columns:
    'ID', 'ElementName', 'CodeLevel', 'ConsoleIP', 'OtherIdentifyingInfo', 'Status', 'StatusDescriptions', 'StatisticsFrequency', 'StatisticsStatus'
    'StatisticTime', 'InstanceID', 'KBytesRead', 'KBytesWritten', 'KBytesTransferred', 'ReadIOs', 'WriteIOs', 'TotalIOs', 'ReadIOTimeCounter',  'WriteIOTimeCounter', 'IOTimeCounter'
    'StatisticTime', 'InstanceID', 'ReadIOs', 'WriteIOs', 'TotalIOs', 'ReadHitIOs', 'WriteHitIOs'
    'StatisticTime', 'InstanceID', 'KBytesRead', 'KBytesWritten', 'KBytesTransferred', 'ReadIOs', 'WriteIOs', 'TotalIOs', 'ReadIOTimeCounter', 'WriteIOTimeCounter', 'IOTimeCounter', 'ReadHitIOs', 'WriteHitIOs'
    'StatisticTime', 'InstanceID', 'KBytesRead', 'KBytesWritten', 'KBytesTransferred', 'ReadIOs', 'WriteIOs', 'TotalIOs'

作者: netliu
时间：
"""
import pywbem
wbemc = pywbem.WBEMConnection("https://localhost", ("username", "password"), "root/ibm", no_verification=True)
query_language = "DMTF:CQL"
# cim_class = IBMTSSVC_Cluster
request = "select 'ID', 'ElementName', 'CodeLevel', 'ConsoleIP', 'OtherIdentifyingInfo', 'Status', 'StatusDescriptions', " \
          "'StatisticsFrequency', 'StatisticsStatus' from IBMTSSVC_Cluster"
sys_info = wbemc.ExecQuery(query_language, request)
result = []
for fld in sys_info:
    # Process fields explicitly as they have to be handled differently before adding them into the list.
    result.append(
        [
            fld.properties['ID'].value, fld.properties['ElementName'].value, fld.properties['CodeLevel'].value,
            fld.properties['ConsoleIP'].value, fld.properties['OtherIdentifyingInfo'].value[4],
            fld.properties['Status'].value, fld.properties['StatusDescriptions'].value[0],
            int(fld.properties['StatisticsFrequency'].value), bool(fld.properties['StatisticsStatus'].value)
        ]
    )

# cim_class =
