import asyncio
import logging
import socket
import struct
import time
from random import randrange
from aioping_SO_MARK import aioping
#ip, mark, port, timeout
async def check_tcp(host, mark,port=80, timeout=1):
    #Get the current event loop
    loop = asyncio.get_running_loop()
    #Create a TCP socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Set the SO_MARK with value 10
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_MARK, mark)
    #Make socket non-blocking
    sock.setblocking(False)
    #Try to connect

    try:
          await loop.sock_connect(sock, (host, port))
          logging.info(f"{host} is reachable on {port} TCP")
          return True
    except Exception as e:
          logging.error(f"Connection failed to {host}:{port} TCP: {e}")
    finally:
          sock.close()

#itt jobban járnék ha a verbose pinget alakítanám át, még a timeoutokkal játszani kell az aiopingben       
#host: ip, mark: SO_MARK, seq: how many times the ICMP echo request should be sent
async def check_icmp(host, mark, count, timeout, success_percentage):
      results = []
      delay = 0
      for _ in range(count):
            try:
                delay = await aioping.ping(host, mark)
            except TimeoutError as e:
                 logging.error(f'{host} timed out after {timeout}s ICMP')
            except Exception as e:
                 logging.error(f'Reaching {host} failed: {str(e)}')

            if delay != 0:
                  delay *= 1000
                  logging.info(f'{host} get ping in {delay:.4f}ms')
                  results.append(host)
      if count * success_percentage < len(results):
                 logging.info(f'{host} is reachable with ICMP.')
                 
                 return True      
                        