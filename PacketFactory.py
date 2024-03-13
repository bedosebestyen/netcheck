import random
from PacketsBase import TCP_packet, ICMP_packet, DNS_packet
from ConfigLoad import Configuration

config = Configuration()
class PacketFactory():
     def __init__(self,  ICMP_base, TCP_base, DNS_base) -> None:
        self.config = config.load_config()
        self.ICMP_base = ICMP_base
        self.TCP_base = TCP_base
        self.DNS_base = DNS_base
     def create_packet(self):
            chance = random.randint(1, 100)
            
            tcp_chance=config.tcp_chance
            icmp_chance=config.icmp_chance
            if chance <= tcp_chance:
                ip = random.sample(self.TCP_base, 1)[0]
                #ip, mark, timeout, port
                return TCP_packet(ip,config.tcp_mark, config.tcp_timeout_tcp, config.tcp_port)
            elif chance <= (tcp_chance + icmp_chance):
                ip = random.choice(list(self.ICMP_base.keys()))
                dns_name = self.ICMP_base[ip]
                #ip, mark, timeout(waiting for response),timeout(time between the pings), number of ping sent to one host, success
                return ICMP_packet(ip, config.icmp_mark, config.icmp_timeout_waiting_for_response , config.icmp_timeout_between_pings, config.icmp_count, config.icmp_success, dns_name)
            else:
                 ip = random.sample(self.DNS_base, 1)[0]
                 return DNS_packet(ip)