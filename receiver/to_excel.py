import numpy as np
from scipy.signal import correlate
from scipy.io import loadmat

import pandas as pd
import os
from library.gn_model import  Span as GnSpan,Signal as GnSignal
#
# FIBER = {
#     1: {"alpha": 0.2, 'D': 16.7, 'gamma': 1.3},
#     2: {"alpha": 0.18, "D": 20.1, "gamma": 0.9},
#     3: {"alpha": 0.21, "D": 4.3, "gamma": 1.47}
# }
#
#
#
# def calc_gn_res(config_ith):
#     import joblib
#     config = joblib.load('../simulate_data/config_setting')[config_ith]
#
#
# basedir = '../extracted_features/'
# names = os.listdir(basedir)
#
# res = []
# import tqdm
#
# for name in tqdm.tqdm(names,ascii=True):
#     data = loadmat(basedir+name)
#     feature = data['spec_lms']
#     target = data ['target']
#     fea_target = np.hstack((feature,target))
#     res.append(fea_target[0].tolist())
#
# data = pd.DataFrame(np.array(res))
# data.to_csv('./spec_lms.csv',index=None,header=None)





def calc_anc(noise):
    noise_1 = noise[0]
    noise_2 = noise[1]
    correlation_sequence = correlate(noise_1,noise_2)/len(noise_1)
    arg_max = np.argmax(correlation_sequence)
    correlation_sequence = correlation_sequence[arg_max]
    return correlation_sequence

basedir = '../extracted_features/'
names = os.listdir(basedir)

res = []
import tqdm

for name in tqdm.tqdm(names,ascii=True):
    data = loadmat(basedir+name)
    # feature = data['spec_lms']
    # target = data ['target']
    # fea_target = np.hstack((feature,target))
    # res.append(fea_target[0].tolist())




data = pd.DataFrame(np.array(res))
data.to_csv('./spec_lms.csv',index=None,header=None)


