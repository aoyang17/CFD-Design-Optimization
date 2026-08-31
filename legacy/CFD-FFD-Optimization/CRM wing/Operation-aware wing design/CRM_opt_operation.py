import argparse
import ast
from calendar import c
import os

import numpy as np
import pandas as pd
from adflow import ADFLOW
from baseclasses import AeroProblem
from idwarp import USMesh
from mpi4py import MPI
from multipoint import multiPointSparse
from pygeo import DVConstraints, DVGeometry, geo_utils
from pyoptsparse import OPT, Optimization


# Use Python's built-in Argument parser to get commandline options
parser = argparse.ArgumentParser()
parser.add_argument("--output", type=str, default="output_ffd_L3_operation")
parser.add_argument("--opt", type=str, default="SLSQP", choices=["IPOPT", "SLSQP", "SNOPT"])
parser.add_argument("--gridFile", type=str, default="crm_mesh_L3.cgns")
# parser.add_argument("--FFDFile", type=str, default="./input/FFD_large.xyz")
parser.add_argument("--gmmcsvFile", type=str, default="hybrid_extend_GMM_gmm_30.csv")
parser.add_argument("--FFDFile", type=str, default="ADODG4_FFD.xyz")
# parser.add_argument("--dataoutputFile", type=str, default="./gen_data/data_gen_L3_opt_ffd.txt")
parser.add_argument("--optOptions", type=ast.literal_eval, default={}, help="additional optimizer options to be added")
args = parser.parse_args() 

# assign number of processors
nGroup = 1
nProcPerGroup = MPI.COMM_WORLD.size
MP = multiPointSparse(MPI.COMM_WORLD)
MP.addProcessorSet("cruise", nMembers=nGroup, memberSizes=nProcPerGroup)
comm, setComm, setFlags, groupFlags, ptID = MP.createCommunicators()
if not os.path.exists(args.output):
    if comm.rank == 0:
        os.mkdir(args.output)

meshOptions = {
    'gridFile':args.gridFile,
    'fileType':'CGNS',
    'aExp': 3.0,
    'bExp': 5.0,
    'LdefFact':100.0,     # affects how far the deformations are pushed away from the surface
    'alpha':0.1,
    'errTol':1e-5
    }
mesh = USMesh(options=meshOptions, comm=comm)


