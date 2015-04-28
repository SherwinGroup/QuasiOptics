# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 20:22:10 2015

@author: dreadnought

"Brevity required, prurience preferred"
"""

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt


def theta_out(theta_in, m, grate, wavelength):
    '''
    returns the output angle of the incoming light
    
    I think I want m = +1?  It seems that there aren't a lot of geometries that
    have allowed lines at m < 0
    '''
    a = 1e6/grate
    return (180 / np.pi) * np.arcsin((m * wavelength / a) - np.sin((np.pi / 180) * theta_in))

def distance(output, focus):
    return focus * np.tan((np.pi / 180) * (output - theta_out(60, 1, 1800, 775)))

theta_in = np.linspace(0, 90, num=1000)

plt.close()
wavelength = np.linspace(700, 850, num=300)

#plt.plot(theta_in, theta_out(theta_in, 1, 1800, 850) - theta_in)
"""
for wavelength in [700, 750, 800, 850]:
    plt.plot(theta_in, theta_out(theta_in, 1, 1800, wavelength))
"""


plt.plot(wavelength, distance(theta_out(60, 1, 1800, wavelength), 75))

#plt.xlim(45, 90)
plt.show()

print distance(theta_out(60, 1, 1800, 765), 75) - distance(theta_out(60, 1, 1800, 763), 75)