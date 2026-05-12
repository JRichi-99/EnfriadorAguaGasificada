import numpy as np
from Elements.Tube import Tube
from Elements.Coil import Coil
import fluids as fl

class Shell(Tube):
    def __init__(self, d_in, d_out, lenght, orientation, material, contain : Coil):
        super().__init__(d_in, d_out, lenght, orientation, material)
        self.contain = contain

        self.vol_in_free = self.vol_in - self.contain.vol_out
        self.wetted_area = self.area_in + self.contain.area_out 
        self.d_hidraulico = 4*self.vol_in_free/self.wetted_area
        
        self.vol_porosity = self.vol_in_free/self.vol_in
        self.area_seccion_in = self.vol_porosity*np.pi*self.d_in**2/4
    
        self.re_crit = 100 
        self.drag_factor = None
        self.ht_nu = None
        self.ht_h = None
    
    def add_mass(self, d_mass, h_mass):
        self.vol_in_free = self.vol_in_free - np.pi*(d_mass/2)**2*h_mass
        self.wetted_area = self.wetted_area + np.pi*d_mass*h_mass
        self.d_hidraulico = 4*self.vol_in_free/self.wetted_area
        self.vol_porosity = self.vol_in_free/self.vol_in
        self.area_seccion_in = self.vol_porosity*np.pi*self.d_in**2/4



    def set_reynolds(self, rho, mu):
        self.re = self.u*rho*self.d_hidraulico/mu
        self.check_regimen()
        return self.re
    
    def set_friction_factor(self):
        self.drag_factor = (0.3164 / self.re**0.25) * (1 + 0.095 * (self.d_in / self.contain.curvature_d)**0.5 * self.re**0.25)
        return self.drag_factor
    
    def set_perdida_altura(self):
        self.perdida_alt_friccion = self.drag_factor * (self.lenght / self.d_in) * (self.u**2 / (2 * 9.81))
        self.perdida_alt_altura = np.sin(np.deg2rad(self.orientation)) * self.lenght
        self.perdida_alt = self.perdida_alt_altura + self.perdida_alt_friccion
        return self.perdida_alt

    def set_Nu(self, pr, mu, mu_w):
        if self.re <= 6000 and self.re >= 50:
            self.ht_nu = 0.6*self.re**0.5*pr**0.31
        elif self.re > 6000 and self.re < 10000:
            self.ht_nu = 0.224*self.re**0.6*pr**0.33
        else:
            self.ht_nu = 0.36*self.re**0.55*pr**0.333*(mu/mu_w)**0.14
        return self.ht_nu
    
    def set_convection_h(self, k):
        self.ht_h = self.ht_nu * k / self.d_hidraulico
        return self.ht_h

    def get_ht(self, pr, mu, mu_w, k):
        self.set_Nu(pr,mu,mu_w)
        return self.set_convection_h(k)
    
    

    
    
     
