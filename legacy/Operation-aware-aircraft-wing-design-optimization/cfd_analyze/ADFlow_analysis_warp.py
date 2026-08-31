import os
import argparse
import ast
import numpy as np
from calendar import c
from mpi4py import MPI
from baseclasses import AeroProblem
from adflow import ADFLOW
from pygeo import DVGeometry, DVConstraints, geo_utils
from pyoptsparse import Optimization, OPT
from idwarp import USMesh
from multipoint import multiPointSparse
import pyspline



data = np.loadtxt('data.txt')
# traindata = traindata[16100:, :]
modedata = np.loadtxt('/home/aobo/MACH-Aero/input/modes.dat')
modes = modedata[:50,:].copy()

parser = argparse.ArgumentParser()
parser.add_argument("--output", type=str, default="output")
parser.add_argument("--task", choices=["analysis", "polar"], default="analysis")
parser.add_argument("--gridFile", type=str, default='/home/aobo/MACH-Aero/input/L3_peter_rotat_mirror_bc.cgns')
parser.add_argument("--FFDFile", type=str, default='/home/aobo/MACH-Aero/input/rot.xyz')
args = parser.parse_args()


MP = multiPointSparse(MPI.COMM_WORLD)
MP.addProcessorSet("cruise", nMembers=1, memberSizes=MPI.COMM_WORLD.size)
comm, setComm, setFlags, groupFlags, ptID = MP.createCommunicators()

if not os.path.exists(args.output):
    if comm.rank == 0:
        os.mkdir(args.output)


for i in range(10):

    # Set up mesh warping
    meshOptions = {
        'gridFile':args.gridFile,
        'fileType':'CGNS',
        # 'aExp': 3.0,
        # 'bExp': 5.0,
        # 'LdefFact':100.0,     # affects how far the deformations are pushed away from the surface
        # 'alpha':0.1,
        # 'errTol':1e-5
        }
    mesh = USMesh(options=meshOptions, comm=comm)

    coords0 = mesh.getSurfaceCoordinates()

    DVGeo = DVGeometry(args.FFDFile)
    nSpanwise = 8

    # Create the Ref line
    coef = DVGeo.FFD.vols[0].coef.copy()
    X = np.zeros((nSpanwise,3))
    for ispan in range(nSpanwise):
        Lep = 0.5*(coef[0,ispan,0,:]+coef[0,ispan,1,:])
        Tep = 0.5*(coef[-1,ispan,0,:]+coef[-1,ispan,1,:]) 
        X[ispan,:] = Lep + 0.25*(Tep - Lep)

    c1 = pyspline.Curve(X=X, k=2)
    DVGeo.addRefAxis('wing', c1)
    
    def twist(val, geo):
        # Set all the twist values
        for i in range(nSpanwise-1):
            geo.rot_z['wing'].coef[i+1] = val[i]

    DVGeo.addLocalDV('shape', lower=-2.0, upper=2.0, scale=20.0)
    DVGeo.addGlobalDV('wing_twist', np.zeros(nSpanwise-1), twist, lower=-1., upper=1., scale=0.2) 
    
    DVList={'shape':np.dot(data[i,10:60], modes),
        'wing_twist':data[i,3:10]}  

    # This part is stupid, but it makes sure of the wing geo change under different version of pygeo and adflow 

    DVGeo.addPointSet(coords0, "coords")
    DVGeo.setDesignVars(DVList)
    newcoords = DVGeo.update("coords")
    DVGeo.writePointSet("coords", "surf")
    mesh.setSurfaceCoordinates(newcoords)
    mesh.warpMesh()
    mesh.writeGrid('L3_mirror_warped_NN_update.cgns')
    
    aeroOptions = {
        # I/O Parameters
        "gridFile": 'L3_mirror_warped_NN_update.cgns',
        "outputDirectory": args.output,
        "monitorvariables": ["resrho", "cl", "cd", "cmz"],
        
        'isoSurface':{'shock':1.0},     
        # Physics Parameters
        'equationType':'RANS',#args.mode,
        'smoother':'DADI',#gridops[args.level]['s'],
        'frozenturbulence':False,
        'writeVolumeSolution':False,
        'writeSurfaceSolution':True,
        # Solver Parameters
        'CFL':1.0,
        'CFLCoarse':1.0,
        'MGCycle':'sg',
        'MGStartLevel':-1,
        'nCyclesCoarse':5000,
        'nCycles':10000,
        'nsubiterturb':7,
        'useNKSolver':True,
        'useANKSolver':True,
        'nkswitchtol':1e-7,
        'rkreset': True,
        'nrkreset': 200,
        'liftIndex': 2,
        'writeVolumeSolution':True,
        'writeSurfaceSolution':True,
        #'ANKmaxIter' : 40,
        #'ANKsecondordswitchtol' : 1e-16,
        #'ANKcoupledswitchtol' : 1e-12,
        'useanksolver' : True,
        #'nsubiterturb' : 10,
        'useNKSolver':True,
        'ankstepfactor' : 0.5,
        # 'ankstepinit' : 0.1,
        # 'ankstepexponent' : 0.5,
        'ANKCFLExponent' : 0.5,
        'anklinearsolvetol' : 0.05,

        # Convergence Parameters
        'L2Convergence':1e-10,
        'adjointL2Convergence':1e-12,
        'ADPC':True,
        'adjointMaxIter': 500,
        'adjointSubspaceSize':150,
        'ILUFill':2,
        'ASMOverlap':1,
        'outerPreconIts':3,

    }
    
    
    DVGeo.setDesignVars(DVList) 
    CFDSolver = ADFLOW(options=aeroOptions)
    CFDSolver.addLiftDistribution(100, "z")

    span = 3.758150834
    pos = np.array([0.0235, 0.267, 0.557, 0.695, 0.828, 0.944])*span
    CFDSolver.addSlices('z', pos, sliceType='absolute')

    ap = AeroProblem(
        name="flowcase%d" % i,
        alpha=data[i, 2],
        mach=data[i, 0],
        altitude=data[i, 1],
        # reynolds=5e6,
        # reynoldsLength=1.0,
        # T=326.45,
        areaRef= 3.407014,
        xRef=1.20777,
        yRef=.007669,
        zRef=0,
        chordRef=1.0,
        evalFuncs=["cl", "cd", 'cmz'],
    )
        # Add angle of attack variable
    ap.addDV("alpha", value=data[i, 2], lower=0, upper=10.0, scale=1.0)


    if args.task == "analysis":
        # Solve
        CFDSolver(ap)
        # rst Evaluate and print
        funcs = {}
        CFDSolver.evalFunctions(ap, funcs)
        # Print the evaluated functions
        if comm.rank == 0:
            print(funcs)          
            coeff = [funcs[f"{ap.name}_cl"],funcs[f"{ap.name}_cd"],funcs[f"{ap.name}_cmz"]]
            coeff = np.array(coeff,dtype=object)
            data = np.hstack((traindata[i,:60],coeff)).reshape(1,63)
            # print(data)
            # print(data.shape)
            # f.write(data)
            with open('data_GEN_warp.txt','ab') as f:
                np.savetxt(f,data)
    
