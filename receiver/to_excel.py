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
basedir = '../data/'
names = os.listdir(basedir)

res = []
import tqdm

for name in tqdm.tqdm(names, ascii=True):
    try:
        data = loadmat(basedir + name)
    except Exception:
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
    feature.append(target)
    
    # no_filter_samples = data['nli_rx_samples']
    # no_filter_symbol = data['nli_tx_symbol']

    # amplitude_noise = np.abs(no_filter_samples) - np.abs(no_filter_symbol)
    # phase_noise = np.angle(no_filter_samples)/np.angle(no_filter_symbol)
    # anc_xy = calc_anc(amplitude_noise)
    # anc_xx = calc_anc(np.vstack((amplitude_noise[0], amplitude_noise[0])))
    # pnc_xx = calc_anc(phase_noise)
    # pnc_yy = calc_anc(np.vstack((phase_noise[0], phase_noise[0])))
    
    # filter_samples = data['real_rx_samples']
    # filter_symbol = data['real_tx_symbol']
    # amplitude_noise = np.abs(filter_samples) - np.abs(filter_symbol)
    # phase_noise = np.angle(filter_samples)/np.angle(filter_symbol)
    # anc_xy_filtered = calc_anc(amplitude_noise)
    # anc_xx_filtered = calc_anc(np.vstack((amplitude_noise[0], amplitude_noise[0])))
    # pnc_xx_filtered = calc_anc(phase_noise)
    # pnc_yy_filtered = calc_anc(np.vstack((phase_noise[0], phase_noise[0])))
    




    res.append(feature)

data = pd.DataFrame(np.array(res))
data.to_csv('./feature_target.csv',index=None,header=None)
