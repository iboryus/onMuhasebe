import tkinter as tk
from tkinter import messagebox
import database

class MusteriYonetimiPenceresi(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Müşteri Yönetimi")
        self.geometry("600x400")

        database.create_tables()

        self.create_widgets()

    def create_widgets(self):
        form_frame = tk.LabelFrame(self, text="Yeni Müşteri Ekle", padx=10, pady=10)
        form_frame.pack(padx=20, pady=10, fill="x")

        tk.Label(form_frame, text="Ad Soyad:").grid(row=0, column=0, pady=2, sticky="w")
        self.ad_soyad_entry = tk.Entry(form_frame, width=40)
        self.ad_soyad_entry.grid(row=0, column=1, pady=2, sticky="ew")

        tk.Label(form_frame, text="Vergi/TC No:").grid(row=1, column=0, pady=2, sticky="w")
        self.vergi_tc_no_entry = tk.Entry(form_frame, width=40)
        self.vergi_tc_no_entry.grid(row=1, column=1, pady=2, sticky="ew")

        tk.Label(form_frame, text="Adres:").grid(row=2, column=0, pady=2, sticky="w")
        self.adres_entry = tk.Entry(form_frame, width=40)
        self.adres_entry.grid(row=2, column=1, pady=2, sticky="ew")

        tk.Label(form_frame, text="Telefon:").grid(row=3, column=0, pady=2, sticky="w")
        self.telefon_entry = tk.Entry(form_frame, width=40)
        self.telefon_entry.grid(row=3, column=1, pady=2, sticky="ew")

        tk.Label(form_frame, text="E-posta:").grid(row=4, column=0, pady=2, sticky="w")
        self.email_entry = tk.Entry(form_frame, width=40)
        self.email_entry.grid(row=4, column=1, pady=2, sticky="ew")

        kaydet_button = tk.Button(form_frame, text="Müşteriyi Kaydet", command=self.kaydet_musteri)
        kaydet_button.grid(row=5, column=0, columnspan=2, pady=10)

        self.liste_frame = tk.LabelFrame(self, text="Müşteriler Listesi", padx=10, pady=10)
        self.liste_frame.pack(padx=20, pady=10, fill="both", expand=True)

        tk.Label(self.liste_frame, text="Müşteriler burada listelenecek...").pack()
        
        form_frame.grid_columnconfigure(1, weight=1)

    def kaydet_musteri(self):
        ad_soyad = self.ad_soyad_entry.get()
        vergi_tc_no = self.vergi_tc_no_entry.get()
        adres = self.adres_entry.get()
        telefon = self.telefon_entry.get()
        email = self.email_entry.get()

        if not ad_soyad:
            messagebox.showwarning("Eksik Bilgi", "Lütfen müşteri adını ve soyadını girin.")
            return

        conn = database.connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO musteriler (ad_soyad, vergi_tc_no, adres, telefon, email)
                VALUES (?, ?, ?, ?, ?)
            ''', (ad_soyad, vergi_tc_no, adres, telefon, email))
            conn.commit()
            messagebox.showinfo("Başarılı", "Müşteri başarıyla kaydedildi!")
            self.clear_form()
        except sqlite3.Error as e:
            messagebox.showerror("Veritabanı Hatası", f"Müşteri kaydedilirken bir hata oluştu: {e}")
        finally:
            conn.close()

    def clear_form(self):
        self.ad_soyad_entry.delete(0, tk.END)
        self.vergi_tc_no_entry.delete(0, tk.END)
        self.adres_entry.delete(0, tk.END)
        self.telefon_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.ad_soyad_entry.focus_set()

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    app = MusteriYonetimiPenceresi(root)
    app.mainloop()