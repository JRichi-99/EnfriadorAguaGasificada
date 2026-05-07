import numpy as np
from Elements.Tube import Tube

class Coil(Tube):
    def __init__(self, d_in, d_out, lenght, orientation, material, vueltas, pitch):
        super().__init__(d_in, d_out, lenght, orientation, material)

        self.vueltas = vueltas
        self.av_d = lenght/vueltas/np.pi
        self.pitch = pitch
        self.projected_d = np.sqrt(self.av_d**2-(self.pitch/np.pi)**2)
        self.curvature_d = self.projected_d*(1+(self.pitch/(np.pi*self.projected_d))**2)

        self.projected_d_out = self.projected_d + self.d_out
        self.altura = self.pitch * vueltas
        
        self.re_crit = 2300 * (1 + 8.6 * (self.d_in / self.curvature_d)**0.45)

        # Transferencia de calor
        self.ht_nu = None
        self.ht_h = None
    
    def set_friction_factor(self):
        re = self.re
        if re < self.re_crit and re > 1:
            self.friction_factor = (64 / re) * (1 + 0.033 * (np.log10(re * np.sqrt(self.d_in/ self.curvature_d)))**4)
        elif re >= self.re_crit and re < 1e5:
            self.friction_factor = (0.3164 / re**0.25) * (1 + 0.095 * (self.d_in / self.curvature_d)**0.5 * re**0.25)
        else:
            # pag 732 VDI
            self.friction_factor = (0.3164/self.re**0.25+0.03*np.sqrt(self.d_in/self.curvature_d))
        return self.friction_factor

    def set_perdida_altura(self):
        self.perdida_alt_friccion = self.friction_factor * (self.lenght / self.d_in) * (self.u**2 / (2 * 9.81))
        self.perdida_alt_altura = np.sin(np.deg2rad(self.orientation)) * self.altura
        self.perdida_alt = self.perdida_alt_altura + self.perdida_alt_friccion
        return self.perdida_alt
    
    def get_Nu_laminar(self, pr, prw, re):
        m = 0.5 + 0.2903 * (self.d_in / self.curvature_d)**0.194
        term_curvatura = 1 + 0.8 * (self.d_in / self.curvature_d)**0.9
        return 3.66 + 0.08 * term_curvatura * re**m * pr**(1/3) * (pr / prw)**0.14

    def get_Nu_turb(self, pr, prw, mu, muw, re):
        friccion_factor = (0.3164/re**0.25+0.03*np.sqrt(self.d_in/self.curvature_d))*(muw/mu)**0.27
        return ((friccion_factor/8*re*pr)/(1+12.7*np.sqrt(friccion_factor/8)*(pr**(2/3)-1))) * (pr / prw)**0.14

    def set_Nu(self, pr, prw, mu, muw):
        if self.re <= self.re_crit:
            self.ht_nu = self.get_Nu_laminar(pr,prw, self.re)
        elif self.re > 2.2e4:
            self.ht_nu = self.get_Nu_turb(pr,prw,mu,muw, self.re)
        else:
            gamma = (2.2e4 - self.re)/(2.2e4 - self.re_crit)
            self.ht_nu = gamma*self.get_Nu_laminar(pr,prw,self.re_crit) + (1-gamma)*self.get_Nu_turb(pr,prw,mu,muw, 2.2e4)
        return self.nu
    
    def set_convection_h(self, k):
        self.ht_h = self.ht_nu * k / self.d_in
        return self.ht_h
        
    

            

            
        
    
            
    