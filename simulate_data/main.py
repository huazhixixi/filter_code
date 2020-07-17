from library.channel import LinearFiber
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from library import QamSignal
from library import NonlinearFiber
from library import WSS
from library import ConstantGainEdfa, Laser
import numpy as np
import copy

FIBER = {
    1: {"alpha": 0.2, 'D': 16.7, 'gamma': 1.3},
    2: {"alpha": 0.18, "D": 20.1, "gamma": 0.9},
    3: {"alpha": 0.21, "D": 4.3, "gamma": 1.47}
}

base_dir = '../data'

def simulate_one_span(signal, linear_fiber, nonlinear_fiber, edfa, wss):
    second_signal = copy.deepcopy(signal)
    # nonlinear prop
    signal = nonlinear_fiber.prop(signal)
    signal = edfa.prop(signal)
    power_now = np.sum(np.mean(np.abs(signal.samples) ** 2, axis=-1))
    signal = wss.prop(signal)
    power_after = np.sum(np.mean(np.abs(signal.samples) ** 2, axis=-1))
    gain = np.sqrt(power_after / power_now)
    signal[:] = gain * signal[:]
    import cupy as cp
    noise_sequence = copy.deepcopy(edfa.noise_sequence)
    noise_sequence = cp.asnumpy(noise_sequence)
    # linear prop
    second_signal = linear_fiber.prop(second_signal)
    second_signal[:] = np.sqrt( 10 ** ((linear_fiber.alpha * linear_fiber.length) / 10)) * second_signal[:]
    second_signal[:] += noise_sequence
    power_now = np.sum(np.mean(np.abs(second_signal.samples) ** 2, axis=-1))
    second_signal = wss.prop(second_signal)
    power_after = np.sum(np.mean(np.abs(second_signal.samples) ** 2, axis=-1))
    gain = np.sqrt(power_after / power_now)
    second_signal[:] = gain * second_signal[:]
    signal.cpu()
    return signal, signal[:] - second_signal[:]


def genreate_signal(signal_power):
    signal = QamSignal(16, 35e9, 2, 4, 65536, 2)
    signal.prepare(0.02)
    laser = Laser(0, None, 193.1e12, signal_power)
    signal = laser.prop(signal)
    return signal



def simulate(config,config_ith,power):

    #power = config[0]
    nonlinear_fibers = []
    linear_fibers = []
    nonlinear_noises = []
    signal = genreate_signal(power)
    tx_samples = copy.deepcopy(signal.samples)
    for kind in config[1:]:
        alpha = FIBER[kind]['alpha']
        D = FIBER[kind]['D']
        gamma = FIBER[kind]['gamma']

        nonlinear_fibers.append(NonlinearFiber(alpha, D, 80, 1550, 0, 'single',gamma=gamma))

        linear_fibers.append(LinearFiber(alpha,D,80,0,1550))
    
    for linear_fiber,nonlinear_fiber in zip(linear_fibers,nonlinear_fibers):
        edfa = ConstantGainEdfa(gain=nonlinear_fiber.length * nonlinear_fiber.alpha, nf=5, is_ase=True)
        wss = WSS(0,37.5e9,8.8e9)
        signal, nonlinear_noise_one_span = simulate_one_span(signal, linear_fiber, nonlinear_fiber, edfa, wss)
        
        nonlinear_noises.append(nonlinear_noise_one_span)

    signal.save(f'{base_dir}/{power}_{config_ith}', is_mat_file=True)
    
    from scipy.io import loadmat,savemat
    data = loadmat(f'{base_dir}/{power}_{config_ith}.mat')
    data['nonlinear_noises_each_span'] = np.array(nonlinear_noises)
    data['tx_samples'] = tx_samples

    savemat(f'{base_dir}/{power}_{config_ith}.mat', data)
    
import tqdm
    
def main(config_name):
    import joblib
    total_config = joblib.load(config_name)
    # 此处可以开多进程
    for power in tqdm.tqdm(range(4)):
        config = total_config[0]
        simulate(config,0,power)


main('config_setting')