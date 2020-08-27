# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 11:02:59 2019

@author: Gabriel Rodrigues
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def diode(V,I_s,Alpha):
    return I_s*(1-np.exp(-1.*Alpha*V))

def avalanche(V,Kapa):
    return Kapa*V

def breakdown(V,Vthr,Beta,Delta):
    return Beta*np.exp(Delta*(V-Vthr))

def curr_model(V,I_s,Vthr,Alpha,Kapa,Beta,Delta):
    return I_s*(1-np.exp(-1.*Alpha*V)) + Kapa*V + Beta*np.exp(Delta*(V-Vthr))

k = np.loadtxt("../Gabriel/TIL_7_Good_17_00_16_15_Feb_19.txt")

U = (-1)*np.ones(len(k)-7)
V = [k[_][0] for _ in range(len(k)-7)]*U
I = [k[_][1] for _ in range(len(k)-7)]*U

# initial parameters
Is_0 = 1.0*10e-6
Alpha_0 = 0.018
Kapa_0 = 0.0086*10e-6
Delta_0 = 0.066
Vth_0 = 400
Beta_0 = 2.0*10e-5
init = [Is_0,Vth_0,Alpha_0,Kapa_0,Beta_0,Delta_0]

best, covar = curve_fit(curr_model, V, I, p0=init)

print(best, covar)

diode_data = []
av_data = []
break_data = []
fit_data = []

for v in V:
    diode_data.append(diode(v,Is_0,Alpha_0))
    av_data.append(avalanche(v,Kapa_0))
    break_data.append(breakdown(v,Vth_0,Beta_0,Delta_0))
    fit_data.append(curr_model(v,best[0],best[1],best[2],best[3],best[4],best[5]))

fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(V,I,color='blue',s=10,marker='o',label='Data')
ax.scatter(V,diode_data,color='green',s=10,marker='_',label='Diode')
ax.scatter(V,av_data,color='red',s=10,marker='_',label='Avalanche')
ax.scatter(V,break_data,color='orange',marker='_',label='Breakdown')
ax.plot(V,fit_data,color='magenta',label='Fit')
plt.title("I vs V")
plt.ylabel("current(A)")
plt.xlabel("Voltage(V)")
plt.ylim(-0.000002,0.00011)
plt.xlim(-5,600)
plt.legend()
plt.show()
