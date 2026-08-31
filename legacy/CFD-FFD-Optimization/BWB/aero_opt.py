'''
The leading edges are fixed, and the trailing edge of root is fixed as well.
'''
# ======================================================================
#         Import modules
# ======================================================================
from __future__ import print_function
import os
import argparse
import numpy
from mpi4py import MPI
from baseclasses import *
from adflow import ADFLOW
from pygeo import *
from pyspline import *
from multipoint import *
from repostate import *
from pyoptsparse import Optimization, OPT, SqliteDict
from idwarp import USMesh
# Ignore deprecation warnings
import warnings
warnings.filterwarnings('ignore')

# ======================================================================
#         Input Information
# ======================================================================
parser = argparse.ArgumentParser()
parser.add_argument('--mode', help='rans or euler. adflow solver only', type=str, default='rans')
parser.add_argument('--task', help='what to do', type=str, default='opt', choices=['opt', 'postprocess', 'analysis'])
parser.add_argument('--opt', help='optimizer to use', type=str, default='slsqp')
parser.add_argument('--hotStart', help='history file to start with', type=str, default=None)
parser.add_argument('--level', type=str, default='L3', choices=['L3','L2','L1'])
parser.add_argument('--odir', type=str, default='./')
parser.add_argument("--nmode", help='Number of modes to use', type=int,default=2)
parser.add_argument("--concm", help="Cm con", type=float, default=0.0)
parser.add_argument("--concl", help="Cl con", type=float, default=0.2)
parser.add_argument("--myM", help="Mach number", type=float, default=0.85)
parser.add_argument("--myAlti", help="Altitude", type=float, default=10000.)

args = parser.parse_args()
saveRepositoryInfo(args.odir)

#mymission=numpy.loadtxt('mission.dat')

mycm  = 0.0
mycl  = 0.200561319832222#mymission[2]
myaltitude  = 10670.#mymission[1]
myMach  = 0.85#mymission[0]

gridFile = './input/bwb.cgns'

FFDFile = './input/FFD_bwb.xyz'
nGroup = 1
nProcPerGroup = 16
outputDirectory = args.odir


# Setup Flight Information
cl_star = mycl
cmx_star = mycm
nFlowCases = 1
feetcoef = 0.3048 
wingarea = 15860*feetcoef*feetcoef*0.5
wingchord = 86*feetcoef

ap = AeroProblem(name='fc', mach=myMach, altitude=myaltitude, areaRef=wingarea, chordRef=wingchord, 
                  alpha=0.58, xRef=26, yRef=.0, zRef=0, evalFuncs=['cd', 'cl', 'cmz'])

