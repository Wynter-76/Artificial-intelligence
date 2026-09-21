from inference import DiagnosaLaptop 
from facts import Laptop 
 
engine = DiagnosaLaptop() 
engine.reset() 
 
# ========================== 
# Input Gejala + CF User 
# ========================== 
 
engine.declare(Laptop(power="hidup",cf=0.8))        
# Tingkat keyakinan user terhadap gejala power mati 
engine.declare(Laptop(overheat="ya",cf=0.6))      
# Tingkat keyakinan user terhadap gejala charger hidup 
 
# Jalankan inferensi 
engine.run()