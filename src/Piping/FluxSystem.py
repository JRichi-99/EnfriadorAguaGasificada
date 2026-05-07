from Elements.Coil import Coil
from Elements.Shell import Shell
from Elements.Singularities import SingularityLoss
from Elements.Tube import Tube
from Pumps.Lauda.LaudaPumpFit import Pa4m3s
from scipy.optimize import newton

class FluxSystem():
    def __init__(self):
        self.n_elements = 0
        self.system = []
        self.tubes = []
        self.singularities = []
        self.pressures = []
        self.perdida_altura = []
    
    def add_element(self, element):
        self.system.append(element)
        if isinstance(element, Tube):
            self.tubes.append((element, self.n_elements))
        elif isinstance(element, SingularityLoss):
            self.singularities.append((element, self.n_elements))
        self.n_elements += 1

    def add_coil(self, element: Coil):
        self.add_element(element)
        
    def add_shell(self, element: Shell):
        self.add_element(element)
    
    def add_tube(self, element: Tube):
        self.add_element(element)
    
    def add_singularity_loss(self, element: SingularityLoss):
        self.add_element(element)

    def conect(self):
        for i, element in enumerate(self.system):
            if i == 0 or i == self.n_elements-1:
                continue
            if isinstance(element, SingularityLoss):
                element.set_in_out(self.system[i-1], self.system[i+1])

    # Funcion deprecada
    def set_caudal(self, Q, rho, mu, P0):
        self.perdida_altura = [None] * self.n_elements
        self.pressures = [None] * (self.n_elements + 1)
        self.pressures[0] = P0
        for i , element_id in enumerate(self.tubes):
            element, id = element_id
            element.set_hidraulica(Q, rho, mu)
            dh = element.perdida_alt
            self.perdida_altura[id] = dh
                
        for i , element_id in enumerate(self.singularities):
            element, id = element_id
            dh = element.set_perdida_altura()
            self.perdida_altura[id] = dh
        dh = sum(self.perdida_altura)

        for i in range(self.n_elements):
            self.pressures[i+1] = self.pressures[i]-self.system[i].perdida_alt*rho*9.81

        return dh, self.pressures

    def get_perdida_altura_closed(self, Q, rho, mu):
        dh = 0
        for i , element_id in enumerate(self.tubes):
            element, id = element_id
            element.set_hidraulica(Q, rho, mu)
            dh += element.perdida_alt
                
        for i , element_id in enumerate(self.singularities):
            element, id = element_id
            dh += element.set_perdida_altura()

        return dh, dh*rho*9.81
    
    def get_perdida_altura_open(self, Q, rho, mu, P0, P1):
        dh, dp = self.get_perdida_altura_closed(Q,rho,mu)
        dh = (P1-P0)/rho/9.81  + (self.system[0].u**2-self.system[-1].u**2)/2/9.81 + dh
        return dh, dh*rho*9.81


    def cross_system_pump(self, rho, mu, pump_f, Q_guess, verbose=False, open = False , P0 = 101325, P1 = 101325):
        def cross_dp(Q):
            Q_eval = abs(Q)
            if not open:
                dh, dp_sys = self.get_perdida_altura_closed(Q_eval, rho, mu)
            if open:
                dh, dp_sys = self.get_perdida_altura_open(Q_eval, rho, mu, P0, P1)
            dp_pump = pump_f(Q_eval) 
            return dp_pump - dp_sys

        Q_guess = 3.25e-5
        
        try:
            Q_op = newton(func=cross_dp, x0=Q_guess, maxiter=500)
            Q_op = abs(Q_op)
            
            Q_op_lmin = Q_op * 60000
            dp_op = pump_f(Q_op)
            dh_op = dp_op/rho/9.81

            if verbose:
                print("\n" + "═" * 45)
                print(" 🎯 PUNTO DE OPERACIÓN DEL SISTEMA ".center(45, " "))
                print("═" * 45)
                print(f" 🔹 Caudal volumétrico : {Q_op_lmin:>8.3f} L/min")
                print(f" 🔹 Caudal másico      : {Q_op:>8.2e} m³/s")
                print(f" 🔹 Presión de cruce   : {dp_op:>8.1f} Pa")
                print(f" 🔹 Pérdida de altura  : {dh_op:>8.3f} m.c.a.")
                print("═" * 45 + "\n")

            return Q_op, Q_op_lmin, dp_op, dh_op

        except RuntimeError:
            if verbose:
                print("\n[ERROR] El solver no pudo converger.\n")
            return None, None, None, None



            
            
            
        
        
            


    

    

        