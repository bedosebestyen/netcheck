import asyncio
from Checker import task_creator
import sys
from PacketLogic import PacketLogic
from IpPool import IpPool
from PacketFactory import PacketFactory
from LogHelper import setup_runtime_logger, setup_summary_logger
"""
TODO: 
        DNS
"""

async def main(packet_manager, packet_create) -> None:
    #Creates 10 async tasks
    tasks = task_creator(packet_manager, packet_create, 10)
    #Gathers the tasks
    await asyncio.gather(*tasks, return_exceptions=True)
    
    
if __name__ == '__main__':
    try:
        ip_pool = IpPool()
        #the base pool for the protocol checks
        ICMP_base, TCP_base = ip_pool.hosts_from_file()
        #ip_manager instance with the base ip_pool args
        packet_manager = PacketLogic(ICMP_base, TCP_base)
        packet_create = PacketFactory(ICMP_base, TCP_base)
        runtime_logger = setup_runtime_logger()
        summary_logger = setup_summary_logger()
        while True:
            try:
                asyncio.run(main(packet_manager, packet_create))
            except Exception as e:
                runtime_logger.exception(f"An error occured during __main__: {e}")
                sys.exit()
    except KeyboardInterrupt:
        #Stop when ctrl + c or ctrl + z is pressed
        sys.exit()