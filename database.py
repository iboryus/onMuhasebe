import sqlite3

def connect_db():
    conn = sqlite3.connect('muhasebe.db')
    return conn

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE İF NOT EXISTS musteriler(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   ad_soyad TEXT KEY AUROINCREMENT,
                   vergi_tc_no TEXT,
                   adres TEXT,
                   telefon TEXT,
                   email TEXT
                   )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__name__':
    create_tables()
    print("Veritabanı ve müşteri tablosu başarıyla oluşturuldu.")