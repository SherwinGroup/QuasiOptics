import numpy as np

def getq(w, z, freq):
    '''
    This is for converting more common beam parameters (w, z, freq) to complex beam parameter.
    w is the beam waist
    z is the distance along the beam path
    freq is the frequency

    mks units
    '''
    return z+1j*np.pi*w**2*freq/2.9979e8

class beam(object):
    '''
    This class is just for INITIALIZING a beam. It goes into the network class.
    This is NOT for propagating the beam -- that is done with the network methods.
      
    The beam is declared in the following manner:
    beam(q, freq)
    **As of v2: no more lists!!**
    
    q is the complex beam parameter.
    
    w0 is the beam waist, freq is the frequency.
    mks units
    '''
    def __init__(self, q_in, freq_in):
        self.q = q_in #complex beam parameter
        self.freq = freq_in #frequency
        self.z = self.q.real #distance along beam path
        self.zr = self.q.imag #Rayleigh range/depth of field
        self.R = (1/self.q).real #radius of curvature
        self.w = np.sqrt(-1/((1/self.q).imag*self.freq/2.9979e8*np.pi)) #beam radius
        self.gouy = np.arctan(self.q.real/self.q.imag) #gouy phase

    def ampl(self,r):
        '''
        Calculates field amplitude at a distance r from center of beam
        Assume phase fronts with circular symmetry!
        '''
        return 1/self.q*np.exp(-1j*2*np.pi*self.freq/2.9979e8/2/self.q*r**2)

class element(object):
    '''
    The elements are the discrete quasioptical components--usually mirrors and lenses.
    A network is a sequence of these objects.

    **Changed significantly in v2. In v1, "free space" was treated as a network element. This is no longer the case; you declare the length of your quasioptical network when you initialize the network itself.
    Because of this, I got rid of the some of the functionality from v1, in which you could propagate the beam through finite pieces of dielectric. I'll have to think more carefully about how to include this, but I don't think anybody needs this for now (?)

    The attributes of an element are:
    element.etype: string specifying what it is (v2: only one type, the lens/mirror!)
    element.mat: the ABCD matrix for the element.

    **Just use the new wrapper function and you don't need to worry about this!**
    '''

    def __init__(self, dtype, fl):
        '''
        for the 'lens' type, give the keyword 'fl': this is the focal length of the mirror in meters.
        '''
        if dtype == 'lens':
            self.tag = 'lens'
            self.etype = 'Lens/focusing mirror'
            self.fl = fl
            self.mat = np.array([[1.,0.],[-1./self.fl,1.]])
        else:
            print 'Invalid element name'
        
class network(object):
    def __init__(self, elts_in, locations, beam_in, length):
        '''   
        The network object is a sequence of elements with a location parameter for each element 
        (the distance of the element from the start of the beam path).
        The beam you put in is the initial state of the beam -- for us, the parameters radiating out from the horns.
        
        locations is 1D numpy array of the distance of each element from the beginning
        of the beam path. The closest element to the beginning of the beam path should be the first, 
        and so on, and the first entry in locations should correspond to the first entry in elts_in, etc.
       

        The beam object is an array "vector" of the usual gausian beam parameters.
        
        Give the total length of the network in meters; this just specifies the last point the beam is calculated at.
        

        '''

        #initial state of beam -- see beam object
        self.beam_0 = beam_in

        #total length of quasioptical network
        self.length = length

        self.locations = locations
        
        #setup is a dict: the key is the distance along the beam path, and the value is the element object at that point
        self.setup = {}
        for ii in range(len(locations)):
            self.setup[locations[ii]] = elts_in[ii]
        
    #calculates abcd matrix that transforms input beam to beam at distance d
    def mat(self, d):
        if (self.locations[-1] >= self.length):
            raise IOError("Elements found beyond the length of the beam path!")
        else:
            #initialize identity matrix
            abcd = np.array([[1.,0.],[0.,1.]])
            elts_behind = 0
            last_elt_dist = 0.
            flg = 1
            distlist = self.setup.keys()
            distlist.append(self.length)
            distlist.sort()
            for elt_dist in distlist:
            #see if you're trying to calculate parameters exactly at a boundary
                if d == elt_dist:
                    flg = 0
                elif d > elt_dist:
                    elts_behind = elts_behind+1
                else: 
                    break
            #go through, figure out the right abcd matrices -- especially the last one!
#            print ' '
            if flg == 1:
                for elt_dist in distlist:
