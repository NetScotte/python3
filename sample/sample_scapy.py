from scapy.all import *
"""
我想持续运行嗅探程序
可以打印srcIP, srcPort, dstIP, dstPort
"""
def sample_sniff():
    def show_pacakge(pacakge):
        # summary(): Ether / IP / TCP 203.119.169.109:https > 192.168.3.15:52108 A / Padding
        # nsummary():
        # show(): human format
        # sniffed_on: eth3
        # sprintf("{IP:%IP.src%  -> %IP.dst%\n}{Raw:%Raw.load%\n}")
        print(pacakge.sprintf("{IP:%IP.src% -> %IP.dst%\n}"))
    sniff(prn=show_pacakge)


if __name__ == "__main__":
    sample_sniff()

