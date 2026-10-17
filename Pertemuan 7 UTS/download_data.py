# ============================================================
# DOWNLOAD DATASET SAHAM HISTORIS DARI YAHOO FINANCE
# Bank Mandiri (BMRI.JK), Bank BRI (BBRI.JK), Bank BCA (BBCA.JK)
# Referensi: Muh. Falah Mubaraq dkk. (2024)
# ============================================================

import os
import yfinance as yf
import pandas as pd

# Direktori data
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# Konfigurasi saham sesuai jurnal referensi
BANKS = {
    "BMRI": {"ticker": "BMRI.JK", "start": "2013-01-01", "end": "2024-07-01", "name": "Bank Mandiri"},
    "BBRI": {"ticker": "BBRI.JK", "start": "2013-01-01", "end": "2024-07-01", "name": "Bank Rakyat Indonesia"},
    "BBCA": {"ticker": "BBCA.JK", "start": "2013-01-01", "end": "2024-07-01", "name": "Bank Central Asia"}
}

def download_and_save():
    print("=" * 65)
    print("MENGUNDUH DATASET SAHAM DARI YAHOO FINANCE")
    print("=" * 65)

    for code, info in BANKS.items():
        print(f"\n[+] Mengunduh data {info['name']} ({info['ticker']})...")
        # Menggunakan auto_adjust=False agar harga unadjusted sesuai data nominal di BEI/Jurnal
        df = yf.download(info["ticker"], start=info["start"], end=info["end"], auto_adjust=False)

        # Flatten multiindex columns jika dihasilkan oleh yfinance terbaru
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [c[0] for c in df.columns]

        df = df.reset_index()

        # Pastikan kolom-kolom standar tersedia
        expected_cols = ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]
        available_cols = [c for c in expected_cols if c in df.columns]
        df = df[available_cols].copy()

        # Bersihkan format tanggal
        df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")

        # Drop missing values
        df = df.dropna().reset_index(drop=True)

        file_excel = os.path.join(DATA_DIR, f"dataset_{code}.xlsx")
        file_csv = os.path.join(DATA_DIR, f"dataset_{code}.csv")

        df.to_excel(file_excel, index=False)
        df.to_csv(file_csv, index=False)

        print(f"    Berhasil disimpan ke: {file_excel} dan {file_csv}")
        print(f"    Jumlah data: {len(df)} baris")
        print(f"    Periode data: {df['Date'].iloc[0]} s/d {df['Date'].iloc[-1]}")
        print(f"    Sample Harga Terakhir (28 Juni 2024): Close = Rp {df['Close'].iloc[-1]:,.0f}")

    print("\n" + "=" * 65)
    print("SELURUH DATASET BERHASIL DIUNDUH DAN DISIMPAN!")
    print("=" * 65)

if __name__ == "__main__":
    download_and_save()