#                    print 'Elt dist: ', elt_dist
                    if elts_behind >= 0:
                        if d > elt_dist:
                            #If we are measuring beyond the current element, first propagate up to the element...
                            abcd = np.dot(np.array([[1., elt_dist-last_elt_dist], [0., 1.]]), abcd)
                            #...then calculate the effect of the element itself
                            abcd = np.dot(self.setup[elt_dist].mat,abcd)
                            last_elt_dist = elt_dist
                            elts_behind = elts_behind-1
                        elif elt_dist > d:
                            abcd = np.dot(np.array([[1., d-last_elt_dist], [0.,1.]]), abcd)
                            elts_behind = elts_behind-1
                        else:
                            print "Element placement error."
            #if the distance you want to calculate is exactly one of the element distances, just take the abcd matrix not including the contribution of that element.
            elif flg == 0:
                for elt_dist in distlist:
                    if elts_behind >= 0:
                        if d > elt_dist:
                            #If we are measuring beyond the current element, first propagate up to the element...
                            abcd = np.dot(np.array([[1., elt_dist-last_elt_dist], [0., 1.]]),abcd)
                            #...then calculate the effect of the element itself
                            abcd = np.dot(self.setup[elt_dist].mat,abcd)
                            last_elt_dist = elt_dist
                            elts_behind = elts_behind-1
                        elif elt_dist == d:
                            #If we are measuring beyond the current element, first propagate up to the element...
                            abcd = np.dot(np.array([[1., elt_dist-last_elt_dist], [0., 1.]]),abcd)
                            elts_behind = elts_behind-1
                        else:
                            print "Element placement error."
            else:
                print "Element placement error."
        return abcd
       
    def beam_f(self, d):
        '''
        output beam object at a point along path
        '''
        abcd = self.mat(d)
        qi = self.beam_0.q
        qf = (abcd[0, 0]*qi+abcd[0, 1])/(abcd[1, 0]*qi+abcd[1, 1])
        return beam(qf, self.beam_0.freq)

    def make_fullbeam(self, window):
        '''
        Makes a dict object: the keys are floats which indicate a distance along the beam path, and the corresponding values are a beam object representing the state of the beam at that point. 

        I guess this is the most general thing you might want, but the dict itself isn't very easy to use. The methods below turn this dict into useful info (i.e. beam radius)

        Window is the number of points at which the beam will be calculated.
        '''
        self.fullbeam = {}
        self.dists = np.linspace(0, self.length,window)
        for dist in self.dists:
            self.fullbeam[dist] = self.beam_f(dist)
            
    def make_radius_mat(self):
        '''
        puts a matrix containing the distance along the beam path in the first column and the beam radius at that point in the second column into self.radius_mat
        '''
        vec_of_radius = np.array([])
        for dist in self.dists:
            vec_of_radius=np.append(vec_of_radius, self.fullbeam[dist].w)
        self.radius_mat = np.hstack((self.dists.reshape((len(self.dists),1)),vec_of_radius.reshape((len(vec_of_radius),1))))

'''
easiest thing to do: use this wrapper function! 
This generates the network class for you. All you have to do is give it a matrix which has the following structure:
 [[ (distance of mirror 1 FROM START IN CM)      (focal length of mirror 1 IN CM) ]
  [ (location of mirror 2 FROM MIRROR 1 IN CM)   (focal length of mirror 2 IN CM) ]
  ...
  [ (location of mirror N FROM MIRROR N-1 IN CM) (focal length of mirror N IN CM) ]]
So you're supplying relative rather than absolute distances.

Note that you now specify the distance from a particular mirror FROM THE PREVIOUS MIRROR (so that changing one of the positions will shift everything that follows).
Note also that, unlike previous version and the rest of the code, you should give all dimensions in cm ***EXCEPT THE INITIAL BEAM WAIST WHICH SHOULD BE IN mm!!***

For maximum convenience, just change the ezscript.py file!
##################
Function i/o:
The mirr_matrix is described above.

length is the total beam path length in cm.

numpts is the number of points you want to calculate the beam at.

bm_waist_initial is the initial beam radius ___IN mm!!!___

freq is the frequency.

The output of the function is a matrix with the distance along the beam path as the first column and the beam waist ***in mm!!!*** as the second.
'''
def ezbeam(mirr_matrix, length, numpts, bm_waist_initial, freq):
    locations = (np.cumsum(mirr_matrix[:,0])/100.).tolist()
    elts_in = []
    for fl in mirr_matrix[:,1]:
        elts_in.append(element('lens', fl/100.))
    beam_in = beam(getq(bm_waist_initial/1000., 0., freq), freq)
    net1=network(elts_in, locations, beam_in, length/100.)
    net1.make_fullbeam(numpts)
    net1.make_radius_mat()
    radmat=net1.radius_mat
    radmat[:,1]=radmat[:,1]*1000.
    return radmat
