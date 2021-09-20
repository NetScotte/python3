# -*- coding: utf-8 -*-
"""
功能：
设计：
备注：
时间：
"""
import atexit

from pyVim import connect
from pyVmomi import vmodl
from pyVmomi import vim
import ssl


def print_vm_info(virtual_machine):
    summary = virtual_machine.summary
    print("keys: ", dir(summary))
    print("Name     : ", summary.config.name)
    print("Template : ", summary.config.template)
    print("Path     : ", summary.config.vmPathName)
    print("Guest    : ", summary.config.guestFullName)
    print("Instance UUID     : ", summary.config.instanceUuid)
    print("Bios UUID         : ", summary.config.uuid)
    annotation = summary.config.annotation
    if annotation:
        print("Annotation : ", annotation)
    print("State : ", summary.runtime.powerState)
    if summary.guest is not None:
        ip_address = summary.guest.ipAddress
        tools_version = summary.guest.toolsStatus
        if tools_version is not None:
            print("VMware-tools : ", tools_version)
        else:
            print("VMware-tools : None")
        if ip_address:
            print("IP       : ", ip_address)
        else:
            print("IP       : None")
    if summary.runtime.question:
        print("Question : ", summary.runtime.question.text)
    print(" ")


# 基于globals获取对象的名称
def get_variable_name(dict, obj):
    """
    基于locals获取对象的名称
    :param dict: locals()
    :param obj: 变量
    :return:
    """
    locals().update(dict)
    mydict = locals()
    for name in mydict:
        if name == "obj":
            continue
        if mydict[name] is obj:
            return name


# 基于dir获取对象的所有值
def get_all_attr(obj):
    for key in dir(obj):
        if "_" in key:
            continue
        print(key, eval("{}.{}".format(get_variable_name(locals(), obj), key)))


def print_host_info(host):
    summary = host.summary
    print("Name             : ", summary.config.name)
    print("UUID             : ", summary.hardware.uuid)
    print("CPUMhz           : ", summary.hardware.cpuMhz)
    print("CPUModel         : ", summary.hardware.cpuModel)
    print("Memory           : ", summary.hardware.memorySize)
    print("Model            : ", summary.hardware.model)
    print("NumCpuCores      : ", summary.hardware.numCpuCores)
    print("NumCpuPkgs       : ", summary.hardware.numCpuPkgs)
    print("NumCpuThreads    : ", summary.hardware.numCpuThreads)
    print("numHBAs          : ", summary.hardware.numHBAs)
    print("numNics          : ", summary.hardware.numNics)
    print(" ")



# 获取服务实例，也可以使用connect.SmartConnectNoSSL
def main():
    sslcontext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    sslcontext.verify_mode = ssl.CERT_NONE
    service_instance = connect.SmartConnect(host="172.31.61.200", port=443, user="aa", pwd="aa", sslContext=sslcontext, connectionPoolTimeout=30)
    atexit.register(connect.Disconnect, service_instance)
    content = service_instance.RetrieveContent()
    container = content.rootFolder
    get_all_attr(vim)
    exit(0)
    # viewType = [vim.VirtualMachine]
    viewType = [vim.HostSystem]
    recursive = True
    containerView = content.viewManager.CreateContainerView(container, viewType, recursive)
    children = containerView.view
    if not children:
        print("no virtual_machine")
    for child in children:
        # print_vm_info(child)
        print_host_info(child)


if __name__ == "__main__":
    main()