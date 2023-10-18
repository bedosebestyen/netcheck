import asyncio
import logging
import socket
import struct
import time
from random import randrange
from aioping_SO_MARK import aioping
#ip, mark, port, timeout

#packetet adok meg hogy utólag lehessen ellenőrizni hogy melyik unreachable-be kell rakni
async def check_tcp(packet):
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
          await loop.sock_connect(sock, (packet.ip, packet.port))
          logging.info(f"{packet.ip} is reachable on {packet.port} TCP")
          return True
    except Exception as e:
          logging.error(f"Connection failed to {packet.ip}:{packet.port} TCP: {e}")
          return packet
    finally:
          sock.close()

#itt jobban járnék ha a verbose pinget alakítanám át, még a timeoutokkal játszani kell az aiopingben       

async def check_icmp(packet):
      success_counter = 0
      successful_delays = 0
      delay = 0
      for _ in range(packet.count):
            try:
                delay = await aioping.ping(packet.ip, packet.mark)
            except TimeoutError as e:
                  logging.error(f"{packet.ip} timed out: {packet.timeout}")
            except Exception as e:
                 logging.error(f'Reaching {packet.ip} failed: {str(e)}')
                 return packet

            if delay != 0:
                  delay *= 1000
                  successful_delays += delay
                  success_counter += 1
#lehet ide kell átrakni majd a hiuba kiírást is
      avg_delay = successful_delays / success_counter
      success_rate = success_counter / packet.count
      if packet.count * packet.success <= success_counter:
                 logging.info(f'{packet.ip} is reachable with ICMP. \n\t\t\t\t Avg_Succ_Delay: {avg_delay:.4f} ms \n\t\t\t\t Succ_Rate: {success_rate:.2%}')
                 return True
      else:
        logging.info(f'{packet.ip} is not reachable with ICMP.\n'
                     f'Succ_Rate: {success_rate:.2%}')
        return False
                        