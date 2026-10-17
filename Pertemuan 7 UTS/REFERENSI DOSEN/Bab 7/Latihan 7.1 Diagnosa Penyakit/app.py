from flask import Flask, render_template, request

from inference import DiagnosaPenyakit
from facts import Pasien


app = Flask(__name__)


# =====================================
# KONVERSI JAWABAN KE CF
# =====================================

cf_user = {
    "A": ("tidak", 0.0),
    "B": ("ya", 0.2),
    "C": ("ya", 0.4),
    "D": ("ya", 0.6),
    "E": ("ya", 0.8),
    "F": ("ya", 1.0)
}


# =====================================
# DAFTAR GEJALA
# =====================================

gejala = {
    "demam": "Apakah Anda mengalami demam?",
    "batuk": "Apakah Anda mengalami batuk?",
    "pilek": "Apakah Anda mengalami pilek?",
    "tenggorokan": "Apakah tenggorokan terasa sakit?",
    "mual": "Apakah Anda mengalami mual?",
    "nyeri_perut": "Apakah Anda mengalami nyeri perut?",
    "nafsu_makan": "Apakah nafsu makan menurun?",
    "nyeri_otot": "Apakah Anda mengalami nyeri otot?",
    "sakit_kepala": "Apakah Anda mengalami sakit kepala?",
    "nyeri_ulu_hati": "Apakah Anda mengalami nyeri ulu hati?",
    "muntah": "Apakah Anda mengalami muntah?"
}


# =====================================
# HALAMAN UTAMA
# =====================================

@app.route("/")
def index():

    return render_template(
        "index.html",
        gejala=gejala
    )


# =====================================
# PROSES DIAGNOSA
# =====================================

@app.route("/diagnosa", methods=["POST"])
def diagnosa():

    # Membuat inference engine
    engine = DiagnosaPenyakit()

    engine.reset()

    # Membaca jawaban dari form
    for atribut in gejala:

        jawaban = request.form.get(atribut)

        status, cf = cf_user[jawaban]

        # Nilai gejala
        if atribut == "tenggorokan":

            nilai = "sakit" if status == "ya" else "tidak"

        elif atribut == "nafsu_makan":

            nilai = "turun" if status == "ya" else "tidak"

        else:

            nilai = "ya" if status == "ya" else "tidak"

        # Masukkan fact ke Experta
        engine.declare(
            Pasien(
                **{
                    atribut: nilai,
                    "cf": cf
                }
            )
        )

    # Jalankan inference
    engine.run()

    # Ambil hasil
    hasil = engine.hasil

    # Urutkan berdasarkan CF terbesar
    hasil.sort(
        key=lambda x: x["cf"],
        reverse=True
    )

    return render_template(
        "hasil.html",
        hasil=hasil
    )


# =====================================
# RUN FLASK
# =====================================

# if __name__ == "__main__":
#     app.run(debug=True)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=7860
    )