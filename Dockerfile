# Gunakan base image Airflow yang stabil
FROM apache/airflow:2.8.1-python3.10

# Copy file requirements.txt dari laptopmu ke dalam Docker
COPY requirements.txt /

# Install library menggunakan pip
RUN pip install --no-cache-dir -r /requirements.txt