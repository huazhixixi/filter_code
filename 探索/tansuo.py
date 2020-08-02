import numpy as np
import matplotlib.pyplot as plt
from library.channel import NonlinearFiber
from library import ConstantGainEdfa,WSS
from simulate_data.main import simulate_one_span,genreate_signal
from library.channel import LinearFiber



def generate_instruments(jiange):

    ins = []
    span_cnt = 0
    for i in range(12):
        ins.append(NonlinearFiber(0.2,16.7,80,1550,0,'single'))
        ins.append(ConstantGainEdfa(16,5,True))
        span_cnt+=1
        if not divmod(span_cnt,jiange)[1]:
            ins.append(WSS(0,37.5e9,8.8e9))
    
    return ins


def main(base_dir):
    import copy
    for jiange in [1,2,3,4,6]:

        for signal_power in range(4):
            nonlinear_noises = []
            span_cnt = 0
            signal = genreate_signal(signal_power)
            tx_samples = copy.deepcopy(signal.samples)

            for span_index in range(12):
                span_cnt+=1
                edfa = ConstantGainEdfa(gain= 16, nf=5, is_ase=True)
                nonlinear_fiber = NonlinearFiber(0.2,16.7,80,1550,0,'single')
                linear_fiber = LinearFiber(0.2,16.7,80,0,1550)
                if not divmod(span_cnt,jiange)[1]:
                    wss = WSS(0, 37.5e9, 8.8e9)
                else:
                    wss = None
                signal, nonlinear_noise_one_span = simulate_one_span(signal,linear_fiber, nonlinear_fiber, edfa, wss)

                nonlinear_noises.append(nonlinear_noise_one_span)


            signal.save(f'{base_dir}/{signal_power}_{jiange}', is_mat_file=True)

            from scipy.io import loadmat, savemat

            data = loadmat(f'{base_dir}/{signal_power}_{jiange}.mat')
            data['nonlinear_noises_each_span'] = np.array(nonlinear_noises)
            data['tx_samples'] = tx_samples

            savemat(f'{base_dir}/{signal_power}_{jiange}.mat', data)

main('./data/')