import aioping
import socket
import sys
import asyncio
import logging



async def check_tcp(host, port=80, timeout=1):
    try:
        await asyncio.wait_for(asyncio.open_connection(host, port), timeout=timeout)
        logging.info(f"{host} is reachable TCP")
        return True
    except (asyncio.TimeoutError, OSError) as e:
             logging.error(f"Connection to {host}:{port} timed out: {e}")
             
        
    
async def check_icmp(host, timeout=2):
    try:
        delay = await aioping.ping(host, timeout=timeout)
        if delay is not None:
            logging.info(f"{host} is reachable ({delay} ms) ICMP")
            
            return True
            

        
    except (asyncio.TimeoutError, OSError) as e:
             logging.error(f"Connection to {host} timed out: {e}")
        
        
    
       





