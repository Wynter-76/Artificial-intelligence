# 📈 Proyek UTS Kecerdasan Buatan: Prediksi Harga Saham Bank Indonesia dengan Multilayer Perceptron (MLP)

Aplikasi web berbasis Flask untuk peramalan harga penutupan (*Close Price*) saham perbankan terbesar di Indonesia (**Bank Mandiri - BMRI**, **Bank BRI - BBRI**, dan **Bank BCA - BBCA**) menggunakan algoritma **Multilayer Perceptron (MLP)**.

---

## 🎯 Informasi Proyek UTS
* **Mata Kuliah:** Kecerdasan Buatan (Semester Genap)
* **Program Studi:** D3 Manajemen Informatika - PSDKU Kediri, Politeknik Negeri Malang
* **Topik:** Prediksi Data (Time Series Forecasting)
* **Algoritma:** Multilayer Perceptron (MLP) Regressor
* **Evaluasi:** Mean Absolute Error (MAE), Mean Squared Error (MSE), RMSE, MAPE, dan $R^2$ Score
* **Framework Web:** Flask (Python) + Chart.js + Vanilla CSS Modern

---

## 📚 Artikel Jurnal Referensi Utama
* **Judul:** *Implementasi Metode Backpropagation Neural Network Untuk Memprediksi Saham Bank Terbesar di Indonesia*
* **Penulis:** Muh. Falah Mubaraq, Nelti Juliana Sahera, Indri, Rizal Adi Saputra (Teknik Informatika, Universitas Halu Oleo)
* **Publikasi:** Jurnal INFORMATIKA Universitas Labuhanbatu, Vol. 12 No. 3 / Juli 2024.
* **ISSN:** 2615-1855 (E-ISSN) / 2303-2863 (P-ISSN)

---

## 📂 Struktur Direktori Proyek
```text
Pertemuan 7 UTS/
├── data/                       # Dataset historis saham (Excel & CSV)
│   ├── dataset_BMRI.xlsx
│   ├── dataset_BBRI.xlsx
│   └── dataset_BBCA.xlsx
├── models/                     # Model terlatih & scaler (.pkl)
│   ├── model_BMRI.pkl
│   ├── scaler_X_BMRI.pkl
│   ├── scaler_y_BMRI.pkl
│   └── evaluasi_summary.json
├── static/
│   ├── css/
│   │   └── style.css           # Styling FinTech modern (Dark Slate)
│   └── plots/                  # Visualisasi grafik pengujian & loss
│       ├── actual_vs_predicted_BMRI.png
│       └── training_loss_BMRI.png
├── templates/                  # Antarmuka Web Flask (HTML5)
│   ├── base.html
│   ├── index.html              # Dashboard utama & interaktif chart
│   ├── prediksi.html           # Simulator formulir prediksi harga
│   ├── evaluasi.html           # Matriks evaluasi MAE & MSE
│   └── komparasi.html          # Analisis Poin 8 UTS (Project vs Jurnal)
├── download_data.py            # Skrip penarik data otomatis Yahoo Finance
├── Train_model.py              # Skrip pelatihan model (Sesuai Modul Bab 6)
├── Test_model.py               # Skrip pengujian interaktif terminal
├── app.py                      # Aplikasi server web Flask
├── requirements.txt            # Daftar pustaka dependency
└── Procfile                    # Konfigurasi deployment server
```

---

## 🚀 Cara Menjalankan Proyek Secara Lokal

### 1. Jalankan Pelatihan Model (Jika Belum)
```bash
python Train_model.py
```
Skrip ini akan memproses dataset, melatih model MLP untuk BMRI, BBRI, dan BBCA, menghitung nilai MAE dan MSE, menyimpan model `.pkl`, serta meng-generate grafik evaluasi.

### 2. Jalankan Pengujian Terminal (Opsional)
```bash
python Test_model.py
```

### 3. Jalankan Aplikasi Web Flask
```bash
python app.py
```
Akses di browser melalui URL: `http://127.0.0.1:5000`

---

## 🌐 Panduan Deployment Online Gratis (Poin 4 UTS)

### Opsi A: Deploy ke Render.com (Direkomendasikan)
1. Buat repositori baru di GitHub (misal `uts-kecerdasan-buatan-prediksi-saham`), lalu push seluruh folder ini.
2. Buka [render.com](https://render.com) dan login menggunakan akun GitHub.
3. Klik **New +** $\rightarrow$ **Web Service**.
4. Pilih repositori GitHub proyek ini.
5. Konfigurasi:
   * **Runtime:** Python 3
   * **Build Command:** `pip install -r requirements.txt`
   * **Start Command:** `gunicorn app:app`
6. Klik **Deploy Web Service**. Dalam 2–3 menit, Anda akan mendapatkan tautan HTTPS publik (misal: `https://stockpredict-polinema.onrender.com`).

---

## 📊 Hasil Evaluasi & Komparasi (Poin 8 UTS)

| Bank | Arsitektur | MAE Project | MAE Jurnal | MSE Project | MAPE Project | R² Score |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **BMRI** | 3 Neuron | **Rp 35.04** | Rp 38.31 | **2,004.14** | **0.58%** | **0.9948** |
| **BBRI** | 12 Neuron | **Rp 86.90** | Rp 39.55 | **13,469.52** | **1.55%** | **0.9364** |
| **BBCA** | 6 Neuron | **Rp 49.34** | Rp 47.76 | **4,012.43** | **0.53%** | **0.9708** |

*Semua nilai MAPE berada di bawah 2% dengan koefisien determinasi ($R^2 > 0.93$), membuktikan model sangat akurat dan mereplikasi temuan jurnal secara valid.*
