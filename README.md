# 🚂 End-to-End Batch Data Pipeline with Airflow & Docker

Project ini adalah simulasi **ETL Pipeline** (Extract, Transform, Load) sederhana yang memindahkan data CSV secara otomatis ke Database PostgreSQL menggunakan **Apache Airflow**.

## 🛠️ Tech Stack
- **Language:** Python 3.8
- **Orchestration:** Apache Airflow 2.7
- **Database:** PostgreSQL 13
- **Containerization:** Docker & Docker Compose
- **Tools:** pgAdmin 4 (Database Interface), Pandas

## 📂 Project Structure
```text
.
├── dags/                   # Folder berisi script DAG Airflow (Otak Robot)
├── data/                   # Folder simulasi data
│   ├── input/              # Taruh file CSV di sini
│   ├── processed/          # File akan pindah ke sini setelah sukses
│   └── error/              # File pindah ke sini jika gagal
├── docker-compose.yaml     # Konfigurasi Service (Airflow, Postgres, pgAdmin)
└── requirements.txt        # Dependency Python


🚀 How to Run
Pastikan kamu sudah menginstall Docker Desktop atau Docker Engine.

1.Clone Repository

git clone [https://github.com/Raihannoorx/end-to-end-airflow-docker.git](https://github.com/Raihannoorx/end-to-end-airflow-docker.git)
cd end-to-end-airflow-docker
Jalankan Docker

2. Jalankan Docker

docker-compose up -d --build
Tunggu beberapa menit hingga semua container (Webserver, Scheduler, Postgres) berjalan.

Tunggu beberapa menit hingga semua container (Webserver, Scheduler, Postgres) berjalan.

3.Akses Dashboard

    Airflow UI: http://localhost:8081

    User: admin

    Pass: admin

    pgAdmin: http://localhost:8080

    Email: admin@admin.com

    Pass: root

Cara Kerja (Simulation)

Letakkan file .csv apapun di folder data/input/.

Airflow akan mendeteksi file tersebut (Jadwal: Setiap 5 Menit).

Data otomatis di-upload ke tabel customers_raw di PostgreSQL.

File dipindahkan ke folder data/processed/.

---
