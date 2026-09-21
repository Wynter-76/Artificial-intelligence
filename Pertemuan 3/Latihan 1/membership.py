import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


# Variabel input dan output
luas_bangunan = ctrl.Antecedent(np.arange(30, 301, 1), 'luas_bangunan')
lokasi = ctrl.Antecedent(np.arange(0, 101, 1), 'lokasi')
umur_bangunan = ctrl.Antecedent(np.arange(0, 41, 1), 'umur_bangunan')
harga = ctrl.Consequent(np.arange(100, 2001, 1), 'harga')


# Fungsi membership luas bangunan
luas_bangunan['kecil'] = fuzz.trimf(luas_bangunan.universe, [30, 30, 100])
luas_bangunan['sedang'] = fuzz.trimf(luas_bangunan.universe, [80, 150, 220])
luas_bangunan['besar'] = fuzz.trimf(luas_bangunan.universe, [180, 300, 300])

# Fungsi membership lokasi
lokasi['kurang'] = fuzz.trimf(lokasi.universe, [0, 0, 45])
lokasi['strategis'] = fuzz.trimf(lokasi.universe, [35, 60, 85])
lokasi['sangat'] = fuzz.trimf(lokasi.universe, [75, 100, 100])

# Fungsi membership umur bangunan
umur_bangunan['baru'] = fuzz.trimf(umur_bangunan.universe, [0, 0, 10])
umur_bangunan['sedang'] = fuzz.trimf(umur_bangunan.universe, [8, 18, 28])
umur_bangunan['tua'] = fuzz.trimf(umur_bangunan.universe, [25, 40, 40])

# Fungsi membership harga (juta rupiah)
harga['murah'] = fuzz.trimf(harga.universe, [100, 100, 700])
harga['sedang'] = fuzz.trimf(harga.universe, [600, 1000, 1400])
harga['mahal'] = fuzz.trimf(harga.universe, [1200, 2000, 2000])
