"""
This script is used to generate cfd data using ADflow, please run this on HPC
"""

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



traindata = np.loadtxt('L2_train_coeff_input.dat')
traindata = traindata[1:, :]
modedata = np.loadtxt('/home/aobo/MACH-Aero/input/modes.dat')
modes = modedata[:50,:].copy()

parser = argparse.ArgumentParser()
parser.add_argument("--output", type=str, default="output")
parser.add_argument("--task", choices=["analysis", "polar"], default="analysis")
args = parser.parse_args()


MP = multiPointSparse(MPI.COMM_WORLD)
MP.addProcessorSet("cruise", nMembers=1, memberSizes=MPI.COMM_WORLD.size)
comm, setComm, setFlags, groupFlags, ptID = MP.createCommunicators()

if not os.path.exists(args.output):
    if comm.rank == 0:
        os.mkdir(args.output)


gridFile = '/home/aobo/MACH-Aero/input/L3_peter_rotat_mirror_bc.cgns'
FFDFile = '/home/aobo/MACH-Aero/input/rot.xyz'

# Set up mesh warping
meshOptions = {
    'gridFile':gridFile,
    'fileType':'CGNS',
    # 'aExp': 3.0,
    # 'bExp': 5.0,
    # 'LdefFact':100.0,     # affects how far the deformations are pushed away from the surface
    # 'alpha':0.1,
    # 'errTol':1e-5
    }
mesh = USMesh(options=meshOptions)

coords0 = mesh.getSurfaceCoordinates()

for i in range(156):

    DVGeo = DVGeometry(FFDFile)
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
    
    DVList={'shape':np.dot(traindata[i,10:60], modes),
        'wing_twist':traindata[i,3:10]}  

    # This part is stupid, but it makes sure of the wing geo change under different version of pygeo and adflow 

    DVGeo.addPointSet(coords0, "coords")
    DVGeo.setDesignVars(DVList)
    newcoords = DVGeo.update("coords")
    DVGeo.writePointSet("coords", "surf")
    mesh.setSurfaceCoordinates(newcoords)
    mesh.warpMesh()
    mesh.writeGrid('L2_mirror_warped_NN_update.cgns')
    
    aeroOptions = {
        # I/O Parameters
        "gridFile": 'L2_mirror_warped_NN_update.cgns',
        # "outputDirectory": args.output,
        "writeSurfaceSolution":True,
        "writeVolumeSolution":True,
        "monitorvariables": ["resrho", "cl", "cd", "cmz"],
        #lift direction
        'isoSurface':{'shock':1.0},    
        #lift direction
        "liftIndex":2,
        # "useZipperMesh":True,
        # Physics Parameters
        "equationType": "RANS",
        # Solver Parameters
        # "smoother": "Runge-Kutta",
        "smoother": "DADI",
        "CFL":1.7,
        "CFLCoarse":1.0,
        "MGCycle": "sg",
        "MGStartLevel":-1,
        'nCyclesCoarse':250,
        'nCycles':100000,   
        'nsubiterturb':5,
        'useblockettes':False, 
        'useNKsolver':True,
        'useANKsolver':True,

        # "infchangecorrection": True,

        'usematrixfreedrdw':True,
        # nk
        'nkadpc':True,
        'nkswitchtol':1.0e-7,

        # Convergence Parameters
        'L2Convergence':1e-12,
        'L2ConvergenceCoarse':1e-2,

        # Adjoint Parameters
        'adjointL2Convergence':1e-12,
        'ADPC':True,
        'adjointMaxIter': 1500,
        'adjointSubspaceSize':150,
        'ILUFill':2,
        'ASMOverlap':2,
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
        alpha=traindata[i, 2],
        mach=traindata[i, 0],
        altitude=traindata[i, 1],
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
            with open('Data_Gen_L2_validate.txt','ab') as f:
                np.savetxt(f,data)
    
