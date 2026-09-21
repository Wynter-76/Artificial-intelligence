import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


# Variabel input dan output
suhu_ruangan = ctrl.Antecedent(np.arange(18, 41, 1), 'suhu_ruangan')
jumlah_orang = ctrl.Antecedent(np.arange(0, 21, 1), 'jumlah_orang')
kelembapan = ctrl.Antecedent(np.arange(20, 101, 1), 'kelembapan')
suhu_ac = ctrl.Consequent(np.arange(18, 29, 1), 'suhu_ac')


# Fungsi membership suhu ruangan
suhu_ruangan['dingin'] = fuzz.trimf(suhu_ruangan.universe, [18, 18, 24])
suhu_ruangan['normal'] = fuzz.trimf(suhu_ruangan.universe, [22, 26, 30])
suhu_ruangan['panas'] = fuzz.trimf(suhu_ruangan.universe, [28, 40, 40])

# Fungsi membership jumlah orang
jumlah_orang['sedikit'] = fuzz.trimf(jumlah_orang.universe, [0, 0, 7])
jumlah_orang['sedang'] = fuzz.trimf(jumlah_orang.universe, [5, 9.5, 14])
jumlah_orang['banyak'] = fuzz.trimf(jumlah_orang.universe, [12, 20, 20])

# Fungsi membership kelembapan
kelembapan['rendah'] = fuzz.trimf(kelembapan.universe, [20, 20, 45])
kelembapan['sedang'] = fuzz.trimf(kelembapan.universe, [40, 55, 70])
kelembapan['tinggi'] = fuzz.trimf(kelembapan.universe, [65, 100, 100])

# Fungsi membership suhu AC
suhu_ac['dingin'] = fuzz.trimf(suhu_ac.universe, [18, 18, 22])
suhu_ac['sedang'] = fuzz.trimf(suhu_ac.universe, [21, 23, 25])
suhu_ac['hangat'] = fuzz.trimf(suhu_ac.universe, [24, 28, 28])
