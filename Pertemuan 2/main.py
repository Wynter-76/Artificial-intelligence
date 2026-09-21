from inference import DiagnosaLaptop
from facts import Laptop

engine = DiagnosaLaptop()

engine.reset()

engine.declare(Laptop(lambat="ya"))
engine.declare(Laptop(hdd="bunyi"))

engine.run()