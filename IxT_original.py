import numpy as np
import matplotlib.pyplot as plt
import noise_to_current

voltages = [110,140,250,550]

DT = eval(input('DT'))
DI = eval(input('DI'))

m35_140noise,m35_140mask = noise_to_current.loadNoise('T-35V-140_0')
m40_140noise,m40_140mask = noise_to_current.loadNoise('T-40V-140_0')
m40_250noise,m40_250mask = noise_to_current.loadNoise('T-40V-250_0')
m35_250noise,m35_250mask = noise_to_current.loadNoise('T-35V-250_0')
m40_110noise,m40_110mask = noise_to_current.loadNoise('T-40V-110_0')
m40_550noise,m40_550mask = noise_to_current.loadNoise('T-40V-550_0')

m35_140noise,m35_140mask = noise_to_current.average_quantity(m35_140noise,m35_140mask,16)
m40_140noise,m40_140mask = noise_to_current.average_quantity(m40_140noise,m40_140mask,16)
m35_250noise,m35_250mask = noise_to_current.average_quantity(m35_250noise,m35_250mask,16)
m40_250noise,m40_250mask = noise_to_current.average_quantity(m40_250noise,m40_250mask,16)
m40_110noise,m40_110mask = noise_to_current.average_quantity(m40_110noise,m40_110mask,16)
m40_550noise,m40_550mask = noise_to_current.average_quantity(m40_550noise,m40_550mask,16)

I40_140 = noise_to_current.noiseToCurrent(m40_140noise, 16, (34000.+DI)*1e-9)
I35_140 = noise_to_current.noiseToCurrent(m35_140noise, 16, (60000.+DI)*1e-9)
I40_250 = noise_to_current.noiseToCurrent(m40_250noise, 16, (50000.+DI)*1e-9)
I35_250 = noise_to_current.noiseToCurrent(m35_250noise, 16, (75000.+DI)*1e-9)
I40_110 = noise_to_current.noiseToCurrent(m40_110noise, 16, (30000.+DI)*1e-9)
I40_550 = noise_to_current.noiseToCurrent(m40_550noise, 16, (101000.+DI)*1e-9)

I35_140hyp = noise_to_current.currForAnotherTemp(I40_140, 273-(40.+DT), 273-(35.+DT))
I40_140hyp = noise_to_current.currForAnotherTemp(I35_140, 273-(35.+DT), 273-(40.+DT))
I40_250hyp = noise_to_current.currForAnotherTemp(I40_250, 273-(40.+DT), 273-(35.+DT))
I35_250hyp = noise_to_current.currForAnotherTemp(I35_250, 273-(35.+DT), 273-(40.+DT))

plt.ion()
plt.subplots(3,3)
plt.subplot(3,3,1)
plt.plot(I40_140hyp.flatten(), I40_140.flatten(),'ok',label='35 rescaled to 40')
plt.plot(I35_140hyp.flatten(), I35_140.flatten(),'or',label='40 rescaled to 35')
plt.xlim(0.,3e-7)
plt.ylim(0.,3e-7)
plt.legend()
plt.grid()
plt.subplot(3,3,2)
plt.plot(I40_250hyp.flatten(), I40_250.flatten(),'ok',label='35 rescaled to 40')
plt.plot(I35_250hyp.flatten(), I35_250.flatten(),'or',label='40 rescaled to 35')
plt.xlim(0.,3e-7)
plt.ylim(0.,3e-7)
plt.legend()
plt.grid()
plt.subplot(3,3,3)
plt.plot(1-(I40_140.flatten()/I40_140hyp.flatten()),'ok')
plt.plot(1-(I35_140.flatten()/I35_140hyp.flatten()),'or')
plt.subplot(3,3,4)
plt.plot(1-(I40_250.flatten()/I40_250hyp.flatten()),'ok')
plt.plot(1-(I35_250.flatten()/I35_250hyp.flatten()),'or')
plt.subplot(3,3,5)
plt.plot(I40_110,color='green',label='I40_110')
plt.plot(I40_140,color='blue',label='I40_140')
plt.plot(I40_250,color='red',label='I40_250')
plt.plot(I40_550,color='brown',label='I40_550')
plt.show()

input()

