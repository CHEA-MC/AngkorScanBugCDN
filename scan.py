import ipaddress
import socket
import threading
from tqdm import tqdm
import os
import time
import sys
import json

# ការ Setup សម្រាប់ពណ៌ (Color) และ Library
try:
    from colorama import Fore, Style, init
    import requests
    init()
    G = Fore.GREEN + Style.BRIGHT; Y = Fore.YELLOW + Style.BRIGHT; R = Fore.RED + Style.BRIGHT
    C = Fore.CYAN + Style.BRIGHT; B = Fore.BLUE + Style.BRIGHT; M = Fore.MAGENTA + Style.BRIGHT
    W = Fore.WHITE + Style.BRIGHT; RS = Style.RESET_ALL
except ImportError:
    print("\n[!] Warning: Required modules not found. 'pip install colorama requests'\n")
    G, Y, R, C, B, M, W, RS = "", "", "", "", "", "", "", ""
    sys.exit()

# --- Global Variables & Helper Functions ---
alive_ips = []
alive_subdomains = []
requests.packages.urllib3.disable_warnings() # បិទ Warning ពេល Scan HTTPS

def type_text(text, delay=0.01):
    for char in text: sys.stdout.write(char); sys.stdout.flush(); time.sleep(delay)
    print()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = f"""
{C}    ___                __ __              __    __    ______
{C}   /   |  ____  ____ _/ //_/___  _____   / /   / /   / ____/
{C}  / /| | / __ \/ __ `/ ,< / __ \/ ___/  / /   / /   / /     
{C} / ___ |/ / / / /_/ / /| / /_/ / /     / /___/ /___/ /___   
{C}/_/  |_/_/ /_/\__, /_/ |_\____/_/     /_____/_____/\____/   
{C}             /____/                                         
{RS}{M}    [ Developed by CheaOfficial ]     [v1.1 - Angkor Bug SCAN]
    """
    print(banner)

def open_telegram_link():
    """
    A more robust function to open the Telegram link.
    Tries Termux method first, falls back to webbrowser, then prints the link.
    """
    url = 'https://t.me/EquinoxDataCenter'
    print(f"{Y}[~] Attempting to open creator's Telegram: {C}{url}{RS}")
    try:
        # Priority 1: Termux method (most likely environment)
        if "com.termux" in os.environ.get("PREFIX", ""):
            # os.system returns 0 on success
            if os.system(f'termux-open-url {url}') == 0:
                print(f"{G}[SUCCESS] Check your Telegram app!{RS}")
                return  # Success, exit the function

            # If the command failed, it's likely termux-api is not installed
            print(f"{R}[WARN] 'termux-open-url' command failed.{RS}")
            print(f"{Y}[INFO] This might be because 'termux-api' is not installed.{RS}")
            print(f"{Y}[INFO] Please run: {C}pkg install termux-api{Y} and try again.{RS}")
        
        # Priority 2: Default webbrowser (for PC, other environments)
        import webbrowser
        if webbrowser.open(url):
            print(f"{G}[SUCCESS] Opened in your default browser.{RS}")
        else:
            # This case is rare but possible on systems without a GUI browser
            print(f"{R}[WARN] Could not find a web browser to open the link.{RS}")
            print(f"{Y}[INFO] Please open it manually: {C}{url}{RS}")

    except Exception as e:
        # Final fallback for any other error (e.g., webbrowser module not found)
        print(f"\n{R}[ERROR] Could not open link automatically: {e}{RS}")
        print(f"{Y}[INFO] Please open it manually: {C}{url}{RS}")


def expand_and_save_cidrs(cidrs, file_name, pbar_desc):
    all_ips = []
    print(f"\n{Y}[~] Expanding CIDR ranges...{RS}")
    for cidr in cidrs:
        try:
            network = ipaddress.ip_network(cidr)
            for ip in network.hosts():
                all_ips.append(str(ip))
        except ValueError:
            print(f"{R}[WARN] Skipping invalid CIDR: {cidr}{RS}")

    desc = f"{C}Writing to {M}{file_name}{RS}"
    with tqdm(total=len(all_ips), desc=desc, bar_format=f" {G}{{l_bar}}{{bar:30}}{G}{{r_bar}}{RS}") as pbar:
        with open(file_name, "w") as f:
            for ip in all_ips:
                f.write(ip + "\n")
                pbar.update(1)
    print(f"\n{G}[SUCCESS]{W} Total {Y}{len(all_ips)}{W} IPs saved to {C}{file_name}{RS}")

