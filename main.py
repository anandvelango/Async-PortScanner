import socket
import asyncio
import time
import sys

async def main():
    target = input("[-] Target (e.g. example.com, 192.168.1.1): ")
    
    try:
        host = socket.gethostbyname(target)
    except socket.gaierror:
        print(f"[!] {target} is not a valid domain name")
        sys.exit(0)

    reqs = [(scan(host, port)) for port in range(1,6000)]
    ports = await asyncio.gather(*reqs)
    open_ports = filter(lambda x: x!= None, ports)
    print("\n".join(open_ports))

async def scan(host, port):
    try:
        req = asyncio.open_connection(host, port)
        recv, conn = await asyncio.wait_for(req, 3)
        conn.close()
        return f"[+] Open: {port}"
    except asyncio.exceptions.TimeoutError:
        pass

if __name__ == "__main__":
    try:
        start = time.perf_counter()
        asyncio.run(main())
        end = time.perf_counter()
        print(f"[>] Total duration: {round(end-start, 2)}")
    except KeyboardInterrupt:
        print("[!] Exited the program")
        sys.exit(0)