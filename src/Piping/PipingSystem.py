from scipy.optimize import newton
from FluxSystem import FluxSystem


class PipingSystem(FluxSystem):
    def __init__(self):
        super().__init__()
        self.pressures = []
        self.perdida_altura = []
    
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
        
        try:
            Q_op = newton(func=cross_dp, x0=Q_guess, maxiter=500)
            Q_op = abs(Q_op)
            
            Q_op_lmin = Q_op * 60000
            dp_op = pump_f(Q_op)
            dh_op = dp_op/rho/9.81

            if verbose:
                print("\n" + "═" * 45)
                print(" UNTO DE OPERACIÓN DEL SISTEMA ".center(45, " "))
                print("═" * 45)
                print(f" Caudal volumétrico : {Q_op_lmin:>8.3f} L/min")
                print(f" Caudal volumétrico      : {Q_op:>8.2e} m³/s")
                print(f" Presión de cruce   : {dp_op:>8.1f} Pa")
                print(f" Pérdida de altura  : {dh_op:>8.3f} m.c.a.")
                print("═" * 45 + "\n")

            return Q_op, Q_op_lmin, dp_op, dh_op

        except RuntimeError:
            if verbose:
                print("\n[ERROR] El solver no pudo converger.\n")
            return None, None, None, None