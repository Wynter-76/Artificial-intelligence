# ============================================================
# APLIKASI WEB FLASK - PREDIKSI SAHAM BANK MENGGUNAKAN MLP
# UTS KECERDASAN BUATAN - POLITEKNIK NEGERI MALANG
# Mengadopsi Pola Referensi Dosen: Bab 7 Latihan 7.3 & Modul Bab 6
# ============================================================

import os
import json
import joblib
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")
DATA_DIR = os.path.join(BASE_DIR, "data")

# Konfigurasi Saham
BANK_INFO = {
    "BMRI": {
        "name": "Bank Mandiri (Persero) Tbk",
        "ticker": "BMRI.JK",
        "code": "BMRI",
        "badge": "BUMN",
        "color": "#2563eb",
        "hidden_layer": "3 Neuron",
        "journal_mae": 38.3087,
        "journal_rmse": 49.5650,
        "journal_mse": 2456.689,
        "journal_mape": 0.63
    },
    "BBRI": {
        "name": "Bank Rakyat Indonesia (Persero) Tbk",
        "ticker": "BBRI.JK",
        "code": "BBRI",
        "badge": "BUMN",
        "color": "#059669",
        "hidden_layer": "12 Neuron",
        "journal_mae": 39.5462,
        "journal_rmse": 50.0030,
        "journal_mse": 2500.300,
        "journal_mape": 0.74
    },
    "BBCA": {
        "name": "Bank Central Asia Tbk",
        "ticker": "BBCA.JK",
        "code": "BBCA",
        "badge": "Swasta",
        "color": "#7c3aed",
        "hidden_layer": "6 Neuron",
        "journal_mae": 47.7587,
        "journal_rmse": 62.4340,
        "journal_mse": 3898.004,
        "journal_mape": 0.51
    }
}

# ============================================================
# HELPER: LOAD MODEL, SCALER, DAN DATA
# ============================================================
def load_bank_assets(bank_code):
    """Memuat model MLP dan scaler untuk bank yang dipilih."""
    model_path = os.path.join(MODELS_DIR, f"model_{bank_code}.pkl")
    scaler_x_path = os.path.join(MODELS_DIR, f"scaler_X_{bank_code}.pkl")
    scaler_y_path = os.path.join(MODELS_DIR, f"scaler_y_{bank_code}.pkl")

    if not (os.path.exists(model_path) and os.path.exists(scaler_x_path) and os.path.exists(scaler_y_path)):
        return None, None, None

    model = joblib.load(model_path)
    scaler_X = joblib.load(scaler_x_path)
    scaler_y = joblib.load(scaler_y_path)
    return model, scaler_X, scaler_y

def get_latest_stock_data(bank_code):
    """Mendapatkan data baris terakhir dari file Excel dataset."""
    file_path = os.path.join(DATA_DIR, f"dataset_{bank_code}.xlsx")
    if not os.path.exists(file_path):
        return None
    df = pd.read_excel(file_path)
    last_row = df.iloc[-1]
    prev_close = float(df["Close"].iloc[-2]) if len(df) > 1 else float(last_row["Close"])
    return {
        "date": str(last_row["Date"])[:10],
        "open": float(last_row["Open"]),
        "high": float(last_row["High"]),
        "low": float(last_row["Low"]),
        "close": float(last_row["Close"]),
        "volume": int(last_row["Volume"]),
        "prev_close": prev_close
    }

def load_eval_summary():
    """Memuat ringkasan evaluasi dari models/evaluasi_summary.json"""
    summary_path = os.path.join(MODELS_DIR, "evaluasi_summary.json")
    if os.path.exists(summary_path):
        with open(summary_path, "r") as f:
            return json.load(f)
    return {}

# ============================================================
# ROUTE: HOME / DASHBOARD
# ============================================================
@app.route("/")
def index():
    eval_summary = load_eval_summary()
    latest_data = {}
    for code in BANK_INFO.keys():
        latest_data[code] = get_latest_stock_data(code)

    return render_template(
        "index.html",
        banks=BANK_INFO,
        eval_summary=eval_summary,
        latest_data=latest_data
    )

