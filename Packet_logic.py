from packets import ICMP_packet, TCP_packet, SingletonMeta
import logging
class  Packet_logic(metaclass=SingletonMeta):
    
    def __init__(self, ICMP_base, TCP_base) -> None:
        self.reachable_ICMP = []
        self.reachable_TCP = []
        self.unreachable_ICMP = []
        self.unreachable_TCP = []
        self.unreachable_limit = 10
        self.unreachable_TCP_count = 0
        self.unreachable_ICMP_count = 0
        self.ICMP_base = ICMP_base
        self.TCP_base = TCP_base
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
    def remove_unreachable_ip(self, ip):
         if ip in self.unreachable_ICMP:
                self.unreachable_ICMP.remove(ip)
         elif ip in self.unreachable_TCP:
                self.unreachable_TCP.remove(ip)
    
    def unreachable_ip_add(self, packet):
        if isinstance(packet, ICMP_packet):  
            self.unreachable_ICMP.append(packet.ip)
            #remove ip from reachable
            self.remove_reachable_ip(packet.ip)
            self.unreachable_ICMP_count += 1
            #Check if the count exceeds the limit
            if self.unreachable_ICMP_count > (self.unreachable_limit - 1):
                oldest_ip = self.unreachable_ICMP[0]
                self.remove_unreachable_ip(oldest_ip)
                self.ICMP_base.append(oldest_ip)
                self.unreachable_ICMP_count -= 1
                logging.info(f'ICMP unreachable reached max capacity first element will be put back into reachable, ip: {oldest_ip}')

        elif isinstance(packet, TCP_packet):
            self.unreachable_TCP.append(packet.ip)
            #remove ip from reachable
            self.remove_reachable_ip(packet.ip)
            self.unreachable_TCP_count += 1
            #remove the oldes IP and add it to the ip pool, need to test it!!!!!!
            if self.unreachable_TCP_count > self.unreachable_limit:
                oldest_ip = self.unreachable_TCP[0]
                self.TCP_base.append(oldest_ip)
                self.unreachable_TCP_count -= 1
                logging.info(f'TCP unreachable reached max capacity first element will be but back into reachable, ip: {oldest_ip}')