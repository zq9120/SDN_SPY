from scapy.all import *

client_pacp = rdpcap("client.pcap")
server_pacp = rdpcap("server.pcap")

client_time = []
server_time = []


for i in range(0, len(client_pacp)):
    packet = client_pacp[i]
    if str(packet.load).startswith("SDN_SPY"):
        print packet.time
        client_time.append(packet.time)

for i in range(0, len(server_pacp)):
    packet = server_pacp[i]
    if str(packet.load).startswith("SDN_SPY"):
        print packet.time
        server_time.append(packet.time)


print "client_time_count: ", len(client_time)
print "server_time_count: ", len(server_time)