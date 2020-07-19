from library import NonlinearFiber, LinearFiber
import numpy as np
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

    argmax = np.argmax(spectrum)
    freq_1 = freq[:argmax]
    freq_2 = freq[argmax:]

    function1 = interp1d(spectrum[:argmax], freq_1)
    freq1 = function1(-x)

    function2 = interp1d(spectrum[:argmax], freq_1)
    freq2 = function2(x)
    return freq2 - freq1

    

    
    