aeroOptions = {
    # I/O Parameters
    "gridFile": args.gridFile,
    "outputDirectory": args.output,
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

# #multi_point_aero_conditions
coeff = pd.read_csv(args.gmmcsvFile)
nflowcase = coeff.shape[0]
# nflowcase = 30

mach = coeff['mach_means']
alpha = coeff['aoa_means']
alt = coeff['alt_means']
cl_list = coeff['CL_means']
w = coeff['weights']

CFDSolver = ADFLOW(options=aeroOptions, comm=comm)
CFDSolver.addLiftDistribution(200, "y")

span = 3.758150834
pos = np.array([0.0235, 0.267, 0.557, 0.695, 0.828, 0.944])*span
CFDSolver.addSlices('y', pos, sliceType='absolute')

# CFDSolver = ADFLOW(options=aeroOptions, comm=comm)
CFDSolver.setMesh(mesh)

aeroProblems = []
for i in range(nflowcase):

    ap = AeroProblem(
        name="wing%d" % i,
        alpha=alpha[i],
        mach=mach[i],
        altitude=alt[i],
        # reynolds=Re[i],
        # reynoldsLength=1.0,
        # T=326.45,
        areaRef= 3.407014,
        xRef=1.20777,
        yRef=0,
        zRef=.007669,
        chordRef=1.0,
        evalFuncs=["cl", "cd", "cmy"],
    )
    # Add angle of attack variable
    ap.addDV("alpha", value=alpha[i], lower=0, upper=10.0, scale=1.0)
    aeroProblems.append(ap)

#Design variables setup

# Create DVGeometry object
DVGeo = DVGeometry(args.FFDFile)

# Create reference axis
DVGeo.addRefAxis("wing", xFraction=0.25, alignIndex="j", rotType=5)
nTwist = 8


# Set up global design variables
def twist(val, geo):
    # Set all the twist values
    for i in range(nTwist):
        geo.rot_y['wing'].coef[i] = val[i]

DVGeo.addGlobalDV(dvName="twist", value=[0] * nTwist, func=twist, lower=-10.0, upper=10.0, scale=1.0)


# Set up local design variables
DVGeo.addLocalDV("shapez", lower=-1.0, upper=1.0, axis="z", scale=1.0)
# DVGeo.addLocalSectionDV("slocal", secIndex="j", axis=1, lower=-0.5, upper=0.5, scale=1)

# Add DVGeo object to CFD solver
CFDSolver.setDVGeo(DVGeo)




DVCon = DVConstraints()
DVCon.setDVGeo(DVGeo)

# Only ADflow has the getTriangulatedSurface Function
DVCon.setSurface(CFDSolver.getTriangulatedMeshSurface())

# Volume constraints
LE_pt = np.array([0.01, 0.01, 0.0])
break_pt = np.array([0.848, 1.119, 0.0])
tip_pt = np.array([2.855, 3.755, 0.0])
root_chord = 1.689
break_chord = 1.036
tip_chord = 0.390

leList = [
    [LE_pt[0] + 0.01 * root_chord, LE_pt[1], LE_pt[2]],
    [break_pt[0] + 0.01 * break_chord, break_pt[1], break_pt[2]],
    [tip_pt[0] + 0.01 * tip_chord, tip_pt[1], tip_pt[2]],
]

teList = [
    [LE_pt[0] + 0.99 * root_chord, LE_pt[1], LE_pt[2]],
    [break_pt[0] + 0.99 * break_chord, break_pt[1], break_pt[2]],
    [tip_pt[0] + 0.99 * tip_chord, tip_pt[1], tip_pt[2]],
]

# volume constraint
# DVCon.addVolumeConstraint(leList, teList, nSpan=25, nChord=30, lower=1.0, upper=3, scaled=True)
# DVCon.addVolumeConstraint(leList, teList, nSpan=25, nChord=30, lower=0.85, upper=1.15, scaled=True)
DVCon.addVolumeConstraint(leList, teList, nSpan=25, nChord=30, lower=1.0, upper=1.05, scaled=True)
# thickness constraint
# DVCon.addThicknessConstraints2D(leList, teList, nSpan=25, nChord=30, lower=0.5, upper=3.0, scaled=True)
# DVCon.addThicknessConstraints2D(leList, teList, nSpan=25, nChord=30, lower=0.25, upper=3.0, scaled=True)
DVCon.addThicknessConstraints2D(leList, teList, nSpan=25, nChord=30, lower=0.98, upper=3.0, scaled=True)

# Le/Te constraints
DVCon.addLeTeConstraints(0, "iLow")
DVCon.addLeTeConstraints(0, "iHigh")

if comm.rank == 0:
    # Only make one processor do this
    DVCon.writeTecplot(os.path.join(args.output, "constraints.dat"))

meshOptions = {
    "gridFile": args.gridFile,
    # "useRotations":False,
    # "symmetryPlanes":[[[0.0, 0.0, 0.0],[0.0, 1.0, 0.0]]],
}
mesh = USMesh(options=meshOptions, comm=comm)
CFDSolver.setMesh(mesh)

def cruiseFuncs(x):
    if comm.rank == 0:
        print(x)
    # Set design vars
    DVGeo.setDesignVars(x)
    ap.setDesignVars(x)
    # Run CFD
    CFDSolver(ap)
    # Evaluate functions
    funcs = {}
    DVCon.evalFunctions(funcs)
    
    for i in range(nflowcase):
        if i % nGroup == ptID:
            aeroProblems[i].setDesignVars(x)
            CFDSolver(aeroProblems[i])
            CFDSolver.evalFunctions(aeroProblems[i], funcs)
            CFDSolver.checkSolutionFailure(aeroProblems[i], funcs)
    if MPI.COMM_WORLD.rank == 0:
        print(funcs)
    return funcs


def cruiseFuncsSens(x, funcs):
    funcsSens = {}
    DVCon.evalFunctionsSens(funcsSens)
    for i in range(nflowcase):
        if i % nGroup == ptID:
            CFDSolver.evalFunctionsSens(aeroProblems[i], funcsSens)
            CFDSolver.checkAdjointFailure(aeroProblems[i], funcsSens)
    if MPI.COMM_WORLD.rank == 0:
        print(funcsSens)
    return funcsSens


def objCon(funcs, printOK):
    # Assemble the objective and any additional constraints:
    funcs["obj"] = 0.0
    for i in range(nflowcase):
        ap = aeroProblems[i]
        funcs["obj"] += funcs[ap["cd"]] * w[i]
        funcs["cl_con_" + ap.name] = funcs[ap["cl"]] - cl_list[i]
        # funcs['cmz_con_'+ ap.name] = 0.17 - funcs[ap["cmz"]]
        
    # funcs['cmz_con_'+ aeroProblems[4].name] = funcs[aeroProblems[4]["cmz"]] - cmcon
    if printOK:
        print("funcs in obj:", funcs)
    return funcs

# ######################

# alpha4CLTarget = ADFLOW.solveCL(aeroProblem=ap, CLStar=cl_target,alpha0=2.2)
# print(alpha4CLTarget)


# ######################

# Create optimization problem
optProb = Optimization("opt", MP.obj, comm=comm)

# Add objective
optProb.addObj("obj", scale=1)

# Add variables from the AeroProblem
for ap in aeroProblems:
    ap.addVariablesPyOpt(optProb)

# Add DVGeo variables
DVGeo.addVariablesPyOpt(optProb)

# Add constraints
DVCon.addConstraintsPyOpt(optProb)
for ap in aeroProblems:
    optProb.addCon(f"cl_con_{ap.name}", lower=0.0, upper=10.0,scale=1.0)
# optProb.addCon("cm_con_" + ap.name, lower=0.0, scale=1.0)
# The MP object needs the 'obj' and 'sens' function for each proc set,
# the optimization problem and what the objcon function is:
MP.setProcSetObjFunc("cruise", cruiseFuncs)
MP.setProcSetSensFunc("cruise", cruiseFuncsSens)
MP.setObjCon(objCon)
MP.setOptProb(optProb)
optProb.printSparsity()

# Set up optimizer

if args.opt == "SLSQP":
    optOptions = {
        "ACC":1.0e-7,
        "MAXIT":500,
        "IFILE": os.path.join(args.output, "SLSQP.out"),
    } 
elif args.opt == "SNOPT":
    optOptions = {
        "Major feasibility tolerance": 1e-5,
        "Major optimality tolerance": 1e-5,
        "Minor feasibility tolerance": 1.0e-7,
        "Verify level": -1,
        "Function precision": 1.0e-7,
        "Major iterations limit": 200,
        "Nonderivative linesearch": None,
        "Hessian full memory": None,
        "Print file": os.path.join(args.output, "SNOPT_print.out"),
        "Summary file": os.path.join(args.output, "SNOPT_summary.out"),
        "Major iterations limit": 1000,
    }
elif args.opt == "IPOPT":
    optOptions = {
        "limited_memory_max_history": 1000,
        "print_level": 5,
        "tol": 1e-6,
        "acceptable_tol": 1e-5,
        "max_iter": 300,
        "start_with_resto": "yes",
    }
optOptions.update(args.optOptions)
opt = OPT(args.opt, options=optOptions)

# Run Optimization
sol = opt(optProb, MP.sens, storeHistory=os.path.join(args.output, "opt.hst"))
if comm.rank == 0:
    print(sol)