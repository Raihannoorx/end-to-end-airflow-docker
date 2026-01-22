import os
import shutil
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

# --- KONFIGURASI JALUR ---
# Host-nya 'localhost', Port-nya '5433' .
DB_URL = 'postgresql://postgres:password@localhost:5433/iron_horse'

# Folder kerja
BASE_DIR = os.getcwd()
INPUT_FOLDER = os.path.join(BASE_DIR, 'data/input')
PROCESSED_FOLDER = os.path.join(BASE_DIR, 'data/processed')
ERROR_FOLDER = os.path.join(BASE_DIR, 'data/error')

# Bikin koneksi mesin
engine = create_engine(DB_URL)

def pindahkan_file(file_asal, folder_tujuan):
    nama_file = os.path.basename(file_asal)
    tujuan = os.path.join(folder_tujuan, nama_file)
    
    # Kalau di tujuan udah ada file dengan nama sama, timpa aja (overwrite)
    if os.path.exists(tujuan):
        os.remove(tujuan)
        
    shutil.move(file_asal, tujuan)
    print(f" File dipindahkan ke: {folder_tujuan}")

def jalankan_robot():
    print(f" Robot Bangun! Mengecek folder: {INPUT_FOLDER}")
    
    # 1. Absen file apa aja yang ada di folder Input
    # List comprehension: Ambil file yang akhiran .csv saja
    daftar_file = [f for f in os.listdir(INPUT_FOLDER) if f.endswith('.csv')]
    
    if not daftar_file:
        print(" Kosong. Tidak ada CSV baru.")
        return

    print(f" Ditemukan {len(daftar_file)} file antrian.")

    for nama_file in daftar_file:
        path_lengkap = os.path.join(INPUT_FOLDER, nama_file)
        
        try:
            print(f"\n Sedang memproses: {nama_file}...")
            
            # 2. BACA CSV
            df = pd.read_csv(path_lengkap)
            
            # Bersih-bersih dikit (Postgres gasuka NaN)
            df = df.where(pd.notnull(df), None)

            # 3. UPLOAD KE DATABASE
            df.to_sql('customers_raw', con=engine, if_exists='append', index=False)
            print("✅ Sukses masuk database!")

            # 4. PINDAHKAN KE FOLDER PROCESSED (SUKSES)
            pindahkan_file(path_lengkap, PROCESSED_FOLDER)
            
        except Exception as e:
            print(f" ERROR Gawat: {e}")
            # 5. KALAU ERROR, LEMPAR KE FOLDER ERROR
            pindahkan_file(path_lengkap, ERROR_FOLDER)

if __name__ == "__main__":
    jalankan_robot()