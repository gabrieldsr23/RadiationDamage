# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 12:49:05 2019

@author: Gabriel Rodrigues
"""

import numpy as np
import matplotlib.pyplot as plt

k = np.loadtxt("../Gabriel/CR003482_IV_-42deg 0_1000_17_06_42_01_Mar_19.txt")
h = np.loadtxt("../Gabriel/TIL_7_Good_17_00_16_15_Feb_19.txt")

V = [k[_][0] for _ in range(len(k))]
I = [k[_][1] for _ in range(len(k))]
Vn = [h[_][0] for _ in range(len(h))]
In = [h[_][1] for _ in range(len(h))]

U = (-1)*np.ones(len(k))
Un = (-1)*np.ones(len(h))


plt.scatter(V*U,I*U,color='blue',s=10,marker='o',label='irrad_82')
plt.scatter(Vn*Un,In*Un,color='red',s=10,marker='x',label='non_irrad_til7')
plt.ylim(0.0,0.0001)
plt.legend()
plt.show()
