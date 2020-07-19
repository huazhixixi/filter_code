import numpy as np
from scipy.signal import correlate
from scipy.io import loadmat

import pandas as pd
import os

basedir = '../extracted_features/'
names = os.listdir(basedir)

res = []
import tqdm

for name in tqdm.tqdm(names,ascii=True):
    data = loadmat(basedir+name)
    feature = data['spec_lms']
    target = data ['target']
    fea_target = np.hstack((feature,target))
    res.append(fea_target[0].tolist())

data = pd.DataFrame(np.array(res))
data.to_csv('./spec_lms.csv',index=None,header=None)
