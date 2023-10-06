import asyncio
from chcker import check_tcp, check_icmp
import logging
import sys
from ip_pool import IP_Pool
from packets import TCP_packet, ICMP_packet, IPManager

"""
TODO: Test on linux, cli could be deleted, other protocols in chcker, implement some success ratio
        make the code more readable/cleaner, implementing SO_MARK, implementing scripts for IP pool,
        when there is an exception script pauses a little need to know why exactly, timeouts needs streamlining
"""

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.StreamHandler(sys.stdout),
                        logging.FileHandler("base_log", mode="w")
                    ])

async def main() -> None:
    # Define the maximum number of concurrent tasks (maybe useless)
    max_concurrent_tasks = 10
    # Reading from the files
    ip_pool = IP_Pool()
    
    ICMP_base, TCP_base = ip_pool.hosts_from_file()
    
    # This contains the reachable and unreachable list and the logic to add objects to them, and the logic to packet creation
    ip_manager = IPManager(ICMP_base, TCP_base)
    
    tasks = []
    while len(tasks) < max_concurrent_tasks:
        # Create a new packet
        packet = ip_manager.create_packet()
    
        if isinstance(packet, ICMP_packet):
            task = asyncio.create_task(check_icmp(packet.ip, packet.mark, packet.count, packet.timeout, packet.success))
        elif isinstance(packet, TCP_packet):
            task = asyncio.create_task(check_tcp(packet.ip, packet.mark, packet.port, packet.timeout))

        # Packet, task tuple added to tasks. Packet makes it easier to identify
        tasks.append((packet, task))

    # valami nagyon gyász, vissza kell állni oda ami az utolsó commit githubon,
    # végig kell mennem rajta és megnézni hogy mi pontosan mit és miért csinál, mert most nagyon zavaros
    # túl lett bonyolítva kegyetlen mód
    for completed_task in asyncio.as_completed([task for packet, task in tasks]):

        try:
            result = await completed_task
            packet, task = next((packet, task) for packet, task in tasks if task == completed_task)

            if not result:
                ip_manager.unreachable_ip_manager(packet)

            ip_manager.add_reachable_packet(packet)
        except Exception as e:
            logging.error(f'An exception occurred during the checks: {e}')
            ip_manager.unreachable_ip_manager(packet)

    logging.info(f'Unreachable ICMP: {ip_manager.unreachable_ICMP} |||| Unreachable TCP: {ip_manager.unreachable_TCP}')
    # Remove completed tasks from the task list
    tasks = [(packet, task) for packet, task in tasks if not task.done()]

    
if __name__ == '__main__':
    try:
        while True:
            try:
                asyncio.run(main())
            except Exception as e:
                logging.exception(f"An error occured during __main__: {e}")
                sys.exit()
    except KeyboardInterrupt:
        #Stop when ctrl + c or ctrl + z is pressed
        logging.info("Exiting the program...")
        
    
        
    
    
