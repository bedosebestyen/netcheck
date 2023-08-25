import socket
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

async def check_tcp_syn(host, port, timeout=1):
    try:        
        try:
            socket.gethostbyname(host)
        except socket.gaierror as e:
            raise ValueError(f"Invalid IP address or hostname: {host}")
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            """if mark is not None:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_MARK, mark)"""
            try:
                #_, _ placeholder for reader, writer
                _, _ = await asyncio.wait_for(asyncio.open_connection(host, port), timeout)
                print("siker")
            except asyncio.TimeoutError as e:
                 logging.error(f"Connection to {host}:{port} timed out: {e}")
                 return(f"Connection to {host}:{port} timed out: {e}")
    except OSError as e:
        logging.error(f"Socket error: {e}")
        return(f"Socket error: {e}")
    

async def send_icmp_echo_request(host, timeout):
    """
    Send an ICMP echo request to the specified host.

    Args:
        host (str): The host to send the ICMP echo request to.
        timeout (float): The timeout value in seconds.

    Returns:
        None
    """
    try:
        reader, writer = await asyncio.open_connection(host, 1024, timeout=timeout)  # Using port 1 for ICMP
        writer.write(b'')  # Sending an empty packet as ICMP echo request
        await writer.drain()  # Wait until data is flushed (optional)
        writer.close()  # Close the writer

        # Receiving a response (if any)
        data = await reader.read(1024)

        if data:
            print("ICMP echo successful")
        else:
            print("No ICMP response received")

    except asyncio.TimeoutError as e:
        print(f"ICMP echo to {host} timed out: {e}")
    except OSError as e:
        print(f"Socket error: {e}")
    finally:
        writer.close()
       





