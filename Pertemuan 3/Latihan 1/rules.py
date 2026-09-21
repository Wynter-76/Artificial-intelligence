from skfuzzy import control as ctrl
from membership import luas_bangunan, lokasi, umur_bangunan, harga


rules = [
    ctrl.Rule(luas_bangunan['besar'] & lokasi['sangat'] & umur_bangunan['baru'], harga['mahal']),
    ctrl.Rule(luas_bangunan['besar'] & lokasi['strategis'] & umur_bangunan['baru'], harga['mahal']),
    ctrl.Rule(luas_bangunan['besar'] & lokasi['strategis'] & umur_bangunan['sedang'], harga['mahal']),
    ctrl.Rule(luas_bangunan['sedang'] & lokasi['sangat'] & umur_bangunan['baru'], harga['mahal']),
    ctrl.Rule(luas_bangunan['sedang'] & lokasi['strategis'] & umur_bangunan['sedang'], harga['sedang']),
    ctrl.Rule(luas_bangunan['sedang'] & lokasi['kurang'] & umur_bangunan['tua'], harga['murah']),
    ctrl.Rule(luas_bangunan['kecil'] & lokasi['sangat'] & umur_bangunan['baru'], harga['sedang']),
    ctrl.Rule(luas_bangunan['kecil'] & lokasi['strategis'] & umur_bangunan['sedang'], harga['murah']),
    ctrl.Rule(luas_bangunan['kecil'] & lokasi['kurang'] & umur_bangunan['tua'], harga['murah']),
]
