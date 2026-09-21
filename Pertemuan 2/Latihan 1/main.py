from inference import DiagnosaPenyakit
from facts import Penyakit

engine = DiagnosaPenyakit()
engine.reset()

engine.declare(Penyakit(suhu="demam", cf=0.8))
engine.declare(Penyakit(otot="nyeri", cf=0.9))
engine.declare(Penyakit(kepala="sakit", cf=0.85))

# Jalankan inferensi
engine.run()
