import matplotlib.pyplot as plt

from inference import simulasi
from membership import harga


print('=' * 45)
print('SISTEM FUZZY PENENTUAN HARGA RUMAH')
print('=' * 45)

luas_input = float(input('Luas bangunan (30-300 m2): '))
lokasi_input = float(input('Nilai lokasi (0-100): '))
umur_input = float(input('Umur bangunan (0-40 tahun): '))

simulasi.input['luas_bangunan'] = luas_input
simulasi.input['lokasi'] = lokasi_input
simulasi.input['umur_bangunan'] = umur_input
simulasi.compute()

hasil = simulasi.output['harga']

#100    200
#30     50
#40     10
print('\n' + '=' * 45)
print('HASIL')
print('=' * 45)
print(f'Luas bangunan : {luas_input:.1f} m2')
print(f'Lokasi        : {lokasi_input:.1f}')
print(f'Umur bangunan : {umur_input:.1f} tahun')
print(f'Harga rumah   : {hasil:.2f} juta rupiah')

harga.view(sim=simulasi)
plt.show()