# --- CDN Download Functions ---
def download_bunny_ips():
    file_name = "bunny_ips.txt"
    url = "https://bunny.net/api/infrastructure/public/ips"
    print(f"\n{C}[~] Fetching Bunny.net IPs from API...{RS}")
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        ips = response.text.splitlines()
        
        desc = f"{C}Writing to {M}{file_name}{RS}"
        with tqdm(total=len(ips), desc=desc, bar_format=f" {G}{{l_bar}}{{bar:30}}{G}{{r_bar}}{RS}") as pbar:
            with open(file_name, "w") as f: [f.write(ip + "\n") for ip in ips]
            pbar.update(len(ips))
        print(f"\n{G}[SUCCESS]{W} Total {Y}{len(ips)}{W} IPs saved to {C}{file_name}{RS}")
    except requests.exceptions.RequestException as e:
        print(f"\n{R}[ERROR]{W} Could not fetch Bunny.net IPs: {e}{RS}")

def download_cf_ips():
    file_name = "cloudflare_ips.txt"; print(f"\n{C}[~] Fetching Cloudflare IP ranges...{RS}")
    try:
        cf_ranges = requests.get('https://www.cloudflare.com/ips-v4', timeout=15).text.splitlines()
        expand_and_save_cidrs(cf_ranges, file_name, "Cloudflare")
    except requests.exceptions.RequestException as e:
         print(f"\n{R}[ERROR]{W} Could not fetch Cloudflare IPs: {e}{RS}")

def download_fastly_ips():
    file_name = "fastly_ips.txt"; url = "https://api.fastly.com/public-ip-list"
    print(f"\n{C}[~] Fetching Fastly IP ranges from API...{RS}")
    try:
        response = requests.get(url, timeout=15); response.raise_for_status()
        cidrs = response.json().get("addresses", [])
        expand_and_save_cidrs(cidrs, file_name, "Fastly")
    except requests.exceptions.RequestException as e: print(f"\n{R}[ERROR]{W} Could not fetch Fastly IPs: {e}{RS}")

def download_cloudfront_ips():
    file_name = "cloudfront_ips.txt"; url = "https://ip-ranges.amazonaws.com/ip-ranges.json"
    print(f"\n{C}[~] Fetching AWS IP ranges from API...{RS}")
    try:
        response = requests.get(url, timeout=15); response.raise_for_status()
        data = response.json()
        cidrs = [item['ip_prefix'] for item in data['prefixes'] if item['service'] == 'CLOUDFRONT']
        expand_and_save_cidrs(cidrs, file_name, "CloudFront")
    except requests.exceptions.RequestException as e: print(f"\n{R}[ERROR]{W} Could not fetch AWS IPs: {e}{RS}")

# --- IP & Subdomain Scanning Functions ---
def check_alive_ip(ip, pbar):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1.5); s.connect((str(ip), 443))
            alive_ips.append(str(ip))
    except (socket.timeout, ConnectionRefusedError, OSError): pass
    finally: pbar.update(1)

def check_alive_subdomain(subdomain, pbar):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        requests.get(f"https://{subdomain}", headers=headers, timeout=5, verify=False, allow_redirects=True)
        alive_subdomains.append(subdomain)
    except requests.exceptions.RequestException:
        try:
            requests.get(f"http://{subdomain}", headers=headers, timeout=5, allow_redirects=True)
            alive_subdomains.append(subdomain)
        except requests.exceptions.RequestException: pass
    finally: pbar.update(1)

