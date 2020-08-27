import sys
import numpy as np
import matplotlib.pyplot as plt
import glob
import sys,yaml


def dict_yaml(f):
    """
    Import yaml file and make convert to dictionary

    :param f: the file path
    :return:
    """
    #Import Yaml Config
    config_file = open(f, "r")
    yaml_gen = yaml.load_all(config_file)

    config = {}
    for yaml_doc in yaml_gen:
        if 'type' in yaml_doc.keys():
            config[yaml_doc["type"]] = yaml_doc
        else:
            for k in yaml_doc.keys():
                config[k] = yaml_doc[k]
    return config



def merge_data(path, asicID, config,trims = ["Trim0", "TrimF"]):
        for i in range(0,len(trims)):
            # get the size of the data
            nscans = (config["max_global_threshold"][i] - config["min_global_threshold"][i])/config["global_threshold_step"][i]

            data = []   # create a list to append the multiple arrays from the text files
            dataSet = np.zeros((256*int(nscans), 256))  # define a zero list where the data will be added into

            # obtain the count of the files which are specified by the following path
            numberID = 0
            for n in glob.glob(path+"Pixel_"+asicID+"_"+trims[i]+"_*"): numberID += 1


            ### Load Data ###
            # repeat and add the text file into the data list
            print('here')
            for x in range(0,numberID):
                try:
                    data.append(np.loadtxt(path+"Pixel_"+asicID+"_"+trims[i]+"_"+'{:d}'.format(x+1)+".txt", dtype=int, delimiter=','))
                except Exception as e:
                    print('blabla',e)
                    pass

            # compute the summation matrix
            for x in range(0,numberID):
                print(numberID)
                dataSet += data.pop()  # pop the array element from the data list and added to the current values array

            savepath = path+"Pixel_"+asicID+"_"+trims[i]+".txt"
            np.set_printoptions(threshold=np.inf, linewidth=np.inf)
            with open(savepath, 'wb') as f:
                np.savetxt(f, dataSet, fmt='%d', delimiter=",")

def get_mean_std_single_scan(options):
    """
    Get the mean of the two DAC scans and the noise over the two scans
    :param options:
    :return:
    """
    # get the output directory
    f = options["output_directory"] + "/"
    asicID = options["asic"]

    print("[Status] Loading Scans")
    # Load the data and reshape it to (x,nscanpoints,256,256)

    try:
        h = np.loadtxt(f + 'Pixel_%s_Trim0.txt' % asicID,delimiter=',').reshape(1, -1, 256, 256)
    except :
        print('Bad File')
        pass

    print("[Status] Manipulating input data")
    # Switch shape to (x,256,256,nscanpoints)
    h = np.swapaxes(h, 1, 2)
    h = np.swapaxes(h, 2, 3)

    # Clip DAC counts smaller than set value dac_noise
    dac_clip = options['dac_noise'] if 'dac_noise' in options.keys() else 0
    h[h <= dac_clip] = 0

    # Remove edge of scan effects
    indices = np.zeros(np.shape(h), dtype=bool)
    subindices = (h[:, :, :, 0] > 0) & (h[:, :, :, 1] == 0)  # High edge
    indices[:, :, :, 0] = subindices
    subindices = (h[:, :, :, -1] > 0) & (h[:, :, :, -2] == 0)  # Low edge
    indices[:, :, :, -1] = subindices
    # Remove 1-scan-point wide spikes in DAC count
    subindices = (h[:, :, :, 1:-1] > 0) & (h[:, :, :, 2:] == 0) & (
    h[:, :, :, :-2] == 0)  # shape (1,256,256, nscanpoints-2)
    indices[:, :, :, 1:-1] = subindices
    h[indices] = 0

    # Identify the pixels with no or permanent response during the scans by summing over all their DAC counts
    _maskA = np.where(np.sum(h, axis=-1) < 1e-1)
    _maskC = np.where(np.sum(h, axis=-1) > 50 * len(h[0, 0, 0, :]))
    # assign epsilon values to the DAC counts of those pixels
    h[_maskA] = 1e-8
    h[_maskC] = 1e-8

    print("[Status] Computing mean and std")
    # Compute the average
    dac = np.zeros(np.shape(h), dtype=int)
    print(h.shape)
    # The scans start from 'max_global_threshold'

    dac[0, :, :, :] = np.arange(options['max_global_threshold'][0],
                            options['min_global_threshold'][0],
                            -options['global_threshold_step'][0])

    # use data as weights
    mean = np.average(dac, weights=h, axis=-1)

    mean[_maskA] = 0
    catA = np.count_nonzero((mean[0] < 1e-1) )
    mean[_maskC] = 0
    catC = np.count_nonzero((mean[0] < 1e-1) ) - catA

    # get the mask (average null on one of the two scans)
    mask = (mean[0] < 1e-1)

    print("  Masked CAT A: %d" % catA)
    print("  Masked CAT C: %d" % catC)
    options["Mask_CatA"] = catA
    options["Mask_CatC"] = catC

    # save means
    np.savetxt(f + asicID + "_threshold_0.txt", mean[0], fmt='%d', delimiter=",")

    options["0_Trim"] = [np.average(mean[0]), np.std(mean[0])]
    print("  0-Trim: %.2f +/- %.2f" % (options["0_Trim"][0], options["0_Trim"][1]))

    # calculate noise (first scan only)
    std = np.sqrt(np.average((dac - mean.reshape(1, 256, 256, 1)) ** 2, weights=h, axis=-1))

    # clip the masked pixels
    std[0][mask == 1] = 0.

    return mean, std, mask


if __name__ == '__main__':

    # Get the configuration
    for aa in [0,1,2]:
        print('running asic%d'%aa)
        config = dict_yaml(sys.argv[1] + '/VP2_Asic%d_config.yaml' % aa)

        path = config["output_directory"] + "/"
        config["output_directory"] = path
        asicID = config["asic"]
        doMerge = config["mask_pattern"]
        isControl = 0

        # Check individual pixels
        # plot_equal_pixelScan.plot_pixel(path, asicID, 0, 0)

        # Merge if necessary
        if (doMerge):
            merge_data(path, asicID, config, trims=['Trim0']);

        # Run the analysis
        mean, std, mask = get_mean_std_single_scan(config)
        print(mean.shape, mean.dtype, mean[np.isnan(mean)])
        with open(path + 'Threshold_%s.txt' % asicID, 'wb') as f:
            np.savetxt(f, mean[0], delimiter=',', fmt='%.5f')
        with open(path + 'Noise_%s.txt' % asicID, 'wb') as f:
            np.savetxt(f, std[0], fmt='%.5f', delimiter=',')
        with open(path + 'Mask_%s.txt' % asicID, 'wb') as f:
            np.savetxt(f, mask[0], fmt='%1f', delimiter=',')
        plt.ion()
        plt.subplots(3, 1)
        plt.subplot(3, 1, 1)
        plt.hist(mean.flatten(), bins=100)
        plt.subplot(3, 1, 2)
        plt.hist(std.flatten(), bins=100)
        plt.subplot(3, 1, 3)
        plt.imshow(mask)
        plt.show()

