# ============================================================
# TRAIN MODEL MLP - PREDIKSI HARGA SAHAM BANK TERBESAR DI INDONESIA
# Studi Kasus: Bank Mandiri (BMRI), Bank BRI (BBRI), Bank BCA (BBCA)
# Referensi: Muh. Falah Mubaraq dkk. (Jurnal INFORMATIKA, 2024)
# Sesuai Format Modul Bab 6: Praktikum 6.2 & 6.4 (Machine Learning MLP)
# ============================================================

import os
import json
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Buat direktori output
os.makedirs("models", exist_ok=True)
os.makedirs("static/plots", exist_ok=True)
os.makedirs("data", exist_ok=True)

# ============================================================
# KONFIGURASI SESUAI JURNAL REFERENSI (Tabel 5 & 6)
# ============================================================
CONFIG = {
    "BMRI": {
        "name": "Bank Mandiri (BMRI.JK)",
        "file": "data/dataset_BMRI.xlsx",
        "neurons": (3,),       # Best neuron dari Tabel 6 jurnal: 3 neuron
        "lr": 0.01,
        "max_iter": 1200,
        "journal_mae": 38.3087,
        "journal_rmse": 49.5650,
        "journal_mse": 2456.689,
        "journal_mape": 0.63
    },
    "BBRI": {
        "name": "Bank Rakyat Indonesia (BBRI.JK)",
        "file": "data/dataset_BBRI.xlsx",
        "neurons": (12,),      # Best neuron dari Tabel 6 jurnal: 12 neuron
        "lr": 0.01,
        "max_iter": 1200,
        "journal_mae": 39.5462,
        "journal_rmse": 50.0030,
        "journal_mse": 2500.300,
        "journal_mape": 0.74
    },
    "BBCA": {
        "name": "Bank Central Asia (BBCA.JK)",
        "file": "data/dataset_BBCA.xlsx",
        "neurons": (6,),       # Best neuron dari Tabel 6 jurnal: 6 neuron
        "lr": 0.01,
        "max_iter": 1200,
        "journal_mae": 47.7587,
        "journal_rmse": 62.4340,
        "journal_mse": 3898.004,
        "journal_mape": 0.51
    }
}

