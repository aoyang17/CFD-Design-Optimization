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
from DVGeometry_FFD_MODE import DVGeometry_FFD_MODE
import pyspline

# from MF_adjoint_free.EGO_opt import DVList 

# Use Python's built-in Argument parser to get commandline options
parser = argparse.ArgumentParser()
parser.add_argument("--output", type=str, default="output_single")
parser.add_argument("--opt", type=str, default="SLSQP", choices=["IPOPT", "SLSQP", "SNOPT"])
parser.add_argument("--gridFile", type=str, default="./input/L3_peter_rotat_mirror_bc.cgns")
parser.add_argument("--FFDFile", type=str, default="./input/rot.xyz")
parser.add_argument("--task", choices=["analysis", "polar"], default="analysis")
parser.add_argument("--optOptions", type=ast.literal_eval, default={}, help="additional optimizer options to be added")
args = parser.parse_args()

MP = multiPointSparse(MPI.COMM_WORLD)
MP.addProcessorSet("cruise", nMembers=1, memberSizes=MPI.COMM_WORLD.size)
comm, setComm, setFlags, groupFlags, ptID = MP.createCommunicators()

if not os.path.exists(args.output):
    if comm.rank == 0:
        os.mkdir(args.output)

data = np.loadtxt("optmum.dat")
gridFile = './input/L3_peter_rotat_mirror_bc.cgns'
output = 'output_single'
FFDFile = './input/rot.xyz'
modedata = np.loadtxt('./input/modes.dat')
modes = modedata[:50,:].copy()
nmode = 50

optbounds = np.loadtxt('./input/bounds.txt')
nmode = 50

modedata = np.loadtxt('./input/modes.dat')
modes = modedata[:nmode,:].copy()


aeroOptions = {
        # I/O Parameters
        "gridFile": args.gridFile,
        "outputDirectory": args.output,
        # Common Parameters
        'monitorVariables':["resrho", "cl", "cd", "cmz"],
        'volumeVariables':['cp','mach'],
        'isoSurface':{'shock':1.0},     
        # Physics Parameters
        'equationType':'RANS',#args.mode,
        'smoother':'DADI',#gridops[args.level]['s'],
        'frozenturbulence':False,
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



DVGeo = DVGeometry_FFD_MODE(args.FFDFile)

nSpanwise = 8
# Create the Ref line
coef = DVGeo.FFD.vols[0].coef.copy()
X = np.zeros((nSpanwise,3))
for ispan in range(nSpanwise):
    Lep = 0.5*(coef[0,ispan,0,:]+coef[0,ispan,1,:])
    Tep = 0.5*(coef[-1,ispan,0,:]+coef[-1,ispan,1,:]) 
    X[ispan,:] = Lep + 0.25*(Tep - Lep)

c1 = pyspline.Curve(X=X, k=2)
DVGeo.addRefAxis('wing', c1, axis='z')

def twist(val, geo):
    # Set all the twist values
    for i in range(nSpanwise-1):
        geo.rot_z['wing'].coef[i+1] = val[i]

DVGeo.addGeoDVLocal_Mode('shape', modes, lower=optbounds[10:,0], upper=optbounds[10:,1], scale=1.0)
DVGeo.addGeoDVGlobal('wing_twist', np.zeros(nSpanwise-1), twist, lower=optbounds[3:10,0], upper=optbounds[3:10,1])

alpha = data[0]
twists = data[1:8]
mode_coeff = data[8:58]
mach_list = [0.85]
alt_list = [11740]

meshOptions = {"gridFile":args.gridFile}
mesh = USMesh(options=meshOptions)
coords = mesh.getSurfaceCoordinates()
DVGeo.writePlot3d("ffd_no_deform.xyz")

DVGeo.addPointSet(coords, "coords")
# dvDict = DVGeo.getValues()
# dvDict["wing_twist"] = np.array(twists)
# dvDict["shape"] = np.array(mode_coeff)

# DVGeo.setDesignVars(dvDict)
# DVGeo.update("coords")
# DVGeo.writePlot3d("ffd_deformed.xyz")
# DVGeo.writePointSet("coords", "surf")
# print(np.array(mode_coeff))
DVList={'shape':mode_coeff,'wing_twist':twists}   
DVGeo.setDesignVars(DVList) 
CFDSolver = ADFLOW(options=aeroOptions)
CFDSolver.addLiftDistribution(200, "z")

# print(DVGeo.getValues())

span = 3.758150834
pos = np.array([0.0235, 0.267, 0.557, 0.695, 0.828, 0.944])*span
CFDSolver.addSlices('z', pos, sliceType='absolute')

ap = AeroProblem(
    name="fc" ,
    alpha=alpha,
    mach=0.85,
    altitude=11740,
    # reynolds=5e6,
    # reynoldsLength=1.0,
    # T=326.45,
    areaRef= 3.407014,
    xRef=1.20777,
    yRef=.007669,
    zRef=0,
    chordRef=1.0,
    evalFuncs=["cl", "cd", "cmz"],
)
# Add angle of attack variable
ap.addDV("alpha", value=alpha, lower=1.0, upper=3.0, scale=1.0)

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
