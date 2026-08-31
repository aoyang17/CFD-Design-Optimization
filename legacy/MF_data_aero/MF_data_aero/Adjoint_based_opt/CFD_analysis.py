import numpy as np
import argparse
import os
from adflow import ADFLOW
from baseclasses import AeroProblem
from mpi4py import MPI
import argparse
import ast
from calendar import c
import os

import numpy as np
from adflow import ADFLOW
from baseclasses import AeroProblem
from idwarp import USMesh
from mpi4py import MPI
from multipoint import multiPointSparse
from pygeo import DVConstraints, DVGeometry, geo_utils
from pyoptsparse import OPT, Optimization

# Use Python's built-in Argument parser to get commandline options
parser = argparse.ArgumentParser()
parser.add_argument("--output", type=str, default="output_ADODG_analysis_L3_baseline")
parser.add_argument("--opt", type=str, default="SLSQP", choices=["IPOPT", "SLSQP", "SNOPT"])
parser.add_argument("--gridFile", type=str, default="/home/ayangae/MACH/ADODG_case/L3_peter_rotat_mirror_bc.cgns")
parser.add_argument("--task", choices=["analysis", "polar"], default="analysis")
parser.add_argument("--optOptions", type=ast.literal_eval, default={}, help="additional optimizer options to be added")
args = parser.parse_args() 

MP = multiPointSparse(MPI.COMM_WORLD)
MP.addProcessorSet("cruise", nMembers=1, memberSizes=MPI.COMM_WORLD.size)
comm, setComm, setFlags, groupFlags, ptID = MP.createCommunicators()
 
if not os.path.exists(args.output):
    if comm.rank == 0:
        os.mkdir(args.output)

aeroOptions = {
    # I/O Parameters
    "gridFile": args.gridFile,
    "outputDirectory": args.output,
    "monitorvariables": ["resrho", "cl", "cd", "cmz"],
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
    'nkswitchtol':1.0e-6,

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

# Create solver
CFDSolver = ADFLOW(options=aeroOptions)

# Add features
CFDSolver.addLiftDistribution(200, "z")
span = 3.758150834
pos = np.array([0.0235, 0.267, 0.557, 0.695, 0.828, 0.944])*span
CFDSolver.addSlices('z', pos, sliceType='absolute')

alphaList = [2.229033]
mach = 0.85
alt = 11740


ap = AeroProblem(name="wing", alpha=2.229033, mach=mach, altitude=alt, reynolds=5e6, \
    reynoldsLength=1.0, T=326.45, areaRef= 3.407014, chordRef=1.0, \
    xRef=1.20777, yRef=0, zRef=.007669, evalFuncs=["cl", "cd", "cmz"])

if args.task == "analysis":
    # Solve
    CFDSolver(ap)
    # rst Evaluate and print
    funcs = {}
    CFDSolver.evalFunctions(ap, funcs)
    # Print the evaluated functions
    if comm.rank == 0:
        print(funcs)

elif args.task == "polar":
    # Create an array of alpha values.
    # In this case we create 6 evenly spaced values from 0 - 5.
    alphaList = np.linspace(0, 5, 6)

    # Create storage for the evaluated lift and drag coefficients
    CLList = []
    CDList = []


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

    # Print the evaluated functions in a table
    if comm.rank == 0:
        print("{:>6} {:>8} {:>8}".format("Alpha", "CL", "CD"))
        print("=" * 24)
        for (alpha, cl, cd) in zip(alphaList, CLList, CDList):
            print(f"{alpha:6.1f} {cl:8.4f} {cd:8.4f}")


