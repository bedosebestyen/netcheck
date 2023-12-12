import asyncio
from chcker import task_creator
import logging
import sys
from Packet_logic import Packet_logic
from ip_pool import IP_Pool
from packet_factory import PacketFactory
"""
TODO: 
        loggal valami nagyon nem jó javítani kell
        DNS
        Logging to a file, and something that keeps all the log files for 1 day
"""

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.StreamHandler(sys.stdout),
                        logging.FileHandler("base_log", mode="w")
                    ])

async def main(packet_manager, packet_create) -> None:
    #Packet_logic class instance, max concurrent tasks, it's in checkers I should place it somewhere else, maybe packetfactory
    #Megint szarul csnélja a summaryt és nem írja ki ha unreachable megtelt
    tasks = task_creator(packet_manager, packet_create, 10)
    await asyncio.gather(*tasks, return_exceptions=True)
    
    
if __name__ == '__main__':
    try:
        ip_pool = IP_Pool()
        #the base ip_pool for the protocols
        ICMP_base, TCP_base = ip_pool.hosts_from_file()
        #ip_manager instance with the base ip_pool args
        packet_manager = Packet_logic(ICMP_base, TCP_base)
        packet_create = PacketFactory(ICMP_base, TCP_base)
        while True:
            try:
                asyncio.run(main(packet_manager, packet_create))
            except Exception as e:
                logging.exception(f"An error occured during __main__: {e}")
                sys.exit()
    except KeyboardInterrupt:
        #Stop when ctrl + c or ctrl + z is pressed
        logging.info("Exiting the program...")