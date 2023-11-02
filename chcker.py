import asyncio
import logging
import socket
from random import randrange
from aioping_SO_MARK import aioping
from packets import ICMP_packet, TCP_packet

def task_creator(ip_manager, max_concurrent_tasks):
            
            # Reading from the files
        
            tasks = []
            for _ in range(max_concurrent_tasks):
                # Create a new packet
                packet = ip_manager.create_packet()

                if isinstance(packet, ICMP_packet):
                    task = asyncio.create_task(check_icmp(packet, ip_manager))
                elif isinstance(packet, TCP_packet):
                    task = asyncio.create_task(check_tcp(packet, ip_manager))

                # Tasks added to tasks[]
                tasks.append(task)
            return tasks

#packetet adok meg hogy utólag lehessen ellenőrizni hogy melyik unreachable-be kell rakni
async def check_tcp(packet, ip_manager):
    #Get the current event loop
    loop = asyncio.get_running_loop()
    #Create a TCP socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Set the SO_MARK with value 10
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_MARK, packet.mark)
    #Make socket non-blocking
    sock.setblocking(False)
    #Try to connect

    try:
          await asyncio.wait_for(loop.sock_connect(sock, (packet.ip, packet.port)), timeout=5)
          logging.info(f"{packet.ip} is reachable on {packet.port} TCP")
          ip_manager.add_reachable_packet(packet)
          return True
    except Exception as e:
          logging.error(f"Connection failed to {packet.ip}:{packet.port} TCP: {e}")
          ip_manager.unreachable_ip_add(packet)
          logging.info(f'Unreachable ICMP: {ip_manager.unreachable_ICMP} |||| Unreachable TCP: {ip_manager.unreachable_TCP}\n\t\t\t\tReachable_ICMP: {ip_manager.reachable_ICMP} |||| Reachable_TCP: {ip_manager.reachable_TCP}') 
          return False
    finally:
          sock.close()

#kell még egy timeout mert e za mostani csak válaszra várást határozza meg, de kell egy olyan ami a packetek elküldése közötti időért felel
async def check_icmp(packet, ip_manager):
      fail_counter = 0
      success_counter = 0
      successful_delays = 0
      delay = 0
      tasks = []
      for _ in range(packet.count): 
            tasks.append(aioping.ping(packet.ip, packet.mark, packet.timeout))
            #wait before sending the next ping
            await asyncio.sleep(packet.timeout_between)
      results = await asyncio.gather(*tasks, return_exceptions=True)
      #át kéne emelni a végső kiértékelést más funcionbe és utána közvetlenebbül meghívni mert így szerintem az asyncio miatt szétcsúszik kicsit
      #singletont át kell nézni mert nem vagyok biztos benne hogy most jól szuperál
      #ki kell tezstelni hogy az okozza bajt ha 100 concurrent task van, vagy ha sok ping megy egy hostra
      #TCP mindig reachable ez kicsit zavar, mert túl jól működik
      #kéne egy pending amiben az éppen teszteltek vannak, hogy ne válasszsa ki 2szer ugyanazt
      
      for result in results:
            if isinstance(result, Exception):
                  fail_counter += 1
                  logging.error(f"{packet.ip} host FAILED ICMP try || Fail_Count: {fail_counter}")
                  if fail_counter == 5:
                        ip_manager.unreachable_ip_add(packet)
                        logging.info(f'{packet.ip} is not reachable with ICMP.\n\t\t\t\t Succ_Rate: 0%')
                        logging.info(f'Unreachable ICMP: {ip_manager.unreachable_ICMP} |||| Unreachable TCP: {ip_manager.unreachable_TCP}\n\t\t\t\tReachable_ICMP: {ip_manager.reachable_ICMP} |||| Reachable_TCP: {ip_manager.reachable_TCP}')
                        return False
            else:
                  result *= 1000
                  successful_delays += result
                  success_counter += 1
                  logging.info(f"{packet.ip} host ICMP try SUCCESS || Success_Count: {success_counter}")
      
      avg_delay = successful_delays / success_counter
      success_rate = success_counter / packet.count
      min_succ_rate = packet.count * packet.success

      
      if int(min_succ_rate) > success_counter:
            logging.info(f'{packet.ip} is not reachable with ICMP.\n\t\t\t\t Succ_Rate: {success_rate:.2%}')
            ip_manager.unreachable_ip_add(packet)
            logging.info(f'Unreachable ICMP: {ip_manager.unreachable_ICMP} |||| Unreachable TCP: {ip_manager.unreachable_TCP}\n\t\t\t\tReachable_ICMP: {ip_manager.reachable_ICMP} |||| Reachable_TCP: {ip_manager.reachable_TCP}') 
            return False
      else:
            logging.info(f'{packet.ip} is reachable with ICMP. \n\t\t\t\t Avg_Succ_Delay: {avg_delay:.4f} ms \n\t\t\t\t Succ_Rate: {success_rate:.2%}')
            ip_manager.add_reachable_packet(packet)
            return True
            
      
      
                        