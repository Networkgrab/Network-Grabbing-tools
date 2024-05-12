import subprocess
import socket
import re
import pyfiglet
from colorama import init, Fore
import os
import threading
from scapy.all import IP, TCP, sr1, RandShort
from scapy.all import *
import base64
import nmap
from scapy.layers.inet import IP, ICMP
from scapy.sendrecv import sr1
import xml.etree.ElementTree as ET
import time

# Initialize colorama
init(autoreset=True)
print(Fore.GREEN + "-" * 100)
text = pyfiglet.figlet_format("Network Grabbing", font="slant")
print(Fore.GREEN + text)
print(" " * 60 + Fore.RED + "\033[1mCREATED BY\033[0m:-")
print(" " * 70 + Fore.BLUE + "->\033[3mAvart Raj\033[0m")
print(" " * 80 + Fore.BLUE + "->\033[3mKhushi\033[0m")
print(" " * 90 + Fore.BLUE + "->\033[3mDeepak\033[0m")
print(" " * 100 + Fore.BLUE + "->\033[3mMansi\033[0m")
print(Fore.GREEN + "-" * 100)


def target_ip(input_str):
    if re.match(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', input_str):
        return input_str

    try:
        ip_address = socket.gethostbyname(input_str)
        return ip_address
    except socket.gaierror:
        return None

def perform_ICMP_sweep(target):
    print(f"Performing ICMP sweep grab for {target}")
    target_ip = socket.gethostbyname(target)
    result = []
    if os.name == 'nt':
        command = f'ping -n 1 {target_ip}'
    else:
        command = f'ping -c 1 {target_ip}'
    response = os.system(command)
    if response == 0:
        result.append((target_ip, "up"))
    else:
        result.append((target_ip, "down"))
    return result

def perform_broadcast_ICMP(target):
    print(f"Performing Broadcast ICMP grab for {target}")
    result = []
    icmp = ICMP()
    icmp.type = 8  # ICMP Echo Request

    ip = IP(dst=target + "/24")  # Assuming /24 subnet, adjust as necessary
    ip.src = "0.0.0.0"  # Set source IP to arbitrary value for broadcast

    packet = ip / icmp

    ans, unans = sr(packet, timeout=2, verbose=False)

    for pkt in ans:
        if pkt[1].type == 0:  # ICMP Echo Reply
            result.append((pkt[1][IP].src, "up"))

    return result

def perform_non_echo_ICMP(target):
    print(f"Performing Non-Echo ICMP grab for {target}")
    target_ip = socket.gethostbyname(target)
    result = []
    if os.name == 'nt':
        command =f'ping -n 1 -l 1 {target_ip}'
    else:
        command = f'ping -c 1 {target_ip}'
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        result.append((target_ip, "up"))
    except subprocess.CalledProcessError:
        result.append((target_ip, "down"))
    return result

def perform_TCP_sweep(target):
    print(f"Performing TCP sweep grab for {target}")
    result = []
    min_port = 80
    max_port = 81
    target_ip = socket.gethostbyname(target)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    for port in range(min_port, max_port+1):
        try:
            sock.connect((target_ip, port))
            result.append((target_ip, port, "up"))
            sock.close()
            continue
        except:
            result.append((target_ip, port, "down"))
            sock.close()
            continue
    return result

def perform_UDP_sweep(target):
    print(f"Performing UDP sweep grab for {target}")
    min_port = 1
    max_port = 1024
    result = []
    target_ip = socket.gethostbyname(target)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for port in range(min_port, max_port+1):
        sock.settimeout(1)
        try:
            sock.sendto(b"", (target_ip, port))
            result.append((target_ip, "up"))
            sock.close()
            break
        except:
            pass
        sock.close()
    else:
        result.append((target_ip, "down"))
    return result

def perform_host_Grab(target):
    print(f"Performing Host Grabbing for {target}")
    while True:
        perform_icmp = input("Do You want to perform ICMP_SWEEP grab? (yes/no/back): ")
        if perform_icmp.lower() == 'yes':
            result = perform_ICMP_sweep(target)
            if result:
                print("ICMP_SWEEP grab results:")
                for ip, status in result:
                    if status == "up":
                        print(Fore.GREEN + f"{ip}: {status}" + Style.RESET_ALL)
                    else:
                        print(Fore.RED + f"{ip}: {status}" + Style.RESET_ALL)
            else:
                print("No hosts responded to the ICMP_SWEEP grab.")
        elif perform_icmp.lower() == 'no':
            break
        elif perform_icmp.lower() == 'back':
            break
        else:
            print("Please Enter 'yes' or 'no' or 'back' to return to the main menu.")

    if perform_icmp.lower() != 'back':
        while True:
            perform_broadcast = input("Do you want to perform Broadcast ICMP grab? (yes/no/back): ")
            if perform_broadcast.lower() == 'yes':
                result = perform_broadcast_ICMP(target)
                if result:
                    print("broadcast_ICMP grab results:")
                    for ip, status in result:
                        if status == "up":
                            print(Fore.GREEN + f"{ip}: {status}" + Style.RESET_ALL)
                        else:
                            print(Fore.RED + f"{ip}: {status}" + Style.RESET_ALL)
                else:
                    print("No hosts responded to the broadcast_ICMP grab.")
            elif perform_broadcast.lower() == 'no':
                break
            elif perform_broadcast.lower() == 'back':
                break
            else:
                print("Please enter 'yes' or 'no' or 'back' to return to the main menu.")

    if perform_icmp.lower() != 'back' and perform_broadcast.lower() != 'back':
        while True:
            perform_non_echo = input("Do you want to perform Non-Echo ICMP grab? (yes/no/back): ")
            if perform_non_echo.lower() == 'yes':
                result = perform_non_echo_ICMP(target)
                if result:
                    print("Non-Echo ICMP grab results:")
                    for ip, status in result:
                        if status == "up":
                            print(Fore.GREEN + f"{ip}: {status}" + Style.RESET_ALL)
                        else:
                            print(Fore.RED + f"{ip}: {status}" + Style.RESET_ALL)
                else:
                    print("No hosts responded to the broadcast_ICMP grab.")
            elif perform_non_echo.lower() == 'no':
                break
            elif perform_non_echo.lower() == 'back':
                break
            else:
                print("Please enter 'yes' or 'no' or 'back' to return to the main menu.")
    if perform_icmp.lower() != 'back' and perform_broadcast.lower() != 'back' and perform_non_echo.lower() != 'back':
        while True:
            perform_TCP_sweep_grab = input("Do you want to perform TCP Sweep  grab? (yes/no/back): ")
            if perform_TCP_sweep_grab.lower() == 'yes':
                result = perform_TCP_sweep(target)
                if result:
                    print("TCP_SWEEP grab results:")
                    for ip, port, status in result:
                        if status == "up":
                            print(Fore.GREEN + f"{ip} @ {port}: {status}" + Style.RESET_ALL)
                        else:
                            print(Fore.RED + f"{ip} @ {port}: {status}" + Style.RESET_ALL)
                else:
                    print("No hosts responded to the TCP_SWEEP grab.")
            elif perform_TCP_sweep_grab.lower() == 'no':
                break
            elif perform_TCP_sweep_grab.lower() == 'back':
                break
            else:
                print("Please enter 'yes' or 'no' or 'back' to return to the main menu.")
    if perform_icmp.lower() != 'back' and perform_broadcast.lower() != 'back' and perform_non_echo.lower() != 'back' and perform_TCP_sweep_grab.lower()!= 'back':
        while True:
            perform_UDP_sweep_grab = input("Do you want to perform UDP sweep  grab? (yes/no/back): ")
            if perform_UDP_sweep_grab.lower() == 'yes':
                result = perform_UDP_sweep(target)
                if result:
                    print("UDP_SWEEP grab results:")
                    for ip, status in result:
                        if status == "up":
                            print(Fore.GREEN + f"{ip}: {status}" + Style.RESET_ALL)
                        else:
                            print(Fore.RED + f"{ip}: {status}" + Style.RESET_ALL)
                else:
                    print("No hosts responded to the TCP_SWEEP grab.")
            elif perform_UDP_sweep_grab.lower() == 'no':
                break
            elif perform_UDP_sweep_grab.lower() == 'back':
                break
            else:
                print("Please enter 'yes' or 'no' or 'back' to return to the main menu.")

#------------------------***Port Grabbing funtions**----------------------------#****

def perform_tcp_connect_grab(target):
    print("Performing TCP Connect grab on", target)
    # Simulating TCP Connect Grab
    start_time = time.time()
    print("Port \tPortName \tStatus")
    for port in range(1, 6000):
        thread = threading.Thread(target=check_port, args=(target, port))
        thread.start()
    end_time = time.time()
    print("grabning completed in: ", end_time - start_time)
def check_port(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        sock.connect((target, port))
        sock.close()
        print(f"{port}\t\t{socket.getservbyport(port)}\topen")
    except socket.error:
        sock.close()
    except KeyboardInterrupt:
        sock.close()
        return
    except:
        sock.close()
        print(f"{port}\t\t{socket.getservbyport(port)}\tclosed")
          
        


# ANSI escape codes for colors
PORT_COLOR = "\033[95m"  # Purple
PORT_NAME_COLOR = "\033[94m"  # Blue
STATUS_COLOR = "\033[92m"    # Green
RESET = "\033[0m"

def grab_syn_port(port, target, open_ports):
    try:
        nmap_output = subprocess.run(["nmap", "-p", str(port), "-sS", "--open", "-oX", "-", target], capture_output=True, text=True)
        if nmap_output.returncode == 0:
            root = ET.fromstring(nmap_output.stdout)
            for p in root.iter('port'):
                portid = p.get('portid')
                state = p.find('state').get('state')
                service = p.find('service').get('name')
                if state == 'open':
                    open_ports.append((portid, service))
    except Exception as e:
        print(f"An error occurred while scanning port {port}: {e}")

def perfrom_tcp_syn_grab(target):
    print("Performing TCP SYN Grab on", target)
    print(f"{PORT_COLOR}Port\t{PORT_NAME_COLOR}PortName\t{STATUS_COLOR}Status{RESET}")

    open_ports = []
    threads = []

    start_time = time.time()

    try:
        for port in range(1, 6000):
            thread = threading.Thread(target=grab_syn_port, args=(port, target, open_ports))
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()

        for port, service in open_ports:
            print(f"{PORT_COLOR}{port}\t{PORT_NAME_COLOR}{service}\t\t{STATUS_COLOR}Open{RESET}")

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Scanning completed in {elapsed_time:.2f} seconds.")
    except Exception as e:
        print(f"An error occurred during port scanning: {e}")



#stealth scan
def grab_port(port, target, open_ports):
    try:
        command = f"nmap -sS -p{port} {target}"
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            output = result.stdout.decode()
            if "open" in output:
                open_ports.append((port, "open"))
        elif result.returncode != 0:
            output = result.stderr.decode()
            if "sudo" in output:
                print(f"Error: Please run this script with administrator privileges to grab port {port}")
            elif "nmap" in output:
                print(f"Error: Nmap not found. Please install Nmap to grab port {port}")
    except Exception as e:
        print(f"An error occurred while grabning port {port}: {e}")

# Wait for all threads to complete
for thread in threading.enumerate():
    if thread is not threading.current_thread():
        thread.join()

"""If the target machine responds with a RST packet, the port is marked as open. 
 If the target machine
 # responds with anything else, the port is marked as closed."""


def get_open_ports(target, port_range, result_list):
    open_ports = []
    for port in port_range:
        try:
            packet = IP(dst=target) / TCP(dport=port, flags="S")
            tcp_response = sr1(packet, timeout=1, verbose=0)
            if tcp_response is not None and TCP in tcp_response:
                if tcp_response[TCP].flags == 0x12:
                    open_ports.append((port, socket.getservbyport(port, 'tcp'), "Open"))
                elif tcp_response[TCP].flags == 0x14:
                    open_ports.append((port, socket.getservbyport(port, 'tcp'), "Closed"))
        except Exception as e:
            print(f"Error: {e}")
    result_list.extend(open_ports)
    
def grab_ports(target, port_range):
    open_ports = []
    threads = []
    result_list = []

    
    print("grabning.......")
    for port in port_range:
        t = threading.Thread(target=get_open_ports, args=(target, [port], result_list))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
    return result_list

def perform_tcp_stealth_grab(target):
    print("Performing TCP Stealth grab on", target)
    # Simulating TCP Stealth grab
    start_time = time.time()

    open_ports = grab_ports(target, range(1, 6000))
    for port, name, status in open_ports:
        print("Port \tPortName\tStatus")
        print(f"{port}, \t{name}, \t{status}")
    end_time = time.time()
    grab_time = end_time - start_time
    print(f"grab completed in {grab_time} seconds.")

     





 ### Working on it later @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@######



# ANSI escape codes for colors
PORT_COLOR = '\033[95m'   # Purple
PORT_NAME_COLOR = '\033[94m'  # Blue
STATUS_OPEN_COLOR = '\033[92m' # Green
STATUS_CLOSED_COLOR = '\033[91m' # Red
RESET = '\033[0m'

def perform_ftp_bounce_grab(target):
    print("Performing FTP Bounce grab on", target)

    try:
        ftp_server_ip = input("Enter FTP server IP address: ")
        nmap_command = ["nmap", "-b", ftp_server_ip, target]
        process = subprocess.Popen(nmap_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, _ = process.communicate()
        if process.returncode == 0:
            for line in stdout.split('\n'):
                if line.startswith("Discovered open port"):
                    fields = line.split()
                    port = fields[3].split("/")[0]
                    port_name = fields[4]
                    status = "open"
                    print(f"{PORT_COLOR}{port}\t{PORT_NAME_COLOR}{port_name}\t\t{STATUS_OPEN_COLOR}{status}{RESET}")
                elif line.startswith("Discovered closed port"):
                    fields = line.split()
                    port = fields[3].split("/")[0]
                    port_name = fields[4]
                    status = "closed"
                    print(f"{PORT_COLOR}{port}\t{PORT_NAME_COLOR}{port_name}\t{STATUS_CLOSED_COLOR}{status}{RESET}")
        else:
            print("Nmap scan failed.")
    except Exception as e:
        print(f"An error occurred during port scanning: {e}")
    
    






def perform_port_Grab(target):
    print(f"Performing Port Grabbing for {target}")
    while True:
        TCP_connect_grab = input("Do You want to perform TCP grab? (yes/no/back): ")
        if TCP_connect_grab.lower() == 'yes':
             perform_tcp_connect_grab(target)
             
        elif TCP_connect_grab.lower() == 'no':
            break
        elif TCP_connect_grab.lower() == 'back':
            break
        else:
            print("Please Enter 'yes' or 'no' or 'back' to return to the main menu.")
    if TCP_connect_grab.lower() != 'back':
        while True:
            TCP_SYN_grab = input("Do you want to perform Perform TCP SYN Grab? (yes/no/back): ")
            if TCP_SYN_grab.lower() == 'yes':
                 perfrom_tcp_syn_grab(target)
            elif TCP_SYN_grab.lower() == 'no':
                break
            elif  TCP_SYN_grab.lower() == 'back':
                break
            else:
                print("Please enter 'yes' or 'no' or 'back' to return to the main menu.")
    
    if TCP_connect_grab.lower() != 'back' and TCP_SYN_grab.lower() != 'back':
        while True:
            TCP_Stealth_grab = input("Do you want to perform  TCP Stealth Grab? (yes/no/back): ")
            if TCP_Stealth_grab.lower() == 'yes':
                 perform_tcp_stealth_grab(target)
            elif TCP_Stealth_grab.lower() == 'no':
                break
            elif TCP_Stealth_grab.lower() == 'back':
                break
            else:
                print("Please enter 'yes' or 'no' or 'back' to return to the main menu.")    

    if TCP_connect_grab.lower() != 'back' and TCP_SYN_grab.lower() != 'back' and TCP_Stealth_grab.lower() != 'back':
        while True:
            FTP_Bounce_grab = input("Do you want to perform FTP Bounce Grab? (yes/no/back): ")
            if FTP_Bounce_grab.lower() == 'yes':
                  perform_ftp_bounce_grab(target)
            elif FTP_Bounce_grab.lower() == 'no':
                break
            elif FTP_Bounce_grab.lower() == 'back':
                break
            else:
               print("Please enter 'yes' or 'no' or 'back' to return to the main menu.")


#### service and version grabbing ####

# ANSI escape codes for text formatting
class Color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def grab_port(target, port):
    try:
        # Create a socket object
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Set the timeout for the socket
            s.settimeout(2)
            # Attempt to connect to the target on the specified port
            result = s.connect_ex((target, port))
            if result == 0:
                service = socket.getservbyport(port)
                banner = retrieve_banner(s)
                print(f"Port: {port:<5} | Status: { Color.OKGREEN +'Open' if result == 0 else 'Closed':<6} | Service: {service:<10} | Version: {banner}")
    except socket.timeout:
        print(f"Port: {port:<5} | Status: {Color.WARNING}Timeout | Service: N/A         | Version: N/A{Color.ENDC}")
    except socket.error as e:
        print(f"Port: {port:<5} | Status: {Color.FAIL}Error   | Service: N/A         | Version: N/A{Color.ENDC}")



def retrieve_banner(socket):
    banner = ""
    try:
        banner = socket.recv(1024).decode('utf-8').strip()
    except UnicodeDecodeError:
        try:
            banner = socket.recv(1024).decode('iso-8859-1').strip()
        except UnicodeDecodeError:
            try:
                banner = base64.b64encode(socket.recv(1024)).decode('utf-8')
            except:
                pass

    return banner if banner else "Unknown"
 #------>>>> nmamp module<<<<<<------#

def perform_service_and_version_scanning(target):
    print(f"Performing Service and Version Scanning for {target}")

    try:
        nm = nmap.PortScanner()
        nm.scan(hosts=target, arguments='-sV')

        for host in nm.all_hosts():
            print("Host: \033[1m%s\033[0m" % host)
            print("State: \033[92m%s\033[0m" % nm[host].state())

            for proto in nm[host].all_protocols():
                print("Protocol: \033[94m%s\033[0m" % proto)

                port_info = nm[host][proto].items()
                for port, port_data in port_info:
                    print(f"Port: \033[95m{port}\033[0m | State: \033[92m{port_data['state']}\033[0m | Service: \033[96m{port_data['name']}\033[0m | Version: \033[93m{port_data['product']} {port_data['version']}\033[0m")

        print(f"\nScan completed in \033[1m{nm.scanstats()['elapsed']}\033[0m seconds")

    except nmap.PortScannerError as e:
        print(f"An error occurred during scanning: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def perform_service_and_version_grabbing(target):
    print(f"Performing Service and Version Grabbing for {target}")
    while True:
        Service_and_version_grab = input("Do You want to perform Service and Version Grab technique 1? (yes/no/back): ")
        if Service_and_version_grab.lower() == 'yes':
            start_port = int(input("Enter the starting port: "))
            end_port = int(input("Enter the ending port: "))

            threads = []
            for port in range(start_port, end_port + 1):
                t = Thread(target=grab_port, args=(target, port))
                threads.append(t)

            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()

            print("Grab complete.")
        elif Service_and_version_grab.lower() == 'no':
            break
        elif Service_and_version_grab.lower() == 'back':
            break
        else:
            print("Invalid input! Please enter 'yes', 'no', or 'back'.")

    if Service_and_version_grab.lower() != 'back':
        while True:
            version_and_service_Grab2 = input("Do you want to perform service and version grabbing technique 2? (yes/no/back): ")
            if version_and_service_Grab2.lower() == 'yes':
                 thread = Thread(target=perform_service_and_version_scanning, args=(target,))
                 thread.start()
                 thread.join()
            elif version_and_service_Grab2.lower() == 'no':
                break
            elif  version_and_service_Grab2.lower() == 'back':
                break
            else:
                print("Please enter 'yes' or 'no' or 'back' to return to the main menu.")



### OS grabbing techniqes  ###




HIGHLIGHT = '\033[93m'  # Yellow color for highlighting
RESET = '\033[0m'  # Reset to default color

total_time = 0  # Initialize total_time as a global variable

def grab_os_info_nmap(target):
    """Function to extract OS information using Nmap."""
    try:
        global total_time  # Access global total_time variable
        start_time = time.time()
        nm = nmap.PortScanner()
        nm.scan(target, arguments='-A -O')
        os_info = nm[target]['osmatch']
        elapsed_time = time.time() - start_time
        if os_info:
            print(HIGHLIGHT + f"OS information for {target} (Time taken: {elapsed_time:.2f} seconds):" + RESET)
            for match in os_info:
                print(HIGHLIGHT + f"  {match['name']} ({match['accuracy']}%)" + RESET)
        else:
            print(HIGHLIGHT + f"No OS information found for {target}" + RESET)
        
        total_time += elapsed_time  # Update total time
        
    except Exception as e:
        print(HIGHLIGHT + f"Error occurred for {target}: {e}" + RESET)

def grab_os_info_scapy(target):
    """Function to extract OS information using Scapy."""
    try:
        global total_time  # Access global total_time variable
        start_time = time.time()
        response = sr1(IP(dst=target)/ICMP(), timeout=3, verbose=False)
        elapsed_time = time.time() - start_time
        if response:
            print(HIGHLIGHT + f"OS information for {target} (Time taken: {elapsed_time:.2f} seconds):" + RESET)
            # Detect OS based on TTL value and characteristics of the response packet
            if response.ttl <= 64:
                print(HIGHLIGHT + f"  Probable OS: Linux" + RESET)
            else:
                print(HIGHLIGHT + f"  Probable OS: Windows" + RESET)
        else:
            print(HIGHLIGHT + f"No OS information found for {target}" + RESET)
        
        total_time += elapsed_time  # Update total time
        
    except Exception as e:
        print(HIGHLIGHT + f"Error occurred for {target}: {e}" + RESET)
    
def perform_OS_get(targets):
    """Function to perform OS extraction for multiple targets."""
    threads = []
    for target in targets:
        
        thread = threading.Thread(target=grab_os_info_scapy, args=(target,))
        threads.append(thread)
        thread.start()
         

    for thread in threads:
        thread.join()

    print(HIGHLIGHT + f"Total time taken: {total_time:.2f} seconds" + RESET)  # Display total time after all threads have completed

def perform_OS_extraction(targets):
    """Function to perform OS extraction for multiple targets."""
    threads = []
    for target in targets:
        
        thread = threading.Thread(target=grab_os_info_nmap, args=(target,))
        threads.append(thread)
        thread.start()
         

    for thread in threads:
        thread.join()

    print(HIGHLIGHT + f"Total time taken: {total_time:.2f} seconds" + RESET)  # Display total time after all threads have completed

def perform_OS_Grab(target):
    print(f"Performing OS-info Grabbing for {target}")
    while True:
        os_info_grab = input("Do you want to perform OS-info grab technique 1 (Nmap)? (yes/no/back): ")
        if os_info_grab == 'yes':
            perform_OS_extraction([target])
            break
        elif os_info_grab == 'no':
            break
        elif os_info_grab.lower() == 'back':
            break
        else:
            print("Please enter 'yes', 'no', or 'back' to return to the main menu.")
    if os_info_grab.lower() != 'back':
        while True:
            OS_get = input("Do you want to perform Perform  OS-info grab technique 2 (scapy)? (yes/no/back): ")
            if  OS_get.lower() == 'yes':
                 perform_OS_get([target])
            elif  OS_get.lower() == 'no':
                break
            elif   OS_get.lower() == 'back':
                break
            else:
                print("Please enter 'yes' or 'no' or 'back' to return to the main menu.")


# <<-----------------VUlnerabilty scanning technique  start------------>>

from colorama import init, Fore, Back, Style


# Initialize colorama
init()

def beautify_line(line):
    keywords = [
         "IDs", "References", "Check results", "CSRF vulnerabilities", "Path",
        "Form id", "Form action", "sql-injection", "XSS", "misconfiguration"
    ]
    colors = [
        Back.RED, Fore.CYAN, Fore.MAGENTA, Fore.YELLOW, Fore.RED, Fore.GREEN,
        Fore.GREEN, Fore.GREEN, Back.YELLOW + Fore.BLACK, Back.YELLOW + Fore.BLACK, Back.YELLOW + Fore.BLACK
    ]
    for keyword, color in zip(keywords, colors):
        if keyword in line:
            line = line.replace(keyword, f"{color}{keyword}{Style.RESET_ALL}")
    if "VULNERABLE" in line:
        return Back.RED + Fore.WHITE + line + Style.RESET_ALL
    elif "NOT VULNERABLE" in line:
        return Back.YELLOW + Fore.BLACK + line + Style.RESET_ALL
    elif "DESCRIPTION:" in line:
        return Fore.RED + line + Style.RESET_ALL
    elif "http://" in line or "https://" in line:
        return Fore.BLUE + line + Style.RESET_ALL
    else:
        return Fore.GREEN + line.replace("Scanning", "Grabbing").replace("Nmap", "Network grabbing") + Style.RESET_ALL


def scan_vulnerabilities(target):
    try:
        # Run Nmap command to scan for vulnerabilities with faster timing and increased threads
        nmap_command = f'nmap -T4 -v --script vuln -p- {target}'
        process = subprocess.Popen(nmap_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        while True:
            output_line = process.stdout.readline()
            if output_line == '' and process.poll() is not None:
                break
            if output_line and "Starting Nmap" not in output_line and "Raw packets sent:" not in output_line and "Completed NSE at" not in output_line and "Initiating ARP Ping Scan" not in output_line and "Discovered open port" not in output_line and "Completed SYN Stealth Scan" not in output_line and "Read data files from" not in  output_line:  # Filter out specific lines
                print(beautify_line(output_line.strip()))  # Print beautified output line by line
        process.stdout.close()
        return_code = process.poll()
        if return_code != 0:
            return f"Error: Nmap process exited with return code {return_code}"
    except Exception as e:
        return f"Error: {e}"



def perform_scan(target):
    print("Starting vulnerability Grabbing...")
    output = scan_vulnerabilities(target)
    


def perform_Vulnerability_Grab(target):
    print(f"Performing Vulnarability Grabbing technique for {target}")
    while True:
        vul_info_grab = input("Do you want to perform Vulnerabilty Grabbing? (yes/no/back): ")
        if  vul_info_grab == 'yes':
            perform_scan(target)
        elif  vul_info_grab == 'no':
            break
        elif  vul_info_grab.lower() == 'back':
            break
        else:
            print("Please enter 'yes', 'no', or 'back' to return to the main menu.")





####---------->>Mitigation<<----------##

def mitigate_vulnerability(vulnerability):
    # Dictionary containing vulnerabilities and their mitigation steps
    vulnerability_to_mitigation = {
        "SQL Injection": "\033[91m1. Use parameterized queries or prepared statements to interact with databases.\n"
                         "2. Sanitize and validate user input.\n"
                         "3. Implement least privilege access control for database users.\033[0m",
        "Cross-Site Scripting (XSS)": "\033[91m1. Use proper output encoding when displaying user input on web pages.\n"
                                       "2. Enable Content Security Policy (CSP) headers to restrict "
                                       "the sources of executable scripts.\n"
                                       "3. Encode user input before rendering it on web pages.\033[0m",
        "Command Injection": "\033[91m1. Use libraries or frameworks that provide safe interfaces for executing commands.\n"
                             "2. Validate and sanitize user input before passing it to system commands.\n"
                             "3. Use platform-specific security features like subprocess module in Python.\033[0m",
        "Sensitive Data Exposure": "\033[91m1. Encrypt sensitive data before storing it in databases or transmitting over networks.\n"
                                    "2. Use secure protocols like HTTPS to protect data transmission.\n"
                                    "3. Implement access controls to restrict access to sensitive data.\033[0m",
        "Insecure Deserialization": "\033[91m1. Avoid deserializing data from untrusted sources.\n"
                                     "2. Validate and sanitize serialized data before deserialization.\n"
                                     "3. Use safe serialization formats or libraries.\033[0m",
        "Broken Authentication": "\033[91m1. Use strong and unique passwords.\n"
                                 "2. Implement multi-factor authentication.\n"
                                 "3. Enforce session management best practices.\033[0m",
        "Insecure Direct Object References": "\033[91m1. Implement proper access controls to ensure users can only access authorized resources.\n"
                                             "2. Use indirect references or access tokens instead of exposing direct object references.\n"
                                             "3. Regularly audit and review access controls.\033[0m",
        "Security Misconfiguration": "\033[91m1. Regularly update and patch software dependencies and frameworks.\n"
                                      "2. Follow security best practices for server configurations.\n"
                                      "3. Use automated tools for scanning and detecting misconfigurations.\033[0m",
        "Cross-Site Request Forgery (CSRF)": "\033[91m1. Use anti-CSRF tokens to protect against CSRF attacks.\n"
                                              "2. Implement same-site cookie attributes.\n"
                                              "3. Validate and sanitize user input for critical actions.\033[0m",
        "XML External Entity (XXE) Injection": "\033[91m1. Disable XML external entity processing in XML parsers.\n"
                                                "2. Use safer alternatives to XML, such as JSON, if possible.\n"
                                                "3. Implement input validation and filtering for XML inputs.\033[0m",
        "Unvalidated Redirects and Forwards": "\033[91m1. Avoid using user input to construct redirect or forward URLs.\n"
                                               "2. Use whitelists or predefined lists for allowed redirect destinations.\n"
                                               "3. Implement server-side checks to validate redirect URLs.\033[0m",
        "Security Headers Misconfiguration": "\033[91m1. Configure security headers like X-Content-Type-Options, X-Frame-Options, "
                                              "and X-XSS-Protection.\n"
                                              "2. Implement Content Security Policy (CSP) to mitigate client-side "
                                              "attacks like XSS.\n"
                                              "3. Regularly check and update security headers based on best practices.\033[0m",
        "Remote Code Execution (RCE)": "\033[91m1. Validate and sanitize user input, especially when executing code or commands remotely.\n"
                                        "2. Use secure APIs and libraries to handle user input and data.\n"
                                        "3. Implement strict firewall rules and network segmentation to limit the attack surface.\033[0m",
        "Server-Side Request Forgery (SSRF)": "\033[91m1. Validate and sanitize URLs provided by users before making requests.\n"
                                                "2. Implement allowlists or denylists for acceptable URL schemes and hosts.\n"
                                                "3. Use proxies or other intermediaries to control outgoing requests and restrict access.\033[0m",
        "Directory Traversal": "\033[91m1. Use proper input validation and sanitization to prevent attackers from accessing unauthorized files.\n"
                                "2. Implement file path restrictions and validate user input against allowed file paths.\n"
                                "3. Configure file system permissions to restrict access to sensitive directories.\033[0m",
        "File Inclusion Vulnerability": "\033[91m1. Avoid using user-controllable input to include files.\n"
                                         "2. Implement whitelisting for acceptable file inclusions.\n"
                                         "3. Use secure file access methods and avoid dynamic file inclusion where possible.\033[0m",
        "Session Fixation": "\033[91m1. Regenerate session identifiers upon login or privilege escalation.\n"
                             "2. Implement session expiration and inactivity timeouts.\n"
                             "3. Use HTTPS to protect session cookies from interception.\033[0m",
        "Buffer Overflow": "\033[91m1. Use safe programming practices such as bounds checking and input validation.\n"
                            "2. Use compiler or runtime protections like stack canaries or ASLR.\n"
                            "3. Regularly update software to patch known vulnerabilities.\033[0m",
        "Information Leakage": "\033[91m1. Minimize verbose error messages that reveal sensitive information.\n"
                                "2. Implement access controls to restrict unauthorized access to sensitive data.\n"
                                "3. Regularly audit system logs and monitor for unauthorized access attempts.\033[0m",
        "Denial of Service (DoS)": "\033[91m1. Implement rate limiting or throttling to mitigate excessive requests.\n"
                                    "2. Use load balancers and redundant servers to distribute traffic.\n"
                                    "3. Configure firewalls and intrusion detection systems to block malicious traffic.\033[0m",
        "Insufficient Logging and Monitoring": "\033[91m1. Implement comprehensive logging of security-related events.\n"
                                                "2. Regularly review logs for signs of suspicious activity.\n"
                                                "3. Set up automated alerts for abnormal behavior or potential security incidents.\033[0m",
        "Insufficient Authorization": "\033[91m1. Implement proper access controls to restrict users' actions based on their roles and permissions.\n"
                                        "2. Use principle of least privilege to grant only necessary access to resources.\n"
                                        "3. Regularly review and update access control policies to align with organizational requirements.\033[0m",
        "Insecure Cryptographic Storage": "\033[91m1. Use strong encryption algorithms and key management practices to protect sensitive data.\n"
                                            "2. Avoid storing plaintext passwords and use hashing algorithms with salt.\n"
                                            "3. Regularly rotate encryption keys and update cryptographic protocols as needed.\033[0m",
        "Weak Passwords": "\033[91m1. Enforce password complexity requirements, including minimum length and character diversity.\n"
                            "2. Implement account lockout mechanisms to prevent brute-force attacks.\n"
                            "3. Educate users on password best practices and encourage the use of password managers.\033[0m",
        "LDAP Injection": "\033[91m1. Use parameterized queries or LDAP APIs to interact with LDAP directories.\n"
                            "2. Sanitize and validate user input before constructing LDAP queries.\n"
                            "3. Implement access controls and least privilege principles for LDAP directory users.\033[0m",
        "Insecure File Upload": "\033[91m1. Implement file type validation based on allowed file extensions and content types.\n"
                                 "2. Store uploaded files in a secure location outside of the web root.\n"
                                 "3. Implement server-side scanning for malware and malicious content in uploaded files.\033[0m",
        "Outdated Services": "\033[91m1. Regularly update and patch all software, including operating systems, applications, and services.\n"
                              "2. Monitor vendor security advisories and apply patches promptly.\n"
                              "3. Consider using automated vulnerability scanners to identify and prioritize updates.\033[0m",
        "Open Ports": "\033[91m1. Close or restrict access to unnecessary open ports.\n"
                       "2. Use firewalls to filter incoming and outgoing traffic.\n"
                       "3. Regularly scan for open ports and services using network security tools.\033[0m",
        "Insecure APIs": "\033[91m1. Implement authentication and authorization mechanisms for API endpoints.\n"
                           "2. Validate and sanitize input received from API requests.\n"
                           "3. Encrypt sensitive data transmitted via APIs and use secure communication protocols.\033[0m",
        "Sensitive Data Exposure": "\033[91m1. Encrypt sensitive data at rest and in transit.\n"
                                    "2. Implement proper access controls to limit access to sensitive data.\n"
                                    "3. Use secure encryption algorithms and key management practices.\033[0m",
        "Missing Security Headers": "\033[91m1. Implement security headers like Content-Security-Policy (CSP), "
                                     "Strict-Transport-Security (HSTS), and X-Content-Type-Options.\n"
                                     "2. Regularly audit and update security headers to align with best practices.\n"
                                     "3. Use security headers to mitigate common web security vulnerabilities.\033[0m",
        "Cross-Site Request Forgery (CSRF)": "\033[91m1. Use anti-CSRF tokens to protect against CSRF attacks.\n"
                                              "2. Implement same-site cookie attributes.\n"
                                              "3. Validate and sanitize user input for critical actions.\033[0m",
        "SSL/TLS Vulnerabilities": "\033[91m1. Use strong encryption algorithms such as AES and RSA for SSL/TLS.\n"
                                    "2. Keep SSL/TLS libraries and dependencies up-to-date.\n"
                                    "3. Disable SSLv2 and SSLv3 protocols, and prefer TLSv1.2 or higher.\033[0m",
        "Cross-Site Script Inclusion (XSSI)": "\033[91m1. Implement Content Security Policy (CSP) to restrict the domains from which scripts can be loaded.\n"
                                                "2. Avoid including user-controlled content in script src attributes.\n"
                                                "3. Use the 'nonce' attribute for script tags to ensure only trusted scripts are executed.\033[0m",
        "Clickjacking": "\033[91m1. Implement X-Frame-Options header to prevent your website from being embedded in an iframe on another domain.\n"
                        "2. Use frame-busting techniques such as JavaScript to prevent your site from being framed.\n"
                        "3. Utilize the 'Referrer-Policy' header to limit the information sent in the Referrer header.\033[0m",
        "Session Fixation": "\033[91m1. Generate a new session identifier when a user logs in.\n"
                             "2. Regenerate session identifiers after a user authenticates or their privilege level changes.\n"
                             "3. Use session identifiers that are not easily guessable or predictable.\033[0m",
        "Cross-Origin Resource Sharing (CORS) Misconfiguration": "\033[91m1. Implement proper CORS policies to restrict cross-origin requests.\n"
                                                                   "2. Validate and sanitize user input to prevent XSS attacks.\n"
                                                                   "3. Use server-side checks to verify the origin and permissions of incoming requests.\033[0m",
        "Broken Access Control": "\033[91m1. Implement access controls at both the server and client sides.\n"
                                    "2. Use role-based access controls (RBAC) to restrict access based on user roles.\n"
                                    "3. Regularly review and update access control policies to ensure they align with security requirements.\033[0m",
        "Data Validation Bypass": "\033[91m1. Use strict input validation to reject any input that does not adhere to expected formats.\n"
                                    "2. Sanitize and escape user input to prevent injection attacks.\n"
                                    "3. Use server-side validation and verification to supplement client-side validation.\033[0m",
        "Elevation of Privilege": "\033[91m1. Implement least privilege principles to restrict user permissions to the minimum necessary.\n"
                                    "2. Monitor for suspicious activities and unauthorized privilege escalations.\n"
                                    "3. Regularly review and update user roles and permissions.\033[0m",
        "XML Injection": "\033[91m1. Use XML parsers that support input validation and sanitize input before processing.\n"
                            "2. Implement proper error handling to prevent information disclosure.\n"
                            "3. Restrict XML processing to trusted sources and ensure the XML schema is well-defined.\033[0m",
        "Software Vulnerability": "\033[91m1. Regularly update and patch software to fix known vulnerabilities.\n"
                                   "2. Monitor vendor security advisories and apply patches promptly.\n"
                                   "3. Use intrusion detection systems and network scanners to identify vulnerable software.\033[0m",
        "Unpatched Systems": "\033[91m1. Establish a patch management process to regularly update operating systems and software.\n"
                              "2. Prioritize critical patches and apply them promptly.\n"
                              "3. Use vulnerability scanners to identify unpatched systems and prioritize remediation.\033[0m",
        "Weak Encryption": "\033[91m1. Use strong encryption algorithms with appropriate key lengths.\n"
                            "2. Avoid using deprecated or weak cryptographic algorithms.\n"
                            "3. Regularly update encryption protocols and algorithms to adhere to best practices.\033[0m",
        "Default Credentials": "\033[91m1. Change default usernames and passwords immediately after installation.\n"
                                 "2. Use strong, unique passwords for all accounts.\n"
                                 "3. Implement multi-factor authentication to add an extra layer of security.\033[0m",
        "Improper Error Handling": "\033[91m1. Implement detailed error handling to provide minimal information to attackers.\n"
                                    "2. Avoid displaying sensitive data or stack traces in error messages.\n"
                                    "3. Log errors securely and regularly review error logs for signs of attacks.\033[0m",
        "Insecure Wireless Network": "\033[91m1. Use strong encryption (WPA2 or higher) and a unique, complex password for Wi-Fi networks.\n"
                                       "2. Disable SSID broadcasting to make the network less visible to attackers.\n"
                                       "3. Implement MAC address filtering to allow only authorized devices to connect.\033[0m",
        # Add more vulnerabilities and their mitigation steps here
    }

    # Check if the provided vulnerability is in the dictionary
    if vulnerability in vulnerability_to_mitigation:
        mitigation_steps = vulnerability_to_mitigation[vulnerability]
        return mitigation_steps
    else:

        return "\033[91mMitigation steps for this vulnerability are not available.\033[0m"
def mitigation_step():
    user_vulnerability = input("Enter the vulnerability: ")
    print(Fore.GREEN + "-" * 100)
    mitigation = mitigate_vulnerability(user_vulnerability)
    print("\033[91mMitigation Steps for {}\033[0m:".format(user_vulnerability))
    print(Fore.CYAN + "-" * 45)
    print("\033[92m" + mitigation + "\033[0m")  
    print(Fore.GREEN + "-" * 100)

def perform_Mitigation(User_vulnerability):
    while True:
        Mitigation_info_grab = input("Do you want to perform Mitigation step  Grabbing? (yes/no/back): ")
        if  Mitigation_info_grab == 'yes':
             mitigation_step()
        elif  Mitigation_info_grab == 'no':
            break
        elif  Mitigation_info_grab.lower() == 'back':
            break
        else:
            print("Please enter 'yes', 'no', or 'back' to return to the main menu.")




######------Main Section--------#########


def main():
    while True:
        user_input = input("Enter an IP address or domain name: ")
        target = target_ip(user_input)

        if target:
            print(f"Target IP address: {target}")
            while True:
                print("\nSelect a Grabbing technique:")
                print("1. Host Grabbing Techniques")
                print("2. Port Grabbing Technique")
                print("3. Service and Version Grabbing Technique")
                print("4. OS Grabbing Technique")
                print("5.Vulnerability Grabbing technique")
                print("6.Mitigation related to the Vulnerability technique")
                print("7. Quit")

                choice = input("Enter your choice (1-7): ")

                if choice == '1':
                    print("Performing host grabbing techniques:")
                    perform_host_Grab(target)
                    print("Back to main menu")
                    continue  # Returning to the main menu

                elif choice == '2':
                    print("Performing port Grabbing technique:")
                    perform_port_Grab(target)
                    print("Back to main menu")
                    continue  # Returning to the main menu
                elif choice == '3':
                    print("Performing Service and Version Grabbbing technique:")
                    perform_service_and_version_grabbing(target)
                    print("Back to main menu")
                    continue  # Returning to the main menu
                elif choice == '4':
                    print("Performing Os Grabbing technique:")
                    perform_OS_Grab(target)
                    print("Back to main menu")
                    continue  # Returning to the main menu
                elif choice == '5':
                    print("Welcome to Network Grabbing - Vulnerability Scanner")
                    perform_Vulnerability_Grab(target)
                    print("Back to main menu")
                    continue  # Returning to the main menu
                elif choice == '6':
                    print("Performing Mitigation  steps related Bugs technique:")
                    perform_Mitigation(target)
                    print("Back to main menu")
                    continue  # Returning to the main menu
                
                elif choice == '7':
                    print("Exiting...")
                    return  # Exiting the entire program

                else:
                    print("Invalid choice. Please enter a number between 1 and 7.")

        else:
            print("Invalid IP address or domain")


if __name__ == "__main__":
    main()
