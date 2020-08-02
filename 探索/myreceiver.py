import numpy as np
from scipy.io import loadmat

from library import QamSignal, LinearFiber, cd_compensation
from tools import fiber_for_reconstruct


def __reconstruct_signal(name):
    fibers = [LinearFiber(0.2,16.7,80,0,1550) for _ in range(12)]
    signal = QamSignal.load(name, True)
    data = loadmat(name)
    tx_samples = data['tx_samples']
    nonlinear_noise = data['nonlinear_noises_each_span']
    signal.samples = tx_samples

    for fiber_idx, fiber in enumerate(fibers):
        signal = fiber.prop(signal)
        signal[:] = np.sqrt(10 ** ((fiber.alpha * fiber.length) / 10)) * signal[:]
        signal[:] += nonlinear_noise[fiber_idx]
    return signal


def receiver_nonlinear_noise(name):
    import joblib
    from library.electrical import Resampler
    import resampy
    from library import matched_filter


    signal = __reconstruct_signal(name)
    fibers = [LinearFiber(0.2,16.7,80,0,1550) for _ in range(12)]

    signal = cd_compensation(fibers, signal, signal.fs_in_fiber)
    signal.samples = resampy.resample(
        signal[:], signal.sps_in_fiber, 2, axis=-1, filter='kaiser_fast')

    signal = matched_filter(signal, 0.02)
    signal.samples = signal[:, ::2]

    phase = np.angle(np.mean(signal.samples / signal.symbol, axis=-1, keepdims=True))
    signal.samples = signal.samples * np.exp(-1j * phase)

    signal.inplace_normalise()
    noise = signal.samples - signal.symbol

    noise_power = np.sum(np.mean(np.abs(noise) ** 2, axis=-1))

    nonlinear_snr = 10 * np.log10((2 - noise_power) / noise_power)

    return nonlinear_snr, signal,noise
nonlinear_snr_wss1 , signal1 , noise1 = receiver_nonlinear_noise('./data/3_1.mat')
nonlinear_snr_wss2 , signal2 , noise2 = receiver_nonlinear_noise('./data/3_2.mat')
nonlinear_snr_wss3 , signal3 , noise3 = receiver_nonlinear_noise('./data/3_3.mat')
nonlinear_snr_wss4 , signal4 , noise4 = receiver_nonlinear_noise('./data/3_4.mat')
nonlinear_snr_wss6 , signal6 , noise6 = receiver_nonlinear_noise('./data/3_6.mat')

print(nonlinear_snr_wss1)
print(nonlinear_snr_wss2)
print(nonlinear_snr_wss3)
print(nonlinear_snr_wss4)



import matplotlib.pyplot as plt
with plt.style.context(['ieee','science','high-vis','no-latex']):
    plt.psd(noise1[0],label='12WSS',)
    plt.psd(noise2[0],label = '6WSS')
    plt.psd(noise3[0],label = '4WSS')
    plt.psd(noise4[0],label = '3WSS')

    plt.legend()

    plt.show()

