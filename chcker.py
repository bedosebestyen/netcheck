import aioping
import socket
import asyncio
import logging


logging.basicConfig(level=logging.INFO)

async def check_tcp(host, port, timeout=1):
    try:
        """
        try:
            socket.gethostbyname(host)
        except socket.gaierror as e:
            raise ValueError(f"Invalid IP address or hostname: {host}")
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            """
            if mark is not None:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_MARK, mark)
            """
            try:
                _, _ = await asyncio.wait_for(asyncio.open_connection(host, port), timeout=timeout)
                logging.info(f"{host} is reachable TCP")
                return True
            except asyncio.TimeoutError as e:
                 logging.exception(f"Connection to {host}:{port} timed out: {e}")
                 raise
    except OSError as e:
        logging.exception(f"Socket error: {e}")
        raise
    
async def check_icmp(host, timeout=2):
    """
    Sends an ICMP echo request to the specified host.

    Args:
            host (str): The IP address or hostname of the target host.
            weight (int): The number of echo requests to send.
            timeout (float, optional): The maximum time to wait for a response, in seconds. Defaults to 2.

        Returns:
            bool: True if the host responded, False otherwise.

        Raises:
            asyncio.TimeoutError: If the ping times out.
            Exception: If an error occurs while pinging the host.
    """
    try:
        delay = await aioping.ping(host, timeout=timeout)
        if delay is not None:
            logging.info(f"{host} is reachable ({delay} ms) ICMP")
            return True
        else:
            logging.error(f"Host {host} did not respond")
            raise
    except asyncio.TimeoutError:
        logging.exception(f"Timeout while pinging {host}")
        raise
    except Exception as e:
        logging.exception(f"An error occurred while pinging {host}: {e}")
        raise
        
    
       





