from skfuzzy import control as ctrl
from membership import suhu_ruangan, jumlah_orang, kelembapan, suhu_ac


rules = [
    ctrl.Rule(suhu_ruangan['panas'] & jumlah_orang['banyak'] & kelembapan['tinggi'], suhu_ac['dingin']),
    ctrl.Rule(suhu_ruangan['panas'] & jumlah_orang['sedang'] & kelembapan['tinggi'], suhu_ac['dingin']),
    ctrl.Rule(suhu_ruangan['panas'] & jumlah_orang['sedikit'] & kelembapan['sedang'], suhu_ac['sedang']),
    ctrl.Rule(suhu_ruangan['normal'] & jumlah_orang['banyak'] & kelembapan['tinggi'], suhu_ac['sedang']),
    ctrl.Rule(suhu_ruangan['normal'] & jumlah_orang['sedang'] & kelembapan['sedang'], suhu_ac['sedang']),
    ctrl.Rule(suhu_ruangan['normal'] & jumlah_orang['sedikit'] & kelembapan['rendah'], suhu_ac['hangat']),
    ctrl.Rule(suhu_ruangan['dingin'] & jumlah_orang['banyak'] & kelembapan['sedang'], suhu_ac['sedang']),
    ctrl.Rule(suhu_ruangan['dingin'] & jumlah_orang['sedang'] & kelembapan['rendah'], suhu_ac['hangat']),
    ctrl.Rule(suhu_ruangan['dingin'] & jumlah_orang['sedikit'] & kelembapan['rendah'], suhu_ac['hangat']),
]
