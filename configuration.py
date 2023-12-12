import json

class Configuration:
    def __init__(self, config_file_path='config.json') -> None:
        self.config_file_path = config_file_path
        self.load_config()

    def load_config(self):
        with open(self.config_file_path) as f:
            config_data = json.load(f)
        #TCP_packet
        tcp_packet_values = config_data['tcp_packet']
        self.tcp_mark = tcp_packet_values['mark']
        self.tcp_timeout_tcp = tcp_packet_values['timeout_tcp']
        self.tcp_port = tcp_packet_values['port']

        #ICMP packet
        icmp_packet_values = config_data['icmp_packet']
        self.icmp_mark = icmp_packet_values['mark']
        self.icmp_timeout_waiting_for_response = icmp_packet_values['timeout_waiting_for_response']
        self.icmp_timeout_between_pings = icmp_packet_values['timeout_between_pings']
        self.icmp_count = icmp_packet_values['count']
        self.icmp_success = icmp_packet_values['success']