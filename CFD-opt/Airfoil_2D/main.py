# ======================================================================
#         Import modules
# ======================================================================
import os
import argparse
import numpy
from mpi4py import MPI
from baseclasses import *
from adflow import ADFLOW
from idwarp import USMesh
from pygeo import *
from pyspline import *
from multipoint import *
from repostate import *
from pyoptsparse import Optimization, OPT

# ======================================================================
#         Input Information
# ======================================================================
parser = argparse.ArgumentParser()
parser.add_argument("--solver", help="solver to use: adflow or tripan",
                    type=str, default='adflow')
parser.add_argument("--mode", help="rans or euler. adflow solver only",
                   type=str, default='rans')
parser.add_argument("--output", help='Output directory', type=str,
                    default='./')
parser.add_argument("--shape", help='Use shape variables', type=int,
                    default=0)

parser.add_argument("--opt", help="optimizer to use", type=str, default='slsqp')
#parser.add_argument('--optOptions', type=str, help='Options for the optimizer', default="{}")

parser.add_argument("--cl", help="Cl", type=float, default=0.8)
parser.add_argument("--ma", help="Mach number", type=float, default=0.72)
parser.add_argument("--alti", help="Altitude", type=float, default=10000.)
args = parser.parse_args()

myMa  = 0.734#args.ma
mycl  = 0.824#args.cl
myAltitude = 11740.0#args.alti
cmcon = 0.092

optOptions={}
outputDirectory = args.output
saveRepositoryInfo(outputDirectory)

ransFile = './input/baseairfoil.cgns'
FFDFile = './input/FFD.xyz'
nGroup = 1
nProcPerGroup = 8
aeroProblems = []
nFlowCases = 1 #len(mach)

name = 'fc'
ap = AeroProblem(name=name, mach=myMa,  altitude=myAltitude, 
                 alpha=2.0,
                 areaRef=1., chordRef=1.00,xRef=0.25,yRef=0.0,zRef=0.0, evalFuncs=['cl','cd','cmz'])
ap.addDV('alpha', value=2.0, lower=0.5, upper=4.0, scale=1.0)
aeroProblems.append(ap)

gridFile = ransFile
MGCycle = 'sg'
AEROSOLVER = ADFLOW 

aeroOptions = {
    # Common Parameters
    'gridFile':gridFile,
    'outputDirectory':outputDirectory,

    # Physics Parameters
    'equationType':'RANS',
    'smoother':'dadi',

    'CFL':0.8,
    'CFLCoarse':0.4,
    'MGCycle':MGCycle,
    'MGStartLevel':-1,
    'nCyclesCoarse':1500,
    'nCycles':7000,
    'monitorvariables':['resrho','cl','cd','cmz'],
    'useNKSolver':True,
    'useanksolver' : True,
    'nsubiterturb' : 10,
    'liftIndex':2,
    # Convergence Parameters
    'L2Convergence':1e-12,
    'L2ConvergenceCoarse':1e-4,
    # Adjoint Parameters
    'adjointSolver':'gmres', #gmres,tfqmr,rechardson,bcgs,ibcgs
    'adjointL2Convergence':1e-12,
    'ADPC':True,
    #'ADPC':False, #hxl
    'adjointMaxIter': 1000,
    'adjointSubspaceSize':400,
    'ILUFill':3,
    #'ILUFill':2, #hxl
    'ASMOverlap':3,
    'outerPreconIts':3,
    #'innerPreconIts':2, #hxl
    'NKSubSpaceSize':400,
    'NKASMOverlap':4,
    'NKPCILUFill':4,
    'NKJacobianLag':5,
    'nkswitchtol':1e-6, #2e-4,
    'nkouterpreconits':3,
    'NKInnerPreConIts':3,
    'writeSurfaceSolution':False,
    'writeVolumeSolution':False,
    'frozenTurbulence':False,
    'restartADjoint':False,
    'rkreset':True,
    'nrkreset':100,
    }

meshOptions = {
    'gridFile':gridFile,
    'warpType':'algebraic',
    }