# Add angle of attack variable
ap.addDV('alpha', lower=0, upper=2.5, scale=1.0)
AEROSOLVER = ADFLOW
aeroOptions = {
    # Common Parameters
    'gridFile':gridFile,
    'outputDirectory':args.odir,
    'monitorVariables':['cl','cd','cmz'],
    'volumeVariables':['cp','mach'],
    'isoSurface':{'shock':1.0},     
    # Physics Parameters
    'equationType':'rans',#args.mode,
    'smoother':'dadi',#gridops[args.level]['s'],
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
    'ankstepinit' : 0.1,
    'ankstepexponent' : 0.5,
    'ankcflexponent' : 0.5,
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

# ======================================================================
#         Create multipoint communication object
# ======================================================================
MP = multiPointSparse(MPI.COMM_WORLD)
MP.addProcessorSet('cruise', nMembers=nGroup, memberSizes=nProcPerGroup)
comm, setComm, setFlags, groupFlags, ptID = MP.createCommunicators()

# Create solver
CFDSolver = AEROSOLVER(options=aeroOptions, comm=comm)


# Set up mesh warping
meshOptions = {
    'gridFile':gridFile,
    'warpType':'unstructured',
    'aExp': 3.0,
    'bExp': 5,
    'LdefFact':100.0,     # affects how far the deformations are pushed away from the surface
    'alpha':0.1,
    'errTol':1e-5
    }
mesh = USMesh(options=meshOptions, comm=comm)
CFDSolver.setMesh(mesh)

span = 42
pos = numpy.array([2.1, 7.56, 13.02, 18.48, 23.94, 29.4, 34.86, 40.32])
CFDSolver.addSlices('z', pos, sliceType='absolute')
CFDSolver.addLiftDistribution(100, 'z')

# ======================================================================
#         DVGeometry
# ======================================================================
#DVGeo = DVGeometryMode(FFDFile)
DVGeo = DVGeometry(FFDFile)
#DVGeo.addRefAxis('wing', xFraction=.25, alignIndex='j', rotType=5)
nSpanwise = 8
# Create the Ref line
coef = DVGeo.FFD.vols[0].coef.copy()
X = numpy.zeros((nSpanwise,3))
for ispan in range(nSpanwise):
    Lep = 0.5*(coef[0,0,ispan,:]+coef[0,1,ispan,:])
    Tep = 0.5*(coef[-1,0,ispan,:]+coef[-1,1,ispan,:]) 
    X[ispan,:] = Lep + 0.25*(Tep - Lep)

c1 = pySpline.Curve(X=X, k=2)
DVGeo.addRefAxis('wing', c1)


def twist(val, geo):
    # Set all the twist values
    for i in range(nSpanwise-1):
        geo.rot_z['wing'].coef[i+1] = val[i]

#DVGeo.addRefAxis('wing', xFraction=.25, alignIndex='j', rotType=5)
DVGeo.addGeoDVLocal('shape', lower=-3., upper=3.0, scale=1.0)
DVGeo.addGeoDVGlobal('wing_twist', numpy.zeros(nSpanwise-1), twist, lower=-5.0, upper=5.0)

CFDSolver.setDVGeo(DVGeo)

# ======================================================================
#         DVConstraints
# ======================================================================
DVCon = DVConstraints()
DVCon.setDVGeo(DVGeo)
DVCon.setSurface(CFDSolver.getTriangulatedMeshSurface())

# Setup curves for ref_axis
x_le = numpy.loadtxt('./input/leref.dat')
x_te = numpy.loadtxt('./input/teref.dat')

#DVCon.addVolumeConstraint(x_le, x_te, nSpan=25, nChord=30, lower=1.0, upper=5, scaled=True)
DVCon.addThicknessConstraints2D(name='thickness', leList=x_le, teList=x_te, nSpan=25, nChord=30, lower=1.0, upper=1.0)

if MPI.COMM_WORLD.rank == 0:
    fileName = os.path.join(args.odir, 'constraints.dat')
    DVCon.writeTecplot(fileName)

#DVCon.addLeTeConstraints(volID=0,faceID='iLow')
#DVCon.addLeTeConstraints(volID=0,faceID='iHigh')


# ======================================================================
#         Functions:
# ======================================================================
def cruiseFuncs(x):
    if MPI.COMM_WORLD.rank == 0:
        print(x)
    funcs = {}
    DVGeo.setDesignVars(x)
    DVCon.evalFunctions(funcs)
    ap.setDesignVars(x)
    CFDSolver(ap)
    CFDSolver.evalFunctions(ap, funcs)
    CFDSolver.checkSolutionFailure(ap, funcs)

    sol = CFDSolver.getSolution()
    global iteration

    if MPI.COMM_WORLD.rank == 0:
        f = open(outputDirectory+str(iteration)+'_cdcl.dat','w')
        f.write('%f %f %f %f %f %f\n'%(sol['cd'],sol['cd'],sol['cl'],sol['cmx'],sol['cmy'],sol['cmz']))
        f.close()

    if MPI.COMM_WORLD.rank == 0:
        print(x, funcs)

    iteration = iteration + 1

    return funcs

def cruiseFuncsSens(x, funcs):
    funcsSens = {}
    DVCon.evalFunctionsSens(funcsSens)
    CFDSolver.evalFunctionsSens(ap, funcsSens)
    #if MPI.COMM_WORLD.rank == 0:
        #print(funcsSens)
    return funcsSens

def objCon(funcs, printOK):
    # Assemble the objective and any additional constraints:
    funcs['obj'] = funcs[ap['cd']]
    funcs['cl_con_'+ap.name] = funcs[ap['cl']] - cl_star
    funcs['cmz_con'] = funcs[ap['cmz']] - cmx_star
    if printOK:
       print('funcs in obj:', funcs)
    return funcs


# ======================================================================
#         Set-up Optimization Problem
# ======================================================================

iteration = 0

optProb = Optimization('opt', MP.obj, comm=MPI.COMM_WORLD)

# Add variables from each aeroProblem
ap.addVariablesPyOpt(optProb)

# Add DVGeo variables
DVGeo.addVariablesPyOpt(optProb)

# Add DVConstraints
DVCon.addConstraintsPyOpt(optProb)

# Add Objective
optProb.addObj('obj', scale=1e1)

# Aerodynamic constraints
optProb.addCon('cl_con_'+ap.name, lower=0, upper=0, scale=1.0)
optProb.addCon('cmz_con', lower=0.0, upper=0.0, scale=1.0)

# The MP object needs the 'obj' and 'sens' function for each proc set,
# the optimization problem and what the objcon function is:
MP.setProcSetObjFunc('cruise', cruiseFuncs)
MP.setProcSetSensFunc('cruise', cruiseFuncsSens)
MP.setObjCon(objCon)
MP.setOptProb(optProb)
optProb.printSparsity()

# Make Instance of Optimizer
optOptions = {}
opt = OPT(args.opt, options=optOptions)

# Hot-start option
hotStart = None
if args.hotStart:
    #  hotStart = args.hotStart
        db = SqliteDict(args.hotStart)
        xhist = db[db['last']]['xuser']
        db.close()
        optProb.setDVs(xhist)

# Run Optimization
histFile = os.path.join(args.odir, '%s_hist.hst'%args.opt)
sol = opt(optProb, MP.sens, storeHistory=histFile, hotStart=hotStart)
if MPI.COMM_WORLD.rank == 0:
    print(sol)

DVGeo.writePlot3d(args.odir + 'modifiedFFD.dat')
