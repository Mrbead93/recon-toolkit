import socket
import threading

RESET = "\033[0m"
GREEN = "\033[32m"
CYAN = "\033[36m"
BOLD = "\033[1m"

open_ports = []
lock = threading.Lock()

def get_service(port):
    try:
        return socket.getservbyport(port)
    except:
        return "unknown"

def scan_port(target, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    result = s.connect_ex((target, port))
    if result == 0:
        service = get_service(port)
        with lock:
            open_ports.append(port)
            print(f"{GREEN}[OPEN]{RESET} Port {BOLD}{port}{RESET} — {CYAN}{service}{RESET}")
    s.close()

print(f"\n{BOLD}=== Python Port Scanner v3 ==={RESET}\n")
target = input("Target IP or hostname: ")
start_port = int(input("Start port: "))
end_port = int(input("End port: "))

print(f"\nScanning {CYAN}{target}{RESET} from port {start_port} to {end_port}...\n")

threads = []
for port in range(start_port, end_port + 1):
    t = threading.Thread(target=scan_port, args=(target, port))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"\n{BOLD}Scan complete.{RESET} Open ports: {sorted(open_ports)}")
