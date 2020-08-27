# libraries
import matplotlib.pyplot as plt
import numpy as np
import noise_to_current
import sys

# values for input some differents current and temperature (old)

# load data from noise document
m1_noise,m1_mask = noise_to_current.loadNoise(sys.argv[1])
m2_noise,m2_mask = noise_to_current.loadNoise(sys.argv[2])

# take average noise from data
m1_noise,m1_mask = noise_to_current.average_quantity(m1_noise,m1_mask,16)
m2_noise,m2_mask = noise_to_current.average_quantity(m2_noise,m2_mask,16)

# transform the noise into current with the formula
I1 = noise_to_current.noiseToCurrent(m1_noise, 16, (95000.)*1e-9)
I2 = noise_to_current.noiseToCurrent(m2_noise, 16, (56000.)*1e-9)

T1 = sys.argv[1][2:4]
T2 = sys.argv[2][2:4]
V = sys.argv[1][6:9]

# apply the scaling
I1_hyp = noise_to_current.currForAnotherTemp(I2, 273-eval(T2), 273-eval(T1))
I2_hyp = noise_to_current.currForAnotherTemp(I1, 273-eval(T1), 273-eval(T2))

# error on current/pixel for the graphic
print(I1[0][0])
e1 = (I1[0][0])*0.07
e2 = (I1[0][0])*0.2

# the plots
plt.ion()
plt.subplots(2,1)
plt.subplot(2,1,1)
plt.title('Current from CR003482\n')
plt.errorbar(I2_hyp.flatten(), I2.flatten(),e1,e1,'ob',label=T1+' rescaled to '+T2,ms=0.5)
plt.errorbar(I1_hyp.flatten(), I1.flatten(),e2,e2,'og',label=T2+' rescaled to '+T1,ms=0.5)
plt.plot(np.arange(0,3e-7,1e-8),np.arange(0,3e-7,1e-8),color='red')
plt.xlim(0.e-7,3.e-7)
plt.ylim(0.e-7,3.e-7)
plt.legend()
plt.grid()
plt.subplot(2,1,2)
plt.plot(1-(I2.flatten()/I2_hyp.flatten()),'ob', ms=1.0)
plt.plot(1-(I1.flatten()/I1_hyp.flatten()),'og', ms=1.0)

# just put a option to save 
save = input('Save (y/n)')
if save == 'y':
    plt.savefig('rescale_'+T1+'_'+T2+'_'+V+'_82'+'.png')
    
plt.show()