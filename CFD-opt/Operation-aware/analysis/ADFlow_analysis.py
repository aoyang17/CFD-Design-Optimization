import numpy as np
import pandas as pd
import argparse
import os
from adflow import ADFLOW
from baseclasses import AeroProblem
from mpi4py import MPI
import argparse
import ast
from calendar import c
import os

from adflow import ADFLOW
from baseclasses import AeroProblem
from idwarp import USMesh
from mpi4py import MPI
from multipoint import multiPointSparse
from pygeo import DVConstraints, DVGeometry, geo_utils
from pyoptsparse import OPT, Optimization

# Use Python's built-in Argument parser to get commandline options
parser = argparse.ArgumentParser()
parser.add_argument("--output", type=str, default="output_Kmeans_mach_0.83_alpha_2.52")
parser.add_argument("--opt", type=str, default="SLSQP", choices=["IPOPT", "SLSQP", "SNOPT"])
parser.add_argument("--gridFile", type=str, default="/home/aobo/MACH-Aero/Operate_mission_ASO/Mode_based_ASO/opeartion_mode_based/ADODG429_092_vol.cgns")
parser.add_argument("--task", choices=["analysis", "polar"], default="analysis")
parser.add_argument("--optOptions", type=ast.literal_eval, default={}, help="additional optimizer options to be added")
args = parser.parse_args()

MP = multiPointSparse(MPI.COMM_WORLD)
MP.addProcessorSet("cruise", nMembers=1, memberSizes=MPI.COMM_WORLD.size)
comm, setComm, setFlags, groupFlags, ptID = MP.createCommunicators()

if not os.path.exists(args.output):
    if comm.rank == 0:
        os.mkdir(args.output)


new_data = {}



aeroOptions = {
    # I/O Parameters
    "gridFile": args.gridFile,
    "outputDirectory": args.output,
    "monitorvariables": ["resrho", "cl", "cd", "cmz"],
    
    'isoSurface':{'shock':1.0},     
    # Physics Parameters
    'equationType':'RANS',#args.mode,
    'smoother':'DADI',#gridops[args.level]['s'],
    'frozenturbulence':False,
    'writeVolumeSolution':True,
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

# Create solver
CFDSolver = ADFLOW(options=aeroOptions, comm=comm)
CFDSolver.addLiftDistribution(200, "z")

span = 3.758150834
pos = np.array([0.0235, 0.267, 0.557, 0.695, 0.828, 0.944])*span
CFDSolver.addSlices('z', pos, sliceType='absolute')


ap = AeroProblem(name='wing', mach=0.83, reynolds=5e6, altitude= 11740, alpha=2.52, areaRef=3.407014, chordRef=1.00, xRef=1.20777, yRef=.007669, zRef=0, evalFuncs=['cd', 'cl', 'cmz'])
CLList = []
CDList = []
CMList = []

# alphaList = [0, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
alphaList = [2.52]
# Loop over the alpha values and evaluate the polar
for alpha in alphaList:
    ap.name = f"wing_{alpha:4.2f}"

    # Update the alpha in aero problem and print it to the screen.
    ap.alpha = alpha
    if comm.rank == 0:
        print(f"current alpha: {ap.alpha}")    
    # Solve the flow
    CFDSolver(ap)

    # Evaluate functions
    funcs = {}
    CFDSolver.evalFunctions(ap, funcs)

    # Store the function values in the output list
    CLList.append(funcs[f"{ap.name}_cl"])
    CDList.append(funcs[f"{ap.name}_cd"])
    CMList.append(funcs[f"{ap.name}_cmz"])

print(CLList)
print(CDList)
print(CMList)