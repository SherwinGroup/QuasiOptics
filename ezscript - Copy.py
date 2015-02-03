import numpy as np
import quasioptics as qo
import matplotlib.pylab as plt

#in cm, except beam waist!!
#This is an example of what I get with the VNA setup at one of the bands



data = np.genfromtxt('ParametersToReference.txt', skiprows = 7, delimiter = ',')
data = np.fliplr(data/10) #/10 to account for mm in VI to cm here
data[:, 0] = data[:, 0] - data[0, 0] + 1
# Change distance to relative instead of absolute
for i in range(len(data)-1, 0, -1):
    data[i,0] = data[i, 0] - data[i-1, 0]
    
mirr_matrix = data
print mirr_matrix
#
#
#data2 = np.genfromtxt('ParametersToReference.txt', skiprows = 7, delimiter = ',')
#data2 = np.fliplr(data2/10) #/10 to account for mm in VI to cm here
## Change distance to relative instead of absolute
#for i in range(len(data2)-1, 0, -1):
#    data2[i,0] = data2[i, 0] - data2[i-1, 0]
#    
#mirr_matrix2 = data2
#print mirr_matrix2
#
#
#
#Originals
#                    mirr_matrix = np.array([
#                            [116.84, 20.32],
#                            [33.02, 12.5],
#                            [50.8, 15.24],
#                            [27.94, 12.5],
#                            [15.24, 20.32]
#                            ])
#                            
#                    mirr_matrix2 = np.array([
#                        [116.84, 20.32],
#                        [33.02, 12.5],
#                        [43.18, 12.5]
#                        ])


#mirr_matrix = np.array([
#        [46., 20.32],
#        [13., 12.5],
#        [20., 15.24],
#        [11., 12.5],
#        [6., 20.32]
#        ])

#mirr_matrix2 = np.array([
#        [46., 20.32],
#        [13., 12.5],
#        [20., 15.24],
#        [12., 12.5],
#        [6., 20.32]
#        ])

#mirr_matrix2 = np.array([
#    [46., 20.32],
#    [13., 12.5],
#    [17., 12.5],
#    [8, 2*2.54]
#    ])
#    
#mirr_matrix = np.array([
#    [46., 20.32],
#    [14., 12.5],
#    [17., 12.5], 
#    [8, 2*2.54]
#    ])


#mirr_matrix[:, 0] = mirr_matrix[:, 0] * 2.54 
#mirr_matrix2[:, 0] = mirr_matrix2[:, 0] * 2.54 
#print mirr_matrix2

#mirr_matrix = mirr_matrix2
#first column: mirror locations relative to the previous mirror, in cm
#  (the first one is the relative distance of the first mirror to the beginning of beam)
#second column: focal length of mirror in cm
#mirr_matrix = np.array([
#    [25., 25.],
#    [37.5, 12.5],
#    [25., 12.5],
#    [37.5, 25.],
#    [25, 12.5]])

#total beam path in cm
length = 450.
length2 = 250.

#total number of points you want to plot
numpts = 10000.

#initial beam waist ****IN mm, NOT cm!!!****
bm_waist_initial = 2.5

#frequency in Hz
freq = 500e9

# get beam radius matrix (see lib)
radmat = qo.ezbeam(mirr_matrix, length, numpts, bm_waist_initial, freq)
#radmat2 = qo.ezbeam(mirr_matrix2, length2, numpts, bm_waist_initial, freq)

#plot the beam radius in mm against the distance along beam path
plt.plot(radmat[:,0]*39.37**0, radmat[:,1])
#plt.plot(radmat2[:,0]*39.37, radmat2[:,1])
plt.xlabel('Position (in)')
plt.ylabel('Beam Waist (mm)')

plt.plot([0, length*39.37**0/100], [.25*2.54*10]*2)

plt.show()


















