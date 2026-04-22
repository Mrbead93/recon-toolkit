import socket
import threading

open_ports = []
lock = threading.Lock()

def scan_port(target, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    result = s.connect_ex((target, port))
    if result == 0:
        with lock:
            open_ports.append(port)
            print(f"[OPEN] Port {port}")
    s.close()

target = input("Enter target IP or hostname: ")
print(f"\nScanning {target}...\n")

threads = []
for port in range(1, 1025):
    t = threading.Thread(target=scan_port, args=(target, port))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"\nScan complete. Open ports: {sorted(open_ports)}")
