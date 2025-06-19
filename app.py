import tkinter as tk
import database 
from musteri_yonetimi import MusteriYonetimiPenceresi

class AnaUygulama(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ön Muhasebe Programı - Ana Manü")
        self.geometry("400x300")
        self.configure(bg="#F0F0F0")

        database.create_tables()

        self.create_wingets()

    def create_wingets(self):
        baslik_etiket = tk.Label(self, text="Hoş Geldiniz!", font=("Arial", 20, "bold"), bg="#F0F0F0", fg="#333333")
        baslik_etiket.pack(pady=20)

        button_frame = tk.Frame(self, bg="#F0F0F0")
        button_frame.pack(pady=10)

        musteri_button = tk.Button(button_frame, text="Müşteri Yönetimi",
                                   command=self.open_musteri_yonetimi,
                                   font=("Arial", 12), padx=15, pady=10,
                                   bg="#4CAF50", fg="white", relief="raised")
        musteri_button.pack(pady=5, fill="x")

        tk.Button(button_frame, text="Cari Hesap Takibi", 
                  command=lambda: print("Cari Hesap Modülü Açılacak"), # Şimdilik sadece bir mesaj basıyor
                  font=("Arial", 12), padx=15, pady=10,
                  bg="#2196F3", fg="white", relief="raised").pack(pady=5, fill="x")

        tk.Button(button_frame, text="Raporlar", 
                  command=lambda: print("Raporlar Modülü Açılacak"), # Şimdilik sadece bir mesaj basıyor
                  font=("Arial", 12), padx=15, pady=10,
                  bg="#FFC107", fg="black", relief="raised").pack(pady=5, fill="x")
        
        def open_musteri_yonetimi(self): 
            musteri_penceresi = MusteriYonetimiPenceresi(self)
            musteri_penceresi.grab_set()
            selferi_penceresi.focus_set()

if __name__ == "__main__":
    app = AnaUygulama()
    app.mainloop()
