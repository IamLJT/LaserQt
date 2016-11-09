# -*- coding: utf-8 -*-
from scapy.all import srp, Ether, ARP

def scan_local_area_network_ip():
    try:
        ans, unans = srp(Ether(dst="FF:FF:FF:FF:FF:FF")/ARP(pdst="192.168.1.*"), timeout=2)
    except Exception, e:
        return 0
    else:
        listAddr = []
        for send, rcv in ans:
            listAddr.append(rcv.sprintf("%ARP.psrc%"))
        return listAddr
