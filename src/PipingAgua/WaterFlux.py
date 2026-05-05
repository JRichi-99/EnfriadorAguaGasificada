import numpy as np
import CoolProp.CoolProp as cp 
from Coil import Coil
import fluids as fl
import copy  # Añadido para copiar diccionarios de forma segura

class SystemWaterFlux:
    def __init__(self):
        pass

    def pressure_drop_pipe(self, tramos, Q, mu, rho, g=9.81, to_iterate = False):
        n = len(tramos)
        
        # Copia profunda para no alterar la lista de diccionarios original
        data = copy.deepcopy(tramos) 
        
        # Inicialización de arreglos de NumPy para vectorización
        D = np.zeros(n)
        Lx = np.zeros(n)
        Ly = np.zeros(n)
        A = np.zeros(n)
        F = np.zeros(n)
        V = np.zeros(n)
        E = np.zeros(n)
        Re = np.zeros(n)
        Ks = np.zeros(n)

        # Iteración sobre cada tramo para extraer propiedades y calcular variables
        for i in range(n):
            tramo = tramos[i]
            largo = tramo["l"]
            diametro = tramo["d"]
            material = tramo["mat"]
            direccion = tramo["dir"]
            
            # Asignación de longitud según la dirección del tubo (horizontal o vertical)
            if direccion == "h":
                Lx[i] = largo
            elif direccion == "v":
                Ly[i] = largo
                
            Ks[i] = tramo["ks"]
            D[i] = diametro
            
            # Cálculo del área transversal y actualización del diccionario
            A[i] = np.pi * (diametro / 2)**2
            data[i]["area"] = A[i]
            
            # Cálculo de la velocidad del fluido
            V[i] = Q / A[i]
            data[i]["velo"] = V[i]
            
            # Cálculo del número de Reynolds
            Re[i] = (rho * V[i] * D[i]) / mu
            data[i]["Re"] = Re[i]
            
            # Obtención de la rugosidad absoluta y el factor de fricción de Darcy
            E[i] = fl.friction.material_roughness(material)
            data[i]["E"] = E[i]
            
            F[i] = fl.friction_factor(Re[i], E[i] / D[i])  
            data[i]["F"] = F[i]

        # Caída de carga (h) debida a la fricción en tramos horizontales y verticales
        delta_h_friction = F * (Lx / D) * (V**2 / (2 * g)) + F * (Ly / D) * (V**2 / (2 * g))

        # Caída de carga debida a la diferencia de altura (gravedad)
        delta_h_height = Ly

        # Caída de carga debida a los accesorios (fittings)
        delta_h_fittings = Ks * (V**2 / (2 * g))

        # Balance de energía total usando la ecuación de Bernoulli
        # Asumiendo Pin y Pout como atmosféricas
        total_delta_h = sum(delta_h_friction) + sum(delta_h_height) + sum(delta_h_fittings) + (V[-1]**2 / (2 * g)) - (V[0]**2 / (2 * g))
        
        if to_iterate: # Si se desea calcular una bomba para el metodo de newton-raphson
            return total_delta_h
        return total_delta_h, delta_h_friction, delta_h_height, delta_h_fittings, data
    




















