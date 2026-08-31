# ======================================================================
#       Import modules
# ======================================================================

import os
import argparse
import numpy
from mpi4py import MPI
from baseclasses import *
from adflow import ADFLOW

from idwarp import *
from pygeo import *
from pyspline import *
from multipoint import *
from repostate import *
from pyoptsparse import Optimization, OPT

# Ignore deprecation warnings
import warnings
warnings.filterwarnings("ignore")

# from sqlitedict import SqliteDict

# ======================================================================
#         Input Information
# ======================================================================
parser = argparse.ArgumentParser()
parser.add_argument("--procs", help="number of processors", type=int, default=24)
parser.add_argument("--opt", help="optimizer to use", type=str, default='slsqp')
args = parser.parse_args()

outputDirectory = './output'
os.system('mkdir {0}'.format(outputDirectory))
#saveRepositoryInfo(outputDirectory)

ransFile = './input/vol0.cgns' # specify the initial CFD grid
FFDFile = './input/new.xyz' # specify the initial FFD control volume

geoSetup = './setup_geometry.py'
geoConsSetup = './setup_constraints.py'

nTwistwing = 7  # In this case, we have 10 sections, however, the wing root is not supposed to be rotated.
nTwisttail = 2
nGroup = 1   # Typically a group uses only one grid, but could do series of flow condition, like different Mach numbers 
nProcPerGroup = args.procs

Mach = [0.85] # a python list contains series of Mach numbers
H = [10670]   # a python list contains series of Altitude
Cltarg= [0.5] # a python list contains series of CL target

myaltitude=H[0]

'''
Re = [5e6] # reynolds
T = [310.928] # 100F
'''

LEline=numpy.loadtxt('./input/LEcon.dat')
TEline=numpy.loadtxt('./input/TEcon.dat')
TailLEline=numpy.loadtxt('./input/TailLEcon.dat')
TailTEline=numpy.loadtxt('./input/TailTEcon.dat')


Sref = [191.845] # semi aicraft area
Chord = [7.005]  # aerodynamic chord

T=273.0
reynolds = 5.0e6
reynoldsLength = 7.005
Alphaini = [2.791] 
Alphaini_upper =[4.0]
Alphaini_floor =[1.0]
Pref = [33.677, 0.0077, 4.52] # reference point 

aeroProblems = []  # Initialization the aeroProblems object
nFlowCases = len(Mach) 

ap =AeroProblem(name='AeroCRM', mach=Mach[0],altitude=myaltitude, 
                areaRef=Sref[0], alpha=Alphaini[0], chordRef=Chord[0],
                evalFuncs=['cl','cd','cmy'],
                xRef=Pref[0], yRef=Pref[1], zRef=Pref[2] )
ap.addDV('alpha', value= Alphaini[0], lower=Alphaini_floor[0], upper=Alphaini_upper[0], scale=1.0)
aeroProblems.append(ap)

AEROSOLVER = ADFLOW

# Options settings for flow and ajoint solver (ADFLOW)
aeroOptions = {

    # Common Parameters  
    
    'gridFile':ransFile,
    'outputDirectory':outputDirectory,
    'writeSurfaceSolution':True,
    'writeVolumeSolution':True,
    'numberSolutions':True,
    'isoSurface':{'shock':0.98,'vx':-0.0001},
    'loadbalanceiter':2,

    # Physics Parameters'
    
    'equationType':'RANS',

    # Common Parameters
    
    'liftIndex':3,
    'CFL':1.25,
    'CFLCoarse':1.0,
    'MGCycle':'sg',

    'nCyclesCoarse':15000,
    'nCycles':20000,
    'nsubiterturb':10,

    'useANKSolver':True,
	'ankmaxiter' : 60,
    'anksecondordswitchtol':1e-3,


    'useNKSolver':True,
    # 'rkreset':True,
    # 'nrkreset':100,
    'nkadpc':True,
    'nksubspacesize':150,

    'nkls':'non monotone',
    #'nkviscpc':True,
    'nkswitchtol':1.0e-6,
    'nkpcilufill':2,
    'turbresscale':30000.0,          
    'dissipationlumpingparameter':5.0,
    'nkjacobianlag':5,
    'nkouterpreconits':3,
    'nkadpc':True,
    #'nkpcfastcoloring':False,
    'nkasmoverlap':2,
    'matrixordering':'rcm',
    'preconditionerside':'right',
    
    # Convergence Parameters
    'L2Convergence':1e-12,
    'L2ConvergenceCoarse':1e-5,

    # Load Balance Paramters
    
    'blockSplitting':True,
    'loadImbalance':0.10,
    'loadbalanceiter':2,

    # Misc Paramters
    
    'printIterations':True,
    'printTiming':True,
    'monitorVariables':['totalR','resrho','cl','cd','cmy','yplus'],
    'surfaceVariables':['vx','vy','vz','rho','P','mach','cp','temp'],
    'volumevariables':['resrho','rhoe','vort','mach','dist','eddy','resturb','cp','ptloss'],
    'numberSolutions':True,

    # Adjoint Paramters
    
    'adjointL2Convergence':1e-12,
    'approxPC': True,
    'viscPC':False,
    'ADPC':True,
    'restartAdjoint':True,
    'adjointSolver': 'GMRES',
    'adjointMaxIter': 1000,
    'adjointSubspaceSize' : 200,
    'adjointMonitorStep': 10,
    'preconditionerSide': 'RIGHT',
    'matrixOrdering': 'RCM',
    'globalPreconditioner': 'Additive Schwartz',
    'localPreconditioner' : 'ILU',
    'ILUFill':2,
    'ASMOverlap':2,
    'innerpreconits':1,
    'outerpreconits':3,
    'frozenTurbulence':False,
    }

