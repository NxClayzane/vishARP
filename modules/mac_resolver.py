import socket

def get_mac(ip):
    try:
        return socket.gethostbyname_ex(ip)[2][0]
    except socket.error as e:
        print(f"Error resolving MAC address for {ip}: {e}")
        return None
