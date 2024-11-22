from arp_scan import scan
from mac_resolver import get_mac
from discord import send_to_discord
from utils import display_banner
import argparse

def main():
    display_banner()

    parser = argparse.ArgumentParser(description="visARP - A modular ARP tool.")
    parser.add_argument("-r", "--range", help="IP range to scan (e.g., 192.168.1.0/24)", type=str)
    parser.add_argument("-m", "--mac", help="Resolve MAC address for an IP", type=str)
    parser.add_argument("-w", "--webhook", help="Discord webhook URL", required=True, type=str)
    args = parser.parse_args()

    result = ""
    if args.range:
        devices = scan(args.range)
        result = "\n".join([f"IP: {device['ip']} - MAC: {device['mac']}" for device in devices])
    elif args.mac:
        mac = get_mac(args.mac)
        result = f"IP: {args.mac} - MAC: {mac}" if mac else "Failed to resolve MAC address."
    else:
        print("No valid action specified. Use -h for help.")
        return

    print(result)
    send_to_discord(args.webhook, result)

if __name__ == "__main__":
    main()
