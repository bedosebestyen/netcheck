import random
from PacketsBase import TCP_packet, ICMP_packet
from ConfigLoad import Configuration

config = Configuration()
class PacketFactory():
     def __init__(self,  ICMP_base, TCP_base) -> None:
        self.config = config.load_config()
        self.ICMP_base = ICMP_base
        self.TCP_base = TCP_base
     def create_packet(self):
            chance = random.randint(1, 100)
            
            tcp_chance=config.tcp_chance
            icmp_chance=config.icmp_chance
            if chance <= tcp_chance:
                ip = random.sample(self.TCP_base, 1)[0]
                #ip, mark, timeout, port
                return TCP_packet(ip,config.tcp_mark, config.tcp_timeout_tcp, config.tcp_port)
            else:
                ip = random.sample(self.ICMP_base, 1)[0]
                #ip, mark, timeout(waiting for response),timeout(time between the pings), number of ping sent to one host, success
                return ICMP_packet(ip, config.icmp_mark, config.icmp_timeout_waiting_for_response , config.icmp_timeout_between_pings, config.icmp_count, config.icmp_success)