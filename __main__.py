import asyncio

import sys
from PacketLogic import PacketLogic
from IpPool import IpPool
from PacketFactory import PacketFactory
from LogHelper import setup_runtime_logger, setup_summary_logger
"""
TODO: 
        DNS
"""

async def main() -> None:
    ip_pool = IpPool()
    #the base pool for the protocol checks
    ICMP_base, TCP_base, DNS_base = ip_pool.hosts_from_file()
    #ip_manager instance with the base ip_pool args
    packet_manager = PacketLogic(ICMP_base, TCP_base, DNS_base)
    packet_create = PacketFactory(ICMP_base, TCP_base, DNS_base)

    await packet_manager.all_checks_succ(packet_manager, packet_create)
        
if __name__ == '__main__':
    try:
        
        while True:
            try:

                runtime_logger = setup_runtime_logger()
                summary_logger = setup_summary_logger()
                asyncio.run(main())
            except Exception as e:
                runtime_logger.exception(f"An error occured during __main__: {e}")
                sys.exit()
    except KeyboardInterrupt:
        #Stop when ctrl + c or ctrl + z is pressed
        sys.exit()