usoptions = {
  'gridFile':gridFile,
  'fileType':'CGNS',
  'specifiedSurfaces':None,
  'symmetrySurfaces':None,
  'symmetryPlanes':[],
  'aExp': 3.0,
  'bExp': 5.0,
  'LdefFact':1.0,
  'alpha':0.25,
  'errTol':0.0001,
  'evalMode':'fast',
  'useRotations':True,
  'zeroCornerRotations':True,
  'cornerAngle':30.0,
  'bucketSize':8,
}
# ======================================================================
#         Create multipoint communication object
# ======================================================================
MP = multiPointSparse(MPI.COMM_WORLD)
MP.addProcessorSet('cruise', nMembers=nGroup, memberSizes=nProcPerGroup)
comm, setComm, setFlags, groupFlags, ptID = MP.createCommunicators()

# Call common geometry setup
execfile('./setup_geometry.py')

# Create solver
CFDSolver = AEROSOLVER(options=aeroOptions, comm=comm)
CFDSolver.setDVGeo(DVGeo)

span = 1.0
pos = numpy.array([0.5])*span
CFDSolver.addSlices('z',pos,sliceType='absolute')


if args.solver == 'adflow':
    #mesh = MBMesh(options=meshOptions)#, comm=comm)
    mesh = USMesh(options=usoptions, comm=comm)
    CFDSolver.setMesh(mesh)

# Call common geometry constraint setup
execfile('./setup_constraints.py')

# ======================================================================
#         Functions:
# ======================================================================
def cruiseFuncs(x):
    if MPI.COMM_WORLD.rank == 0:
        print x

    funcs = {}
    DVGeo.setDesignVars(x)
    DVCon.evalFunctions(funcs)
    print DVCon
    for i in range(nFlowCases):
        if i%nGroup == ptID:
            aeroProblems[i].setDesignVars(x)
            CFDSolver(aeroProblems[i])
            CFDSolver.evalFunctions(aeroProblems[i], funcs)
            CFDSolver.checkSolutionFailure(aeroProblems[i], funcs)
    if MPI.COMM_WORLD.rank == 0:
        print funcs

    return funcs

def cruiseFuncsSens(x, funcs):
    funcsSens = {}
    DVCon.evalFunctionsSens(funcsSens)
    for i in range(nFlowCases):
        if i%nGroup == ptID:
            CFDSolver.evalFunctionsSens(aeroProblems[i], funcsSens)
    if MPI.COMM_WORLD.rank == 0:
        print funcsSens
    return funcsSens

def objCon(funcs, printOK):
    # Assemble the objective and any additional constraints:
    funcs['obj'] = 0.0
    for i in range(nFlowCases):
        ap = aeroProblems[i]
        funcs['obj'] += funcs[ap['cd']] / nFlowCases  
        funcs['cl_con_'+ap.name] = funcs[ap['cl']] - mycl
        funcs['cm_con_'+ap.name] = funcs[ap['cmz']] - cmcon
    if printOK:
       print 'funcs in obj:', funcs 
    return funcs
# ======================================================================
#         Set-up Optimization Problem
# ======================================================================
optProb = Optimization('opt', MP.obj, comm=MPI.COMM_WORLD)

# Add variables from each aeroProblem
for ap in aeroProblems:
    ap.addVariablesPyOpt(optProb)

# Add DVGeo variables
DVGeo.addVariablesPyOpt(optProb)

# Add DVConstraint constraints
DVCon.addConstraintsPyOpt(optProb)

# Add Objective
optProb.addObj('obj', scale=100)

# Aerodynamic constraints
for i in range(nFlowCases):
    ap = aeroProblems[i]
    optProb.addCon('cl_con_'+ap.name, lower=0.0, upper=0.0, scale=1.0)
    optProb.addCon('cm_con_'+ap.name, lower=-10.0, upper=0.0, scale=1.0)

    #optProb.addCon('sepsensor_con_'+ap.name, upper=0.04, scale=1.0)

# The MP object needs the 'obj' and 'sens' function for each proc set,
# the optimization problem and what the objcon function is:
MP.setProcSetObjFunc('cruise', cruiseFuncs)
MP.setProcSetSensFunc('cruise', cruiseFuncsSens)
MP.setObjCon(objCon)
MP.setOptProb(optProb)
optProb.printSparsity()

# Make Instance of Optimizer
opt = OPT(args.opt, options=optOptions)

# Run Optimization
histFile = os.path.join(outputDirectory, '%s_hist.hst'%args.opt)
sol = opt(optProb, MP.sens, storeHistory=histFile)
if MPI.COMM_WORLD.rank == 0:
    print sol
