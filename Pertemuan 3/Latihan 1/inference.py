from skfuzzy import control as ctrl
from rules import rules


sistem = ctrl.ControlSystem(rules)
simulasi = ctrl.ControlSystemSimulation(sistem)
