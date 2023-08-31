import asyncio
from chcker import check_tcp, check_icmp
import logging
import sys
iplistdir = "google.com"

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.StreamHandler(sys.stdout),
                        logging.FileHandler("base_log", mode="w")
                    ])
async def main() -> None:
    try:
        
        await check_tcp("google.com", 80, 2)
        await check_icmp("google.com", 2)
    except Exception as e:
        logging.exception(f'An exception occured during the checks: {e}')
    

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        logging.exception(f"An error occured during __main__: {e}")
    
        
    
    