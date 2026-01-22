from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import shutil
import pandas as pd
from sqlalchemy import create_engine

# --- KONFIGURASI KHUSUS DOCKER ---
# 1. Database: Pakai host 'postgres' dan port '5432' (Jalur Internal Docker)
DB_URL = 'postgresql://postgres:password@postgres:5432/iron_horse'

# 2. Folder: Pakai jalur absolut di dalam container Airflow
BASE_DIR = '/opt/airflow'
INPUT_FOLDER = os.path.join(BASE_DIR, 'data/input')
PROCESSED_FOLDER = os.path.join(BASE_DIR, 'data/processed')
ERROR_FOLDER = os.path.join(BASE_DIR, 'data/error')

# Setup Koneksi
engine = create_engine(DB_URL)

def pindahkan_file(file_asal, folder_tujuan):
    nama_file = os.path.basename(file_asal)
    tujuan = os.path.join(folder_tujuan, nama_file)
    if os.path.exists(tujuan):
        os.remove(tujuan)
    shutil.move(file_asal, tujuan)
    print(f"📦 File dipindahkan ke: {folder_tujuan}")

def logika_robot():
    print("🤖 Robot Airflow Mulai Bekerja...")
    
    # Cek folder input
    if not os.path.exists(INPUT_FOLDER):
        print(f"⚠️ Folder tidak ditemukan: {INPUT_FOLDER}")
        return

    daftar_file = [f for f in os.listdir(INPUT_FOLDER) if f.endswith('.csv')]
    
    if not daftar_file:
        print("💤 Kosong. Tidak ada CSV baru.")
        return

    print(f"🔎 Ditemukan {len(daftar_file)} file baru.")

    for nama_file in daftar_file:
        path_lengkap = os.path.join(INPUT_FOLDER, nama_file)
        try:
            print(f"🔄 Memproses: {nama_file}")
            
            # Baca CSV
            df = pd.read_csv(path_lengkap)
            
            # Upload ke Database
            df.to_sql('customers_raw', con=engine, if_exists='append', index=False)
            print("✅ Sukses masuk database!")

            # Pindahkan ke Processed
            pindahkan_file(path_lengkap, PROCESSED_FOLDER)
            
        except Exception as e:
            print(f"❌ ERROR: {e}")
            pindahkan_file(path_lengkap, ERROR_FOLDER)

# --- DEFINISI DAG (JADWAL) ---
default_args = {
    'owner': 'Han_DE',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id='robot_pemindah_data_v1',
    default_args=default_args,
    description='Robot pemindah CSV ke Postgres otomatis',
    start_date=datetime(2023, 1, 1),
    schedule_interval='*/5 * * * *',  # <--- JALAN TIAP 5 MENIT
    catchup=False,
    tags=['data_engineering', 'batch']
) as dag:

    # Task 1: Jalankan Fungsi Python tadi
    task_pindah_data = PythonOperator(
        task_id='eksekusi_robot',
        python_callable=logika_robot
    )

    task_pindah_data