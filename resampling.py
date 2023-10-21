import numpy as np
from numpy.random import random

def resampling(Xt, Wt):
    
    N = len(Wt)
    positions = (random(N) + range(N)) / N

    indexes = np.zeros(N, 'i')
    cumulative_sum = np.cumsum(Wt)
    i , j = 0, 0
    while i < N:
        if positions[i] < cumulative_sum[j]:
            indexes[i] = j
            i += 1
        else:
            j += 1
        
    return Xt[indexes]

if __name__ == '__main__':

    Xt = np.array([1, 12, 3, 4, 5])
    Wt = np.array([0.1, 0.2, 0.2, 0.2, 0.3])

    sample = resampling(Xt, Wt)

    print(sample)