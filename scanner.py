import socket
import subprocess
import threading
import ipaddress
import logging
import re
import os
import sys

# Set up logging
logging.basicConfig(filename="scan_results.log", level=logging.INFO, format='%(asctime)s - %(message)s')

# List of common ports to scan
common_ports = [22, 80, 443, 21, 53, 3306, 8080]

# Function to check if the script is running with elevated privileges (root)
def check_permission():
    if not is_user_root():
        print("WARNING: This script may require elevated privileges (root) to scan all ports and networks.")
        sys.exit(1)

def is_user_root():
    """ Check if the user is running as root (Linux) """
    return os.geteuid() == 0

# Function to get the local IP address of a given network interface (eth0, wlan0, etc.)
def get_local_ip(interface):
    """
    Get the local IP address of a given network interface (eth0, wlan0, etc.)
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip = subprocess.check_output(['ip', 'addr', 'show', interface]).decode('utf-8')
    match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)', ip)
    if match:
        return match.group(1)
    else:
        raise Exception(f"Could not find IP address for interface {interface}")

# Function to get the network address from the local IP (calculate /24 network)
def get_network_from_ip(local_ip):
    """
    Given a local IP, calculate the network address with the subnet mask /24.
    """
    match = re.match(r"(\d+\.\d+\.\d+)\.\d+", local_ip)
    if match:
        network_base = match.group(1)
        return f"{network_base}.0/24"  # Network address in CIDR format (e.g., 192.168.1.0/24)
    else:
        raise Exception("Unable to determine the local network")

# Function to grab the banner from an open port (for service identification)
def grab_banner(target_ip, target_port):
    try:
        # Attempt to connect to the target port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((target_ip, target_port))
        banner = sock.recv(1024).decode().strip()
        if banner:
            return banner
        return "No banner"
    except Exception as e:
        return "No banner"
    finally:
        sock.close()

# Function to scan a port and grab banner if open
def scan_port(target_ip, target_port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target_ip, target_port))
        if result == 0:
            print(f"[+] Port {target_port} is OPEN on {target_ip}")
            banner = grab_banner(target_ip, target_port)
            logging.info(f"OPEN {target_ip}:{target_port} - Banner: {banner}")
        else:
            print(f"[-] Port {target_port} is CLOSED on {target_ip}")
        sock.close()
    except socket.error:
        print(f"Couldn't connect to {target_ip} on port {target_port}")

# Function to discover live IPs in a subnet
def discover_ips(network):
    live_ips = []
    for ip in network.hosts():
        ip_str = str(ip)
        response = subprocess.call(['ping', '-c', '1', ip_str], stdout=subprocess.DEVNULL)
        if response == 0:
            print(f"[+] {ip_str} is live")
            live_ips.append(ip_str)
    return live_ips

# Function to scan a range of ports on a live IP using multi-threading
def scan_ports_on_ip(target_ip, start_port, end_port):
    threads = []
    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=scan_port, args=(target_ip, port))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

# Function to get the first active wireless interface
def get_wireless_interface():
    interfaces = subprocess.check_output(['ls', '/sys/class/net']).decode().splitlines()
    # Look for wlan* interface names
    for interface in interfaces:
        if interface.startswith('wlan'):
            return interface
    return None

# Function to scan a network (subnet) for live IPs and open ports
def scan_network_for_ports(network_str, start_port, end_port):
    network = ipaddress.ip_network(network_str)
    live_ips = discover_ips(network)
    for ip in live_ips:
        print(f"\nScanning IP {ip} for open ports...")
        scan_ports_on_ip(ip, start_port, end_port)

# Main function to execute the scanning process
def main():
    # Check if we have root (elevated) permissions
    check_permission()

    # Get local IP address for eth0 and wlan0
    try:
        eth0_ip = get_local_ip('eth0')
        print(f"eth0 IP: {eth0_ip}")

        # Try to get wlan IP address dynamically
        wlan_interface = get_wireless_interface()
        if wlan_interface:
            wlan_ip = get_local_ip(wlan_interface)
            print(f"Wireless Interface ({wlan_interface}) IP: {wlan_ip}")
        else:
            print("No wireless interface found.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Automatically get the network range based on the local machine's IP
    network_str = get_network_from_ip(eth0_ip)  # Using eth0 as default network interface
    print(f"Starting scan on network: {network_str} from port 20 to 100")

    # Define the port range
    start_port = 20
    end_port = 100

    # Run the scan
    scan_network_for_ports(network_str, start_port, end_port)

if __name__ == "__main__":
    main()