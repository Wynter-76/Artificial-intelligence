from experta import Rule, MATCH
from facts import Penyakit

class PenyakitRules:

    # R1
    @Rule(
        Penyakit(suhu="demam", cf=MATCH.cf_demam),
        Penyakit(batuk="ada", cf=MATCH.cf_batuk),
        Penyakit(hidung="pilek", cf=MATCH.cf_pilek),
        Penyakit(tenggorokan="sakit", cf=MATCH.cf_tenggorokan)
    )
    def influenza(self, cf_demam, cf_batuk, cf_pilek, cf_tenggorokan):
        cf_rule = 0.90
        cf_evidence = min(cf_demam, cf_batuk, cf_pilek, cf_tenggorokan)
        cf = cf_evidence * cf_rule

        print("\nDiagnosa : Influenza")
        print(f"CF = {cf:.3f}")
        print(f"Tingkat Keyakinan = {cf*100:.2f}%")

    # R2
    @Rule(
        Penyakit(suhu="demam", cf=MATCH.cf_demam),
        Penyakit(mual="ada", cf=MATCH.cf_mual),
        Penyakit(perut="nyeri", cf=MATCH.cf_nyeri_perut),
        Penyakit(bab="diare", cf=MATCH.cf_diare)
    )
    def tifus(self, cf_demam, cf_mual, cf_nyeri_perut, cf_diare):
        cf_rule = 0.92
        cf_evidence = min(cf_demam, cf_mual, cf_nyeri_perut, cf_diare)
        cf = cf_evidence * cf_rule

        print("\nDiagnosa : Tifus")
        print(f"CF = {cf:.3f}")
        print(f"Tingkat Keyakinan = {cf*100:.2f}%")

    # R3
    @Rule(
        Penyakit(suhu="demam", cf=MATCH.cf_demam),
        Penyakit(otot="nyeri", cf=MATCH.cf_otot),
        Penyakit(kepala="sakit", cf=MATCH.cf_kepala)
    )
    def dbd(self, cf_demam, cf_otot, cf_kepala):
        cf_rule = 0.95
        cf_evidence = min(cf_demam, cf_otot, cf_kepala)
        cf = cf_evidence * cf_rule

        print("\nDiagnosa : Demam Berdarah (DBD)")
        print(f"CF = {cf:.3f}")
        print(f"Tingkat Keyakinan = {cf*100:.2f}%")

    # R4
    @Rule(
        Penyakit(mual="ada", cf=MATCH.cf_mual),
        Penyakit(nafsu_makan="turun", cf=MATCH.cf_nafsu_makan),
        Penyakit(ulu_hati="nyeri", cf=MATCH.cf_ulu_hati)
    )
    def maag(self, cf_mual, cf_nafsu_makan, cf_ulu_hati):
        cf_rule = 0.88
        cf_evidence = min(cf_mual, cf_nafsu_makan, cf_ulu_hati)
        cf = cf_evidence * cf_rule

        print("\nDiagnosa : Gastritis (Maag)")
        print(f"CF = {cf:.3f}")
        print(f"Tingkat Keyakinan = {cf*100:.2f}%")

    # R5
    @Rule(
        Penyakit(kepala="sakit", cf=MATCH.cf_kepala),
        Penyakit(ulu_hati="nyeri", cf=MATCH.cf_ulu_hati)
    )
    def migrain(self, cf_kepala, cf_ulu_hati):
        cf_rule = 0.85
        cf_evidence = min(cf_kepala, cf_ulu_hati)
        cf = cf_evidence * cf_rule

        print("\nDiagnosa : Migrain")
        print(f"CF = {cf:.3f}")
        print(f"Tingkat Keyakinan = {cf*100:.2f}%")
