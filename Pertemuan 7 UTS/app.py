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

class PureMLPPredictor:
    """Prediktor forward pass MLP murni (100% portabel, anti-error BitGenerator/NumPy version mismatch)."""
    def __init__(self, params):
        self.W0 = np.array(params["W0"], dtype=np.float64)
        self.b0 = np.array(params["b0"], dtype=np.float64)
        self.W1 = np.array(params["W1"], dtype=np.float64)
        self.b1 = np.array(params["b1"], dtype=np.float64)
        self.X_min = np.array(params["X_min"], dtype=np.float64)
        self.X_max = np.array(params["X_max"], dtype=np.float64)
        self.y_min = float(params["y_min"])
        self.y_max = float(params["y_max"])

    def predict_price(self, open_val, high_val, low_val, vol_val, prev_close):
        x = np.array([open_val, high_val, low_val, vol_val, prev_close], dtype=np.float64)
        denom_X = np.where(self.X_max == self.X_min, 1.0, self.X_max - self.X_min)
        x_scaled = (x - self.X_min) / denom_X
        # Forward pass MLP: h = relu(x * W0 + b0), out = h * W1 + b1
        h = np.maximum(0.0, np.dot(x_scaled, self.W0) + self.b0)
        y_scaled = np.dot(h, self.W1) + self.b1
        # Denormalisasi balik ke Rupiah
        denom_y = self.y_max - self.y_min
        y_pred = float(y_scaled[0] * denom_y + self.y_min)
        return y_pred

def load_bank_assets(bank_code):
    """
    Memuat model prediksi untuk bank terpilih.
    Mendukung JSON parameter murni (100% tahan banting di server cloud)
    serta format pkl Scikit-Learn bawaan modul.
    """
    # 1. Cek parameter bobot JSON murni (paling stabil & portabel)
    params_path = os.path.join(MODELS_DIR, f"model_params_{bank_code}.json")
    if os.path.exists(params_path):
        try:
            with open(params_path, "r") as f:
                params = json.load(f)
            predictor = PureMLPPredictor(params)
            return predictor, "pure_json"
        except Exception as e:
            print(f"[!] Gagal load model params {bank_code}: {e}")

    # 2. Cek file .pkl Scikit-Learn
    model_path = os.path.join(MODELS_DIR, f"model_{bank_code}.pkl")
    scaler_x_path = os.path.join(MODELS_DIR, f"scaler_X_{bank_code}.pkl")
    scaler_y_path = os.path.join(MODELS_DIR, f"scaler_y_{bank_code}.pkl")

    if os.path.exists(model_path) and os.path.exists(scaler_x_path) and os.path.exists(scaler_y_path):
        try:
            model = joblib.load(model_path)
            scaler_X = joblib.load(scaler_x_path)
            scaler_y = joblib.load(scaler_y_path)
            return (model, scaler_X, scaler_y), "sklearn"
        except Exception as e:
            print(f"[!] Gagal load joblib .pkl {bank_code}: {e}")

    return None, None

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

            model_obj, mode = load_bank_assets(selected_bank)
            if model_obj is None:
                error_msg = f"Model {selected_bank} belum tersedia di server. Silakan pastikan file model di folder 'models/' sudah ada."
            else:
                if mode == "pure_json":
                    pred_price = model_obj.predict_price(open_val, high_val, low_val, vol_val, prev_close)
                else:
                    model, scaler_X, scaler_y = model_obj
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
