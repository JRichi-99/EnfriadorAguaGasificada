import numpy as np

class Pump():
    def __init__(self, pressure_caudal_func):
        self.f = pressure_caudal_func
    
    