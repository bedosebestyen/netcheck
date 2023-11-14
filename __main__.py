import asyncio
from chcker import task_creator
import logging
import sys
from Packet_logic import Packet_logic
from ip_pool import IP_Pool

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
    
    #Packet_logic class instance, max concurrent tasks
    tasks = task_creator(ip_manager, 10)

    await asyncio.gather(*tasks, return_exceptions=True)
    
    
    
    # Remove completed tasks from the task list
    
   
if __name__ == '__main__':
    try:
        ip_pool = IP_Pool()
        #the base ip_pool for the protocols
        ICMP_base, TCP_base = ip_pool.hosts_from_file()
        #ip_manager instance with the base ip_pool args
        ip_manager = Packet_logic(ICMP_base, TCP_base)
        while True:
            try:
                asyncio.run(main(ip_manager))
            except Exception as e:
                logging.exception(f"An error occured during __main__: {e}")
                sys.exit()
    except KeyboardInterrupt:
        #Stop when ctrl + c or ctrl + z is pressed
        logging.info("Exiting the program...")