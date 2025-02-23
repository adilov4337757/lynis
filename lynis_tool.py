import os
import subprocess
import platform
import shutil

def check_os_version():
    """ OS versiyasını yoxlayır """
    print("\n[+] OS versiyasını yoxlayırıq...")
    try:
        os_version = subprocess.getoutput("cat /etc/os-release")
        print(os_version)
    except Exception as e:
        print(f"Xəta baş verdi: {e}")

def check_open_ports():
    """ Açıq portları yoxlayır """
    print("\n[+] Açıq portları yoxlayırıq...")
    open_ports = subprocess.getoutput("ss -tulnp | grep LISTEN")
    print(open_ports if open_ports else "Heç bir açıq port tapılmadı.")

def check_firewall():
    """ Firewall aktivdir ya yox onu yoxlayır """
    print("\n[+] Firewall vəziyyətini yoxlayırıq...")
    firewall_status = subprocess.getoutput("sudo ufw status")
    print(firewall_status)

def check_sudo_users():
    """ Sudo hüququ olan istifadəçiləri yoxlayır """
    print("\n[+] Sudo hüququ olan istifadəçilər:")
    sudo_users = subprocess.getoutput("getent group sudo | cut -d: -f4")
    print(sudo_users if sudo_users else "Sudo hüququ olan istifadəçi yoxdur.")

def check_ssh_config():
    """ SSH konfiqurasiyasını yoxlayır """
    print("\n[+] SSH konfiqurasiyasını yoxlayırıq...")
    sshd_config_path = "/etc/ssh/sshd_config"
    
    if os.path.exists(sshd_config_path):
        ssh_config = subprocess.getoutput(f"grep -E 'PermitRootLogin|PasswordAuthentication' {sshd_config_path}")
        print(ssh_config if ssh_config else "SSH təhlükəsizlik parametrləri standart olaraq qalıb.")
    else:
        print("SSH konfiqurasiya faylı tapılmadı.")

def check_antivirus():
    """ Antivirusun olub-olmadığını yoxlayır """
    print("\n[+] Antivirus yoxlanışı...")
    antivirus_installed = subprocess.getoutput("which clamav")
    
    if antivirus_installed:
        print("ClamAV antivirus quraşdırılıb.")
    else:
        print("Antivirus tapılmadı. Tövsiyə olunur: sudo apt install clamav")

def security_recommendations():
    """ Təhlükəsizlik tövsiyələri verir """
    print("\n[+] Təhlükəsizlik tövsiyələri:")
    recommendations = [
        "- SSH üçün root login-i deaktiv et (PermitRootLogin no)",
        "- Password Authentication-i deaktiv et (PasswordAuthentication no)",
        "- Fail2Ban və ya oxşar təhlükəsizlik modulları quraşdır",
        "- İcazəsiz istifadəçilər üçün sudo hüquqlarını məhdudlaşdır",
        "- Güclü parol siyasəti tətbiq et",
        "- Antivirus (ClamAV) quraşdır və mütəmadi olaraq skan et",
        "- Firewall (UFW) aktiv et: sudo ufw enable",
        "- Unudulmuş açıq portları bağla"
    ]
    for rec in recommendations:
        print(rec)

if __name__ == "__main__":
    print("=== Lynis Təhlükəsizlik Analizi Başladı ===")
    
    check_os_version()
    check_open_ports()
    check_firewall()
    check_sudo_users()
    check_ssh_config()
    check_antivirus()
    security_recommendations()
    
    print("\n=== Analiz bitdi. Təhlükəsizlik tədbirlərinizi görün! ===")
