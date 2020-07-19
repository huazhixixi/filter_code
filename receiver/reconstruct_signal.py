import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import joblib
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat

from library import QamSignal, cd_compensation
from tools import fiber_for_reconstruct




FIBER = {
    1: {"alpha": 0.2, 'D': 16.7, 'gamma': 1.3},
    2: {"alpha": 0.18, "D": 20.1, "gamma": 0.9},
    3: {"alpha": 0.21, "D": 4.3, "gamma": 1.47}
}

def __reconstruct_signal(name,config):
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
    return signal

def receiver_nonlinear_noise(name, config_ith):
    import joblib
    from library.electrical import Resampler
    import resampy
    from library import matched_filter
   

    config = joblib.load('../simulate_data/config_setting')[config_ith]
    signal = __reconstruct_signal(name,config)
    fibers = fiber_for_reconstruct(config)
    
    signal = cd_compensation(fibers,signal, signal.fs_in_fiber)
    signal.samples = resampy.resample(
        signal[:], signal.sps_in_fiber, 2, axis=-1, filter='kaiser_fast')
    
    
    signal = matched_filter(signal, 0.02)
    signal.samples = signal[:, ::2]

    phase = np.angle(np.mean(signal.samples / signal.symbol, axis=-1, keepdims=True))
    signal.samples = signal.samples * np.exp(-1j*phase)
    
    signal.inplace_normalise()
    noise = signal.samples - signal.symbol

    noise_power = np.sum(np.mean(np.abs(noise) ** 2, axis=-1))
    
    nonlinear_snr = 10 * np.log10((2 - noise_power) / noise_power)



    return nonlinear_snr,signal

def extract_spectrum(name, config_ith):
    import joblib
    from library.electrical import Resampler
    import resampy
    from library import matched_filter
    from scipy.signal import welch

    config = joblib.load('../simulate_data/config_setting')[config_ith]
    signal = QamSignal.load(name,True)
    fibers = fiber_for_reconstruct(config)
    
    signal = cd_compensation(fibers,signal, signal.fs_in_fiber)
    signal.samples = resampy.resample(
        signal[:], signal.sps_in_fiber, 2, axis=-1, filter='kaiser_fast')
    signal = matched_filter(signal, 0.02)
    [f,pxx] = welch(signal.samples[0],detrend=None,return_onesided = False,nfft = 1024)
    signal.inplace_normalise()
    from library.receiver_dsp import LMS_PLL
    from library.receiver_dsp import syncsignal_tx2rx

    lms = LMS_PLL(0.1, 321, 3, 3, 0.0001)
    signal = lms.equalize(signal)
    tx_symbol = syncsignal_tx2rx(signal.samples, signal.symbol)[:,:signal.samples.shape[1]]

    noise = signal.samples - tx_symbol

    noise_power = np.sum(np.mean(np.abs(noise) ** 2, axis=-1))




    # pxx,lms,signal.samples,tx_symbol

    return pxx, lms, signal, tx_symbol
    
def main():
    import os
    from scipy.fft import fft,fftshift
    from scipy.io import savemat
    names = os.listdir('../data/')
    import tqdm
    for name in tqdm.tqdm(names):
        config_ith = int(name.split('.')[0].split('_')[1])
        full_name = '../data/'+name

        pxx,lms,signal_real,symbol = extract_spectrum(full_name,config_ith)
        wxx = np.abs(fftshift(fft(lms.wxx[0])))
        nonlinear_nsr,signal = receiver_nonlinear_noise(full_name,config_ith)
        savemat(f'../extracted_features/{name}',
                {
                   'spec_lms': np.hstack((pxx,wxx)),
                    'target': nonlinear_nsr,
                    'real_rx_samples':signal_real.samples,
                    'real_tx_symbol':symbol,
                    'nli_rx_samples':signal.samples,
                    'nli_tx_symbl':signal.symbol
                }
        )

main()