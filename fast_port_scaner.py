import argparse
import netifaces
import ipaddress
import socket
import selectors
from concurrent.futures import ProcessPoolExecutor
import multiprocessing
import json
import os
import subprocess

class NetworkScanner:
    def __init__(self, interface=None, ip_range=None, port_range=None):
        self.maximal_ports = 65535
        self.open_ports = {}
        
        # Netzwerkschnittstelle oder IP-Bereich abrufen
        if ip_range:
            hosts = self.get_custom_hosts(ip_range)
        else:
            hosts = self.get_hosts(interface)
        
        if not hosts:
            print("No valid network interface or IP range found. Exiting.")
            return
        
        port_range = port_range if port_range else range(self.maximal_ports)
        max_processes = multiprocessing.cpu_count()
        results = {}

        with ProcessPoolExecutor(max_workers=max_processes) as executor:
            futures = {executor.submit(self.run_scan, str(host), port_range): host for host in hosts}
            for future in futures:
                host = futures[future]
                try:
                    host, open_ports = future.result()
                    results[host] = open_ports
                except Exception as e:
                    print(f"Error scanning host {host}: {e}")

        # Ergebnisse speichern
        current_dir = os.getcwd()
        output_file = os.path.join(current_dir, 'open_ports.json')
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=4)
        
        print("Scan finished. Results saved in 'open_ports.json'.")

    def get_all_local_ips(self):
        interfaces = netifaces.interfaces()
        ip_addresses = {}
        for interface in interfaces:
            addresses = netifaces.ifaddresses(interface)
            if netifaces.AF_INET in addresses:
                ip_info = addresses[netifaces.AF_INET][0]
                ip_addresses[interface] = ip_info['addr']
        return ip_addresses

    def get_net_interface(self, interface):
        interfaces = self.get_all_local_ips()
        return interfaces.get(interface, None)

    def port_scan(self, host, ports):
        selector = selectors.DefaultSelector()
        open_ports = []
        for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setblocking(False)
            try:
                sock.connect_ex((host, port))
            except BlockingIOError:
                pass
            selector.register(sock, selectors.EVENT_WRITE, data=port)
        while True:
            events = selector.select(timeout=1)
            if not events:
                break
            for key, _ in events:
                sock = key.fileobj
                port = key.data
                try:
                    sock.getpeername()
                    open_ports.append(port)
                    print(f"Port {port} is open for host {host}")
                    service = self.identify_service(port)
                    self.open_ports[host] = [port, service]
                except (socket.error, OSError):
                    pass
                finally:
                    selector.unregister(sock)
                    sock.close()
        return open_ports

    def run_scan(self, host, ports):
        open_ports = self.port_scan(host, ports)
        return host, open_ports

    def get_hosts(self, interface):
        net_interface = self.get_net_interface(interface)
        if not net_interface:
            return []
        network = ipaddress.ip_network(f"{net_interface}/24", strict=False)
        hosts = list(network.hosts())
        return hosts

    def get_custom_hosts(self, ip_range):
        network = ipaddress.ip_network(ip_range, strict=False)
        return list(network.hosts())

    def identify_service(self, port):
        try:
            result = subprocess.check_output(['lsof', '-i', f':{port}'], stderr=subprocess.DEVNULL)
            service_name = result.decode().split('\n')[1].split()[0]
            return service_name
        except (IndexError, subprocess.CalledProcessError):
            return "Unknown"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Network Port Scanner")
    parser.add_argument('-i', '--interface', help="Network interface to scan (e.g., 'eno1').")
    parser.add_argument('-r', '--ip-range', help="Custom IP range to scan (e.g., '192.168.1.0/24').")
    parser.add_argument('-p', '--port-range', help="Port range to scan (e.g., '20-80').", default=None)

    args = parser.parse_args()

    # Portbereich parsen
    if args.port_range:
        try:
            start, end = map(int, args.port_range.split('-'))
            port_range = range(start, end + 1)
        except ValueError:
            print("Invalid port range format. Use 'start-end' (e.g., '20-80').")
            exit(1)
    else:
        port_range = None

    NetworkScanner(interface=args.interface, ip_range=args.ip_range, port_range=port_range)
