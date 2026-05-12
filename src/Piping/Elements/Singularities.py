class SingularityLoss():
    def __init__(self, factor_k):
        self.factor_k = factor_k

        self.in_conection = None
        self.out_conection = None
        self.perdida_alt = None
        self.regime = None
    
    def set_in_out(self, in_conection, out_conection):
        self.in_conection = in_conection
        self.out_conection = out_conection

    def set_perdida_altura(self):
        u_in = self.in_conection.u 
        u_out = self.out_conection.u
        u = u_in if u_in > u_out else u_out
        self.perdida_alt= self.factor_k * u**2/ (2*9.81)
        return self.perdida_alt
    

    

    

        