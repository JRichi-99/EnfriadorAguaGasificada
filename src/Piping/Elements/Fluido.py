import CoolProp.CoolProp as cp

class Fluido():
    def __init__(self):
        self.T = None
        self.kelvin_T = None
        self.P = None
        self.mu = None
        self.ht_k = None
        self.ht_pr = None
        self.fluido = None
        
    def set_conditions(self, T, P, fluido, coolprop=True, **kwargs):
        self.T = T
        self.P = P
        self.kelvin_T = T + 273.15
        self.fluido = fluido

        if coolprop:
            self.rho = cp.PropsSI('D', 'T', self.kelvin_T, 'P', P, fluido)
            self.mu = cp.PropsSI('V', 'T', self.kelvin_T, 'P', P, fluido)
            self.ht_pr = cp.PropsSI('Prandtl', 'T', self.kelvin_T, 'P', P, fluido)
            self.ht_k = cp.PropsSI('L', 'T', self.kelvin_T, 'P', P, fluido)
        
        else:
            self.rho = kwargs.get('rho')
            self.mu = kwargs.get('mu')
            self.ht_pr = kwargs.get('pr')
            self.ht_k = kwargs.get('k')
    

        
            


    
        
