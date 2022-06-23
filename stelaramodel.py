import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets

'''
TASKS:
- Create Github repo*
- Implement modular method of solving maintenance function*
- Correct the Ab release formula to account for varying release timings and dosages*
- Create GUI with sliders for 3 params
    - I_dose mass
    - M_dose mass
    - M_dose time
- Add calculate button to GUI to pass params and create graph
- Create graph legend and labels for readability
- Write data to an Excel


MAYBE:
- Add functionality to calculate optimal dose given params
- Implement/model multi-dose dosing schedules
    - Include added dose at a different time (non-initial)
    - Can feasibly do an incremental model where each dose is added to the graph one by one, then include a button to clear graph
- Correct the summation function to continuous integral of times
    - Workaround: Change the units of time to seconds instead of days for all calculations (functions will be same), then correct back to days when graphed
- Correct prop_factor, plasma_vol, and Ab_release_rate as data comes in (remove assumptions)

'''

def M(Ab_total, final_day, start_day=0):

    #calculating rate of antibody release (mg/L/day)
    release_coeff = Ab_total/plasma_vol*prop_factor/final_day
    print("Ab release (mg/day):", release_coeff*plasma_vol)

    M_clear = lambda t: release_coeff*np.exp(-0.036*t)

    M_y = np.zeros(len(x))
    for i in range(1,len(x)):
        if x[i] <= final_day:
            M_y[i:] += M_clear(x)[:-i]

    if start_day != 0:
        M_y = np.pad(M_y, (start_day,0))[:-start_day]

    #print(M_y)
    return M_y

def I(bolus_dose, start_day=0):
    #define bolus injection population over time
    I_clear = lambda t, dose: dose/plasma_vol*prop_factor*np.exp(-0.058*t) #based on 130mg induction / 2.75 * 0.922 = 43.6
    
    I_y = I_clear(x, bolus_dose)
    
    if start_day != 0:
        I_y = np.pad(I_y, (start_day,0))[:-start_day]

    #print(I_y)
    return I_y

#scalable variable definition
#Ab_total = 20
#final_day = 150
#bolus_dose = 0

#constant variable definition
prop_factor = 0.922
plasma_vol = 2.75
threshold = 1.35

#graphing variables
inc = 1
days = 300

x = np.arange(0,days+inc, inc)

#CHANGE THIS
t = I(0)
for i in range(20):
    t += I(5, start_day = 14*i)
y = I(5) + t

#print(y)

#plotting
hfont = {'fontname': 'Arial', 'weight': 'bold', 'size': 10}

ax, fig = plt.subplots(1,1)

#fig.set_size_inches(15, 10)
plt.title("test", **hfont)
plt.ylabel("Serum Conc. (mg/L)", **hfont)
plt.xlabel("Days after Initial Dose", **hfont)
plt.plot(x, y, color = 'green', linewidth = 0.5)
#plt.plot(np.ones(math.ceil(max(y))-math.floor(min(y))+1)*14, np.arange(math.floor(min(y)), math.ceil(max(y))+1), color = 'red', linewidth = 0.2)
#plt.plot(np.ones(math.ceil(max(y)))*7, np.arange(math.ceil(max(y))), color = 'red', linewidth = 0.2)
plt.plot(x, np.ones(len(x))*threshold, color = 'orange', linewidth = 0.25)
plt.show()