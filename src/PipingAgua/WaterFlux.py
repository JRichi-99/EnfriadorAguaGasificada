import numpy as np
import CoolProp.CoolProp as cp 
from Coil import Coil

class Bomba:
    def __init__(self, Q_dp : function):
        self.Q_dp = Q_dp

class Botella:
    def __init__(self, Ti, hi):
        self.T = Ti
        self.h = hi

    def get_Re(self, Q):
        # Área transversal = np.pi * self.d_in**2 / 4
        v = Q / (np.pi * self.d_in**2 / 4)
        return self.rho * v * self.d_in / self.mu

    def reynolds_critico(self):
        return 2300 * (1 + 8.6 * (self.d_in / self.d)**0.45)
    
    def recalc_fluid(self, T, P):
        self.T = T
        self.P = P
        self.mu = cp.PropsSI('V', 'T', T, 'P', P, 'Water') 
        self.rho = cp.PropsSI('D', 'T', T, 'P', P, 'Water') 

    def velocidad_critica(self):
        # Despejando v de Re = rho * v * D / mu  --->  v = Re * mu / (rho * D)
        return self.reynolds_critico() * self.mu / (self.rho * self.d_in)
    
    def flujo_volumetrico_critico(self):
        area = np.pi * self.d_in**2 / 4
        return self.velocidad_critica() * area
    
    def Nu_interno(self, Re):
        m = 0.5 + 0.2903 * (self.d_in / self.d)**0.194
        Pr = cp.PropsSI('Pr', 'T', self.T, 'P', self.P, 'Water')
        Prw = cp.PropsSI('Pr', 'T', self.Tw, 'P', self.P, 'Water')
        Nu = 3.66 + 0.08 * (1 + 0.8 * (self.d_in / self.d)**0.9) * Re**m * Pr**(1/3) * (Pr / Prw)**0.14
        
        return Nu, Nu * 0.85, Nu * 1.15


class SystemWaterFlux:
    def __init__(self, bomba : Bomba, botella : Botella, coil: Coil, tramos: dict):
        self.bomba = bomba
        self.botella = botella
        self.coil = coil
        self.tramos = tramos
    
    def calcular_flujo(self, ):

        