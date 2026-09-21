from inference import DiagnosaMental
from facts import Mental

engine = DiagnosaMental()
engine.reset()


engine.declare(Mental(tidur="tidak", cf=0.8))
engine.declare(Mental(cemas="tidak", cf=0.9))
engine.declare(Mental(perasaan="tidak", cf=0.85))
engine.declare(Mental(minat="tidak", cf=0.85))
engine.declare(Mental(fisik="tidak", cf=0.85))

# Jalankan inferensi
engine.run()
