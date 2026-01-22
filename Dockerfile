FROM apache/airflow:2.7.1

# Copy daftar belanja ke dalam container
COPY requirements.txt .

# Install obat-obatan (Pandas, dll)
RUN pip install --no-cache-dir -r requirements.txt