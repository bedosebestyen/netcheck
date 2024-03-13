import os
source = "/run/known-webservers-for-connectivity-test/latest"


class IpPool:
    def __init__(self) -> None:
        self.ICMP_hosts = {}
        self.TCP_hosts = []
        self.DNS_hosts = []
    def hosts_from_file(self, source=source):
        files = os.listdir(source)

        for file in files:
            if len(self.DNS_hosts) < 500:
                self.DNS_hosts.append(file)
            elif len(self.TCP_hosts) < 500:
                self.TCP_hosts.append(file)
            self.icmp_read(source=source)
            # Stop once all lists contain 500 IPs
            if len(self.ICMP_hosts) == 500 and len(self.TCP_hosts) == 500 and len(self.DNS_hosts) == 500:
                break

        return self.ICMP_hosts, self.TCP_hosts, self.DNS_hosts
    
    def icmp_read(self, source=source):

        for filename in os.listdir(source):
            file_path = os.path.join(source, filename)
            if len(self.ICMP_hosts) < 500:
                if os.path.isfile(file_path):
                    with open(file_path, "r") as file:
                        content = (file.read()).strip("\n")
                        # ext = extract(content)
                        # domain = f"{ext.domain}.{ext.suffix}" 
                        if content:
                            self.ICMP_hosts[filename] = content
        
        return self.ICMP_hosts