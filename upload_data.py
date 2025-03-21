import csv
import sqlite3
import sys  # Untuk keluar dari aplikasi

DATABASE_FILE = "gosdb.db"

def list_tables():
    """Menampilkan daftar semua tabel dalam database SQLite."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        if tables:
            return [table[0] for table in tables]
        else:
            return []
    except sqlite3.Error as e:
        print(f"Terjadi kesalahan SQLite: {e}")
        return []
    finally:
        if conn:
            conn.close()

def get_table_columns(table_name):
    """Mendapatkan daftar nama kolom dari tabel tertentu."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        return [column[1] for column in columns]  # column[1] berisi nama kolom
    except sqlite3.Error as e:
        print(f"Terjadi kesalahan SQLite saat mendapatkan kolom: {e}")
        return []
    finally:
        if conn:
            conn.close()

def upload_csv_to_table(table_name, csv_file_path, expected_columns):
    """Mengunggah data dari file CSV ke tabel SQLite dan memvalidasi header."""

    conn = None

    try:
        # Hubungkan ke database
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()

        # Baca file CSV
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)

            # Dapatkan header (nama kolom) dari baris pertama
            header = next(csv_reader)

            # Validasi header
            if header != expected_columns:
                print("ERROR: Header CSV tidak sesuai dengan kolom tabel.")
                print(f"Header CSV: {header}")
                print(f"Kolom Tabel: {expected_columns}")
                return False  # Validasi gagal

            # Buat placeholder untuk query INSERT
            placeholders = ', '.join('?' * len(header))

            # Query INSERT
            insert_query = f"INSERT INTO {table_name} ({', '.join(header)}) VALUES ({placeholders})"

            # Masukkan data baris per baris
            for row in csv_reader:
                try:
                    #Eksekusi Query Insert
                    cursor.execute(insert_query, row)
                except sqlite3.Error as e:
                    print(f"Error inserting row {row}: {e}")
                    continue #Lanjut ke baris selanjutnya jika error

        # Commit perubahan
        conn.commit()
        print(f"Data dari '{csv_file_path}' berhasil diunggah ke tabel '{table_name}'.")
        return True #Validasi Sukses

    except FileNotFoundError:
        print(f"File CSV '{csv_file_path}' tidak ditemukan.")
        return False
    except sqlite3.Error as e:
        print(f"Terjadi kesalahan SQLite: {e}")
        return False
    except Exception as e:
        print(f"Terjadi kesalahan umum: {e}")
        return False

    finally:
        if conn:
            conn.close()
            print("Koneksi ke database ditutup.")

if __name__ == "__main__":
    # Dapatkan daftar tabel
    tables = list_tables()

    if not tables:
        print("Tidak ada tabel yang ditemukan dalam database. Pastikan Anda telah menjalankan create_db.py.")
        sys.exit()  # Keluar dari aplikasi

    # Tampilkan daftar tabel kepada pengguna
    print("Tabel yang tersedia:")
    for i, table in enumerate(tables):
        print(f"{i+1}. {table}")

    # Minta pengguna memilih tabel
    while True:
        try:
            choice = int(input("Masukkan nomor tabel yang ingin diunggah data: "))
            if 1 <= choice <= len(tables):
                selected_table = tables[choice - 1]
                break
            else:
                print("Nomor tabel tidak valid. Coba lagi.")
        except ValueError:
            print("Input tidak valid. Masukkan nomor yang benar.")

    # Dapatkan daftar kolom untuk tabel yang dipilih
    table_columns = get_table_columns(selected_table)
    if not table_columns:
        print("Tidak dapat mendapatkan daftar kolom untuk tabel yang dipilih.")
        sys.exit()

    print(f"\nKolom untuk tabel '{selected_table}':")
    for column in table_columns:
        print(f"- {column}")

    # Minta pengguna memasukkan jalur file CSV
    csv_file_path = input("\nMasukkan jalur lengkap file CSV: ")

    # Upload data dan validasi header
    if not upload_csv_to_table(selected_table, csv_file_path, table_columns):
        print("Pengunggahan data gagal. Aplikasi akan keluar.")
        sys.exit()  # Keluar dari aplikasi

    print("Pengunggahan data selesai.")
