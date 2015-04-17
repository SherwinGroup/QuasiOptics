# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 09:59:00 2015

@author: hbanks

"Brevity required, prurience preferred."
"""

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt


plt.close("all")

def  angle_out(angle_in, wavelength, m=1, grat=1800):
    '''
    This will calculate angles in and angles out.
    angle_in is in degrees
    wavelength is in nm
    grat is in /mm
    
    returns: angle_out in degrees
    '''
    a = 1e6 / grat
    return (180 / np.pi) * np.arcsin(m * wavelength / a - np.sin((np.pi / 180) * angle_in))

def location(focus, angle_in, wavelength, center_wl, order=1, grating=1800):
    center_angle = angle_out(angle_in, center_wl, m=order, grat=grating)
    dist = focus * np.tan((np.pi / 180) * (angle_out(angle_in, wavelength, m=order, grat=grating) - center_angle))
    return dist

angles = np.linspace(0, 90, 500)

"""
for elem in [700, 750, 800, 850, 900, 950, 1000]:
    plt.plot(angles, angle_out(angles, elem))
"""

wavelengths = np.linspace(700, 850, 300)
#for angle in [45, 60]:
plt.plot(wavelengths, location(60, 60, wavelengths, 775))
plt.plot(wavelengths, location(125, 45, wavelengths, 775, grating=1200))
plt.show()

print "For 1200 grating, ", location(125, 45, 765, 775, grating=1200) - location(125, 45, 764, 775, grating=1200)
print "For 1800 grating, ", location(60, 60, 765, 775) - location(60, 60, 764, 775)