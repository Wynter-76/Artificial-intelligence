# ============================================================
# TEST MODEL MLP - PENGUJIAN PREDIKSI HARGA SAHAM
# Mengadopsi Pola Modul Bab 6: Praktikum 6.2 (Halaman 21-25) & 6.3
# ============================================================

import os
import joblib
import numpy as np
import pandas as pd

def main():
    print("=" * 60)
    print(" PROGRAM PENGUJIAN MODEL PREDIKSI SAHAM (MLP)")
    print(" Bank Mandiri (BMRI), Bank BRI (BBRI), Bank BCA (BBCA)")
    print("=" * 60)

    # 1. PILIH BANK
    print("\nPilih Kode Saham Bank:")
    print("1. BMRI (Bank Mandiri)")
    print("2. BBRI (Bank Rakyat Indonesia)")
    print("3. BBCA (Bank Central Asia)")
    pilihan = input("\nMasukkan pilihan (1/2/3 atau BMRI/BBRI/BBCA) [default BMRI]: ").strip().upper()

    mapping = {
        "1": "BMRI", "BMRI": "BMRI",
        "2": "BBRI", "BBRI": "BBRI",
        "3": "BBCA", "BBCA": "BBCA"
    }
    bank_code = mapping.get(pilihan, "BMRI")
    print(f"\n[+] Saham terpilih: {bank_code}")

    # ============================================================
    # 2. LOAD MODEL & SCALER
    # ============================================================
    model_file = f"models/model_{bank_code}.pkl"
    scaler_x_file = f"models/scaler_X_{bank_code}.pkl"
    scaler_y_file = f"models/scaler_y_{bank_code}.pkl"
    dataset_file = f"data/dataset_{bank_code}.xlsx"

    if not os.path.exists(model_file):
        print(f"[!] Error: File model {model_file} tidak ditemukan. Jalankan Train_model.py terlebih dahulu.")
        return

    model = joblib.load(model_file)
    scaler_X = joblib.load(scaler_x_file)
    scaler_y = joblib.load(scaler_y_file)
    df = pd.read_excel(dataset_file)

    last_row = df.iloc[-1]
    last_close = float(last_row["Close"])
    last_date = str(last_row["Date"])[:10]

    print(f"[+] Model dan Scaler {bank_code} berhasil dimuat.")
    print(f"[+] Data historis terakhir ({last_date}):")
    print(f"    Open   : Rp {float(last_row['Open']):,.0f}")
    print(f"    High   : Rp {float(last_row['High']):,.0f}")
    print(f"    Low    : Rp {float(last_row['Low']):,.0f}")
    print(f"    Close  : Rp {last_close:,.0f}")
    print(f"    Volume : {int(last_row['Volume']):,}")

    # ============================================================
    # 3. PILIH MODE PENGUJIAN
    # ============================================================
    print("\nPilih Mode Pengujian:")
    print("A. Prediksi Harga Penutupan (Close) dari Data Hari Ini")
    print("B. Prediksi Multistep N-Hari ke Depan (Sesuai Praktikum 6.2)")
    mode = input("\nPilihan mode (A/B) [default A]: ").strip().upper()

    if mode == "B":
        # Mode Multistep N-Hari ke Depan (Praktikum 6.2 Hal 23-25)
        try:
            n_hari = int(input("Masukkan jumlah hari prediksi ke depan (contoh: 3 atau 5) [default 3]: ") or "3")
        except ValueError:
            n_hari = 3

        print("\n" + "=" * 60)
        print(f"PREDIKSI HARGA {bank_code} {n_hari} HARI KE DEPAN")
        print("=" * 60)
        print(f"Harga terakhir ({last_date}) : Rp {last_close:,.0f}\n")

        history_close = df["Close"].tolist()
        recent_open = float(last_row["Open"])
        recent_high = float(last_row["High"])
        recent_low = float(last_row["Low"])
        recent_vol = float(last_row["Volume"])

        feature_names = ["Open", "High", "Low", "Volume", "Close_Lag1"]
        hasil_prediksi = []
        for i in range(1, n_hari + 1):
            prev_close = history_close[-1]
            # Estimasi fitur input hari berikutnya
            feat = pd.DataFrame([[recent_open, recent_high, recent_low, recent_vol, prev_close]], columns=feature_names)
            feat_scaled = scaler_X.transform(feat)
            pred_scaled = model.predict(feat_scaled)
            pred_close = scaler_y.inverse_transform(pred_scaled.reshape(-1, 1))[0][0]
            pred_rounded = round(pred_close)

            hasil_prediksi.append(pred_rounded)
            history_close.append(pred_close)
            print(f"Hari ke-{i} : Rp {pred_rounded:,.0f}")

        print("=" * 60)

    else:
        # Mode Input Data Candlestick Baru (Praktikum 6.3 Hal 37-38)
        print("\nMasukkan data harga saham (atau tekan Enter untuk menggunakan data terakhir):")
        inp_open = input(f"Nilai Open   [default {last_row['Open']:.0f}] : ").strip()
        inp_high = input(f"Nilai High   [default {last_row['High']:.0f}] : ").strip()
        inp_low  = input(f"Nilai Low    [default {last_row['Low']:.0f}] : ").strip()
        inp_vol  = input(f"Nilai Volume [default {int(last_row['Volume'])}] : ").strip()

        open_val = float(inp_open) if inp_open else float(last_row["Open"])
        high_val = float(inp_high) if inp_high else float(last_row["High"])
        low_val  = float(inp_low)  if inp_low  else float(last_row["Low"])
        vol_val  = float(inp_vol)  if inp_vol  else float(last_row["Volume"])
        prev_close = last_close

        # ============================================================
        # 4. PREDIKSI DATA BARU
        # ============================================================
        feature_names = ["Open", "High", "Low", "Volume", "Close_Lag1"]
        data_baru = pd.DataFrame([[open_val, high_val, low_val, vol_val, prev_close]], columns=feature_names)
        data_scaled = scaler_X.transform(data_baru)
        pred_scaled = model.predict(data_scaled)
        prediksi_close = scaler_y.inverse_transform(pred_scaled.reshape(-1, 1))[0][0]

        # ============================================================
        # 5. HASIL PREDIKSI
        # ============================================================
        print("\n" + "=" * 60)
        print(f"HASIL PREDIKSI HARGA PENUTUPAN (CLOSE) - {bank_code}")
        print("=" * 60)
        print(f"Input Open        : Rp {open_val:,.0f}")
        print(f"Input High        : Rp {high_val:,.0f}")
        print(f"Input Low         : Rp {low_val:,.0f}")
        print(f"Input Volume      : {int(vol_val):,}")
        print(f"Close Kemarin     : Rp {prev_close:,.0f}")
        print("------------------------------------------------------------")
        print(f"ESTIMASI HARGA PENUTUPAN (CLOSE) : Rp {prediksi_close:,.2f}")
        perubahan = ((prediksi_close - prev_close) / prev_close) * 100
        arah = "NAIK ▲" if perubahan >= 0 else "TURUN ▼"
        print(f"Potensi Perubahan : {perubahan:+.2f}% ({arah})")
        print("=" * 60)

if __name__ == "__main__":
    main()
