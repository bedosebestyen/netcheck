import asyncio
import os
import sys
import time
from chcker import check_tcp_syn, check_icmp
import logging

iplistdir = "/run/known-webservers-for-connectivity-test/latest"
logging.basisConfig(level=logging.INFO)


async def main():
    await check_tcp_syn("google.com", 80, 2)
    await check_icmp("google.com", 2)
    

if __name__ == '__main__':
    asyncio.run(main())
    
        
    
    