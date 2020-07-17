import joblib

import numpy as np 
def generate_config():
    config = set()
    while True:
        power = np.random.randint(0,5)
        span_number = np.random.randint(1,15)
        span_kind = []
        for i in range(span_number):
            span_kind.append(np.random.choice([1,2,3]))

        span_kind.insert(0,power)
        config.add(tuple(span_kind))

        if len(config)>2000:
            break

    config = list(config)
    return config

config = generate_config()
import joblib
joblib.dump(config,'config_setting')