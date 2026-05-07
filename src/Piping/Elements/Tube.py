import numpy as np
import fluids as fl
import ht

class Tube:
    def __init__(self, d_in, d_out, lenght, orientation, material):
        self.d_in = d_in
        self.d_out = d_out
        self.lenght = lenght
        self.orientation = orientation

        self.area_seccion_in = np.pi*d_in**2/4
        self.vol_in = self.area_seccion_in*lenght
        self.area_out = np.pi*d_out*lenght
        self.vol_out = np.pi*d_out**2/4
        self.area_in = np.pi*d_in*lenght
        self.thickness = (d_out-d_in)/2

        
        self.material = material
        self.roughness = fl.friction.material_roughness(material)*1e-3
        self.conductivity = ht.k_material(ht.nearest_material(material))

        self.re_crit = 2300

        self.caudal = None
        self.u = None
        self.re = None
        self.regime = None
        self.friction_factor = None

        self.perdida_alt_friccion = None
        self.perdida_alt_altura = None
        self.perdida_alt = None
    
    def set_velocidad(self, Q):
        self.u = Q/self.area_seccion_in
        return self.u

    def set_reynolds(self, rho, mu):
        self.re = self.u*rho*self.d_in/mu
        self.check_regimen()
        return

    def check_regimen(self):
        if self.re >= self.re_crit:
            self.regime = "turbulent"
        else:
            self.regime = "laminar"
        return self.re

    def set_friction_factor(self):
        self.friction_factor = fl.friction.friction_factor(self.re, self.roughness/(self.d_in))
        return self.friction_factor
    
    def set_caudal(self, Q, rho, mu):
        self.caudal = Q
        self.set_velocidad(Q)
        self.set_reynolds(rho, mu)
        self.set_friction_factor()
    
    def set_perdida_altura(self):
        self.perdida_alt_friccion = self.friction_factor * (self.lenght / self.d_in) * (self.u**2 / (2 * 9.81))
        self.perdida_alt_altura = np.sin(np.deg2rad(self.orientation)) * self.lenght
        self.perdida_alt = self.perdida_alt_altura + self.perdida_alt_friccion
        return self.perdida_alt
    
    def set_hidraulica(self, Q, rho, mu):
        self.set_caudal(Q, rho, mu)
        self.set_perdida_altura()
    



        
    

