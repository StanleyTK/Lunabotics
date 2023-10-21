# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 16:58:58 2023

@author: c5all
"""

import numpy as np
from scipy.stats import multivariate_normal

"""
particle_set = particle set
particle = single particle
N = number of particles
particle = state vector
z = observation set
t = time
h = observation model
f = state transition model
u = control inputs
w = weight
Q = covariance matrix of process noise (uncertainty in state transition model)
R = covariance matrix of observation noise (uncertainty in observation model)
H = jacobian that linearizes the measurement model around the particle estimate
"""

def calc_weight(N, t, z, h, p):
    w = np.ones(N) / N
    for i in range(N):
        likelihood = np.exp(-0.5 * (z[t] - h(p[i, t, :], np.random.normal(0, 0.1)))**2)
        w[i, t] = w[i, t-1] * likelihood / np.sum(w[:, t-1] * likelihood)
    return w

# State transition function
def f(pre_particle, u, w):
    A = np.array([[1, 1], [0, 1]])
    B = np.array([[0.5], [1]])
    f = np.dot(A, pre_particle) + np.dot(B, u) + w
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
def calc_covariance_Q(particle, w):
    
    Q = np.cov(particle, aweights=w)
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
        
        # Resample particles
        w = particle_set[:,-1]
        w /= np.sum(w)
        new_particles = np.zeros_like(particle_set)
        idx = np.random.choice(range(N), size=N, replace=True, p=w)
        new_particles[:,:] = particle_set[idx,:]
        particle_set[:,:] = new_particles
    
    return particle_set

    