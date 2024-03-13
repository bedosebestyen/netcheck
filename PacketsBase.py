from typing import Any

#base packet
class Packet:
    def __init__(self, ip, mark, timeout):
        self.ip = ip
        self.mark = mark
        self.timeout = timeout

class ICMP_packet(Packet):
    def __init__(self, ip, mark, timeout, timeout_between, count, success, dns_name):
        super().__init__(ip, mark, timeout)
        self.count = count
        self.success = success
        self.timeout_between = timeout_between
        self.dns_name = dns_name

class TCP_packet(Packet):
    def __init__(self, ip, mark, timeout,  port):
        super().__init__(ip, mark, timeout)
        self.port = port
class DNS_packet(Packet):
    def __init__(self, ip):
        self.ip = ip
#Implemented singleton pattern for PacketLogic so only one instance will be initiated
#Might be an overkill, but it causes no harm
class SingletonMeta(type):
    instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.instances:
            cls.instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls.instances[cls]