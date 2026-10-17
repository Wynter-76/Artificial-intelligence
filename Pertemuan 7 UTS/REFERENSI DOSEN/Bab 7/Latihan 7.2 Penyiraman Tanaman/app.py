from flask import Flask, render_template, request

from inference import simulasi

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():

    hasil = None
    kelembapan_input = None
    suhu_input = None

    if request.method == "POST":

        kelembapan_input = float(
            request.form["kelembapan"]
        )

        suhu_input = float(
            request.form["suhu"]
        )

        simulasi.input["kelembapan"] = kelembapan_input
        simulasi.input["suhu"] = suhu_input

        simulasi.compute()

        hasil = simulasi.output["penyiraman"]

    return render_template(
        "index.html",
        hasil=hasil,
        kelembapan=kelembapan_input,
        suhu=suhu_input
    )


if __name__ == "__main__":
    app.run(debug=True)