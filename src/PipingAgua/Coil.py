import numpy as np
import CoolProp.CoolProp as cp
import fluids as fl

class Coil:
    def __init__(self, length, d_out, d_in, vueltas, pitch, T, P, Tw, material="Propileno"): 
        # Atributos de geometría básica
        self.l = length
        self.h = pitch
        self.d_out = d_out
        self.d_in = d_in
        self.n = vueltas
        self.material = material
        self.Tw = Tw
        
        # Cálculo de dimensiones derivadas
        size_data = self.calc_size(length, d_out, d_in, vueltas, pitch)
        (self.ds, self.dc, self.d, self.d_total, 
         self.h_total, self.volumen_contenido, 
         self.thickness, self.volumen_ocupado_box, self.volumen_ocupado
         ) = size_data

        # Propiedades del fluido iniciales
        self.recalc_fluid(T, P)

    def calc_size(self, length, d_out, d_in, vueltas, pitch):
        """Calcula las dimensiones geométricas derivadas de la bobina."""
        ds = length / vueltas / np.pi
        dc = np.sqrt(ds**2 - (pitch / np.pi)**2)
        d = dc * (1 + (pitch / np.pi / dc)**2)
        
        d_total = dc + d_out
        h_total = pitch * vueltas
        volumen_ocupado_box = np.pi * d_total**2/4 * h_total
        volumen_ocupado = np.pi * d_out**2/4 *length
        volumen_contenido = np.pi * (d_in / 2)**2 * length
        thickness = (d_out - d_in) / 2
        
        return ds, dc, d, d_total, h_total, volumen_contenido, thickness, volumen_ocupado_box, volumen_ocupado

    def recalc_fluid(self, T, P):
        """Actualiza las propiedades termofísicas del fluido."""
        self.T = T
        self.P = P
        self.mu = cp.PropsSI('V', 'T', T, 'P', P, 'Water') 
        self.rho = cp.PropsSI('D', 'T', T, 'P', P, 'Water') 

    def get_Re(self, Q):
        """Calcula el número de Reynolds para un caudal Q dado."""
        v = Q / (np.pi * self.d_in**2 / 4)
        return self.rho * v * self.d_in / self.mu

    def reynolds_critico(self):
        """Calcula el Reynolds crítico considerando la curvatura."""
        return 2300 * (1 + 8.6 * (self.d_in / self.d)**0.45)
    
    def velocidad_critica(self):
        """Velocidad de transición basada en Re crítico."""
        return self.reynolds_critico() * self.mu / (self.rho * self.d_in)
    
    def flujo_volumetrico_critico(self):
        """Caudal límite para régimen laminar."""
        area = np.pi * self.d_in**2 / 4
        return self.velocidad_critica() * area
    
    def friction_coefficient(self, Re):
        """Calcula el coeficiente de arrastre para flujo laminar."""
        
    
    def pressure_drop(self, Q):
        """Calcula la caída de presión para un caudal Q dado."""
        cp.friction_factor(Re)
        
        Cd = self.drag_coefficient(Re)
        A = np.pi * self.d_in**2 / 4
        v = Q / A
        return Cd * (self.rho * v**2 / 2) * (self.l / self.d_in)

    def Nu_interno(self, Re):
        """Calcula el número de Nusselt interno y sus márgenes de error."""
        if Re >= self.reynolds_critico():
            return "Flujo turbulento: No se puede aplicar la correlación para flujo laminar."
        
        # Parámetros de la correlación
        m = 0.5 + 0.2903 * (self.d_in / self.d)**0.194
        Pr = cp.PropsSI('Pr', 'T', self.T, 'P', self.P, 'Water')
        Prw = cp.PropsSI('Pr', 'T', self.Tw, 'P', self.P, 'Water')
        
        # Cálculo de Nusselt
        term_curvatura = 1 + 0.8 * (self.d_in / self.d)**0.9
        Nu = 3.66 + 0.08 * term_curvatura * Re**m * Pr**(1/3) * (Pr / Prw)**0.14
        
        return Nu, Nu * 0.85, Nu * 1.15