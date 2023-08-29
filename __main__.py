import asyncio
from chcker import check_tcp, check_icmp
import logging

iplistdir = "/run/known-webservers-for-connectivity-test/latest"
logging.basicConfig(level=logging.DEBUG, filename="main.log")

# Logger for exceptions
exception_logger = logging.getLogger("exceptions")
exception_logger.setLevel(logging.DEBUG)
exception_handler = logging.FileHandler("exceptions.log")
exception_logger.addHandler(exception_handler)

# Logger for info messages
info_logger = logging.getLogger("info")
info_logger.setLevel(logging.INFO)
info_handler = logging.FileHandler("info.log")
info_logger.addHandler(info_handler)

def print_logs(*loggers):
    for logger in loggers:
        for handler in logger.handlers:
            with open(handler.baseFilename, "r") as file:
                print(f"Log file: {handler.baseFilename}")
                print(file.read())
                print("=" * 80)
    
async def main():
    await check_tcp("google.com", 80, 2)
    await check_icmp("google.com", 2)
    print_logs(exception_logger, info_logger)
    
    

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        print(f'Exception: {e}')
    
        
    
    