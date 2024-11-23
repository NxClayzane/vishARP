# Modules

from modules.arp_scan import scan
from modules.mac_resolver import get_mac
from modules.discord import send_to_discord
from modules.utils import display_banner
from modules.logging import LogFile

import requests
import argparse
import socket
import sys



def main():
    display_banner()
    

    # Setup argument parser
    parser = argparse.ArgumentParser(description="visARP")
    parser.add_argument("-r", "--range", help="IP range to scan (e.g., 192.168.1.0/24)", type=str)
    parser.add_argument("-m", "--mac", help="Resolve MAC address for an IP", type=str)
    parser.add_argument("-w", "--webhook", help="Discord webhook URL", required=True, type=str)
    args = parser.parse_args()

    # Validate Discord Webhook URL
    if not args.webhook.startswith("https://discord.com/api/webhooks/"):
        print("Error: Invalid Discord webhook URL.")
        logging.error(f"Invalid Discord webhook URL: {args.webhook}")
        sys.exit(1)

    result = ""
    try:
        if args.range:
            # Attempt ARP scan
            try:
                devices = scan(args.range)
                result = "\n".join([f"IP: {device['ip']} - MAC: {device['mac']}" for device in devices])
            except Exception as e:
                print(f"Error scanning range {args.range}: {e}")
                logging.error(f"Error scanning range {args.range}: {e}")
                sys.exit(1)
        elif args.mac:
            # Attempt to resolve MAC address for the given IP
            try:
                mac = get_mac(args.mac)
                if mac:
                    result = f"IP: {args.mac} - MAC: {mac}"
                else:
                    result = "Failed to resolve MAC address."
            except socket.error as e:
                print(f"Error resolving MAC address for {args.mac}: {e}")
                logging.error(f"Socket error resolving MAC for {args.mac}: {e}")
                sys.exit(1)
            except Exception as e:
                print(f"Unexpected error resolving MAC address: {e}")
                logging.error(f"Unexpected error resolving MAC address: {e}")
                sys.exit(1)
        else:
            print("Error: No valid action specified. Use -h for help.")
            logging.error("No valid action specified. Exiting.")
            sys.exit(1)

        print(result)

        # Attempt to send result to Discord
        try:
            send_to_discord(args.webhook, result)
        except requests.exceptions.RequestException as e:
            print(f"Error sending message to Discord: {e}")
            logging.error(f"Error sending message to Discord: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error sending to Discord: {e}")
            logging.error(f"Unexpected error sending to Discord: {e}")
            sys.exit(1)

    except Exception as e:
        print(f"Unexpected error: {e}")
        logging.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
        logging.info("Process interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Unhandled exception: {e}")
        logging.critical(f"Unhandled exception: {e}")
        sys.exit(1)
