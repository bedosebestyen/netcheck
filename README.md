# netcheck

IpPool.py:
Contains IpPool class, that is used to get the IPs from the source and put 100 in ICMP_hosts, and TCP_hosts. These hosts will be checked by the functions in Checker.py.

ConfigLoad.py:
Contains a Configuration class. The values are loaded from the config.json. These values are later used in PacketFacktory to create the packets.

PacketsBase.py:
Contains a base Packet class, its' child classes(ICMP_packet, TCP_packet) and a SingletonMeta class(later used by PacketLogic class).

PacketFactory.py:
This creates the packets depending on adjustable(config.json) chances. The values it uses are from the Configuration class from ConfigLoad.py.

PacketLogic.py:
This contains PacketLogic class, in which are all the functions that are needed for
removing and adding hosts to different lists.(unreachable_ICMP, reachable_TCP)

Checker.py:
For now it contains functions: check_tcp, check_icmp and task_creator(creates async tasks from the aforementioned checker functions).

Config.json:
Contains the adjustable parameters of the packets.
