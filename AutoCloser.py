import tkinter as tk
from tkinter import messagebox
import sys
import os

def kaynak_yolu(relative_path):
    """PyInstaller'da iken de çalışan dosya yolu çözümü"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def zaman_hesapla():
    try:
        saat = int(spin_saat.get())
        dakika = int(spin_dakika.get())
        saniye = int(spin_saniye.get())
        toplam_saniye = saat * 3600 + dakika * 60 + saniye

        if toplam_saniye == 0:
            messagebox.showwarning("Uyarı", "Lütfen geçerli bir süre girin.")
            return

        os.system(f"shutdown -s -t {toplam_saniye}")
        messagebox.showinfo("Zamanlama Ayarlandı", f"Bilgisayar {toplam_saniye} saniye sonra kapanacak.")
    except ValueError:
        messagebox.showerror("Hata", "Sayı girilmesi gerekiyor.")

def zamanlamayi_iptal_et():
    os.system("shutdown -a")
    messagebox.showinfo("İptal Edildi", "Zamanlanmış kapatma iptal edildi.")

# Ana pencere ayarları
pencere = tk.Tk()
pencere.title("Otomatik Kapatma Zamanlayıcı")
pencere.geometry("340x300")
pencere.configure(bg="#f2f2f2")
pencere.resizable(False, False)

# İkon
try:
    pencere.iconbitmap(kaynak_yolu("pyicon.ico"))
except Exception as e:
    print(f"İkon yüklenemedi: {e}")

# Başlık
tk.Label(pencere, text="Kapatma Süresi Seçin", font=("Segoe UI", 13, "bold"), bg="#f2f2f2").pack(pady=15)

# Zaman giriş alanları
frame = tk.Frame(pencere, bg="#f2f2f2")
frame.pack(pady=5)

label_font = ("Segoe UI", 10)
spin_font = ("Segoe UI", 10)

# Saat
tk.Label(frame, text="Saat", font=label_font, bg="#f2f2f2").grid(row=0, column=0, padx=10)
spin_saat = tk.Spinbox(frame, from_=0, to=23, width=6, font=spin_font, justify="center")
spin_saat.grid(row=1, column=0, padx=10)

# Dakika
tk.Label(frame, text="Dakika", font=label_font, bg="#f2f2f2").grid(row=0, column=1, padx=10)
spin_dakika = tk.Spinbox(frame, from_=0, to=59, width=6, font=spin_font, justify="center")
spin_dakika.grid(row=1, column=1, padx=10)

# Saniye
tk.Label(frame, text="Saniye", font=label_font, bg="#f2f2f2").grid(row=0, column=2, padx=10)
spin_saniye = tk.Spinbox(frame, from_=0, to=59, width=6, font=spin_font, justify="center")
spin_saniye.grid(row=1, column=2, padx=10)

# Butonlar
btn_baslat = tk.Button(pencere, text="Zamanla ve Başlat", command=zaman_hesapla,
                       bg="#4CAF50", fg="white", font=("Segoe UI", 10, "bold"), width=25, height=2, relief="flat")
btn_baslat.pack(pady=15)

btn_iptal = tk.Button(pencere, text="Zamanlamayı İptal Et", command=zamanlamayi_iptal_et,
                      bg="#f44336", fg="white", font=("Segoe UI", 10, "bold"), width=25, height=2, relief="flat")
btn_iptal.pack()

# Başlat
pencere.mainloop()
