import math
from re import M
from tkinter import Y
from winreg import REG_MULTI_SZ
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate

'''
TASKS:
- Create Github repo
- Implement modular method of solving maintenance function
- Correct the Ab release formula to account for varying release timings and dosages
- Create GUI with sliders for 3 params
    - I_dose mass
    - M_dose mass
    - M_dose time
- Add calculate button to GUI to pass params and create graph
- Create graph legend and labels for readability


MAYBE:
- Implement/model multi-dose dosing schedules
- Correct the summation function to continuous integral of times
    - Workaround: Change the units of time to seconds instead of days for all calculations (functions will be same), then correct back to days when graphed
- Correct prop_factor, plasma_vol, and Ab_release_rate as data comes in (remove assumptions)

'''

'''
def R(x, i=130, m=90):
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


def M(x):


    M_clear_rate = lambda t, y: y*np.exp(-0.036*t)
    Ab_total = 90
    prop_factor = 0.922
    plasma_vol = 2.75
    Ab_release_rate = Ab_total/plasma_vol*prop_factor*0.008834
    print(Ab_release_rate)

    total = 0
    y = []
    for t in x:
        Ab_release_rate - M_clear_rate(t, total)

    return y
'''

def M(x):

    #calculating rate of antibody release (mg/L/day)
    release_coeff = Ab_total/plasma_vol*prop_factor*0.008834 
    print(release_coeff)

    M_clear = lambda t, y: y*prop_factor*np.exp(-0.036*t) #based on 90mg maintenance * 0.922 = 83.0
    Ab_release = lambda t: release_coeff*t #based on calculations from case study 1

    M_y = []
    for t in x:
        if t <= final_day:
            total = Ab_release(t) - sum([M_clear(i, M_y[i]) for i in range(len(M_y))])
        else:
            total = total - sum([M_clear(i, M_y[i]) for i in range(len(M_y))])
        M_y.append(total)

    print(M_y)

    return M_y

def I(x):
    #define bolus injection population over time
    I_clear = lambda t, dose: dose/plasma_vol*prop_factor*np.exp(-0.058*t) #based on 130mg induction / 2.75 * 0.922 = 43.6
    
    I_y = I_clear(x, bolus_dose)

    print(I_y)

    return I_y

#variable definition
Ab_total = 90
final_day = 115
bolus_dose = 130

prop_factor = 0.922
plasma_vol = 2.75

#graphing
inc = 1
days = 365
x = np.arange(0,days+inc, inc)
y = M(x) + I(x)
#print(y)
#int_y = [integrate.simps(y[0:i], x[0:i]) for i in x[1:]]
plt.title("serum conc.")
plt.xlabel("X axis")
plt.ylabel("Y axis")
plt.plot(x, y, color = 'green', linewidth = 0.5)
#plt.plot(x[1:], int_y, color = 'red', linewidth = 0.5)
plt.plot(np.ones(len(y))*final_day, y, color = 'red', linewidth = 0.1)
plt.plot(x, np.ones(len(x))*1.35, color = 'orange', linewidth = 0.2)
plt.show()