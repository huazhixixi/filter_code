from library import NonlinearFiber, LinearFiber
import numpy as np
import visdom
FIBER = {
    1: {"alpha": 0.2, 'D': 16.7, 'gamma': 1.3},
    2: {"alpha": 0.18, "D": 20.1, "gamma": 0.9},
    3: {"alpha": 0.21, "D": 4.3, "gamma": 1.47}
}



def calc_anc(noise,sequence_length):
    from scipy.signal import correlate
    noise_1 = noise[0]
    noise_2 = noise[1]
    correlation_sequence = correlate(noise_1,noise_2)/len(noise_1)
    arg_max = np.argmax(correlation_sequence)
    correlation_sequence = correlation_sequence[arg_max:]
    if sequence_length == 1:
        correlation_sequence = correlation_sequence[0]
    else:
        correlation_sequence = correlation_sequence[1]
    return correlation_sequence


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



def calc_gn_model(config):
    import joblib
    from library.gn_model import Signal as GnSignal
    from library.gn_model import Span as GnSpan
    from library.gn_model import Edfa as GnEdfa
    power = config[0]
    power_lin = (10 ** (power / 10)) * 0.001
    # print(power_lin)
    baud_rate = 35e9
    space = 50e9
    sigs = [
            GnSignal(signal=power_lin, nli=0, ase=0, carri=193.1e12 + j * space, baudrate=baud_rate, number=j, mf='dp-16qam')

            for j in range(1)]

    spans = []
    edfas = []

    span_config = config[1:]
    for span_kind in span_config:
        alpha = FIBER[span_kind]['alpha']
        D = FIBER[span_kind]['D']
        gamma = FIBER[span_kind]['gamma']

        spans.append(GnSpan(length=80, D=D, gamma=gamma, lam=1550e-9, alpha=alpha))
        edfa = GnEdfa(gain=spans[-1].alpha * spans[-1].length, nf=5)
        edfas.append(edfa)
    center_channel = sigs[int(np.floor(len(sigs)/2))]

    for idx, span in enumerate(spans):
        span.prop(center_channel, sigs)
        edfas[idx].prop(center_channel)        

    snr = center_channel.signal / (center_channel.nli + 0)
    
    return 10 * np.log10(snr)
    



def main():
    from scipy.io import loadmat
    x = loadmat('./data/0_1.mat')['freqs'][0]
    spec = loadmat('./data/0_1.mat')['spec_lms'][0,:1024]
    bandwidth_3db,freq1_3,freq2_3 = calc_xdb_bandwidth(x, spec, 3)
    bandwidth_6db,freq1_6,freq2_6 = calc_xdb_bandwidth(x,spec,6)
    xielv1 = 3 / (freq1_3 - freq1_6)
    xielv2 = 3 / (freq2_3 - freq2_6)




    print('hello world')
if __name__ == '__main__':
    main()

    
    
