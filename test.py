# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 10:36:54 2015

@author: hbanks

"Brevity required, prurience preferred."
"""
import numpy as np
import quasioptics as qo
import matplotlib.pylab as plt

plt.close()
#mirr_matrix = np.array([[  21.1,      20.1   ],
#                        [ 227.,      150.    ],
#                        [ 457.2508,   20.32   ],
#                        [  36.61,     12.5   ],
#                        [  100,   23.8064],
#                        [  74.8358,   27.2236]])

mirr_matrix = np.array([[207.52, 7.5], [17.8, 10.], [142.0, 10]])
print mirr_matrix


#m_squared1 = qo.beam([qo.getq([0.2e-3,0,3.8e14]),3.8e14])
bm_waist_initial = 0.2 # must be in mm
freq = 3.8e14 # in Hz I hope
length = 380 # in cm!
#
##total beam path in cm
#length = 450.
#length2 = 250.
#
##total number of points you want to plot
numpts = 20000.
#
##initial beam waist ****IN mm, NOT cm!!!****
#bm_waist_initial = 2.5
#
##frequency in Hz
#freq = 500e9
#
## get beam radius matrix (see lib)
radmat = qo.ezbeam(mirr_matrix, length, numpts, bm_waist_initial, freq)
#radmat2 = qo.ezbeam(mirr_matrix2, length2, numpts, bm_waist_initial, freq)

#plot the beam radius in mm against the distance along beam path
#plt.plot(radmat[:,0]*39.37**0, radmat[:,1])
#plt.plot(radmat2[:,0]*39.37, radmat2[:,1])
#plt.xlabel('Position (in)')
#plt.ylabel('Beam Waist (mm)')
#
#plt.plot([0, length*39.37**0/100], [.25*2.54*10]*2)


plt.plot(radmat[:,0], radmat[:,1])
plt.xlabel('Position (m)')
plt.ylabel('Beam Waist (mm)')
plt.show()

#
#
#
#
##



