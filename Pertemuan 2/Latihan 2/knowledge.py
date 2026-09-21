from experta import Rule, MATCH
from facts import Mental

class MentalRules:

    # R1
    @Rule(
        Mental(tidur="sulit", cf=MATCH.cf_tidur),
        Mental(konsentrasi="sulit", cf=MATCH.cf_konsentrasi),
        Mental(fisik="lelah", cf=MATCH.cf_lelah),
        Mental(kondisi="kewalahan", cf=MATCH.cf_kewalahan)
    )
    def stabil(self, cf_tidur, cf_konsentrasi, cf_lelah, cf_kewalahan):
        cf_rule = 0.85
        cf_evidence = min(cf_tidur, cf_konsentrasi, cf_lelah, cf_kewalahan)
        cf = cf_evidence * cf_rule

        print("\nDiagnosa : Kondisi mental relatif stabil")
        print(f"CF = {cf:.3f}")
        print(f"Tingkat Keyakinan = {cf*100:.2f}%")

    # R2
    @Rule(
        Mental(tidur="sulit", cf=MATCH.cf_tidur),
        Mental(cemas="mudah", cf=MATCH.cf_cemas),
        Mental(fisik="lelah", cf=MATCH.cf_lelah),
        Mental(kondisi="kewalahan", cf=MATCH.cf_kewalahan)
    )
    def stres_ringan(self, cf_tidur, cf_cemas, cf_lelah, cf_kewalahan):
        cf_rule = 0.95
        cf_evidence = min(cf_tidur, cf_cemas, cf_lelah, cf_kewalahan)
        cf = cf_evidence * cf_rule

        print("\nDiagnosa : Indikasi stres ringan")
        print(f"CF = {cf:.3f}")
        print(f"Tingkat Keyakinan = {cf*100:.2f}%")

    # R3
    @Rule(
        Mental(cemas="mudah", cf=MATCH.cf_cemas),
        Mental(jantung="berdebar", cf=MATCH.cf_jantung),
        Mental(panik="mudah", cf=MATCH.cf_panik)
    )
    def stres_berat(self, cf_cemas, cf_jantung, cf_panik):
        cf_rule = 0.90
        cf_evidence = min(cf_cemas, cf_jantung, cf_panik)
        cf = cf_evidence * cf_rule

        print("\nDiagnosa : Indikasi stres berat")
        print(f"CF = {cf:.3f}")
        print(f"Tingkat Keyakinan = {cf*100:.2f}%")

    # R4
    @Rule(
        Mental(perasaan="sedih", cf=MATCH.cf_sedih),
        Mental(minat="hilang", cf=MATCH.cf_minat),
        Mental(motivasi="turun", cf=MATCH.cf_motivasi)
    )
    def gangguan_kecemasan(self, cf_sedih, cf_minat, cf_motivasi):
        cf_rule = 0.88
        cf_evidence = min(cf_sedih, cf_minat, cf_motivasi)
        cf = cf_evidence * cf_rule

        print("\nDiagnosa : Indikasi gangguan kecemasan")
        print(f"CF = {cf:.3f}")
        print(f"Tingkat Keyakinan = {cf*100:.2f}%")

    # R5 (Kondisi Negasi)
    @Rule(
        Mental(tidur="tidak", cf=MATCH.cf_tidur),
        Mental(cemas="tidak", cf=MATCH.cf_cemas),
        Mental(perasaan="tidak", cf=MATCH.cf_sedih),
        Mental(minat="tidak", cf=MATCH.cf_minat),
        Mental(fisik="tidak", cf=MATCH.cf_lelah)
    )
    def depresi_ringan(self, cf_tidur, cf_cemas, cf_sedih, cf_minat, cf_lelah):
        cf_rule = 1.00
        cf_evidence = min(cf_tidur, cf_cemas, cf_sedih, cf_minat, cf_lelah)
        cf = cf_evidence * cf_rule

        print("\nDiagnosa : Indikasi depresi ringan")
        print(f"CF = {cf:.3f}")
        print(f"Tingkat Keyakinan = {cf*100:.2f}%")
