from library import NonlinearFiber, LinearFiber
import numpy as np
import visdom
FIBER = {
    1: {"alpha": 0.2, 'D': 16.7, 'gamma': 1.3},
    2: {"alpha": 0.18, "D": 20.1, "gamma": 0.9},
    3: {"alpha": 0.21, "D": 4.3, "gamma": 1.47}
}

def fiber_for_reconstruct(config):
    fibers = []
    for kind in config[1:]:
        alpha = FIBER[kind]['alpha']
        D = FIBER[kind]['D']
        gamma = FIBER[kind]['gamma']

        fibers.append(LinearFiber(alpha,D,80,0,1550))

    return fibers


def calc_xdb_bandwidth(freq,spectrum,x):
    from scipy.signal import findfreqs
    from scipy.interpolate import interp1d
    
    spectrum = spectrum / np.max(spectrum)
    spectrum = 10 * np.log10(spectrum)
    argmax = int(len(spectrum)/2)
    freq_1 = freq[:int(len(spectrum)/2)]
    freq_2 = freq[int(len(spectrum)/2):]

    function1 = interp1d(spectrum[:argmax], freq_1)
    freq1 = function1(-x)

    function2 = interp1d(spectrum[argmax:], freq_2)
    freq2 = function2(-x)
    return np.abs(freq2 - freq1)/1e9,freq1/1e9,freq2/1e9


        



def main():
    from scipy.io import loadmat
    x = loadmat('./data/0_1.mat')['freqs'][0]
    spec = loadmat('./data/0_1.mat')['spec_lms'][0,:1024]
    bandwidth_3db,freq1_3,freq2_3 = calc_xdb_bandwidth(x, spec, 3)
    bandwidth_6db,freq1_6,freq2_6 = calc_xdb_bandwidth(x,spec,6)
    xielv1 = 3 / (freq1_3 - freq1_6)
    xielv2 = 3 / (freq2_3 - freq2_6)




    print('hello world')
    
main()

    
    
