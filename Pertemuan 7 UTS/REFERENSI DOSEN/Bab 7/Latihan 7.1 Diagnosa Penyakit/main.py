from inference import DiagnosaPenyakit
from facts import Pasien

# =====================================
# Konversi Jawaban ke CF
# =====================================

cf_user = {
    "A": ("tidak", 0.0),
    "B": ("ya",    0.2),
    "C": ("ya",    0.4),
    "D": ("ya",    0.6),
    "E": ("ya",    0.8),
    "F": ("ya",    1.0)
}

# =====================================
# Daftar Gejala
# =====================================

gejala = {
    "demam": ("Apakah Anda mengalami demam?", "ya"),
    "batuk": ("Apakah Anda mengalami batuk?", "ya"),
    "pilek": ("Apakah Anda mengalami pilek?", "ya"),
    "tenggorokan": ("Apakah tenggorokan terasa sakit?", "sakit"),
    "mual": ("Apakah Anda mengalami mual?", "ya"),
    "nyeri_perut": ("Apakah Anda mengalami nyeri perut?", "ya"),
    "nafsu_makan": ("Apakah nafsu makan menurun?", "turun"),
    "nyeri_otot": ("Apakah Anda mengalami nyeri otot?", "ya"),
    "sakit_kepala": ("Apakah Anda mengalami sakit kepala?", "ya"),
    "nyeri_ulu_hati": ("Apakah Anda mengalami nyeri ulu hati?", "ya"),
    "muntah": ("Apakah Anda mengalami muntah?", "ya")
}

# =====================================
# Header
# =====================================

print("=" * 60)
print("SISTEM PAKAR DIAGNOSA PENYAKIT")
print("Forward Chaining + Certainty Factor ")
print("=" * 60)

print("\nTingkat Keyakinan")
print("A = Tidak Yakin        (0.0)")
print("B = Sedikit Yakin      (0.2)")
print("C = Cukup Yakin        (0.4)")
print("D = Yakin              (0.6)")
print("E = Sangat Yakin       (0.8)")
print("F = Pasti              (1.0)")

# =====================================
# Membuat Engine
# =====================================

engine = DiagnosaPenyakit()
engine.reset()

# =====================================
# Input User
# =====================================

for atribut, (pertanyaan, nilai) in gejala.items():

    while True:

        print(f"\n{pertanyaan}")

        jawab = input("Pilihan [A/B/C/D/E/F] : ").upper()

        if jawab in cf_user:
            break

        print("Pilihan tidak valid!")

    status, cf = cf_user[jawab]

    engine.declare(
        Pasien(
            **{
                atribut: nilai if status == "ya" else "tidak",
                "cf": cf
            }
        )
    )

# =====================================
# Jalankan Inferensi
# =====================================

print("\n" + "=" * 60)
print("HASIL DIAGNOSA")
print("=" * 60)

engine.run()