import numpy as np
def Pa4m3s(Q):
        A = -1.23667290e11
        B = -4.50879282e07
        C = 1.95608371e04
        
        return (A * Q**2) + (B * Q) + C
    
def m3s4Pa(Pa):
    return -2.71801833e-13 *Pa**2 -7.42566003e-09* Pa + 2.52500090e-04
