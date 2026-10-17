from flask import Flask, render_template, request
import pickle
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "model_gizi.pkl"
)

# ============================================================
# LOAD MODEL
# ============================================================

with open(MODEL_PATH, "rb") as file:
    model_data = pickle.load(file)

model = model_data["model"]
gender_encoder = model_data["gender_encoder"]
target_encoder = model_data["target_encoder"]


# ============================================================
# HOME
# ============================================================

@app.route("/")
def index():
    return render_template("index.html")


# ============================================================
# PREDICTION
# ============================================================

@app.route("/predict", methods=["POST"])
def predict():

    jenis_kelamin = request.form["jenis_kelamin"]
    usia = float(request.form["usia"])
    berat_badan = float(request.form["berat_badan"])
    tinggi_badan = float(request.form["tinggi_badan"])

    # Encode jenis kelamin
    jenis_kelamin_encoded = gender_encoder.transform(
        [jenis_kelamin]
    )[0]

    # Data baru
    data_baru = [[
        jenis_kelamin_encoded,
        usia,
        berat_badan,
        tinggi_badan
    ]]

    # Prediksi
    prediksi = model.predict(data_baru)

    hasil = target_encoder.inverse_transform(prediksi)[0]

    # Probabilitas
    probabilitas = model.predict_proba(data_baru)[0]

    probabilities = []

    for i, probability in enumerate(probabilitas):

        nama_kelas = target_encoder.inverse_transform([i])[0]

        probabilities.append({
            "kelas": nama_kelas,
            "nilai": round(probability * 100, 2)
        })

    return render_template(
        "index.html",
        hasil=hasil,
        probabilities=probabilities,
        jenis_kelamin=jenis_kelamin,
        usia=usia,
        berat_badan=berat_badan,
        tinggi_badan=tinggi_badan
    )


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)