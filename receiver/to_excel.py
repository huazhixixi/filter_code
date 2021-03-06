import numpy as np
from scipy.signal import correlate
from scipy.io import loadmat

import pandas as pd
import os





import os
import sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools import calc_gn_model,calc_xdb_bandwidth,calc_anc
basedir = '../extracted_features/'
names = os.listdir(basedir)

res = []
import tqdm

for name in tqdm.tqdm(names, ascii=True):
    try:
        data = loadmat(basedir + name)
    except Exception:
        print(name)
        continue

    config_ith = int(name.split('.')[0].split('_')[-1])
    import joblib
    try:
        config = joblib.load('../simulate_data/config_setting')[config_ith]
    except Exception:
        continue

    target = data['target']
    x = data['freqs'][0]
    spec = data['spec_lms'][0,:1024]
    bandwidth_3db,freq1_3,freq2_3 = calc_xdb_bandwidth(x, spec, 3)
    bandwidth_6db,freq1_6,freq2_6 = calc_xdb_bandwidth(x,spec,6)
    xielv1 = 3 / (freq1_3 - freq1_6)
    xielv2 = 3 / (freq2_3 - freq2_6)
    filter_tap = data['spec_lms'][0, 1024:]
    gn_res = calc_gn_model(config=config)

    feature = filter_tap.tolist()
    feature.insert(0,bandwidth_3db)
    feature.insert(0,bandwidth_6db)
    feature.insert(0,gn_res)
    feature.insert(0,xielv1)
    feature.insert(0,xielv2)
    feature.append(target[0,0])
    
    no_filter_samples = data['nli_rx_samples']
    no_filter_symbol = data['nli_tx_symbl']

    amplitude_noise = np.abs(no_filter_samples) - np.abs(no_filter_symbol)
    phase_noise = np.angle(no_filter_samples/no_filter_symbol)

    anc_xy = 10*np.log10(1/np.abs(calc_anc(amplitude_noise,1)))
    anc_xx = 10*np.log10(1/np.abs(calc_anc(np.vstack((amplitude_noise[0], amplitude_noise[0])),None)))
    pnc_xy = 10*np.log10(1/np.abs(calc_anc(phase_noise,1)))
    pnc_xx = 10*np.log10(1/np.abs(calc_anc(np.vstack((phase_noise[0], phase_noise[0])),None)))


    filter_samples = data['real_rx_samples']
    filter_symbol = data['real_tx_symbol']
    amplitude_noise = np.abs(filter_samples) - np.abs(filter_symbol)
    phase_noise = np.angle(filter_samples)/np.angle(filter_symbol)

    anc_xy_filtered = 10*np.log10(1/np.abs(calc_anc(amplitude_noise,1)))
    anc_xx_filtered = 10*np.log10(1/np.abs(calc_anc(np.vstack((amplitude_noise[0], amplitude_noise[0])),None)))
    pnc_xy_filtered = 10*np.log10(1/np.abs(calc_anc(phase_noise,1)))
    pnc_xx_filtered = 10*np.log10(1/np.abs(calc_anc(np.vstack((phase_noise[0], phase_noise[0])),None)))

    # anc_xx = 0
    # anc_xy = 0
    # pnc_xy = 0
    # pnc_xx = 0

    anc_xx_modified = anc_xx_filtered - anc_xx
    anc_xy_modified = anc_xy_filtered - anc_xy
    pnc_xx_modified = pnc_xx_filtered - pnc_xx
    pnc_xy_modified = pnc_xy_filtered - pnc_xy

    # feature.append(anc_xy_modified)
    # feature.append(anc_xx_modified)
    # feature.append(pnc_xx_modified)
    # feature.append(pnc_xy_modified)

    feature.append(anc_xx)
    feature.append(anc_xy)
    feature.append(pnc_xx)
    feature.append(pnc_xy)

    res.append(feature)

data = pd.DataFrame(np.array(res))
data.to_csv('./feature_target_true_anc_pnc_target.csv',index=None,header=None)
