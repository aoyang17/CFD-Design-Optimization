'''
---------------------------------------------------------
This script is to used to generate warped mesh after mode parameterization 
---------------------------------------------------------
'''

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
# from DVGeometry_FFD_MODE import DVGeometry_FFD_MODE
from pyoptsparse import Optimization, OPT, History
from pyspline import *

# Use Python's built-in Argument parser to get commandline options
parser = argparse.ArgumentParser()
parser.add_argument("--output", type=str, default="output_dmm_optimized")
parser.add_argument("--opt", type=str, default="SLSQP", choices=["IPOPT", "SLSQP", "SNOPT"])
parser.add_argument("--gridFile", type=str, default="/home/aobo/Weizhen_case/ADODG4_iter_125_000_vol.cgns")

# parser.add_argument("--FFDFile", type=str, default="/home/aobo/MACH-Aero/input/rot.xyz")
parser.add_argument("--optOptions", type=ast.literal_eval, default={}, help="additional optimizer options to be added")
args = parser.parse_args()

MP = multiPointSparse(MPI.COMM_WORLD)
MP.addProcessorSet("cruise", nMembers=1, memberSizes=MPI.COMM_WORLD.size)
comm, setComm, setFlags, groupFlags, ptID = MP.createCommunicators()

if not os.path.exists(args.output):
    if comm.rank == 0:
        os.mkdir(args.output)

# meshOptions = {
#     "gridFile":args.gridFile,
#     "fileType":'CGNS',
#     "symmetryPlanes":None,
#     'aExp': 3.0,
#     'bExp': 5.0,
#     'LdefFact':100.0,     # affects how far the deformations are pushed away from the surface
#     'alpha':0.1,
#     'errTol':1e-5
#     }
# mesh = USMesh(options=meshOptions)

# coords0 = mesh.getSurfaceCoordinates()

# DVGeo = DVGeometry(args.FFDFile)
# DVGeo.addRefAxis("wing", xFraction=0.25, alignIndex="j")

# nSpanwise = 8

# def twist(val, geo):
#     # Set all the twist values
#     for i in range(nSpanwise-1):
#         geo.rot_z['wing'].coef[i+1] = val[i]

# def dihedral(val, geo):
#     C = geo.extractCoef('wing')
#     s = geo.refAxis.curves[0].s
#     for i in range(nSpanwise-1):
#         C[i+1,1] += val[i]
#     geo.restoreCoef(C, 'wing')

# DVGeo.addLocalDV('shape', lower=-2.0, upper=2.0, scale=1.0)
# DVGeo.addGlobalDV('wing_twist', np.zeros(nSpanwise-1), twist, lower=-1., upper=1.)
# DVGeo.addGlobalDV('wing_dihedral', np.zeros(nSpanwise-1), dihedral, lower=-5.0, upper=5.0)

aeroOptions = {
    # I/O Parameters
    "gridFile": args.gridFile,
    "outputDirectory": args.output,
    
    'isoSurface':{'shock':1.0},     
    "monitorvariables": ["resrho", "cl", "cd", "cmy"],
    #lift direction
    "liftIndex":3,
    # "useZipperMesh":True,
    # Physics Parameters
    "equationType": "RANS",
    # Solver Parameters
    # "smoother": "Runge-Kutta",
    "smoother": "DADI",
    "CFL":1.0,
    "CFLCoarse":1.0,
    "MGCycle": "sg",
    "MGStartLevel":-1,
    'nCyclesCoarse':5000,
    'nCycles':10000,   
    'nsubiterturb':7,
    'useblockettes':False, 
    'useNKsolver':True,
    'useANKsolver':True,

    # "infchangecorrection": True,

    'usematrixfreedrdw':True,
    # nk
    'nkadpc':True,
    'nkswitchtol':1.0e-7,
    'liftIndex': 3,

    # Convergence Parameters
    'L2Convergence':1e-10,
    # 'L2ConvergenceCoarse':1e-2,

    # Adjoint Parameters
    'adjointL2Convergence':1e-12,
    'ADPC':True,
    'adjointMaxIter': 500,
    'adjointSubspaceSize':150,
    'ILUFill':2,
    'ASMOverlap':1,
    'outerPreconIts':3,

}
CFDSolver = ADFLOW(options=aeroOptions, comm=comm)
CFDSolver.addLiftDistribution(200, "y")

span = 3.758150834
# pos = np.array([0.0235, 0.267, 0.557, 0.695, 0.828, 0.944])*span
pos = np.array([0.0235, 0.267, 0.557, 0.65, 0.828, 0.944])*span
CFDSolver.addSlices('y', pos, sliceType='absolute')

ap = AeroProblem(
    name="crm_dmm_optimized",
    alpha=2.03,
    mach=0.85,
    altitude=11740,
    # reynolds=5e6,
    reynoldsLength=1.0,
    T=326.45,
    areaRef= 3.407014,
    xRef=1.20777,
    yRef=0,
    zRef=0.007669,
    chordRef=1.0,
    evalFuncs=["cl", "cd", "cmy"],
)

# Solve
CFDSolver(ap)
# rst Evaluate and print
funcs = {}
CFDSolver.evalFunctions(ap, funcs)
# Print the evaluated functions
if comm.rank == 0:
    print(funcs)

