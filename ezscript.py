import numpy as np
import quasioptics as qo
import matplotlib.pylab as plt

#in cm, except beam waist!!
#This is an example of what I get with the VNA setup at one of the bands


fil = 'THzHFTSoptics.txt'

with open(fil, 'r') as f:
    h = f.readlines()[:6]

wavelength = float(h[1][len(h[1])-h[1][::-1].find(' '):-1]) #mm
startingPoint = float(h[4][len(h[4])-h[4][::-1].find(' '):-1])/10
bm_waist_initial = float(h[3][len(h[3])-h[3][::-1].find(' '):-1])
length = float(h[5][len(h[5])-h[5][::-1].find(' '):-1])/10
freq = 2.998E11/wavelength
print freq
    



data = np.genfromtxt(fil, skiprows = 7, delimiter = ',')
data = np.fliplr(data/10) #/10 to account for mm in VI to cm here
data[:, 0] = data[:, 0] - startingPoint
# Change distance to relative instead of absolute
for i in range(len(data)-1, 0, -1):
    data[i,0] = data[i, 0] - data[i-1, 0]
    
mirr_matrix = data
#mirr_matrix = np.array([[  21.1,      20.1   ],
# [ 227.,      150.    ],
# [ 457.2508,   20.32   ],
# [  36.61,     12.5   ],
# [  100,   23.8064],
# [  74.8358,   27.2236]])
print mirr_matrix

nickMat = mirr_matrix*10
nickMat[:, 0] = np.cumsum(mirr_matrix[:, 0]*10) + startingPoint*10
nickMat = np.fliplr(nickMat)
for i in nickMat:
    print '{}, {}'.format(i[0], i[1])



#
##total beam path in cm
#length = 450.
#length2 = 250.
#
##total number of points you want to plot
numpts = 10000.
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


plt.plot(radmat[:,0]+startingPoint/100, radmat[:,1])
plt.xlabel('Position (m)')
plt.ylabel('Beam Waist (mm)')
plt.show()

#
#
#
#
##












