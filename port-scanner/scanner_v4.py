import socket
import threading
import time
from datetime import datetime

RESET  = "\033[0m"
GREEN  = "\033[32m"
CYAN   = "\033[36m"
RED    = "\033[31m"
BOLD   = "\033[1m"

open_ports = []
lock = threading.Lock()
semaphore = threading.Semaphore(100)

def get_service(port):
    try:
        return socket.getservbyport(port)
    except:
        return "unknown"

def scan_port(target, port):
    with semaphore:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        result = s.connect_ex((target, port))
        if result == 0:
            service = get_service(port)
            with lock:
                open_ports.append(port)
                print(f"  {GREEN}[OPEN]{RESET}  {BOLD}{port:<6}{RESET}  {CYAN}{service}{RESET}")
        s.close()

def resolve_target(host):
    try:
        ip = socket.gethostbyname(host)
        return ip
    except socket.gaierror:
        print(f"\n{RED}[ERROR]{RESET} Could not resolve hostname: {host}")
        return None

def print_banner(target, ip, start, end):
    print(f"\n{BOLD}{'='*40}{RESET}")
    print(f"  {BOLD}Python Port Scanner v4{RESET}")
    print(f"{'='*40}{RESET}")
    print(f"  Target   : {CYAN}{target}{RESET}")
    print(f"  IP       : {CYAN}{ip}{RESET}")
    print(f"  Ports    : {start} - {end}")
    print(f"  Started  : {datetime.now().strftime('%H:%M:%S')}")
    print(f"{'='*40}\n")

def save_results(target, ip, start, end, ports, duration):
    filename = f"scan_{ip}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    filepath = f"/data/data/com.termux/files/home/projects/python/{filename}"
    with open(filepath, "w") as f:
        f.write(f"Port Scan Report\n")
        f.write(f"{'='*40}\n")
        f.write(f"Target   : {target}\n")
        f.write(f"IP       : {ip}\n")
        f.write(f"Range    : {start} - {end}\n")
        f.write(f"Date     : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Duration : {duration:.2f} seconds\n")
        f.write(f"{'='*40}\n\n")
        if ports:
            for p in sorted(ports):
                service = get_service(p)
                f.write(f"[OPEN] Port {p} — {service}\n")
        else:
            f.write("No open ports found.\n")
    print(f"\n  {GREEN}[SAVED]{RESET} Report saved to: {CYAN}{filename}{RESET}")

target_input = input("Target IP or hostname: ")
start_port   = int(input("Start port: "))
end_port     = int(input("End port: "))

ip = resolve_target(target_input)
if not ip:
    exit()

print_banner(target_input, ip, start_port, end_port)

start_time = time.time()

threads = []
for port in range(start_port, end_port + 1):
    t = threading.Thread(target=scan_port, args=(ip, port))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

duration = time.time() - start_time

print(f"\n{BOLD}{'='*40}{RESET}")
print(f"  Scan complete in {BOLD}{duration:.2f} seconds{RESET}")
print(f"  Open ports found: {BOLD}{len(open_ports)}{RESET}")
print(f"  {sorted(open_ports)}")
print(f"{'='*40}\n")

save_results(target_input, ip, start_port, end_port, open_ports, duration)
