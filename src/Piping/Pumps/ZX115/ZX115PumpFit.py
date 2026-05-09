import numpy as np
def Pa4m3s(Q):
        A = -5.18971071e+13 
        B = -5.46987259e+08  
        C = 3.30978671e+04
        return (A * Q**2) + (B * Q) + C
    