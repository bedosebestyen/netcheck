import asyncio
import logging
import aioping
import socket

async def check_tcp(host, port=80, timeout=1):
    #Get the current event loop
    loop = asyncio.get_running_loop()
    #Create a TCP socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Set the SO_MARK with value 10
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_MARK, 10)
    #Make socket non-blocking
    sock.setblocking(False)
    #Try to connect

    try:
          logging.info('1')
          await loop.sock_connect(sock, (host, port))
          logging.info(f"{host} is reachable on {port} TCP")
          return True
    except Exception as e:
          logging.error(f"Connection failed to {host}:{port} TCP: {e}")
    finally:
          sock.close()
             
        
    
async def check_icmp(host):
    try:
            delay = await aioping.ping(host)
            if delay is not None:
                  logging.info(f"{host} is reachable {delay} ms ICMP")
                  return True
            
    except (Exception, asyncio.TimeoutError) as e:
          logging.error(f"Connection to {host} timed out: {e} ICMP")
          