# ============================================================
# ROUTE: PREDIKSI INTERAKTIF
# ============================================================
@app.route("/prediksi", methods=["GET", "POST"])
def prediksi():
    selected_bank = request.args.get("bank", "BMRI").upper()
    if selected_bank not in BANK_INFO:
        selected_bank = "BMRI"

    latest = get_latest_stock_data(selected_bank)
    hasil_prediksi = None
    multistep_results = None
    input_values = None

    if request.method == "POST":
        action = request.form.get("action", "single")
        selected_bank = request.form.get("bank", selected_bank)
        model, scaler_X, scaler_y = load_bank_assets(selected_bank)

        if model is not None:
            if action == "single":
                # Mode 1: Prediksi Single Day (Hari Berikutnya)
                open_val = float(request.form.get("open", latest["open"]))
                high_val = float(request.form.get("high", latest["high"]))
                low_val = float(request.form.get("low", latest["low"]))
                vol_val = float(request.form.get("volume", latest["volume"]))
                prev_close = float(request.form.get("close_lag1", latest["close"]))

                input_values = {
                    "open": open_val,
                    "high": high_val,
                    "low": low_val,
                    "volume": vol_val,
                    "close_lag1": prev_close
                }

                # Input DataFrame [Open, High, Low, Volume, Close_Lag1]
                feature_names = ["Open", "High", "Low", "Volume", "Close_Lag1"]
                data_in = pd.DataFrame([[open_val, high_val, low_val, vol_val, prev_close]], columns=feature_names)
                data_scaled = scaler_X.transform(data_in)
                pred_scaled = model.predict(data_scaled)
                pred_price = scaler_y.inverse_transform(pred_scaled.reshape(-1, 1))[0][0]

                perubahan_rp = pred_price - prev_close
                perubahan_pct = (perubahan_rp / prev_close) * 100 if prev_close != 0 else 0

                hasil_prediksi = {
                    "bank": selected_bank,
                    "bank_name": BANK_INFO[selected_bank]["name"],
                    "pred_price": round(pred_price, 2),
                    "pred_price_int": round(pred_price),
                    "perubahan_rp": round(perubahan_rp, 2),
                    "perubahan_pct": round(perubahan_pct, 2),
                    "status": "BULLISH (NAIK)" if perubahan_rp >= 0 else "BEARISH (TURUN)",
                    "color_class": "text-green-600" if perubahan_rp >= 0 else "text-red-600"
                }

            elif action == "multistep":
                # Mode 2: Prediksi N-Hari ke Depan (Sesuai Praktikum 6.2 Hal 23-25)
                n_days = int(request.form.get("n_days", 5))
                df_hist = pd.read_excel(os.path.join(DATA_DIR, f"dataset_{selected_bank}.xlsx"))

                history_close = df_hist["Close"].tolist()
                last_r = df_hist.iloc[-1]
                rec_open = float(last_r["Open"])
                rec_high = float(last_r["High"])
                rec_low = float(last_r["Low"])
                rec_vol = float(last_r["Volume"])

                feature_names = ["Open", "High", "Low", "Volume", "Close_Lag1"]
                multistep_results = []
                for step in range(1, n_days + 1):
                    p_close = history_close[-1]
                    feat = pd.DataFrame([[rec_open, rec_high, rec_low, rec_vol, p_close]], columns=feature_names)
                    feat_sc = scaler_X.transform(feat)
                    p_sc = model.predict(feat_sc)
                    p_price = scaler_y.inverse_transform(p_sc.reshape(-1, 1))[0][0]

                    multistep_results.append({
                        "hari": f"Hari ke-{step}",
                        "estimasi_harga": round(p_price),
                        "perubahan_dari_awal": round(p_price - float(last_r["Close"]), 2)
                    })
                    history_close.append(p_price)

    return render_template(
        "prediksi.html",
        banks=BANK_INFO,
        selected_bank=selected_bank,
        latest=latest,
        hasil_prediksi=hasil_prediksi,
        multistep_results=multistep_results,
        input_values=input_values
    )

# ============================================================
# ROUTE: EVALUASI MODEL
# ============================================================
@app.route("/evaluasi")
def evaluasi():
    eval_summary = load_eval_summary()
    return render_template(
        "evaluasi.html",
        banks=BANK_INFO,
        eval_summary=eval_summary
    )

# ============================================================
# ROUTE: ANALISIS KOMPARASI (SYARAT POIN 8 UTS)
# ============================================================
@app.route("/komparasi")
def komparasi():
    eval_summary = load_eval_summary()
    return render_template(
        "komparasi.html",
        banks=BANK_INFO,
        eval_summary=eval_summary
    )

# ============================================================
# API: DATA HISTORIS UNTUK CHART.JS
# ============================================================
@app.route("/api/stock-data/<bank_code>")
def api_stock_data(bank_code):
    bank_code = bank_code.upper()
    if bank_code not in BANK_INFO:
        return jsonify({"error": "Bank tidak valid"}), 400

    file_path = os.path.join(DATA_DIR, f"dataset_{bank_code}.xlsx")
    if not os.path.exists(file_path):
        return jsonify({"error": "Dataset belum tersedia"}), 404

    df = pd.read_excel(file_path)
    # Ambil 100 data terakhir agar grafik browser ringan dan responsif
    recent_df = df.tail(100).copy()
    dates = [str(d)[:10] for d in recent_df["Date"].tolist()]
    close_prices = [round(float(p), 2) for p in recent_df["Close"].tolist()]
    open_prices = [round(float(p), 2) for p in recent_df["Open"].tolist()]

    return jsonify({
        "bank": bank_code,
        "name": BANK_INFO[bank_code]["name"],
        "dates": dates,
        "close": close_prices,
        "open": open_prices
    })

# ============================================================
# RUN APPLICATION
# ============================================================
if __name__ == "__main__":
    app.run(debug=True, port=5000)
