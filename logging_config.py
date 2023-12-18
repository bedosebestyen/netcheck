import logging
import sys

def setup_runtime_logger():
    runtime_logger = logging.getLogger('runtime_logger')
    runtime_log_handler = logging.FileHandler("runtime_log.log", mode="w")
    
    # Add a formatter with a timestamp to the log handler
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    runtime_log_handler.setFormatter(formatter)
    
    runtime_logger.setLevel(logging.INFO)
    runtime_logger.addHandler(logging.StreamHandler(sys.stdout))
    runtime_logger.addHandler(runtime_log_handler)
    
    return runtime_logger

def setup_summary_logger():
    summary_logger = logging.getLogger('summary_logger')
    summary_log_handler = logging.FileHandler("summary.log", mode="w")
    
    # Add a formatter with a timestamp to the log handler
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    summary_log_handler.setFormatter(formatter)
    
    summary_logger.setLevel(logging.INFO)
    summary_logger.addHandler(logging.StreamHandler(sys.stdout))
    summary_logger.addHandler(summary_log_handler)
    
    return summary_logger


runtime_logger = setup_runtime_logger()
summary_logger = setup_summary_logger()

class Logger_Templates():
    #staticmethod is useful here because they are not bound to a class instance, so they can be called directly without creating a class instance
    @staticmethod
    def tcp_reachable_log(ip, port):
        runtime_logger.info(f"{ip} is reachable on {port} TCP")
    @staticmethod
    def tcp_unreachable_log(ip, port, error_message):
        runtime_logger.error(f"Connection failed to {ip}:{port} TCP: {error_message}")
    @staticmethod
    def icmp_reachable_log(ip, success_rate, avg_delay):
        runtime_logger.info(f'{ip} is reachable with ICMP.\n\t\t\t\t Avg_Succ_Delay: {avg_delay:.4f} ms \n\t\t\t\t Succ_Rate: {success_rate:.2%}')
    @staticmethod
    def icmp_unreachable_log(ip, success_rate):
        runtime_logger.info(f'{ip} is not reachable with ICMP.\n\t\t\t\t Succ_Rate: {success_rate:.2%}')
    @staticmethod
    def icmp_packet_success_log(ip):
        runtime_logger.info(f"{ip} host ICMP try SUCCESS")
    @staticmethod
    def icmp_packet_failure_log(ip, fail_count):
        runtime_logger.error(f"{ip} host FAILED ICMP try || Fail_Count: {fail_count}")
    @staticmethod
    def summary_log(unreachable_icmp, unreachable_tcp, reachable_icmp, reachable_tcp):
        summary_logger.info(f'Unreachable ICMP: {unreachable_icmp}\n\t\t\t\tUnreachable TCP: {unreachable_tcp}\n\t\t\t\tReachable_ICMP: {reachable_icmp}\n\t\t\t\tReachable_TCP: {reachable_tcp}')
    @staticmethod
    def icmp_unreachable_full(oldest_ip):
        runtime_logger.info(f'ICMP unreachable reached max capacity first element will be put back into reachable, ip: {oldest_ip}')
        summary_logger.info(f'ICMP unreachable reached max capacity first element will be put back into reachable, ip: {oldest_ip}')
    @staticmethod
    def tcp_unreachable_full(oldest_ip):
        runtime_logger.info(f'TCP unreachable reached max capacity first element will be put back into reachable, ip: {oldest_ip}')
        summary_logger.info(f'TCP unreachable reached max capacity first element will be put back into reachable, ip: {oldest_ip}')
    
    
        