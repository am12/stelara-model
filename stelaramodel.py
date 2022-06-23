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

prop_factor = 0.922
plasma_vol = 2.75
threshold = 1.35

def M(Ab_total, release_time, start_day=0):

    #calculating rate of antibody release (mg/L/day)
    release_coeff = Ab_total/plasma_vol*prop_factor/release_time
    print("Ab release (mg/day):", release_coeff*plasma_vol)

    M_clear = lambda t: release_coeff*np.exp(-0.036*t)

    M_y = np.zeros(len(x))
    for i in range(1,len(x)):
        if x[i] <= release_time:
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

def graph(markers=[]):
    hfont = {'fontname': 'Arial', 'weight': 'bold', 'size': 10}
    fig, ax = plt.subplots(1, 1)
    fig.set_size_inches((10, 5.5))
    plt.title("test", **hfont)
    plt.ylabel("Serum Conc. (mg/L)", **hfont)
    plt.xlabel("Days after Initial Dose", **hfont)

    ax.plot(x, y, color = 'green', linewidth = 0.5)
    ax.plot(x, np.ones(len(x))*threshold, color = 'orange', linewidth = 0.25)
    for i in markers:
        ax.axvline(i, ymin = 0, ymax = 1, color = 'red', linewidth = 0.2)
    #plt.plot(np.ones(math.ceil(max(y)))*7, np.arange(math.ceil(max(y))), color = 'red', linewidth = 0.2)
    plt.show()

#constant variable definition

'''EDIT BELOW'''

if __name__ == '__main__':
    
    #CONTROL PANEL TEST
    '''
    t = I(0)
    for i in range(20):
        t += I(5, start_day = 14*i)
    y = I(5) + t
    '''
    #input controls (induction(IV), subq maintenance, oral?, schedules?)
    induction = int(input("Induction Phase (mg): "))
    maintenance, oral = [], []
    while (0,0,0) not in maintenance:
        maintenance.append(tuple([int(i) for i in input("Maintenance Phase (mg length start): ").split(' ')]))
    maintenance.pop()
    while (0,0) not in oral:
        oral.append(tuple([int(i) for i in input("Oral Phase (mg start): ").split(' ')]))
    oral.pop()

    #setting x
    window = int(input("Window: ")) #setup so that window is automatically created
    inc = 1
    x = np.arange(0,window+inc, inc)

    #y calculation
    y = I(induction)
    for i in maintenance:
        y += M(*i)
    for j in oral:
        y += I(*j)

    #zero discovery
    index = np.where(y <= threshold)[0][0]
    xa, xb, ya, yb = x[index-1], x[index], y[index-1], y[index]
    z = xa + ((threshold-ya)*(xb-xa)/(yb-ya))
    print("Time of expiry:", z)

    #print(y)
    graph([z])