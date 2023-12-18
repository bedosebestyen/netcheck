import asyncio
from chcker import task_creator
import logging
import sys
from Packet_logic import Packet_logic
from ip_pool import IP_Pool
from packet_factory import PacketFactory
from logging_config import setup_runtime_logger, setup_summary_logger
"""
TODO: 
        DNS
        Logging to a file, and something that keeps all the log files for 1 day.
"""

async def main(packet_manager, packet_create) -> None:
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
        runtime_logger.info("Exiting the program...")