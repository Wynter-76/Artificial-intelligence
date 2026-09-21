from experta import Rule, MATCH
from facts import Padi

class PadiRules:

    # R1
    @Rule(
        Padi(daun="menguning", cf=MATCH.cf_daun),
        Padi(tanaman="kerdil", cf=MATCH.cf_tanaman)
    )
    def nitrogen(self, cf_daun, cf_tanaman):
        cf_rule = 0.90
        cf_evidence = min(cf_daun, cf_tanaman)
        cf = cf_evidence * cf_rule

        print("\nDiagnosa : Kekurangan Nitrogen")
        print(f"CF = {cf:.3f}")
        print(f"Tingkat Keyakinan = {cf*100:.2f}%")

    # R2
    @Rule(
        Padi(daun="bercak_coklat", cf=MATCH.cf_daun),
        Padi(ujung_daun="mengering", cf=MATCH.cf_ujung)
    )
    def hawar(self, cf_daun, cf_ujung):
        cf_rule = 0.85
        cf_evidence = min(cf_daun, cf_ujung)
        cf = cf_evidence * cf_rule

        print("\nDiagnosa : Hawar Daun Bakteri")
        print(f"CF = {cf:.3f}")
        print(f"Tingkat Keyakinan = {cf*100:.2f}%")

    # R3
    @Rule(
        Padi(daun="menggulung", cf=MATCH.cf_daun),
        Padi(ulat="ada", cf=MATCH.cf_ulat)
    )
    def ulat(self, cf_daun, cf_ulat):
        cf_rule = 0.95
        cf_evidence = min(cf_daun, cf_ulat)
        cf = cf_evidence * cf_rule

        print("\nDiagnosa : Serangan Ulat Daun")
        print(f"CF = {cf:.3f}")
        print(f"Tingkat Keyakinan = {cf*100:.2f}%")

    # R4
    @Rule(
        Padi(daun="layu", cf=MATCH.cf_daun),
        Padi(akar="busuk", cf=MATCH.cf_akar)
    )
    def akar(self, cf_daun, cf_akar):
        cf_rule = 0.90
        cf_evidence = min(cf_daun, cf_akar)
        cf = cf_evidence * cf_rule

        print("\nDiagnosa : Busuk Akar")
        print(f"CF = {cf:.3f}")
        print(f"Tingkat Keyakinan = {cf*100:.2f}%")

    # R5
    @Rule(
        Padi(batang="busuk", cf=MATCH.cf_batang),
        Padi(bulir="hampa", cf=MATCH.cf_bulir)
    )
    def batang(self, cf_batang, cf_bulir):
        cf_rule = 0.92
        cf_evidence = min(cf_batang, cf_bulir)
        cf = cf_evidence * cf_rule

        print("\nDiagnosa : Busuk Batang")
        print(f"CF = {cf:.3f}")
        print(f"Tingkat Keyakinan = {cf*100:.2f}%")