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
try:
    from collections import OrderedDict
except ImportError:
    try:
        from ordereddict import OrderedDict
    except ImportError:
        print("Could not find any OrderedDict class. For 2.6 and earlier, "
              "use:\n pip install ordereddict")
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

#NonevlueS = 0.0

optOptions = {'Major iterations limit':1000,
                 'Minor iterations limit':5000,
                 'Iterations limit':10000,
                 'Major step limit':1.,
                 'Major feasibility tolerance':1.0e-6,
                 'Major optimality tolerance':1.0e-6,
                 'Minor feasibility tolerance':1.0e-6,
                 'Verify level':-1,
                 'Function precision':3e-6,
                 'Hessian updates':10,}
optOptions={'MAXIT':5000}
outputDirectory = args.output
saveRepositoryInfo(outputDirectory)

ransFile = '../../input/baseairfoil.cgns'
FFDFile = '../../input/FFD.xyz'
nGroup = 1
nProcPerGroup = 8
aeroProblems = []
nFlowCases = 1 #len(mach)

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
    'nCycles':10000,
    'monitorvariables':['resrho','cd'],#,'cl','cmz'],
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
    'nkswitchtol':1e-8, #2e-4,
    'nkouterpreconits':3,
    'NKInnerPreConIts':3,
    'writeSurfaceSolution':True,
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
  'LdefFact':100.0,
  'alpha':0.1,
  'errTol':1e-5
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
    #mesh = MBMesh(options=meshOptions, comm=comm)
    mesh = USMesh(options=usoptions, comm=comm)
    CFDSolver.setMesh(mesh)



name = 'fc'
ap = AeroProblem(name=name, mach=myMa,  altitude=myAltitude, 
                 alpha=0.0,
                 areaRef=1., chordRef=1.00,xRef=0.25,yRef=0.0,zRef=0.0, evalFuncs=['cd'])#['cl','cd','cmz'])

funcs = {}
CFDSolver(ap)
CFDSolver.evalFunctions(ap, funcs)              
DVGeo.writePlot3d('FFD.xyz')                
                 
