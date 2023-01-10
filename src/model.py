from typing import Callable
import arviz as az
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pymc3 as pm
import pymc3.distributions as D

"""
i = trial
j = participant
k = experiment
x = true initial distance
x_{i, j}^{per} = uncertain perceived puck distance
t^{pre} = measured press-time measured on trial i
m_{j, k} = belief about the mass of the puck (dependent on color and phase of experiment k)

p(d, l) = joint distributions
d = {x, t^{pre}} -> observed data
l = {x^{per}, \sigma^{x}, m \sigma^{t}} -> latent variables
"""


class NewtonianModel:
    def __init__(self, data: np.ndarray) -> None:
        self.model = pm.Model('NewtonianModel')
        self.data = data
        self.n_trials, self.n_participants, self.n_experiments = data.shape

    def newtonian(self, puck_mass: np.ndarray, surface_friction: float) -> float:
        ...
    

    def build_model(self, **params) -> pm.Model:
        with self.model:
            assert all(filter(lambda x: x is not None, params.values()))
            perceptual_dist_uncertainties = params.get('x_ij', None)
            sigma_x = params.get('sigma_dist', None)
            friction_coeff = params.get('friction', 1.)

            perceptual_dist_uncertainties = pm.Deterministic('x_ij', perceptual_dist_uncertainties)
            sigma_x = pm.Deterministic('sigma^x', 5e-2)
            x_percept = pm.LogNormal('x_ij^per', perceptual_dist_uncertainties,
                                     sigma_x,
                                     shape=(self.n_trials, self.n_participants),
                                     observed=self.data)


            puck_mass = pm.Gamma('m_jk', 6, 2.5, shape=(self.n_participants, self.n_experiments))
            # tijk
            newtonian = pm.Deterministic('t^int', self.newtonian(puck_mass, friction_coeff))


            sigma_t = pm.Gamma('sigma^t', 1.2, 5, shape=self.n_participants)
            # tpre
            # log-normal
            observed_press_time = pm.LogNormal(newtonian, 
                                               sigma_t,
                                               shape=(self.n_trials, self.n_participants))
            


        return self.model


