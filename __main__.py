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


"""
o add the all_checks_succ function as a task and keep the tasks list filling up again and again, you can modify the task_creator function like this:

def task_creator(ip_manager, packet_create, max_concurrent_tasks, obj): 
    tasks = [] 
    for _ in range(max_concurrent_tasks): 
        # Create a new packet 
        packet = packet_create.create_packet() 
        if isinstance(packet, ICMP_packet): 
            task = asyncio.create_task(check_icmp(packet, ip_manager)) 
        elif isinstance(packet, TCP_packet): 
            task = asyncio.create_task(check_tcp(packet, ip_manager)) 
        # Tasks added to tasks[] 
        tasks.append(task) 

    # Add the all_checks_succ function as a task
    tasks.append(asyncio.create_task(obj.all_checks_succ()))

    return tasks
In this modification, obj is the instance of the class that all_checks_succ belongs to. You need to pass this instance when you call task_creator. The all_checks_succ function will now run asynchronously with the other tasks.
"""