import socket
import asyncio


async def check_icmp(host, timeout=1, mark=None):
    try:
        icmp = socket.getprotobyname('icmp')
        with socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp) as sock:
            if mark is not None:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_MARK, mark)
            sock.settimeout(timeout)
            await asyncio.to_thread(sock.connect, (host, 1))
        return True
    except socket.error:
        return False

async def check_tcp_syn(host, port, timeout=1, mark=None):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if mark is not None:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_MARK, mark)
            sock.settimeout(timeout)
            sock.connect((host, port))
            return True
    except socket.error:
        return False