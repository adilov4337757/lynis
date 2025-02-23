#!/usr/bin/env python3
import os
import subprocess
import argparse
import datetime
import logging
import stat

# ANSI rəngləri
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def init_logger(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logging.info("Lynis Təhlükəsizlik Analizi Başladı")

def print_and_log(message, level="info"):
    print(message)
    if level == "info":
        logging.info(message)
    elif level == "warning":
        logging.warning(message)
    elif level == "error":
        logging.error(message)

def check_os_version():
    print_and_log(f"\n{GREEN}[+] OS versiyasını yoxlayırıq...{RESET}")
    try:
        os_version = subprocess.getoutput("cat /etc/os-release")
        print_and_log(os_version)
    except Exception as e:
        print_and_log(f"{RED}Xəta baş verdi: {e}{RESET}", "error")

def check_open_ports():
    print_and_log(f"\n{GREEN}[+] Açıq portları yoxlayırıq...{RESET}")
    open_ports = subprocess.getoutput("ss -tulnp | grep LISTEN")
    if open_ports:
        print_and_log(open_ports)
    else:
        print_and_log("Heç bir açıq port tapılmadı.")

def check_firewall():
    print_and_log(f"\n{GREEN}[+] Firewall vəziyyətini yoxlayırıq...{RESET}")
    firewall_status = subprocess.getoutput("which ufw && sudo ufw status || echo 'UFW quraşdırılmayıb.'")
    print_and_log(firewall_status)

def check_sudo_users():
    print_and_log(f"\n{GREEN}[+] Sudo hüququ olan istifadəçilər:{RESET}")
    sudo_users = subprocess.getoutput("getent group sudo | cut -d: -f4")
    if sudo_users:
        print_and_log(sudo_users)
    else:
        print_and_log("Sudo hüququ olan istifadəçi tapılmadı.")

def check_ssh_config():
    print_and_log(f"\n{GREEN}[+] SSH konfiqurasiyasını yoxlayırıq...{RESET}")
    sshd_config_path = "/etc/ssh/sshd_config"
    if os.path.exists(sshd_config_path):
        ssh_config = subprocess.getoutput(f"grep -E 'PermitRootLogin|PasswordAuthentication' {sshd_config_path}")
        if ssh_config:
            print_and_log(ssh_config)
        else:
            print_and_log("SSH təhlükəsizlik parametrləri standart olaraq qalıb.")
    else:
        print_and_log("SSH konfiqurasiya faylı tapılmadı.")

def check_antivirus():
    print_and_log(f"\n{GREEN}[+] Antivirus yoxlanışı...{RESET}")
    antivirus_installed = subprocess.getoutput("which clamav || echo ''")
    if antivirus_installed:
        print_and_log("ClamAV antivirus quraşdırılıb.")
    else:
        print_and_log("Antivirus tapılmadı. Tövsiyə olunur: sudo apt install clamav", "warning")

def check_critical_file_permissions():
    print_and_log(f"\n{GREEN}[+] Kritik fayl icazələrini yoxlayırıq...{RESET}")
    files_to_check = ["/etc/passwd", "/etc/shadow"]
    for file in files_to_check:
        if os.path.exists(file):
            st = os.stat(file)
            permissions = stat.filemode(st.st_mode)
            message = f"{file} icazələri: {permissions}"
            print_and_log(message)
        else:
            print_and_log(f"{file} tapılmadı.")

def check_system_updates():
    print_and_log(f"\n{GREEN}[+] Sistem yeniləmələri yoxlanılır...{RESET}")
    updates = subprocess.getoutput("sudo apt update -qq && sudo apt list --upgradable 2>/dev/null")
    if updates:
        print_and_log("Yenilənə biləcək paketlər var:")
        print_and_log(updates)
    else:
        print_and_log("Bütün paketlər güncəldir.")

def security_recommendations():
    print_and_log(f"\n{YELLOW}[+] Təhlükəsizlik tövsiyələri:{RESET}")
    recommendations = [
        "- SSH üçün root login-i deaktiv et (PermitRootLogin no)",
        "- Password Authentication-i deaktiv et (PasswordAuthentication no)",
        "- Fail2Ban və ya oxşar təhlükəsizlik modulları quraşdır",
        "- İcazəsiz istifadəçilər üçün sudo hüquqlarını məhdudlaşdır",
        "- Güclü parol siyasəti tətbiq et",
        "- Antivirus (ClamAV) quraşdır və mütəmadi olaraq skan et",
        "- Firewall (UFW) aktiv et: sudo ufw enable",
        "- Unudulmuş açıq portları bağla",
        "- Kritik faylların icazələrini yoxla (/etc/passwd, /etc/shadow)"
    ]
    for rec in recommendations:
        print_and_log(rec)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lynis - Təhlükəsizlik Analiz Skripti")
    parser.add_argument("--log", type=str, default="lynis_report.txt", help="Çıxış log faylının adı (default: lynis_report.txt)")
    args = parser.parse_args()

    log_file = args.log
    init_logger(log_file)

    print_and_log(f"{GREEN}=== Lynis Təhlükəsizlik Analizi Başladı ==={RESET}")
    
    check_os_version()
    check_open_ports()
    check_firewall()
    check_sudo_users()
    check_ssh_config()
    check_antivirus()
    check_critical_file_permissions()
    check_system_updates()
    security_recommendations()
    
    print_and_log(f"\n{GREEN}=== Analiz bitdi. Təhlükəsizlik tədbirlərinizi nəzərdən keçirin! ==={RESET}")
