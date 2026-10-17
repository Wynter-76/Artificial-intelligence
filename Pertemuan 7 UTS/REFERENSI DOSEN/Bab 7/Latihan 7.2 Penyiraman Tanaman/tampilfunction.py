import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz

# =====================================
# KELEMBAPAN
# =====================================

x_kelembapan = np.arange(0, 101, 1)

kering = fuzz.trapmf(x_kelembapan, [0, 0, 20, 40])
lembap = fuzz.trimf(x_kelembapan, [30, 50, 70])
basah = fuzz.trapmf(x_kelembapan, [60, 80, 100, 100])

plt.figure(figsize=(8,4))
plt.plot(x_kelembapan, kering, label='Kering')
plt.plot(x_kelembapan, lembap, label='Lembap')
plt.plot(x_kelembapan, basah, label='Basah')

plt.title("Membership Function Kelembapan Tanah")
plt.xlabel("Kelembapan (%)")
plt.ylabel("Derajat Keanggotaan")
plt.xlim(0,100)
plt.ylim(-0.05,1.05)
plt.grid(True)
plt.legend()

plt.show()


# =====================================
# SUHU
# =====================================

x_suhu = np.arange(15, 41, 1)

dingin = fuzz.trapmf(x_suhu, [15,15,18,24])
sedang = fuzz.trimf(x_suhu, [22,27,32])
panas = fuzz.trapmf(x_suhu, [30,35,40,40])

plt.figure(figsize=(8,4))
plt.plot(x_suhu, dingin, label='Dingin')
plt.plot(x_suhu, sedang, label='Sedang')
plt.plot(x_suhu, panas, label='Panas')

plt.title("Membership Function Suhu")
plt.xlabel("Suhu (°C)")
plt.ylabel("Derajat Keanggotaan")
plt.xlim(15,40)
plt.ylim(-0.05,1.05)
plt.grid(True)
plt.legend()

plt.show()


# =====================================
# LAMA PENYIRAMAN
# =====================================

x_penyiraman = np.arange(0,31,1)

sebentar = fuzz.trapmf(x_penyiraman,[0,0,5,10])
sedang = fuzz.trimf(x_penyiraman,[8,15,22])
lama = fuzz.trapmf(x_penyiraman,[20,25,30,30])

plt.figure(figsize=(8,4))
plt.plot(x_penyiraman, sebentar, label='Sebentar')
plt.plot(x_penyiraman, sedang, label='Sedang')
plt.plot(x_penyiraman, lama, label='Lama')

plt.title("Membership Function Lama Penyiraman")
plt.xlabel("Waktu (menit)")
plt.ylabel("Derajat Keanggotaan")
plt.xlim(0,30)
plt.ylim(-0.05,1.05)
plt.grid(True)
plt.legend()

plt.show()