def scan_alive_subdomains():
    global alive_subdomains; alive_subdomains = []
    file_path = input(f"{Y}[?] Enter subdomain filename to scan: {W}")
    try:
        with open(file_path, "r") as f: subdomains = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"\n{R}[ERROR]{W} File '{C}{file_path}{W}' not found.{RS}"); time.sleep(2); return

    print(f"\n{G}[INFO]{W} Total Subdomains to scan: {Y}{len(subdomains)}{RS}")
    pbar = tqdm(total=len(subdomains), desc=f"{C}Scanning HTTP/S{RS}", bar_format=f" {G}{{l_bar}}{{bar:30}}{G}{{r_bar}}{RS}")
    threads = []
    for sub in subdomains:
        t = threading.Thread(target=check_alive_subdomain, args=(sub, pbar)); t.start(); threads.append(t)
        if len(threads) >= 200: [th.join() for th in threads]; threads = []
    [th.join() for th in threads]
    pbar.close()

    print(f"\n{G}[INFO]{W} Scan complete! Total alive subdomains: {Y}{len(alive_subdomains)}{RS}")
    if alive_subdomains:
        save_file = file_path.replace(".txt", "_alive.txt")
        with open(save_file, "w") as f: [f.write(sub + '\n') for sub in sorted(list(set(alive_subdomains)))]
        print(f"{G}[SUCCESS]{W} Alive subdomains saved to {C}{save_file}{RS}")
    input(f"\n{Y}Press Enter to return...{RS}")

def scan_alive_ips():
    global alive_ips; alive_ips = []
    file_path = input(f"{Y}[?] Enter IP filename to scan: {W}")
    try:
        with open(file_path, "r") as f: ips = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"\n{R}[ERROR]{W} File '{C}{file_path}{W}' not found.{RS}"); time.sleep(2); return

    print(f"\n{G}[INFO]{W} Total IPs to scan: {Y}{len(ips)}{RS}")
    pbar = tqdm(total=len(ips), desc=f"{C}Scanning Port 443{RS}", bar_format=f" {G}{{l_bar}}{{bar:30}}{G}{{r_bar}}{RS}")
    threads = []
    for ip in ips:
        t = threading.Thread(target=check_alive_ip, args=(ip, pbar)); t.start(); threads.append(t)
        if len(threads) >= 500: [th.join() for th in threads]; threads = []
    [th.join() for th in threads]
    pbar.close()

    print(f"\n{G}[INFO]{W} Scan complete! Total alive IPs: {Y}{len(alive_ips)}{RS}")
    if alive_ips:
        save_file = file_path.replace(".txt", "_alive.txt")
        with open(save_file, "w") as f: [f.write(ip + '\n') for ip in alive_ips]
        print(f"{G}[SUCCESS]{W} Alive IPs saved to {C}{save_file}{RS}")
    input(f"\n{Y}Press Enter to return...{RS}")

def find_subdomains_from_ip():
    ip_to_scan = input(f"{Y}[?] Enter IP to find subdomains for: {W}")
    print(f"\n{C}[~] Searching subdomains for {Y}{ip_to_scan}{C}...{RS}")
    try:
        response = requests.get(f"https://crt.sh/?q={ip_to_scan}&output=json", timeout=20)
        subdomains = sorted(list(set(entry['name_value'] for entry in response.json())))
        print(f"\n{G}[SUCCESS]{W} Found {Y}{len(subdomains)}{W} subdomains.")
        for sub in subdomains: print(f"{G}  - {W}{sub}{RS}")
        if subdomains and input(f"\n{Y}[?] Save to file? (y/n): {W}").lower() == 'y':
            filename = f"subdomains_{ip_to_scan}.txt"
            with open(filename, 'w') as f: f.write('\n'.join(subdomains))
            print(f"\n{G}[INFO]{W} Saved to {C}{filename}{RS}")
    except Exception as e: print(f"\n{R}[ERROR]{W} Could not fetch subdomains: {e}{RS}")
    input(f"\n{Y}Press Enter to return...{RS}")

