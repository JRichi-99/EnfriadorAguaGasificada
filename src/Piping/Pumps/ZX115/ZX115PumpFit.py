import numpy as np
def Pa4m3s(Q):
        A = -5.18971071e+13 
        B = -5.46987259e+08  
        C = 3.30978671e+04
        return (A * Q**2) + (B * Q) + C

def Pa4m3sParalelo(Q):
        A = -1.29742768e+13 
        B =  -2.73493629e+08  
        C = 3.30978671e+04
        return (A * Q**2) + (B * Q) + C