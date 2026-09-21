import matplotlib.pyplot as plt

from inference import simulasi
from membership import suhu_ac


print('=' * 45)
print('SISTEM FUZZY PENGATURAN SUHU AC OTOMATIS')
print('=' * 45)

suhu_input = float(input('Suhu ruangan (18-40 C): '))
orang_input = float(input('Jumlah orang (0-20): '))
kelembapan_input = float(input('Kelembapan ruangan (20-100%): '))

simulasi.input['suhu_ruangan'] = suhu_input
simulasi.input['jumlah_orang'] = orang_input
simulasi.input['kelembapan'] = kelembapan_input
simulasi.compute()

hasil = simulasi.output['suhu_ac']


#20     30
#7      20
#30     70

print('\n' + '=' * 45)
print('HASIL')
print('=' * 45)
print(f'Suhu ruangan : {suhu_input:.1f} C')
print(f'Jumlah orang : {orang_input:.1f}')
print(f'Kelembapan   : {kelembapan_input:.1f}%')
print(f'Suhu AC      : {hasil:.2f} C')

suhu_ac.view(sim=simulasi)
plt.show()
