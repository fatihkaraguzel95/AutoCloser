import tkinter as tk
from tkinter import messagebox
import sys
import os
import smtplib
from email.message import EmailMessage
import datetime
import webbrowser

# Global degiskenler
kalan_saniye = 0
mail_gonderildi = False
geri_sayim_etkin = False
mail_bilgileri = {}


def kaynak_yolu(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def mail_ayarlarini_yukle():
    global mail_bilgileri
    config_path = "mail_config.txt"

    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            for line in f:
                key, value = line.strip().split("=", 1)
                mail_bilgileri[key] = value
        return True
    return False


def mail_ayarlarini_kaydet(from_mail, sifre, to_mails):
    with open("mail_config.txt", "w") as f:
        f.write(f"mail={from_mail}\n")
        f.write(f"sifre={sifre}\n")
        f.write(f"hedef={to_mails}\n")


def mail_gonder():
    global mail_bilgileri

    mesaj = EmailMessage()
    mesaj["Subject"] = "Bilgisayar Kapanıyor"
    mesaj["From"] = mail_bilgileri["mail"]
    mesaj["To"] = mail_bilgileri["hedef"]
    mesaj.set_content(f"Bilgisayar 10 saniye içinde kapanacak.\nTarih/Saat: {datetime.datetime.now()}")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(mail_bilgileri["mail"], mail_bilgileri["sifre"])
            smtp.send_message(mesaj)
        print("Mail gönderildi.")
    except Exception as e:
        print(f"Mail gönderilemedi: {e}")


def zaman_hesapla():
    global kalan_saniye, geri_sayim_etkin, mail_gonderildi
    try:
        saat = int(spin_saat.get())
        dakika = int(spin_dakika.get())
        saniye = int(spin_saniye.get())
        toplam_saniye = saat * 3600 + dakika * 60 + saniye

        if toplam_saniye < 10:
            messagebox.showwarning("Uyarı", "Süre en az 10 saniye olmalıdır (mail için).")
            return

        kalan_saniye = toplam_saniye
        mail_gonderildi = False
        geri_sayim_etkin = True
        geri_sayim()

        os.system(f"shutdown -s -t {toplam_saniye}")
        messagebox.showinfo("Zamanlama Ayarlandı", f"Bilgisayar {toplam_saniye} saniye sonra kapanacak.")
    except ValueError:
        messagebox.showerror("Hata", "Sayı girilmesi gerekiyor.")


def geri_sayim():
    global kalan_saniye, geri_sayim_etkin, mail_gonderildi

    if kalan_saniye >= 0 and geri_sayim_etkin:
        saat = kalan_saniye // 3600
        dakika = (kalan_saniye % 3600) // 60
        saniye = kalan_saniye % 60
        label_sayac.config(text=f"Kalan süre: {saat:02}:{dakika:02}:{saniye:02}")

        if kalan_saniye == 10 and not mail_gonderildi:
            mail_gonder()
            mail_gonderildi = True

        kalan_saniye -= 1
        pencere.after(1000, geri_sayim)
    else:
        label_sayac.config(text="")


def zamanlamayi_iptal_et():
    global geri_sayim_etkin
    os.system("shutdown -a")
    geri_sayim_etkin = False
    label_sayac.config(text="Zamanlama iptal edildi.")
    messagebox.showinfo("İptal Edildi", "Zamanlanmış kapatma iptal edildi.")


def konfig_penceresi():
    def kaydet_ve_devam():
        from_mail = entry_gonderen.get()
        sifre = entry_sifre.get()
        to_mails = entry_alici.get()

        if not from_mail or not sifre or not to_mails:
            messagebox.showerror("Hata", "Tüm alanları doldurmalısınız.")
            return

        mail_ayarlarini_kaydet(from_mail, sifre, to_mails)
        config_win.destroy()
        arayuzu_baslat()

    def linke_git(event):
        webbrowser.open_new("https://myaccount.google.com/apppasswords")

    config_win = tk.Tk()
    config_win.title("Mail Ayarları")
    config_win.geometry("400x340")
    config_win.resizable(False, False)
    config_win.configure(bg="#f2f2f2")

    info_text = ("Lütfen Gmail bilgilerinizi girin.\n"
                 "Mail, bilgisayar kapanmadan 10 saniye önce gönderilecektir.\n"
                 "\n"
                 "Uygulama şifresi almak için buraya tıklayın:")

    tk.Label(config_win, text=info_text, bg="#f2f2f2", font=("Segoe UI", 10), justify="left").pack(pady=(10, 0))
    link = tk.Label(config_win, text="https://myaccount.google.com/apppasswords", fg="blue", cursor="hand2", bg="#f2f2f2")
    link.pack()
    link.bind("<Button-1>", linke_git)

    tk.Label(config_win, text="\nGönderen Gmail:", bg="#f2f2f2").pack()
    entry_gonderen = tk.Entry(config_win, width=40)
    entry_gonderen.pack(pady=5)

    tk.Label(config_win, text="Uygulama Şifresi:", bg="#f2f2f2").pack()
    entry_sifre = tk.Entry(config_win, width=40, show="*")
    entry_sifre.pack(pady=5)

    tk.Label(config_win, text="Alıcı Mail(ler) (virgülle):", bg="#f2f2f2").pack()
    entry_alici = tk.Entry(config_win, width=40)
    entry_alici.pack(pady=5)

    tk.Button(config_win, text="Kaydet ve Devam Et", bg="#4CAF50", fg="white",
              font=("Segoe UI", 10, "bold"), command=kaydet_ve_devam).pack(pady=15)

    config_win.mainloop()


def arayuzu_baslat():
    global pencere, spin_saat, spin_dakika, spin_saniye, label_sayac

    pencere = tk.Tk()
    pencere.title("Otomatik Kapatma Zamanlayıcı")
    pencere.geometry("340x330")
    pencere.configure(bg="#f2f2f2")
    pencere.resizable(False, False)

    try:
        pencere.iconbitmap(kaynak_yolu("pyicon.ico"))
    except Exception:
        pass

    tk.Label(pencere, text="Kapatma Süresi Seçin", font=("Segoe UI", 13, "bold"), bg="#f2f2f2").pack(pady=15)

    frame = tk.Frame(pencere, bg="#f2f2f2")
    frame.pack(pady=5)

    label_font = ("Segoe UI", 10)
    spin_font = ("Segoe UI", 10)

    tk.Label(frame, text="Saat", font=label_font, bg="#f2f2f2").grid(row=0, column=0, padx=10)
    spin_saat = tk.Spinbox(frame, from_=0, to=23, width=6, font=spin_font, justify="center")
    spin_saat.grid(row=1, column=0, padx=10)

    tk.Label(frame, text="Dakika", font=label_font, bg="#f2f2f2").grid(row=0, column=1, padx=10)
    spin_dakika = tk.Spinbox(frame, from_=0, to=59, width=6, font=spin_font, justify="center")
    spin_dakika.grid(row=1, column=1, padx=10)

    tk.Label(frame, text="Saniye", font=label_font, bg="#f2f2f2").grid(row=0, column=2, padx=10)
    spin_saniye = tk.Spinbox(frame, from_=0, to=59, width=6, font=spin_font, justify="center")
    spin_saniye.grid(row=1, column=2, padx=10)

    tk.Button(pencere, text="Zamanla ve Başlat", command=zaman_hesapla,
              bg="#4CAF50", fg="white", font=("Segoe UI", 10, "bold"), width=25, height=2, relief="flat").pack(pady=15)

    tk.Button(pencere, text="Zamanlamayı İptal Et", command=zamanlamayi_iptal_et,
              bg="#f44336", fg="white", font=("Segoe UI", 10, "bold"), width=25, height=2, relief="flat").pack()

    label_sayac = tk.Label(pencere, text="", font=("Segoe UI", 12, "bold"), bg="#f2f2f2", fg="#333")
    label_sayac.pack(pady=10)

    pencere.mainloop()


# Başlatıcı
if mail_ayarlarini_yukle():
    arayuzu_baslat()
else:
    konfig_penceresi()