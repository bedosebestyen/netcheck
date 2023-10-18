import asyncio
from chcker import check_tcp, check_icmp
import logging
import sys
from ip_pool import IP_Pool
from packets import TCP_packet, ICMP_packet, IPManager

"""
TODO: I think it would be nice to implement some pattern for the different packets(Factory???)
Should run the .sh ip_pool generator files before the script
I think main is still not good enough
Checkers needs work
"""

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.StreamHandler(sys.stdout),
                        logging.FileHandler("base_log", mode="w")
                    ])

async def main(ip_manager) -> None:
    # Define the maximum number of concurrent tasks (maybe useless)
    max_concurrent_tasks = 10
    # Reading from the files
    
    
    tasks = []
    for _ in range(max_concurrent_tasks):
        # Create a new packet
        packet = ip_manager.create_packet()

        if isinstance(packet, ICMP_packet):
            task = asyncio.create_task(check_icmp(packet))
        elif isinstance(packet, TCP_packet):
            task = asyncio.create_task(check_tcp(packet))

        # Tasks added to tasks[]
        tasks.append(task)

    
    #bepakolja a 5ször az egy hibásat unreachablebe + nem adja vissza hogy mi a hiba a checks során
    #felesleges összevonni packetet a taskal, mert a task visszaadja amit issza kell, és a createnél már át van neki adva minden
    #exception handling miatt át kell térni asyncio.gather-re valszeg
    results = await asyncio.gather(*tasks, return_exceptions=True)
    #szeretnék ide egy listát amibe mindig bekerül a log sor, tehát igazából strringet hogy látszódjon hogy mi a matek
    for result in results:
        if isinstance(result, Exception):
            if isinstance(packet, ICMP_packet):
                ip_manager.unreachable_ip_add(packet)
            elif isinstance(packet, TCP_packet):
                ip_manager.unreachable_ip_add(packet)
        else:
            # Handle the successful results here
            ip_manager.add_reachable_packet(packet)
        
    logging.info(f'Unreachable ICMP: {ip_manager.unreachable_ICMP} |||| Unreachable TCP: {ip_manager.unreachable_TCP}')
    
    # Remove completed tasks from the task list
    
   
if __name__ == '__main__':
    try:
        ip_pool = IP_Pool()
        #ip_pool.ip_pool_generator()
        
        ICMP_base, TCP_base = ip_pool.hosts_from_file()
        
        # This contains the reachable and unreachable list and the logic to add objects to them, and the logic to packet creation
        ip_manager = IPManager(ICMP_base, TCP_base)
        while True:
            try:
                asyncio.run(main(ip_manager))
            except Exception as e:
                logging.exception(f"An error occured during __main__: {e}")
                sys.exit()
    except KeyboardInterrupt:
        #Stop when ctrl + c or ctrl + z is pressed
        logging.info("Exiting the program...")