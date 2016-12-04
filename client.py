from scapy.all import *
import time
import os

RANDOM_IP_POOL=['0.0.0.0/0']


def get_data():
    data_prefix = "SDN_SPY_"
    return data_prefix + str(int(random.uniform(100000, 999999)))


def get_random_port():
    int(random.uniform(10000, 60000))


def get_random_tos():
    int(random.uniform(0, 8))


def get_random_ip():
    str_ip = RANDOM_IP_POOL[random.randint(0,len(RANDOM_IP_POOL) - 1)]
    str_ip_addr = str_ip.split('/')[0]
    str_ip_mask = str_ip.split('/')[1]
    ip_addr = struct.unpack('>I',socket.inet_aton(str_ip_addr))[0]
    mask = 0x0
    for i in range(31, 31 - int(str_ip_mask), -1):
        mask |= 1 << i
    ip_addr_min = ip_addr & (mask & 0xffffffff)
    ip_addr_max = ip_addr | (~mask & 0xffffffff)
    return socket.inet_ntoa(struct.pack('>I', random.randint(ip_addr_min, ip_addr_max)))


def get_random_mac():
    mac = [0x52, 0x54, 0x00,
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac))


def send_udp(packet):
    sendp(packet)
    time.sleep(1)
    sendp(packet)
    time.sleep(1)

ip_dst = "10.0.0.1"
mac_dst = "00:00:00:00:00:01"

os.system("tcpdump udp -w ./client.pcap&>/dev/null")

print "change dst port"
pkt = Ether(dst=mac_dst)/IP(dst=ip_dst)/UDP(sport=9250, dport=get_random_port())/get_data()
send_udp(pkt)

print "change src port"
pkt = Ether(dst=mac_dst)/IP(dst=ip_dst)/UDP(sport=get_random_port(), dport=9250)/get_data()
send_udp(pkt)

print "change ToS bits"
pkt = Ether(dst=mac_dst)/IP(dst=ip_dst, tos=get_random_tos())/UDP(sport=9250, dport=9250)/get_data()
send_udp(pkt)

print "change src IP"
pkt = Ether(dst=mac_dst)/IP(src=get_random_ip(), dst=ip_dst)/UDP(sport=9250, dport=9250)/get_data()
send_udp(pkt)

print "change dst IP"
pkt = Ether(dst=mac_dst)/IP(dst=get_random_ip())/UDP(sport=9250, dport=9250)/get_data()
send_udp(pkt)

print "change src MAC"
pkt = Ether(src=get_random_mac(), dst=mac_dst)/IP(dst=ip_dst)/UDP(sport=9250, dport=9250)/get_data()
send_udp(pkt)

pkt = Ether(dst=mac_dst)/IP(dst=ip_dst)/UDP(sport=9250, dport=9250)/"SDN_SPY_exit"
sendp(pkt)

os.system("./kill_process.sh tcpdump")
