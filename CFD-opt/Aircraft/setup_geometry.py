# ======================================================================
#         DVGeometry Setup
# ====================================================================== 
# Call common geometry setup
DVGeo = DVGeometry(FFDFile)

# inboard(0-3) outboard(4-8)
wing_vols = [2]
tail_vols = [1]
# =================================================================================
#         Set up wing twist
# =================================================================================

nWingFFDSections = nTwistwing
nTailFFDSections = nTwisttail

# use the quater-chord line as the twist ref axis
sweep_ref_wing0=numpy.zeros((nWingFFDSections,3))
for i in range(nWingFFDSections):
    sweep_ref_wing0[i,:] = 0.75*LEline[i,:] + 0.25*TEline[i,:]

# use the quater-chord line as the twist ref axis
sweep_ref_wing1=numpy.zeros((nTailFFDSections,3))
for i in range(nTailFFDSections):
    sweep_ref_wing1[i,:] = 0.75*TailLEline[i,:] + 0.25*TailTEline[i,:]

# Create the linear spline , and the knot vector in the spanwise direction                                                                                                          
c_wing = pySpline.Curve(X=sweep_ref_wing0,k=2)
c_tail = pySpline.Curve(X=sweep_ref_wing1,k=2)

# add the reference axis respect to which the wing sections would be rotated.
DVGeo.addRefAxis('wing_axis', c_wing , volumes=wing_vols) 
DVGeo.addRefAxis('tail_axis', c_tail , volumes=tail_vols) 

# =====================================================
#        Setup Design Variable Functions                                                                                                                        
# =====================================================

def twistWingFun(val,geo):
    # Set all the twist values               
    for i in xrange(nWingFFDSections):
        geo.rot_y['wing_axis'].coef[i] = val[i]
        #pass 
        #twist is an user defined geometry function rather than an intrinsic DVGeo function. 
        #So if you do not want to use twist as designvariables, just do nothing.                                                                           
    return

def twistTailFun(val,geo):
    # Set all the twist values               
    for i in xrange(nTailFFDSections):
        geo.rot_y['tail_axis'].coef[i] = val[i]
        #pass 
        #twist is an user defined geometry function rather than an intrinsic DVGeo function. 
        #So if you do not want to use twist as designvariables, just do nothing.                                                                           
    return


WingTwistLowerBound = -5*numpy.ones(nWingFFDSections)
WingTwistUpperBound =  5*numpy.ones(nWingFFDSections)
# fix the wing root incidence angle
WingTwistLowerBound[0] = 0.0
WingTwistUpperBound[0] = 0.0

TailTwistLowerBound = -5*numpy.ones(nTailFFDSections)
TailTwistUpperBound =  5*numpy.ones(nTailFFDSections)
# fix the wing root incidence angle


#if MPI.COMM_WORLD.rank == 0:
#    print 'nWingFFDSections=',nWingFFDSections

DVGeo.addGeoDVGlobal('TwistWing', numpy.zeros(nWingFFDSections), twistWingFun, 
                     lower=WingTwistLowerBound, upper=WingTwistUpperBound, scale=1.0)                                
DVGeo.addGeoDVGlobal('TwistTail', numpy.zeros(nTailFFDSections), twistTailFun, 
                     lower=TailTwistLowerBound, upper=TailTwistUpperBound, scale=1.0)                                

# even if you do not want to use twist as design variables , you still have to add twist to DVGeo as DVGlobal.
# or just some other variables else which might do nothing at all but as DVGlobal.
# the lower and upper could not be precisely 0, because it will lead to NaN error during non-dimensionalization (x/(0-0)).

FFDbounds = numpy.loadtxt('input/FFDbounds.txt')
nval = DVGeo.addGeoDVLocal(dvName='shapevars', lower=FFDbounds[:,0], upper=FFDbounds[:,1], scale=1.0, axis='z')





