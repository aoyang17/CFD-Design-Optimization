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
parser.add_argument("--output", type=str, default="output_analysis_non_optimized")
parser.add_argument("--opt", type=str, default="SLSQP", choices=["IPOPT", "SLSQP", "SNOPT"])
# parser.add_argument("--gridFile", type=str, default="/home/aobo/MACH-Aero/Operate_mission_ASO/Mode_based_ASO/opeartion_mode_based/ADODG429_091_vol.cgns")
# parser.add_argument("--gridFile", type=str, default="/home/aobo/MACH-Aero/Operate_mission_ASO/Analyze_warpped_CGNS/GMM_optimzed_wing/ADODG429_057_vol.cgns")
# parser.add_argument("--gridFile", type=str, default="/home/aobo/MACH-Aero/Operate_mission_ASO/Analyze_warpped_CGNS/Single_pt_optimized_wing/ADODG40_061_vol.cgns")
# parser.add_argument("--gridFile", type=str, default="/home/aobo/MACH-Aero/Operate_mission_ASO/Analyze_warpped_CGNS/Ninepts_optimized_wing/ADODG48_088_vol.cgns")
# parser.add_argument("--gridFile", type=str, default="/home/aobo/MACH-Aero/Operate_mission_ASO/Analyze_warpped_CGNS/Ninepts_optimized_wing/ADODG48_088_vol.cgns")
parser.add_argument("--gridFile", type=str, default="/home/aobo/MACH-Aero/input/L3_peter_rotat_mirror_bc.cgns")
parser.add_argument("--task", choices=["analysis", "polar"], default="analysis")
parser.add_argument("--optOptions", type=ast.literal_eval, default={}, help="additional optimizer options to be added")
args = parser.parse_args()

MP = multiPointSparse(MPI.COMM_WORLD)
MP.addProcessorSet("cruise", nMembers=1, memberSizes=MPI.COMM_WORLD.size)
comm, setComm, setFlags, groupFlags, ptID = MP.createCommunicators()
 
if not os.path.exists(args.output):
    if comm.rank == 0:
        os.mkdir(args.output)

# validate_data = pd.read_csv("Aero-validation-m-original.csv")
validate_data = pd.read_csv("/home/aobo/MACH-Aero/Operate_mission_ASO/Analyze_warpped_CGNS/new_data_aero.csv")

new_data = {}

for index, row in validate_data.iterrows():

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

    # Create solver
    CFDSolver = ADFLOW(options=aeroOptions, comm=comm)
    CFDSolver.addLiftDistribution(200, "z")

    span = 3.758150834
    pos = np.array([0.0235, 0.267, 0.557, 0.695, 0.828, 0.944])*span
    CFDSolver.addSlices('z', pos, sliceType='absolute')

    # alphaList = [2.2100]
    mach = 0.85
    alt = 11740
    AoA = 2.298939

    ap = AeroProblem(name='fc%d'%index, mach=row["mach"],alpha=row["alpha"], altitude=11740,
                    areaRef=3.407014, chordRef=1.00,
                    xRef=1.20777, yRef=.007669, zRef=0, evalFuncs=['cd', 'cl', 'cmz'])



    CFDSolver(ap)
    # rst Evaluate and print
    funcs = {}
    CFDSolver.evalFunctions(ap, funcs)
    # Print the evaluated functions
    if comm.rank == 0:
        print(funcs)

    # coeff = [funcs[f"{ap.name}_cl"],funcs[f"{ap.name}_cd"],funcs[f"{ap.name}_cmz"]]
    # coeff = np.array(coeff,dtype=object)

    new_data[index] = pd.DataFrame({
        'alpha': np.array(row["alpha"],dtype=object),
        'mach': np.array(row["mach"],dtype=object),
        # 'alt': np.array(row["alt"],dtype=object),
        'cl': np.array(funcs[f"{ap.name}_cl"],dtype=object),
        'cd': np.array(funcs[f"{ap.name}_cd"],dtype=object),
        'cmz': np.array(funcs[f"{ap.name}_cmz"],dtype=object),
    },index=[0])

final = pd.concat(list(new_data.values()), ignore_index=True)
final.to_csv("Optimized_wing_non_optimized.csv")