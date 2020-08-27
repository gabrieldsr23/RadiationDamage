import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage


# Load Noise distributions
def loadNoise(directory):
    noise = np.zeros((3*256, 256))
    mask = np.zeros((3*256, 256))
    for n in range(3):
        noise[n*256:(n+1)*256] = np.loadtxt(directory+'/Noise_VP2_Asic%d.txt'%n, dtype=float, delimiter=',').T
        mask[n*256:(n+1)*256]  = np.loadtxt(directory+'/Mask_VP2_Asic%d.txt'%n, dtype=float, delimiter=',').T
    noise[255,:]     = noise[255,:]/1.5
    noise[256,:]     = noise[256,:]/1.5
    noise[255+256,:] = noise[255+256,:]/1.5
    noise[256*2,:]   = noise[256*2,:]/1.5
    mask[noise>50]   = 1
    noise[mask>0.5]  = 0.
	

    return noise,mask



def average_quantity(Quantity,Mask, group_pixels_by):

    _filter = np.ones((group_pixels_by,group_pixels_by))
    
    Q0 = ndimage.convolve(Quantity, _filter, mode='constant', cval=0.0)[int(group_pixels_by/2)::group_pixels_by,int(group_pixels_by/2)::group_pixels_by]
    M0 = ndimage.convolve(1 - Mask, _filter, mode='constant', cval=0.0)[int(group_pixels_by/2)::group_pixels_by,int(group_pixels_by/2)::group_pixels_by]
    Q0 = Q0/M0

    return Q0,M0


def display_array(Quantity,Mask, group_pixels_by,title_graph='Average Current', colormap='jet'):  # colormap = 'autumn_r', 'jet', 'rainbow'
    # Displays a 3D array in 3 slices of z, lower, middle and upper.
    #
    Q0,M0=Quantity,Mask
    x_max = 256*3
    y_max = 256
    # Create a meshgrid for the X and Y axes with the real size of the sensor:
    bin_x =  x_max / int(np.floor(group_pixels_by))
    bin_y =  y_max / int(np.floor(group_pixels_by))
    print(x_max,bin_x)
    xi = np.arange(0, x_max + group_pixels_by,group_pixels_by)
    yi = np.arange(0, y_max + group_pixels_by,group_pixels_by)
    print(xi.shape,yi.shape)
    x, y = np.meshgrid(xi, yi)

    # Create a figure with 3 plots:
    fig, ax0 = plt.subplots(1,1,figsize=(17,7))

    # Plot the matrices and edit properties of the axes:
    # TOP image
    im0 = ax0.pcolormesh(x, y, Q0.T, vmin=np.min(Q0), vmax=np.max(Q0), cmap=colormap)
    ax0.axis([0, x_max, 0, y_max])
    ax0.label_outer()

    # Position of the z-layer text
    x_ztext = 0.96
    y_ztext = 0.96
    ax0.text(x_ztext, y_ztext, title_graph, horizontalalignment='right', verticalalignment='top',
             color='black', fontsize=13, transform=ax0.transAxes)
    # limit ticks to 2 digits
    #ax0.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))

    # Modify the tick locations for readability:
    x_offset = 0 * x_max
    x_nticks = 9
    plt.xticks(np.linspace(x_offset, x_max - x_offset, x_nticks))
    y_offset = 0.1 * y_max
    y_nticks = 3
    plt.yticks(np.linspace(y_offset, y_max - y_offset, y_nticks))

    # Create an axe structure to show a single colorbar for all 3 plots:
    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.1, 0.03, 0.8])
    fig.colorbar(im0, cax=cbar_ax, ticks=np.linspace(np.min(Q0), np.max(Q0), 9))

    # Additional modifications to full figure
    plt.subplots_adjust(hspace=0)
    fig.suptitle(str(title_graph), fontsize=16, family='serif')
    fig.patch.set_facecolor('white')

    plt.show()

    return 1

def noiseToCurrent(noise, group_pixels_by, Itotal):
    I = ((noise*group_pixels_by)**2) * Itotal / np.sum((noise*group_pixels_by)**2)
    #I = (noise**2) * Itotal / np.sum(noise)
    return I

def currForAnotherTemp(I0, T0, T1, Eg = 1.214):
    return I0 * (T1/T0)**2 * np.exp( - (Eg / 2) / 8.6173303e-5 * (1./T1 - 1./T0) )


'''def currForAnotherVolt(I0, T0, I1, Eg = 1.214):
    return T1 #I0 * (T1/T0)**2 * np.exp( - Eg / 2 / 8.6173303e-5 * (1./T1 - 1./T0) )
'''

plt.ion()
'''
_noise,_mask = loadNoise(sys.argv[1])
noise,mask = average_quantity(_noise,_mask,16)
I = noiseToCurrent(noise, 16, float(sys.argv[2]))
display_array(I,mask,16)
display_array(_noise,_mask,1)
'''
