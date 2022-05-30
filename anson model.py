import math
from re import M
from tkinter import Y
from winreg import REG_MULTI_SZ
import numpy as np
import matplotlib.pyplot as plt

'''
class IDose():
    def __init__():
        
class MDose():
    def __init__():

class Ab():
    def __init__():
'''

def R(x, i=130, m=60):
    #i = induction phase infusion (mg), m = maintenance phase injection (mg)
    #define M, I, and Ab-release
    #define variables in terms of n and r
    #Linear Ab Release (from NP) Model: y (%) = 0.8834x + 2.9095
    

    prop_factor = 0.922
    plasma_vol = 2.75
    Ab_release_rate = 0.008834

    M_coeff = m*prop_factor/plasma_vol*Ab_release_rate

    I_coeff = i*prop_factor/plasma_vol #this is based off observation of 130 mg dosage and requires further analysis

    D = math.floor(1/Ab_release_rate) #max_days_of_release
    max_weeks_of_release = D/7

    y = []
    for i in x:
         
        if i>D:
            #return R(113) + (43.6*np.exp(-0.058*x)) - np.sum(0.2666 - (0.2666*np.exp(-0.036*np.arange(114, x))))
            r = M_coeff*D + (I_coeff*np.exp(-0.058*i)) - np.sum(M_coeff - (M_coeff*np.exp(-0.036*np.arange(D+1, i+D+1))))
        else:
            r = M_coeff*i + (I_coeff*np.exp(-0.058*i)) - np.sum(M_coeff - (M_coeff*np.exp(-0.036*np.arange(0, i+1))))
        
        y.append(r)
    
    return y 



#graphing
inc = 1
days = 150
x = np.arange(0,days+inc, inc)
y = R(x)
print(y)
plt.title("serum conc.")
plt.xlabel("X axis")
plt.ylabel("Y axis")
plt.plot(x, y, color = 'green', linewidth = 0.5)
plt.plot(np.ones(days+inc)*114, y, color = 'red', linewidth = 0.1)
plt.show()
