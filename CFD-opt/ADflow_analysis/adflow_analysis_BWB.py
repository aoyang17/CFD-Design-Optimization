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
parser.add_argument("--output", type=str, default="output_BWB_dmm_optimized")
parser.add_argument("--opt", type=str, default="SLSQP", choices=["IPOPT", "SLSQP", "SNOPT"])
parser.add_argument("--gridFile", type=str, default="/home/aobo/Weizhen_case/bwb_iter_998_000_vol.cgns")

# parser.add_argument("--FFDFile", type=str, default="/home/aobo/MACH-Aero/input/rot.xyz")
parser.add_argument("--optOptions", type=ast.literal_eval, default={}, help="additional optimizer options to be added")
args = parser.parse_args()

MP = multiPointSparse(MPI.COMM_WORLD)
MP.addProcessorSet("cruise", nMembers=1, memberSizes=MPI.COMM_WORLD.size)
comm, setComm, setFlags, groupFlags, ptID = MP.createCommunicators()

if not os.path.exists(args.output):
    if comm.rank == 0:
        os.mkdir(args.output)

aeroOptions = {
    # Common Parameters
    'gridFile':args.gridFile,
    'outputDirectory':args.output,
    'monitorVariables':['cl','cd','cmz'],
    'volumeVariables':['cp','mach'],
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
    'useANKsolver':True,
     #'nsubiterturb' : 10,
    'useNKSolver':True,
    # 'ankstepfactor' : 0.5,
    # 'ankstepinit' : 0.1,
    # 'ankstepexponent' : 0.5,
    # 'ankcflexponent' : 0.5,
    # 'anklinearsolvetol' : 0.05,

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

CFDSolver = ADFLOW(options=aeroOptions, comm=comm)

span = 42
pos = np.array([2.1, 7.56, 13.02, 18.48, 23.94, 29.4, 34.86, 40.32])
CFDSolver.addSlices('z', pos, sliceType='absolute')
CFDSolver.addLiftDistribution(100, 'z')

nFlowCases = 1
feetcoef = 0.3048 
wingarea = 15860*feetcoef*feetcoef*0.5
wingchord = 86*feetcoef
alpha = 0.58
ap = AeroProblem(name='fc', mach=0.85, altitude=10670, areaRef=wingarea, chordRef=wingchord, 
                  alpha=0.5951537489891052, xRef=26, yRef=.0, zRef=0, evalFuncs=['cd', 'cl', 'cmz'])

# Solve
CFDSolver(ap)
# rst Evaluate and print
funcs = {}
CFDSolver.evalFunctions(ap, funcs)
# Print the evaluated functions
if comm.rank == 0:
    print(funcs)

