import asyncio
import socket
from random import randrange
from aioping_SO_MARK import aioping
from packets import ICMP_packet, TCP_packet
from logging_config import Logger_Templates


#Creates a task from the packets.
def task_creator(ip_manager, packet_create, max_concurrent_tasks):
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
            return tasks


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
          Logger_Templates.tcp_reachable_log(packet.ip, packet.port)
          ip_manager.add_reachable_packet(packet)
          return True
    except Exception as e:
          ip_manager.unreachable_ip_add(packet)
          Logger_Templates.tcp_unreachable_log(packet.ip, packet.port, e)
          
          Logger_Templates.summary_log(ip_manager.unreachable_ICMP, 
                                       ip_manager.unreachable_TCP, 
                                       ip_manager.reachable_ICMP, 
                                       ip_manager.reachable_TCP)
          return False
    finally:
          sock.close()


async def check_icmp(packet, ip_manager):
      fail_counter = 0
      success_counter = 0
      successful_delays = 0
      tasks = []
      min_succ_rate = packet.count * packet.success

      for _ in range(packet.count): 
            tasks.append(aioping.ping(packet.ip, packet.mark, packet.timeout))
            #wait before sending the next ping
            await asyncio.sleep(packet.timeout_between)
      results = await asyncio.gather(*tasks, return_exceptions=True)
      
      #Results contains the pings to one host. This function goes through them and counts the successfull, and failed tries.
      for result in results:
            if isinstance(result, Exception):
                  fail_counter += 1
                  Logger_Templates.icmp_packet_failure_log(packet.ip, fail_counter)
                  if fail_counter == packet.count:
                        ip_manager.unreachable_ip_add(packet)
                        Logger_Templates.icmp_unreachable_log(packet.ip, 0)
                        Logger_Templates.summary_log(ip_manager.unreachable_ICMP, 
                                       ip_manager.unreachable_TCP, 
                                       ip_manager.reachable_ICMP, 
                                       ip_manager.reachable_TCP)                  
                        return False
            else:
                  result *= 1000
                  successful_delays += result
                  success_counter += 1
                  Logger_Templates.icmp_packet_success_log(packet.ip)

      avg_delay = successful_delays / success_counter
      success_rate = success_counter / packet.count
      
      if int(min_succ_rate) <= success_counter:
            ip_manager.add_reachable_packet(packet)
            Logger_Templates.icmp_reachable_log(packet.ip, success_rate, avg_delay)
            Logger_Templates.summary_log(ip_manager.unreachable_ICMP, 
                                    ip_manager.unreachable_TCP, 
                                    ip_manager.reachable_ICMP, 
                                    ip_manager.reachable_TCP)
            return True
      else:
            ip_manager.unreachable_ip_add(packet)
            Logger_Templates.icmp_unreachable_log(packet.ip, success_rate)
            Logger_Templates.summary_log(ip_manager.unreachable_ICMP, 
                                    ip_manager.unreachable_TCP, 
                                    ip_manager.reachable_ICMP, 
                                    ip_manager.reachable_TCP)
            return False
                  



            
      
      
                        