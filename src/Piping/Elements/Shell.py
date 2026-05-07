import numpy as np
from Elements.Tube import Tube
from Elements.Coil import Coil

class Shell(Tube):
    def __init__(self, d_in, d_out, lenght, orientation, material, contain : Coil):
        super().__init__(d_in, d_out, lenght, orientation, material)
        self.contain = contain

        self.vol_in_free = self.vol_in - self.contain.vol_out
        self.weet_area = self.area_in + self.contain.area_out 
        self.d_hidraulico = 4*self.vol_in_free/self.weet_area
        
        self.vol_porosity = self.vol_in_free/self.vol_in
        self.area_seccion_in = self.vol_porosity*np.pi*self.d_in**2/4
    
        self.re_crit = 100 

    def set_reynolds(self, rho, mu):
        self.re = self.u*rho*self.d_hidraulico/mu
        self.check_regimen()
        return
        

    

    
    
     
