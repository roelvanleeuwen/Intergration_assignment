class Battolyser:
    def __init__(self, power: float, h2_capacity: float, h2_export_capacity: float, eff_bat: float, eff_electrlysis: float):
        self.power = power
        self.bat_capacity = power
        self.h2_capacity = h2_capacity
        self.eff_bat = eff_bat
        self.eff_electrolysis = eff_electrlysis
        self.h2_export_capacity = h2_export_capacity
        self.surface_area = 1000/14000

class Fuel_cell:
    def __init__(self, power: float, eff: float):
        self.power = power
        self.eff = eff

