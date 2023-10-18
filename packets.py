
import random
#base packet
class Packet:
    def __init__(self, ip, mark, timeout):
        self.ip = ip
        self.mark = mark
        self.timeout = timeout

class ICMP_packet(Packet):
    def __init__(self, ip, mark, timeout, count, success):
        super().__init__(ip, mark, timeout)
        self.count = count
        self.success = success

class TCP_packet(Packet):
    def __init__(self, ip, mark, timeout,  port):
        super().__init__(ip, mark, timeout)
        self.port = port
        
    
class  IPManager:
    
    def __init__(self, ICMP_base, TCP_base) -> None:
        self.ICMP_base = ICMP_base
        self.TCP_base = TCP_base
        self.reachable_ICMP = []
        self.reachable_TCP = []
        self.unreachable_ICMP = []
        self.unreachable_TCP = []
        self.unreachable_limit = 10
        self.unreachable_TCP_count = 0
        self.unreachable_ICMP_count = 0
    def add_reachable_packet(self, packet):
        if isinstance(packet, ICMP_packet):
            self.reachable_ICMP.append(packet.ip)
        elif isinstance(packet, TCP_packet):
            self.reachable_TCP.append(packet.ip)

    def remove_reachable_ip(self, ip):
        if ip in self.reachable_ICMP:
            self.reachable_ICMP.remove(ip)
        elif ip in self.reachable_TCP:
            self.reachable_TCP.remove(ip)

    def unreachable_ip_add(self, packet):
        if isinstance(packet, ICMP_packet):
            self.unreachable_ICMP.append(packet.ip)
            #remove ip from reachable
            self.remove_reachable_ip(packet.ip)
            self.unreachable_ICMP_count += 1
            #Check if the count exceeds the limit
            if self.unreachable_ICMP_count > self.unreachable_limit:
                #remove the oldes IP and add it to the ip pool
                oldest_ip = self.unreachable_ICMP.pop(0)
                self.ICMP_base.append(oldest_ip)
                self.unreachable_ICMP_count = 0

        elif isinstance(packet, TCP_packet):
            self.unreachable_TCP.append(packet.ip)
            #remove ip from reachable
            self.remove_reachable_ip(packet.ip)
            self.unreachable_TCP_count += 1
            if self.unreachable_TCP_count > self.unreachable_limit:
                oldest_ip = self.unreachable_TCP.pop(0)
                self.TCP_base.append(oldest_ip)
                self.unreachable_TCP_count = 0

    def create_packet(self, tcp_chance=50, icmp_chance=50):
        chance = random.randint(1, 100)
        
        if chance <= tcp_chance:
            ip = random.sample(self.TCP_base, 1)[0]
            return TCP_packet(ip,10, 1, 80)
        else:
            ip = random.sample(self.ICMP_base, 1)[0]
            #ip, mark, timeout, count, success
            return ICMP_packet(ip, 7, 5, 5, 0.5)
        

    
    