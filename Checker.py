import asyncio
import socket
from random import randrange
from aioping_SO_MARK import aioping
from PacketsBase import ICMP_packet, TCP_packet, DNS_packet
from LogHelper import LoggerTemplates
#I guess the result checker should get a task too. But I think for it to run all the time it should be put into a different task group
#research still needed

def task_creator(ip_manager, packet_create, max_concurrent_tasks):
      tasks = []
      for _ in range(max_concurrent_tasks - 1): 
            # Create a new packet 
            packet = packet_create.create_packet() 
            if isinstance(packet, ICMP_packet): 
                  task = asyncio.create_task(check_icmp(packet, ip_manager)) 
            elif isinstance(packet, TCP_packet): 
                  task = asyncio.create_task(check_tcp(packet, ip_manager))
            elif isinstance(packet, DNS_packet):
                  task = asyncio.create_task(check_dns(packet.ip, ip_manager))
            # Tasks added to tasks[]
            tasks.append(task) 
      return tasks

async def check_tcp(packet, ip_manager):
    #Get the current event loop
    loop = asyncio.get_running_loop()
    #Create a TCP socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Set the SO_MARK value
    if packet.mark is not None:
      sock.setsockopt(socket.SOL_SOCKET, socket.SO_MARK, packet.mark)
    #Make socket non-blocking, so it doesn't block the async process
    sock.setblocking(False)

    try:
          await asyncio.wait_for(loop.sock_connect(sock, (packet.ip, packet.port)), timeout=5)
          LoggerTemplates.tcp_reachable_log(packet.ip, packet.port)
          ip_manager.add_reachable_packet(packet)
          ip_manager.success_count += 1
          ip_manager.all_checks_count += 1
          #return True
    except Exception as e:
          ip_manager.unreachable_ip_add(packet)
          LoggerTemplates.tcp_unreachable_log(packet.ip, packet.port, e)
          ip_manager.all_checks_count += 1
          #return False
    finally:
          sock.close()


async def check_icmp(packet, ip_manager):
      fail_counter = 0
      success_counter = 0
      successful_delays = 0
      ping_tasks = []
      min_succ_rate = packet.count * packet.success

      for _ in range(packet.count):
            #packet.timeout is the time that it waits for a response
            ping_tasks.append(aioping.ping(packet.ip, packet.mark, packet.timeout))
            await asyncio.sleep(packet.timeout_between)
      results = await asyncio.gather(*ping_tasks, return_exceptions=True)
      
      #Results contains the pings to one host. This function goes through them and counts the successfull, and failed tries.
      #If the ping wasn't successful an exception is returned
      for result in results:
            if isinstance(result, Exception):
                  fail_counter += 1
                  LoggerTemplates.icmp_packet_failure_log(packet.ip, fail_counter)
                  #in this case all the pings failed
                  if fail_counter == packet.count:
                        ip_manager.unreachable_ip_add(packet)
                        LoggerTemplates.icmp_unreachable_log(packet.ip, 0, packet.dns_name)
                        ip_manager.all_checks_count += 1             
                        #return False
            else:
                  result *= 1000
                  successful_delays += result
                  success_counter += 1
                  LoggerTemplates.icmp_packet_success_log(packet.ip)

      avg_delay = successful_delays / success_counter
      success_rate = success_counter / packet.count
      
      if int(min_succ_rate) <= success_counter:
            ip_manager.add_reachable_packet(packet)
            LoggerTemplates.icmp_reachable_log(packet.ip, success_rate, avg_delay)
            ip_manager.success_count += 1
            ip_manager.all_checks_count += 1
            #return True
      else:
            ip_manager.unreachable_ip_add(packet)
            LoggerTemplates.icmp_unreachable_log(packet.ip, success_rate, packet.dns_name)
            ip_manager.all_checks_count += 1
            #return False
                  

async def check_dns(server, ip_manager,port=53, timeout=5, mark=None):
    #query packet asking for the IPv4 address of www.google.com
    query_packet = b'\x00\x01\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03www\x06google\x03com\x00\x00\x01\x00\x01'
    try:
        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        if mark is not None:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_MARK, mark)
        
        sock.setblocking(False)
        
        loop = asyncio.get_running_loop()

        # Send the DNS query packet to the server
        await loop.sock_sendto(sock, query_packet, (server, port))
        
        # Receive response (if any) with individual timeout
        try:
            response, _ = await asyncio.wait_for(loop.sock_recvfrom(sock, 1024), timeout)
            LoggerTemplates.dns_reachable(server, response)
            ip_manager.success_count += 1
            ip_manager.all_checks_count += 1
        except asyncio.TimeoutError as e:
            LoggerTemplates.dns_unreachable_async(server, e)
            ip_manager.all_checks_count += 1
    except Exception as e:
        LoggerTemplates.dns_unreachable(server, e)
        ip_manager.all_checks_count += 1
    finally:
        sock.close()