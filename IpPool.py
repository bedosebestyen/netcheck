import os
source = "/run/known-webservers-for-connectivity-test/latest"


class IpPool:
    def __init__(self) -> None:
        self.ICMP_hosts = []
        self.TCP_hosts = []
        self.DNS_hosts = []
    def hosts_from_file(self, source="/run/known-webservers-for-connectivity-test/latest"):
        files = os.listdir(source)

        for file in files:
            if len(self.ICMP_hosts) < 500:
                self.ICMP_hosts.append(file)
            elif len(self.TCP_hosts) < 500:
                self.TCP_hosts.append(file)
            elif len(self.DNS_hosts) < 500:
                self.DNS_hosts.append(file)

            # Stop once all lists contain 500 IPs
            if len(self.ICMP_hosts) == 500 and len(self.TCP_hosts) == 500 and len(self.DNS_hosts) == 500:
                break

        return self.ICMP_hosts, self.TCP_hosts, self.DNS_hosts
        


    