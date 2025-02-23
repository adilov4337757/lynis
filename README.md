# Lynis Tool

Lynis Tool, Linux sistemlərinin təhlükəsizlik auditini aparan bir analiz skriptidir.  
Bu skript:
- OS versiyasını, açıq portları və firewall vəziyyətini yoxlayır,
- Sudo hüquqları olan istifadəçiləri və SSH konfiqurasiya parametrlərini araşdırır,
- Antivirus yoxlanışı, kritik fayl icazələri və sistem yeniləmələrini yoxlayır,
- Əlavə təhlükəsizlik tövsiyələri təqdim edir.

## İstifadə Qaydası:

1. Reposu klonlayın:
   ```sh
   git clone https://github.com/adilov4337757/lynis.git
   cd lynis
   python3 lynis_tool.py --log my_lynis_report.txt

# Əgər --log parametrini verməsəniz  nəticələr lynis_report.txt  faylına yazılacaq 