# Options settings for grid input and warping

meshOptions = {
    'gridFile':ransFile,
    'errTol':0.001
    }


# Options settins for optimization
optOptions = {}

# ======================================================================
#         Create multipoint communication object
# ======================================================================

MP = multiPointSparse(MPI.COMM_WORLD)
MP.addProcessorSet('cruise', nMembers=nGroup, memberSizes=nProcPerGroup)
comm, setComm, setFlags, groupFlags, ptID = MP.createCommunicators()

# =================================================================================
#         Set up the Geometry Parameterization using DVGeometry with FFD approach
# =================================================================================
# Call common geometry setup
execfile(geoSetup)

# ======================================================================
#         Solver Settings
# ======================================================================

# Create solver
CFDSolver = AEROSOLVER(options=aeroOptions, comm=comm)
CFDSolver.setDVGeo(DVGeo)
# Set the DVGeometry object that will manipulate geometry in this object. Note that SUmb does not strictly need a DVGeometry object, 
# but if optimization with geometric changes is desired, then it is required.

#mesh = MBMesh(options=meshOptions, comm=comm)
mesh = USMesh(options=meshOptions, comm=comm)

# mesh.writeTopology('mesh.topo')

CFDSolver.setMesh(mesh)
# Set the mesh object to ADFLOW to do geometric deformations

# ================================================================
#         Settings for Lift and Wing Sections Cp monitoring 
# ================================================================

# Faimily list is: ['wing:downwing', 'wing:other', 'wing:upwing', 'sym', 'far']
CFDSolver.addFamilyGroup('wing',['wingte', 'wingu','wingle','wingl'])

span = 29.3815
pos  = numpy.array([0.12, 0.28, 0.45, 0.60, 0.75, 0.9])*span
CFDSolver.addSlices('y', pos, sliceType='absolute', groupName='wing')
pos  = numpy.array([0.12, 0.28])*span
CFDSolver.addSlices('y', pos, sliceType='absolute', groupName='tail')
CFDSolver.addLiftDistribution(200, 'y', groupName='wing')

# ================================================================
#         Settings for Adding Constraints
# ================================================================
# Call common geometry constraint setup
execfile(geoConsSetup)


# ======================================================================
#         Functions:
# ======================================================================

global iCFD
iCFD=0

def cruiseFuncs(x):
        
    global iCFD
    iCFD=iCFD+1
    funcs = {}
    DVGeo.setDesignVars(x)
    DVCon.evalFunctions(funcs)    
    if MPI.COMM_WORLD.rank == 0:
        print 'iCFD=',iCFD

    for i in xrange(nFlowCases):
        if i%nGroup == ptID:
            aeroProblems[i].setDesignVars(x)
            CFDSolver(aeroProblems[i])
            CFDSolver.evalFunctions(aeroProblems[i], funcs)
            CFDSolver.checkSolutionFailure(aeroProblems[i], funcs)
            
    if MPI.COMM_WORLD.rank == 0:
        print x
        print funcs
        
    return funcs

def cruiseFuncsSens(x, funcs):
    funcsSens = {}
    DVCon.evalFunctionsSens(funcsSens)
    for i in xrange(nFlowCases):
        if i%nGroup == ptID:
            CFDSolver.evalFunctionsSens(aeroProblems[i], funcsSens)
    if MPI.COMM_WORLD.rank == 0:
        print funcsSens
    return funcsSens

def objCon(funcs):
    # Assemble the objective and any additional constraints:
    funcs['obj'] = 0.0

    ap_cruise = aeroProblems[0]
    funcs['obj'] += funcs[ap_cruise['cd']]
    funcs['ClConstraints'] = funcs[ap_cruise['cl']] - Cltarg[0]
    funcs['CmyConstraints'] = funcs[ap_cruise['cmy']]
    if MPI.COMM_WORLD.rank == 0:
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
optProb.addObj('obj', scale=10000)

# Aerodynamic constraints
ap_cruise = aeroProblems[0]
optProb.addCon('ClConstraints', lower=0.0, upper=0.0, scale=1.0)
optProb.addCon('CmyConstraints', lower=0.0, upper=0.0, scale=1.0)

# The MP object needs the 'obj' and 'sens' function for each proc set,
# the optimization problem and what the objcon function is:
MP.setProcSetObjFunc('cruise', cruiseFuncs)
MP.setProcSetSensFunc('cruise',cruiseFuncsSens)
MP.setObjCon(objCon)
MP.setOptProb(optProb)
optProb.printSparsity()

# Make Instance of Optimizer
opt = OPT(args.opt, options=optOptions)

#optProb.setDVsFromHistory('./opt.hst')

# Run Optimization
histFile = outputDirectory+'/opt.hst'
sol = opt(optProb, MP.sens, storeHistory=histFile)

#hotStartFile = './opt_hist.hst'
#sol = opt(optProb, MP.sens, storeHistory=histFile , hotStart = hotStartFile)
#use the command above to set the optimization restart from previous one

if MPI.COMM_WORLD.rank == 0:
    print sol