def train_bank_model(bank_code, cfg):
    print("\n" + "=" * 65)
    print(f"MEMULAI PELATIHAN MODEL MLP: {cfg['name']}")
    print("=" * 65)

    # ============================================================
    # 1. LOAD DATASET
    # ============================================================
    print(f"\n[1] Membaca dataset dari: {cfg['file']}")
    df = pd.read_excel(cfg["file"])
    print("    Kolom dataset :", df.columns.tolist())
    print("    Jumlah total baris:", len(df))

    # ============================================================
    # 2. BERSIHKAN DATA & MEMBUAT FITUR (TIME SERIES LAG)
    # ============================================================
    print("\n[2] Preprocessing Data & Feature Engineering")
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").reset_index(drop=True)

    # Tambahkan fitur lag harga penutupan kemarin (sesuai Modul Bab 6 Praktikum 6.2)
    df["Close_Lag1"] = df["Close"].shift(1)
    df = df.dropna().reset_index(drop=True)

    # Fitur input gabungan candlestick (Jurnal) dan Lag Time Series (Modul Dosen)
    features = ["Open", "High", "Low", "Volume", "Close_Lag1"]
    target = "Close"

    X = df[features]
    y = df[target]

    print(f"    Fitur input ({len(features)} variabel): {features}")
    print(f"    Target output: {target}")

    # ============================================================
    # 3. TRAIN TEST SPLIT (90% Training & 10% Testing sesuai Jurnal)
    # ============================================================
    train_size = int(len(df) * 0.90)
    X_train = X.iloc[:train_size]
    X_test = X.iloc[train_size:]
    y_train = y.iloc[:train_size]
    y_test = y.iloc[train_size:]
    dates_test = df["Date"].iloc[train_size:].dt.strftime("%Y-%m-%d").values

    print(f"\n[3] Pembagian Data (Rasio 90:10):")
    print(f"    Data Training : {len(X_train)} baris")
    print(f"    Data Testing  : {len(X_test)} baris")

    # ============================================================
    # 4. NORMALISASI DENGAN MINMAXSCALER (Sesuai Modul Dosen & Jurnal)
    # ============================================================
    print("\n[4] Normalisasi Data menggunakan MinMaxScaler [0, 1]")
    scaler_X = MinMaxScaler(feature_range=(0, 1))
    scaler_y = MinMaxScaler(feature_range=(0, 1))

    X_train_scaled = scaler_X.fit_transform(X_train)
    X_test_scaled = scaler_X.transform(X_test)
    y_train_scaled = scaler_y.fit_transform(y_train.values.reshape(-1, 1)).ravel()

    # ============================================================
    # 5. MEMBANGUN MODEL MLP (Sesuai Modul Praktikum 6.2 & Jurnal)
    # ============================================================
    print(f"\n[5] Membangun Arsitektur MLPRegressor:")
    print(f"    Hidden Layer Neurons : {cfg['neurons']}")
    print(f"    Fungsi Aktivasi      : ReLU")
    print(f"    Optimizer / Solver   : Adam")
    print(f"    Learning Rate Awal   : {cfg['lr']}")

    model = MLPRegressor(
        hidden_layer_sizes=cfg["neurons"],
        activation="relu",
        solver="adam",
        learning_rate_init=cfg["lr"],
        max_iter=cfg["max_iter"],
        tol=1e-6,
        random_state=42,
        early_stopping=True,
        validation_fraction=0.1,
        n_iter_no_change=30
    )

    # ============================================================
    # 6. TRAINING MODEL
    # ============================================================
    print("\n[6] Proses Pelatihan Model (Training)...")
    model.fit(X_train_scaled, y_train_scaled)
    print(f"    Training selesai! Jumlah iterasi: {model.n_iter_}")

    # ============================================================
    # 7. PREDIKSI DATA TESTING
    # ============================================================
    print("\n[7] Menguji Model pada Data Testing...")
    y_pred_scaled = model.predict(X_test_scaled)
    # Denormalisasi balik ke satuan Rupiah
    y_pred = scaler_y.inverse_transform(y_pred_scaled.reshape(-1, 1)).ravel()

    # ============================================================
    # 8. EVALUASI MODEL (MAE, MSE, RMSE, MAPE, R2 Sesuai Syarat Dosen)
    # ============================================================
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mape = np.mean(np.abs((y_test.values - y_pred) / y_test.values)) * 100
    r2 = r2_score(y_test, y_pred)

    print("\n" + "=" * 60)
    print(f"HASIL EVALUASI MODEL MLP - {bank_code}")
    print("=" * 60)
    print(f"MAE  (Mean Absolute Error)     : Rp {mae:,.2f}")
    print(f"MSE  (Mean Squared Error)      : {mse:,.2f}")
    print(f"RMSE (Root Mean Squared Error) : Rp {rmse:,.2f}")
    print(f"MAPE (Mean Abs. Pct Error)     : {mape:.2f}%")
    print(f"R²   (Koefisien Determinasi)   : {r2:.4f}")

    # ============================================================
    # 9. SIMPAN HASIL PREDIKSI KE EXCEL (Format Praktikum 6.2)
    # ============================================================
    hasil_df = pd.DataFrame({
        "Tanggal": dates_test,
        "Harga_Aktual": y_test.values,
        "Harga_Prediksi": y_pred,
        "Selisih_Error": np.abs(y_test.values - y_pred)
    })
    excel_output = f"hasil_test_{bank_code}.xlsx"
    hasil_df.to_excel(excel_output, index=False)
    print(f"\n[9] Hasil prediksi data test tersimpan di: {excel_output}")

    # ============================================================
    # 10. VISUALISASI GRAFIK AKTUAL VS PREDIKSI & LOSS
    # ============================================================
    plot_path = f"static/plots/actual_vs_predicted_{bank_code}.png"
    plt.figure(figsize=(12, 6))
    plt.plot(dates_test, y_test.values, label="Harga Aktual (Rp)", color="#2563eb", linewidth=2)
    plt.plot(dates_test, y_pred, label="Harga Prediksi MLP (Rp)", color="#dc2626", linestyle="--", linewidth=2)
    plt.title(f"Perbandingan Harga Aktual vs Prediksi MLP - {cfg['name']}", fontsize=14, pad=15)
    plt.xlabel("Tanggal", fontsize=11)
    plt.ylabel("Harga Saham (Rp)", fontsize=11)
    # Atur tick label agar tidak terlalu padat
    step = max(1, len(dates_test) // 10)
    plt.xticks(ticks=range(0, len(dates_test), step), labels=[dates_test[i] for i in range(0, len(dates_test), step)], rotation=45)
    plt.legend(fontsize=11)
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.tight_layout()
    plt.savefig(plot_path, dpi=200)
    plt.close()
    print(f"[10] Grafik perbandingan tersimpan di: {plot_path}")

    # Visualisasi Kurva Loss Pelatihan (Praktikum 6.4)
    loss_plot_path = f"static/plots/training_loss_{bank_code}.png"
    plt.figure(figsize=(8, 4.5))
    plt.plot(model.loss_curve_, color="#16a34a", linewidth=2)
    plt.title(f"Kurva Training Loss MLP - {bank_code}", fontsize=13)
    plt.xlabel("Iterasi (Epoch)", fontsize=10)
    plt.ylabel("Loss (MSE Loss)", fontsize=10)
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.tight_layout()
    plt.savefig(loss_plot_path, dpi=200)
    plt.close()

    # ============================================================
    # 11. SIMPAN MODEL & SCALER MENGGUNAKAN JOBLIB (Format Modul Dosen)
    # ============================================================
    model_file = f"models/model_{bank_code}.pkl"
    scaler_x_file = f"models/scaler_X_{bank_code}.pkl"
    scaler_y_file = f"models/scaler_y_{bank_code}.pkl"

    joblib.dump(model, model_file)
    joblib.dump(scaler_X, scaler_x_file)
    joblib.dump(scaler_y, scaler_y_file)

    print(f"[11] Model dan scaler berhasil disimpan ke:")
    print(f"     - {model_file}")
    print(f"     - {scaler_x_file}")
    print(f"     - {scaler_y_file}")

    return {
        "bank_code": bank_code,
        "name": cfg["name"],
        "neurons": str(cfg["neurons"]),
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "mae": round(float(mae), 4),
        "mse": round(float(mse), 4),
        "rmse": round(float(rmse), 4),
        "mape": round(float(mape), 2),
        "r2": round(float(r2), 4),
        "journal_mae": cfg["journal_mae"],
        "journal_rmse": cfg["journal_rmse"],
        "journal_mse": cfg["journal_mse"],
        "journal_mape": cfg["journal_mape"],
        "last_actual_price": float(y_test.iloc[-1]),
        "last_pred_price": round(float(y_pred[-1]), 2),
        "last_date": str(dates_test[-1])
    }

def main():
    print("=" * 65)
    print("EKSEKUSI PELATIHAN MODEL PREDIKSI SAHAM (UTS KECERDASAN BUATAN)")
    print("=" * 65)

    summary = {}
    for code, cfg in CONFIG.items():
        res = train_bank_model(code, cfg)
        summary[code] = res

    # Simpan ringkasan evaluasi ke file JSON untuk dipakai di Web Flask
    with open("models/evaluasi_summary.json", "w") as f:
        json.dump(summary, f, indent=4)

    print("\n" + "=" * 65)
    print("REKAPITULASI EVALUASI SELURUH BANK (DIBANDINGKAN DENGAN JURNAL)")
    print("=" * 65)
    print(f"{'Bank':<6} | {'MAE Project':<12} | {'MAE Jurnal':<12} | {'MAPE Project':<13} | {'MAPE Jurnal':<12} | {'R2':<6}")
    print("-" * 65)
    for code, s in summary.items():
        print(f"{code:<6} | Rp {s['mae']:<9.2f} | Rp {s['journal_mae']:<9.2f} | {s['mape']:<11.2f}% | {s['journal_mape']:<10.2f}% | {s['r2']:<6.4f}")
    print("=" * 65)
    print("SEMUA MODEL SELESAI DILATIH DAN SIAP DIGUNAKAN DI FLASK APP!\n")

if __name__ == "__main__":
    main()
