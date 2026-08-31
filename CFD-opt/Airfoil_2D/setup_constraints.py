# ======================================================================
#         DVConstraint Setup
# ====================================================================== 
DVCon = DVConstraints()
DVCon.setDVGeo(DVGeo)

# Only ADflow has the getTriangulatedSurface Function
DVCon.setSurface(CFDSolver.getTriangulatedMeshSurface())

le=0.001
leList = [[le    , 0, le], [le    , 0, 1.0-le]]
teList = [[1.0-le, 0, le], [1.0-le, 0, 1.0-le]]
DVCon.addVolumeConstraint(leList, teList, 2,30, lower=0.065469492997692169, upper=5.0,scaled=False)
DVCon.addThicknessConstraints2D(leList, teList, 2,50, lower=0.0001, upper=3.0)

if comm.rank == 0:
    fileName = os.path.join(args.output, 'constraints.dat')
    DVCon.writeTecplot(fileName)
