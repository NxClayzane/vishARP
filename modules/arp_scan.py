from scapy.all import srp, Ether, ARP, conf, get_if_hwaddr
import psutil  # For checking the network interface


def get_active_iface():
    # Automatically detect the active network interface
    # We will use psutil to find an active interface
    interfaces = psutil.net_if_addrs()
    for iface in interfaces:
        if psutil.net_if_stats()[iface].isup:  # Check if the interface is up
            return iface
    return None  # If no interface is found


def scan(ip_range):
    iface = get_active_iface()  # Automatically get the active interface
    if not iface:
        print("No active network interface found.")
        return []

    # Set Scapy to use the active interface
    conf.iface = iface

    arp_request = ARP(pdst=ip_range)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request

    try:
        answered_list = srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    except Exception as e:
        print(f"Error during ARP scan: {e}")
        return []

    devices = []
    for element in answered_list:
        devices.append({'ip': element[1].psrc, 'mac': element[1].hwsrc})

    return devices
