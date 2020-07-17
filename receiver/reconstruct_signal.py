import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import numpy as np 
import matplotlib.pyplot as plt 
from library import QamSignal
from tools import fiber_for_reconstruct
from library import cd_compensation
import joblib
from scipy.io import loadmat


FIBER = {
    1: {"alpha": 0.2, 'D': 16.7, 'gamma': 1.3},
    2: {"alpha": 0.18, "D": 20.1, "gamma": 0.9},
    3: {"alpha": 0.21, "D": 4.3, "gamma": 1.47}
}

def reconstruct_signal(name,config):
    fibers = fiber_for_reconstruct(config)
    signal = QamSignal.load(name, True)
    data = loadmat(name)
    tx_samples = data['tx_samples']
    nonlinear_noise = data['nonlinear_noises_each_span']
    signal.samples = tx_samples

    for fiber_idx,fiber in enumerate(fibers):
        signal = fiber.prop(signal)
        signal[:] = np.sqrt(10**((fiber.alpha * fiber.length)/10))*signal[:]
        signal[:] += nonlinear_noise[fiber_idx]


def receiver(name, config_ith):
    import joblib
    from library.electrical import Resampler
    import resampy
    from library import matched_filter
   

    config = joblib.load('../simulate_data/config_setting')[config_ith]
    signal = reconstruct_signal(name)
    fibers = fiber_for_reconstruct(config)
    
    signal = cd_compensation(signal, fibers, signal.fs_in_fiber)
    signal.samples = resampy.resample(
        signal[:], signal.sps_in_fiber, 2, axis=-1, filter='kaiser_fast')
    
    
    signal = matched_filter(signal, 0.02)
    signal.samples = signal[:, ::2]
    
    signal.inplace_normalise()
    noise = signal.samples - signal.symbol

    noise_power = np.sum(np.mean(np.abs(noise) ** 2, axis=-1))
    
    print(10 * np.log10((2 - noise_power) / noise_power))
    

receiver('../data/0_0.mat',0)



    