def find_subdomains_from_domain():
    domain = input(f"{Y}[?] Enter domain (e.g., example.com): {W}")
    print(f"\n{C}[~] Searching subdomains for {Y}{domain}{C}...{RS}")
    try:
        response = requests.get(f"https://crt.sh/?q=%.{domain}&output=json", timeout=30)
        subdomains = sorted(list(set(entry['name_value'].replace('*.','') for entry in response.json())))
        print(f"\n{G}[SUCCESS]{W} Found {Y}{len(subdomains)}{W} subdomains.")
        for sub in subdomains: print(f"{G}  -> {W}{sub}{RS}")
        if subdomains and input(f"\n{Y}[?] Save to file? (y/n): {W}").lower() == 'y':
            filename = f"subdomains_{domain.replace('.','_')}.txt"
            with open(filename, 'w') as f: f.write('\n'.join(subdomains))
            print(f"\n{G}[INFO]{W} Saved to {C}{filename}{RS}")
    except Exception as e: print(f"\n{R}[ERROR]{W} Could not fetch subdomains: {e}{RS}")
    input(f"\n{Y}Press Enter to return...{RS}")

# --- MENUS ---
def download_menu():
    while True:
        clear_screen(); print_banner()
        print(f"{B}╔══════════════════════════════════════════════╗")
        print(f"║ {C}          *** Download CDN IPs *** {B}          ║")
        print(f"╠══════════════════════════════════════════════╣")
        print(f"║ {W}[1]{G} Cloudflare                              {B} ║")
        print(f"║ {W}[2]{G} Bunny.net                               {B} ║")
        print(f"║ {W}[3]{G} Fastly                                  {B} ║")
        print(f"║ {W}[4]{G} AWS CloudFront                          {B} ║")
        print(f"║ {W}[5]{Y} Back to Main Menu                       {B} ║")
        print(f"╚══════════════════════════════════════════════╝{RS}")
        choice = input(f"\n{C}┌──({W}root@angkor_scan/download{C})-[~]\n└─${G}# {W}")
        if choice == '1': download_cf_ips(); input(f"\n{Y}Press Enter...{RS}")
        elif choice == '2': download_bunny_ips(); input(f"\n{Y}Press Enter...{RS}")
        elif choice == '3': download_fastly_ips(); input(f"\n{Y}Press Enter...{RS}")
        elif choice == '4': download_cloudfront_ips(); input(f"\n{Y}Press Enter...{RS}")
        elif choice == '5': break
        else: print(f"\n{R}[ERROR] Invalid option!{RS}"); time.sleep(1)

def main_menu():
    while True:
        clear_screen(); print_banner()
        print(f"{B}╔══════════════════════════════════════════════╗")
        print(f"║ {C}      *** Welcome AngkorSSH™ ***  SCAN CDN {B}  ║")
        print(f"╠══════════════════════════════════════════════╣")
        print(f"║ {W}[1]{M} Download CDN IP Ranges                  {B} ║")
        print(f"║ {W}[2]{G} Scan Alive IPs (from file)              {B} ║")
        print(f"║ {W}[3]{C} Find Subdomains (from IP)               {B} ║")
        print(f"║ {W}[4]{C} Find Subdomains (from Domain)           {B} ║")
        print(f"║ {W}[5]{Y} Scan Alive Subdomains (from file)       {B} ║")
        print(f"║ {W}[6]{R} Exit                                     {B}║")
        print(f"╚══════════════════════════════════════════════╝{RS}")
        try:
            choice = input(f"\n{C}┌──({W}root@angkor_scan{C})-[~]\n└─${G}# {W}")
            if choice == '1': download_menu()
            elif choice == '2': scan_alive_ips()
            elif choice == '3': find_subdomains_from_ip()
            elif choice == '4': find_subdomains_from_domain()
            elif choice == '5': scan_alive_subdomains()
            elif choice == '6': type_text(f"\n{R}[+] Shutting down... Goodbye!{RS}", 0.03); break
            else: print(f"\n{R}[ERROR] Invalid option!{RS}"); time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n\n{R}[!] User interruption detected. Exiting...{RS}"); break

if __name__ == "__main__":
    clear_screen()
    open_telegram_link()
    time.sleep(4) # Pause for a moment so the user can read the link status
    main_menu()

