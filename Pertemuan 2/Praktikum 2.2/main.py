from inference import DiagnosaPadi
from facts import Padi

engine = DiagnosaPadi()

engine.reset()

engine.declare(Padi(daun="menguning"))
engine.declare(Padi(tanaman="kerdil"))

engine.run()