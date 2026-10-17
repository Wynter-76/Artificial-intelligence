import pickle

# ============================================================
# 1. LOAD MODEL
# ============================================================

with open("model_gizi.pkl", "rb") as file:
    model_data = pickle.load(file)

model = model_data["model"]
gender_encoder = model_data["gender_encoder"]
target_encoder = model_data["target_encoder"]

# ============================================================
# 2. INPUT DATA BARU
# ============================================================

jenis_kelamin = input("Jenis Kelamin (L/P): ")
usia = float(input("Usia (bulan): "))
berat_badan = float(input("Berat Badan (kg): "))
tinggi_badan = float(input("Tinggi Badan (cm): "))

# ============================================================
# 3. ENCODE JENIS KELAMIN
# ============================================================

jenis_kelamin_encoded = gender_encoder.transform(
    [jenis_kelamin]
)[0]

# ============================================================
# 4. DATA BARU
# ============================================================

data_baru = [[
    jenis_kelamin_encoded,
    usia,
    berat_badan,
    tinggi_badan
]]

# ============================================================
# 5. PREDIKSI
# ============================================================

prediksi = model.predict(data_baru)

# ============================================================
# 6. HASIL
# ============================================================

hasil = target_encoder.inverse_transform(prediksi)[0]

print("\n===================================")
print("HASIL PREDIKSI")
print("===================================")

print("Status Gizi :", hasil)