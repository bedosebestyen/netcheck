import os
import subprocess
source = "/run/known-webservers-for-connectivity-test/latest"


class IP_Pool:
    def __init__(self) -> None:
        self.ICMP_hosts = []
        self.TCP_hosts = []

    def hosts_from_file(self, source="/run/known-webservers-for-connectivity-test/latest"):
        files = os.listdir(source)

        i = 0
        for file in files:
            
            if i == 0:
                self.ICMP_hosts.append(file)
            else:
                self.TCP_hosts.append(file)
            i = 1 - i  # Toggle between 0 and 1 to alternate between ICMP and TCP

            # Stop once both lists contain 100 IPs
            if len(self.ICMP_hosts) == 100 and len(self.TCP_hosts) == 100:
                break

        return self.ICMP_hosts, self.TCP_hosts
    
    def ip_pool_generator(script_path="./ip_pool.sh", sudo_script_path = "./ipv4_pool.sh"):
        
        try:
            subprocess.run(["sudo", script_path], check=True, shell=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running '{script_path}': {e}")
        
        try:
            subprocess.run(["sudo",sudo_script_path], check=True, shell=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running 'sudo {script_path}': {e}")



    