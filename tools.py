from library import NonlinearFiber,LinearFiber
FIBER = {
    1: {"alpha": 0.2, 'D': 16.7, 'gamma': 1.3},
    2: {"alpha": 0.18, "D": 20.1, "gamma": 0.9},
    3: {"alpha": 0.21, "D": 4.3, "gamma": 1.47}
}

def fiber_for_reconstruct(config):
    fibers = []
    for kind in config[1:]:
        alpha = FIBER[kind]['alpha']
        D = FIBER[kind]['D']
        gamma = FIBER[kind]['gamma']

        fibers.append(LinearFiber(alpha,D,80,0,1550))

    return fibers
