import numpy as np

import matplotlib.pyplot as plt

import pandas as pd

data = pd.read_csv('feature_target_anc_pnc_target.csv',header=None)
data = data.values

gn_res = data[:,2]
real_nli = data[:,-5]

