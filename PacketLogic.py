from PacketsBase import ICMP_packet, TCP_packet, SingletonMeta
from LogHelper import LoggerTemplates
from WriteToFile import write_to_file
import asyncio
class  PacketLogic(metaclass=SingletonMeta):
    
    def __init__(self, ICMP_base, TCP_base) -> None:
        self.reachable_ICMP = []
        self.reachable_TCP = []
        self.unreachable_ICMP = []
        self.unreachable_TCP = []
        self.unreachable_limit = 50
        self.unreachable_TCP_count = 0
        self.unreachable_ICMP_count = 0
        self.ICMP_base = ICMP_base
        self.TCP_base = TCP_base
        #these 2 are used to determine the success percentage of all the checks
        self.success_count = 0
        self.all_checks_count = 0
    def add_reachable_packet(self, packet) -> None:
        if isinstance(packet, ICMP_packet):
                self.reachable_ICMP.append(packet.ip)
        elif isinstance(packet, TCP_packet):
                self.reachable_TCP.append(packet.ip)

    def remove_reachable_ip(self, ip) -> None:
        if ip in self.reachable_ICMP:
                self.reachable_ICMP.remove(ip)
        elif ip in self.reachable_TCP:
                self.reachable_TCP.remove(ip)

    def remove_unreachable_ip(self, ip) -> None:
         if ip in self.unreachable_ICMP:
                self.unreachable_ICMP.remove(ip)
         elif ip in self.unreachable_TCP:
                self.unreachable_TCP.remove(ip)
                
    #Adds unreachable IP to PROTOCOL_unreachable
    #If it is full the function removes the first IP adn puts it back into the ip_pool
    def unreachable_ip_add(self, packet) -> None:
        if isinstance(packet, ICMP_packet):  
            self.unreachable_ICMP.append(packet.ip)
            self.remove_reachable_ip(packet.ip)

            self.unreachable_ICMP_count += 1
            if self.unreachable_ICMP_count > (self.unreachable_limit - 1):
                oldest_ip = self.unreachable_ICMP[0]
                self.remove_unreachable_ip(oldest_ip)

                self.ICMP_base.append(oldest_ip)
                self.unreachable_ICMP_count -= 1
                LoggerTemplates.icmp_unreachable_full(oldest_ip)
                

        elif isinstance(packet, TCP_packet):
            self.unreachable_TCP.append(packet.ip)
            self.remove_reachable_ip(packet.ip)

            self.unreachable_TCP_count += 1
            if self.unreachable_TCP_count > self.unreachable_limit:
                oldest_ip = self.unreachable_TCP[0]
                self.remove_unreachable_ip(oldest_ip)

                self.TCP_base.append(oldest_ip)
                self.unreachable_TCP_count -= 1
                LoggerTemplates.tcp_unreachable_full(oldest_ip)
    #where should i place it?M???
    async def all_checks_succ(self):
        #this will keep it in a loop, sleeping 10 seconds after each check
        while True:
            await asyncio.sleep(10)
            new_number = (self.success_count / self.all_checks_count) * 10
            prev_number = 0
            #to determine if there was change in the percentage bigger than 10%
            if (prev_number + 10) > (new_number + 10) or (prev_number - 10) < (new_number - 10):
                write_to_file(new_number)

                prev_number = new_number
            
