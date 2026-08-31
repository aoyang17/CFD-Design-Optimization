# ======================================================================
#         DVConstraint Setup
# ====================================================================== 
# (Empty) DVConstraint Object                                                              
DVCon = DVConstraints()
DVCon.setDVGeo(DVGeo)

# Load igs file for doing projections                                                      
#wing = pyGeo.pyGeo('iges',file_name=iges_file)                                            

#wingsurf=CFDSolver.getTriangulatedMeshSurface(groupName='wing')

wingsurf= CFDSolver.getTriangulatedMeshSurface(groupName='wing')
p0wing,v1wing,v2wing =wingsurf[0],wingsurf[1],wingsurf[2]

tailsurf=CFDSolver.getTriangulatedMeshSurface(groupName='tail')
p0tail,v1tail,v2tail =tailsurf[0],tailsurf[1],tailsurf[2]



allp0,allv1,allv2 =[],[],[]
#p0wing,v1wing,v2wing = CFDSolver.getTriangulatedMeshSurface(groupName='wing')
for i in range(len(p0wing)):
    allp0.append(p0wing[i])
    allv1.append(v1wing[i])
    allv2.append(v2wing[i])    
for i in range(len(p0tail)):
    allp0.append(p0tail[i])
    allv1.append(v1tail[i])
    allv2.append(v2tail[i])    

allsurf=[allp0,allv1,allv2]
DVCon.setSurface(allsurf)
#DVCon.setSurface(CFDSolver.getTriangulatedMeshSurface())

# Setup curves for defining the wing box area to add volume and thickness constraints
# need two set of points for defining two curves, which are separately along
# span direction at leading edge and trailing edge 
# notice: because the border in sym cannot project a node for thickness constraints sometimes

x_le = numpy.loadtxt('./input/LEcon.dat')
x_te = numpy.loadtxt('./input/TEcon.dat')

# Add the volume constraint
# DVCon.addVolumeConstraint(x_le, x_te, nSpan=40, nChord=25, lower=1.0, upper=3.0, scaled=True)
# since we add enough thickness constraints, so explict volume constraint is not necessary.
#DVCon.addVolumeConstraint(x_le, x_te, nSpan=30, nChord=20, lower=1.0, upper=3.0)
DVCon.addThicknessConstraints2D(x_le, x_te, nSpan=15, nChord=20, lower=1.0, upper=1.0)
'''
for i in xrange(len(x_le)):
    DVCon.addThicknessConstraints1D([x_le[i],x_te[i]], 25, [0,0,1],
                                  lower=1.0, upper=3.0, scaled=True,
                                  scale=1.0, name=None,
                                  addToPyOpt=True)								  
'''
# add the leading edge and trailing edge fix constraint.
# leading edge constraint
DVCon.addLeTeConstraints(volID=2,faceID='iLow')
#DVCon.addLeTeConstraints(volID=0,faceID='iLow')

# trailing edge constraint
DVCon.addLeTeConstraints(volID=2,faceID='iHigh')
#DVCon.addLeTeConstraints(volID=0,faceID='iHigh')


'''
For tail
'''
#DVCon.setSurface(CFDSolver.getTriangulatedMeshSurface())

# Setup curves for defining the wing box area to add volume and thickness constraints
# need two set of points for defining two curves, which are separately along
# span direction at leading edge and trailing edge 
# notice: because the border in sym cannot project a node for thickness constraints sometimes

x_le = numpy.loadtxt('./input/TailLEcon.dat')
x_te = numpy.loadtxt('./input/TailTEcon.dat')

# Add the volume constraint
# DVCon.addVolumeConstraint(x_le, x_te, nSpan=40, nChord=25, lower=1.0, upper=3.0, scaled=True)
# since we add enough thickness constraints, so explict volume constraint is not necessary.
#DVCon.addVolumeConstraint(x_le, x_te, nSpan=6, nChord=10, lower=1.0, upper=3.0)
DVCon.addThicknessConstraints2D(x_le, x_te, nSpan=5, nChord=10, lower=1.0, upper=1.0)

'''
for i in xrange(len(x_le)):
    DVCon.addThicknessConstraints1D([x_le[i],x_te[i]], 25, [0,0,1],
                                  lower=1.0, upper=3.0, scaled=True,
                                  scale=1.0, name=None,
                                  addToPyOpt=True)								  
'''
# add the leading edge and trailing edge fix constraint.
# leading edge constraint
DVCon.addLeTeConstraints(volID=1,faceID='iLow')
#DVCon.addLeTeConstraints(volID=0,faceID='iLow')

# trailing edge constraint
DVCon.addLeTeConstraints(volID=1,faceID='iHigh')
#DVCon.addLeTeConstraints(volID=0,faceID='iHigh')


indSetA=[]
indSetB=[]
factorA=1.0
factorB=-1.0
FFDpairs=numpy.loadtxt('input/pairs.txt',dtype=int)
for i in range(FFDpairs.shape[0]):
    myi,myj = FFDpairs[i,0],FFDpairs[i,1]
    indSetA.append(myi)
    indSetB.append(myj)
DVCon.addLinearConstraintsShape(indSetA, indSetB, factorA, factorB)


# write a visualization file for constraints.
DVCon.writeTecplot('constraints.plt')
