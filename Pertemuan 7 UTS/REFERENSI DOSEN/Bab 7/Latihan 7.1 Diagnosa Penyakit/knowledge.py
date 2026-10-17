from experta import Rule, MATCH
from facts import Pasien


# =====================================
# KNOWLEDGE BASE (MYCIN)
# =====================================

class PenyakitRules:

    # -----------------------------
    # R1 : Influenza
    # CF Rule = 0.90
    # -----------------------------
    @Rule(
        Pasien(demam="ya", cf=MATCH.cf_demam),
        Pasien(batuk="ya", cf=MATCH.cf_batuk),
        Pasien(pilek="ya", cf=MATCH.cf_pilek),
        Pasien(tenggorokan="sakit", cf=MATCH.cf_tenggorokan)
    )
    def influenza(self, cf_demam, cf_batuk, cf_pilek, cf_tenggorokan):

        cf_rule = 0.90

        cf_evidence = min(cf_demam, cf_batuk, cf_pilek, cf_tenggorokan)

        cf = cf_evidence * cf_rule

        self.hasil.append({
            "penyakit": "Influenza",
            "cf": cf,
            "keyakinan": cf * 100
        })

    # -----------------------------
    # R2 : Tifus
    # CF Rule = 0.92
    # -----------------------------
    @Rule(
        Pasien(demam="ya", cf=MATCH.cf_demam),
        Pasien(mual="ya", cf=MATCH.cf_mual),
        Pasien(nyeri_perut="ya", cf=MATCH.cf_perut),
        Pasien(nafsu_makan="turun", cf=MATCH.cf_nafsu)
    )
    def tifus(self, cf_demam, cf_mual, cf_perut, cf_nafsu):

        cf_rule = 0.92

        cf_evidence = min(cf_demam, cf_mual, cf_perut, cf_nafsu)

        cf = cf_evidence * cf_rule

        self.hasil.append({
            "penyakit": "Tifus",
            "cf": cf,
            "keyakinan": cf * 100
        })

    # -----------------------------
    # R3 : Demam Berdarah
    # CF Rule = 0.95
    # -----------------------------
    @Rule(
        Pasien(demam="ya", cf=MATCH.cf_demam),
        Pasien(nyeri_otot="ya", cf=MATCH.cf_otot),
        Pasien(sakit_kepala="ya", cf=MATCH.cf_kepala)
    )
    def dbd(self, cf_demam, cf_otot, cf_kepala):

        cf_rule = 0.95

        cf_evidence = min(cf_demam, cf_otot, cf_kepala)

        cf = cf_evidence * cf_rule

        self.hasil.append({
            "penyakit": "Demam Berdarah",
            "cf": cf,
            "keyakinan": cf * 100
        })

    # -----------------------------
    # R4 : Gastritis
    # CF Rule = 0.88
    # -----------------------------
    @Rule(
        Pasien(mual="ya", cf=MATCH.cf_mual),
        Pasien(nyeri_ulu_hati="ya", cf=MATCH.cf_ulu),
        Pasien(muntah="ya", cf=MATCH.cf_muntah)
    )
    def gastritis(self, cf_mual, cf_ulu, cf_muntah):

        cf_rule = 0.88

        cf_evidence = min(cf_mual, cf_ulu, cf_muntah)

        cf = cf_evidence * cf_rule

        self.hasil.append({
            "penyakit": "Gastritis",
            "cf": cf,
            "keyakinan": cf * 100
        })

    # -----------------------------
    # R5 : Migrain
    # CF Rule = 0.85
    # -----------------------------
    @Rule(
        Pasien(sakit_kepala="ya", cf=MATCH.cf_kepala),
        Pasien(muntah="ya", cf=MATCH.cf_muntah)
    )
    def migrain(self, cf_kepala, cf_muntah):

        cf_rule = 0.85

        cf_evidence = min(cf_kepala, cf_muntah)

        cf = cf_evidence * cf_rule

        self.hasil.append({
            "penyakit": "Migrain",
            "cf": cf,
            "keyakinan": cf * 100
        })