import numpy as np
from random import sample
import math
from scipy.stats import multivariate_normal
from numpy.random import random

def calc_weight(Zt, Q, Zt_1):
    # Q = 1                               # measument covariance
    # Zt_1 = 10                           # predicted Zt

    # w = target(xt) / proposal(xt)

    Wt = (2*math.pi * Q)**(-1/2) * math.exp(-1/2 * (Zt - Zt_1)**2 / Q * (Zt - Zt_1))
    # how to compute weight? Gaussian with replace sigma to Q and x - u with Zt and predicted Zt
    return 1

def varience(mu_d, J): # sigma calc eq
    return (1 / J - 1) * mu_d

def creating_particles(pre_particle, Ut, Zt, Ct): # form of Ut and Zt gotta be different format. This is just for referace.

    # every sample should have : pose(x,y,z), weight, landmarks(list of 2 by 2 kalman filter)
    
    N = 10    # N number of sample, particle created.
    sigma = 3 # Tune or calc??
    Particle_bar = 0
    mu_d = 0
    
    particle_set = np.zeros(N,1) #[x,y,theta, weight]

    for n in range(N):
        x = np.random.normal(pre_particle + Ut, sigma, 1) # Obtain new x value for new sample #starts from uniform distribution
        y = np.random.normal(pre_particle + Ut, sigma, 1) #Obtains new y value for new sample
        theta = np.random.normal(pre_particle + Ut, sigma, 1) #Between 0 and 2pi radians
        
        particle = [x,y,theta]
        
        mu_d += (particle - (pre_particle + Ut))**2 # if we have to do sigma calc, NOT BEING USED IRRELEVANT DONT PAY ATTENTION


    #     ----------------------landmark, Ct-------------------------------
    #     if Ct never seen before: 
    #         1. initialize mean = mu
    #         2. calculate Jacobian = H 
    #         3. initialize covariance
    #         4. default importance weight

    #     else:
    #         <EKF-update> // update landmark # first compute weight and update the map??
    #             measurement prediction = Z_hat
    #             calculate Jacobian = H
    #             measurment covariance = Q
    #             calculate Kalman gain = K
    #             update mean = mu
    #             update covariance
    
        Wt = calc_weight(Zt, 1, 1) # calc weight
        Particle_bar += np.dot(particle, Wt) # predicted pos. assume Wt is probability. We can ignore this(can be replaced by resampling step)

        particle.append(Wt)
        particle_set[N] = particle
    
    
    sigma = varience(mu_d, N)
    particle = resampling(Particle_bar, Particle_bar[n][1]) # resampling from sample set. Need to be fixed

    return particle_set, Particle_bar, sigma

# State transition function
def f(pre_particle, u, Wt):
    A = np.array([[1, 1], [0, 1]])
    B = np.array([[0.5], [1]])
    f = np.dot(A, pre_particle) + np.dot(B, u) + Wt
    return f

# Observation function
def h(particle, v):
    C = np.array([1, 0])
    h = np.dot(C, particle) + v
    return h

# Jacobian calculation function
def calc_jacobian(particle_set, h):
    num_diff = 1e-6
    N = particle_set.shape[0]
    m = h(particle_set).shape[0]
    H = np.zeros((m,N))
    for i in range(N):
        particle_i = particle_set.copy()
        particle_i[i] += num_diff
        H[:,i] = (h(particle_i) - h(particle_set)) / num_diff
    return H

# Calculates covariance matrix for process noise
def calc_covariance_Q(particle, Wt):
    Q = np.cov(particle, aweights=Wt)
    return Q

# Calculates covariance matrix for observation noise
def calc_covariance_R(z):
    z_mean = np.mean(z, axis=1)
    z_diff = z - z_mean.reshape(-1, 1)
    R = np.cov(z_diff)
    return R

# Particle filter algorithm
def particle_update(particle_set, N, u, t, h, f, Q, R, H):
    if t == 0:
        for i in range(N):
            particle_set[i,0] = np.array([0., 0., 0.])
            particle_set[i,1:-1] = np.random.normal(0., 1., size=(particle_set.shape[1]-2)//2)
            particle_set[i,-1] = 1./N
    
    # Predict step
    for i in range(N):
        particle_set[i,0:3] = f(particle_set[i,0:3], particle_set[i,3:])
        particle_set[i,3:] = np.random.multivariate_normal(np.zeros(Q.shape[0]), Q)
    
    # Update step
    for obs in u:
        for i in range(N):
            # Compute weight for particle i
            z_hat = h(particle_set[i,0:3])
            J = H(particle_set[i,0:3])
            S = np.dot(np.dot(J, particle_set[i,3:-1].reshape(-1,2)), J.T) + R
            K = np.dot(np.dot(particle_set[i,3:-1].reshape(-1,2), J.T), np.linalg.inv(S))
            particle_set[i,-1] = multivariate_normal.pdf(obs, mean=z_hat, cov=S) # likelihood
            particle_set[i,3:-1] = np.reshape(particle_set[i,3:-1].reshape(-1,2) + np.dot(K, (obs - z_hat).reshape(-1,1)).flatten(), (-1,)) # update landmark estimates
        
            # Wt = calc_weight(Zt, prev_Q, Zt_1) # calc weight
    #         # keep unobserved ladmark unchanged
    # end for loop
    # resampling and get Xt

def resampling(particle_set):
    
    N = len(particle_set[3])
    positions = (random(N) + range(N)) / N

    indexes = np.zeros(N, 'i')
    cumulative_sum = np.cumsum(particle_set[3])
    i , j = 0, 0
    while i < N:
        if positions[i] < cumulative_sum[j]:
            indexes[i] = j
            i += 1
        else:
            j += 1
        
    return particle_set[indexes]

if __name__ == '__main__':

    particle_set = creating_particles()
    print("particle_set =\n", particle_set)

    sample = resampling(particle_set)
    print(sample)
