# ============================================================
# APLIKASI WEB FLASK - PREDIKSI SAHAM BANK MENGGUNAKAN MLP
# UTS KECERDASAN BUATAN - POLITEKNIK NEGERI MALANG
# Mengadopsi Pola Referensi Dosen: Bab 7 Latihan 7.3 Klasifikasi Status Gizi
# ============================================================

import os
import json
import joblib
import numpy as np
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")
DATA_DIR = os.path.join(BASE_DIR, "data")

BANK_INFO = {
    "BMRI": {"name": "Bank Mandiri (Persero) Tbk", "ticker": "BMRI.JK", "hidden": "3 Neuron"},
    "BBRI": {"name": "Bank Rakyat Indonesia (Persero) Tbk", "ticker": "BBRI.JK", "hidden": "12 Neuron"},
    "BBCA": {"name": "Bank Central Asia Tbk", "ticker": "BBCA.JK", "hidden": "6 Neuron"}
}

def load_bank_assets(bank_code):
    """Memuat model dan scaler untuk bank terpilih."""
    model_path = os.path.join(MODELS_DIR, f"model_{bank_code}.pkl")
    scaler_x_path = os.path.join(MODELS_DIR, f"scaler_X_{bank_code}.pkl")
    scaler_y_path = os.path.join(MODELS_DIR, f"scaler_y_{bank_code}.pkl")

    if not (os.path.exists(model_path) and os.path.exists(scaler_x_path) and os.path.exists(scaler_y_path)):
        return None, None, None

    model = joblib.load(model_path)
    scaler_X = joblib.load(scaler_x_path)
    scaler_y = joblib.load(scaler_y_path)
    return model, scaler_X, scaler_y

def get_latest_data(bank_code):
    """Mengambil data historis terakhir untuk autofill."""
    file_path = os.path.join(DATA_DIR, f"dataset_{bank_code}.xlsx")
    if not os.path.exists(file_path):
        return None
    df = pd.read_excel(file_path)
    last_row = df.iloc[-1]
    return {
        "date": str(last_row["Date"])[:10],
        "open": float(last_row["Open"]),
        "high": float(last_row["High"]),
        "low": float(last_row["Low"]),
        "close": float(last_row["Close"]),
        "volume": int(last_row["Volume"])
    }

def load_eval_summary():
    """Memuat metrik evaluasi model."""
    summary_path = os.path.join(MODELS_DIR, "evaluasi_summary.json")
    if os.path.exists(summary_path):
        with open(summary_path, "r") as f:
            return json.load(f)
    return {}

# ============================================================
# HALAMAN UTAMA: PREDIKSI HARGA SAHAM (FOKUS PREDIKSI)
# ============================================================
@app.route("/", methods=["GET", "POST"])
@app.route("/predict", methods=["POST"])
def index():
    selected_bank = request.form.get("bank", request.args.get("bank", "BMRI")).upper()
    if selected_bank not in BANK_INFO:
        selected_bank = "BMRI"

    latest = get_latest_data(selected_bank)
    eval_summary = load_eval_summary()
    bank_eval = eval_summary.get(selected_bank, {})

    hasil = None
    input_values = None
    error_msg = None

    if request.method == "POST":
        try:
            open_val = float(request.form["open"])
            high_val = float(request.form["high"])
            low_val = float(request.form["low"])
            vol_val = float(request.form["volume"])
            prev_close = float(request.form["close_lag1"])

            input_values = {
                "open": open_val,
                "high": high_val,
                "low": low_val,
                "volume": vol_val,
                "close_lag1": prev_close
            }

            model, scaler_X, scaler_y = load_bank_assets(selected_bank)
            if model is None:
                error_msg = f"Model {selected_bank} belum tersedia di server. Silakan jalankan 'python Train_model.py' di terminal."
            else:
                feature_names = ["Open", "High", "Low", "Volume", "Close_Lag1"]
                data_in = pd.DataFrame([[open_val, high_val, low_val, vol_val, prev_close]], columns=feature_names)
                data_scaled = scaler_X.transform(data_in)
                pred_scaled = model.predict(data_scaled)
                pred_price = float(scaler_y.inverse_transform(pred_scaled.reshape(-1, 1))[0][0])

                perubahan_rp = pred_price - prev_close
                perubahan_pct = (perubahan_rp / prev_close) * 100 if prev_close != 0 else 0

                hasil = {
                    "pred_price": round(pred_price, 2),
                    "pred_price_rounded": round(pred_price),
                    "perubahan_rp": round(perubahan_rp, 2),
                    "perubahan_pct": round(perubahan_pct, 2),
                    "status": "NAIK (BULLISH) ▲" if perubahan_rp >= 0 else "TURUN (BEARISH) ▼",
                    "status_class": "naik" if perubahan_rp >= 0 else "turun"
                }
        except Exception as e:
            error_msg = f"Error saat kalkulasi prediksi: {str(e)}"
            print("Error prediksi:", e)

    return render_template(
        "index.html",
        banks=BANK_INFO,
        selected_bank=selected_bank,
        latest=latest,
        hasil=hasil,
        input_values=input_values,
        eval_data=bank_eval,
        error_msg=error_msg
    )

if __name__ == "__main__":
    app.run(debug=True, port=5000)
