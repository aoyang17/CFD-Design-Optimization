import os
import ast
import sys
import time
import argparse
from mpi4py import MPI
import numpy as np
import tensorflow as tf
from scipy import linalg
from scipy.stats import norm

from multipoint import *
from multipoint import multiPointSparse
from baseclasses import AeroProblem
from adflow import ADFLOW

from pyoptsparse import Optimization, OPT
from smt.sampling_methods import LHS
 
from DVGeometry_FFD_MODE import DVGeometry_FFD_MODE

import pyspline
from idwarp import USMesh
# from MFNN_SUR import AeroSurrogate
from SUR import AeroSurrogate
from pygeo import DVConstraints


os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "1"

parser = argparse.ArgumentParser()
parser.add_argument("--output", type=str, default="history_MF")
parser.add_argument("--opt", type=str, default="SLSQP", choices=["IPOPT", "SLSQP", "SNOPT"])
parser.add_argument("--gridFile", type=str, default="/home/aobo/MACH-Aero/input/L3_peter_rotat_mirror_bc.cgns")
parser.add_argument("--FFDFile", type=str, default="/home/aobo/MACH-Aero/input/rot.xyz")
parser.add_argument("--optOptions", type=ast.literal_eval, default={}, help="additional optimizer options to be added")
args = parser.parse_args()

# os.system('mkdir history')

nFlowCases = 9
mach_list=[0.82,0.82,0.82,0.85,0.85,0.85,0.88,0.88,0.88]
cl_list=[0.483,0.537,0.591,0.45,0.5,0.55,0.42,0.466,0.513]
coefs_list =[1.0/16.0,1.0/8.0,1.0/16.0,1.0/8.0,1.0/4.0,1.0/8.0,1.0/16.0,1.0/8.0,1.0/16.0]
Re_list = [4.82e6, 4.82e6, 4.82e6, 5e6, 5e6, 5e6, 5.18e6, 5.18e6, 5.18e6]

cmcon = -0.17

nGroup = 1
nProcPerGroup = 1
outputDirectory = './'
MP = multiPointSparse(MPI.COMM_WORLD)
MP.addProcessorSet('cruise', nMembers=nGroup, memberSizes=nProcPerGroup)
comm, setComm, setFlags, groupFlags, ptID = MP.createCommunicators()
if not os.path.exists(args.output):
    if comm.rank == 0:
        os.mkdir(args.output)



# Set up mesh warping
meshOptions = {
    'gridFile':args.gridFile,
    'fileType':'CGNS',
    # 'warpType':'unstructured',
    'aExp': 3.0,
    'bExp': 5.0,
    'LdefFact':100.0,     # affects how far the deformations are pushed away from the surface
    'alpha':0.1,
    'errTol':1e-5
    }
mesh = USMesh(options=meshOptions, comm=comm)

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
DVGeo.addRefAxis('wing', c1)

nSpanwise = 8

def twist(val, geo):
    # Set all the twist values
    for i in range(nSpanwise-1):
        geo.rot_z['wing'].coef[i+1] = val[i]

optbounds = np.loadtxt('/home/aobo/MACH-Aero/input/bounds.txt')
nmode = 50

modedata = np.loadtxt('/home/aobo/MACH-Aero/input/modes.dat')
modes = modedata[:nmode,:].copy()

DVGeo.addGeoDVLocal_Mode('shape', modes, lower=optbounds[10:,0], upper=optbounds[10:,1], scale=20.0)
DVGeo.addGeoDVGlobal('wing_twist', np.zeros(nSpanwise-1), twist, lower=-1.0, upper=1.0, scale=0.2)

# Create dummy solver
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

CFDSolver = ADFLOW(options=aeroOptions, comm=comm)
CFDSolver.setMesh(mesh)
CFDSolver.setDVGeo(DVGeo)

# DVConstraints
DVCon = DVConstraints()
DVCon.setDVGeo(DVGeo)
DVCon.setSurface(CFDSolver.getTriangulatedMeshSurface())


LE_pt = np.array([.01, 0.0,0.01])
break_pt = np.array([.8477, 0.0, 1.11853])
tip_pt = np.array([2.85680, 0.0, 3.75816])
root_chord = 1.689
break_chord = 1.03628
tip_chord = .3902497

leList = np.array([[LE_pt[0] + 0.01*root_chord, LE_pt[1], LE_pt[2]],
                    [break_pt[0] + 0.01*break_chord, break_pt[1], break_pt[2]],
                    [tip_pt[0] + 0.01*tip_chord, tip_pt[1], tip_pt[2]]])

teList = np.array([[LE_pt[0] + 0.99*root_chord, LE_pt[1], LE_pt[2]],
                    [break_pt[0] + 0.99*break_chord, break_pt[1], break_pt[2]],
                    [tip_pt[0] + 0.99*tip_chord, tip_pt[1], tip_pt[2]]])
DVCon.addVolumeConstraint(leList, teList, nSpan=25, nChord=30, lower=0.85, upper=1.15, scaled=True)
DVCon.addThicknessConstraints2D(name='thickness', leList=leList, teList=teList, nSpan=25, nChord=30, lower=0.5, upper=3.0, scaled=True)


# set up aerodynamic performance surrogate 
bounds = np.loadtxt('/home/aobo/MACH-Aero/input/bounds.txt')
func_list=['fc_cl', 'fc_cd', 'fc_cmz']
dv_list=[
{'DVname':'alpha_fc','DVnumber':1},
{'DVname':'wing_twist','DVnumber':7},
{'DVname':'shape','DVnumber':nmode}
]
mach_initial=0.85
alt_initial=11740.
AP = AeroSurrogate(bounds, mach_initial, alt_initial, dv_list, func_list)

# assemble design variables and functions
Allfunclist=[]
Alldvlist=[]
for i in range(nFlowCases):
    funclist=['fc%d_cl'%i, 'fc%d_cd'%i, 'fc%d_cmz'%i]
    Allfunclist.append(funclist)
    
    dvlist=[
    {'DVname':'alpha_fc%d'%i,'DVnumber':1},
    {'DVname':'wing_twist','DVnumber':7},
    {'DVname':'shape','DVnumber':nmode}
    ]
    Alldvlist.append(dvlist)


dim = AP.ndim - 2

global currentx
global currentcd
bestx = np.zeros(dim+nFlowCases-1)
currentx = np.zeros(dim+nFlowCases-1)
bestcd = 100000.0
currentcd = 0.0

# we use LHS to generate multiple starting points. This is to see if the optimization could be stuck to local minima.
sampling = LHS(xlimits=bounds[2:,:], criterion = 'm')
nstart = 10
xt = sampling(nstart)

for i in range(bounds.shape[0]-2):
    xt[0,i] = 0.5 * (bounds[i+2, 0] + bounds[i+2, 1])
    xt[1,i] = 0.5 * (bounds[i+2, 0] + bounds[i+2, 1])

for istart in range(1):
    #startingpoint = samptxt[-1-istart,:dim].copy()
    startingpoint = xt[istart,:].copy()
    myalpha = startingpoint[0]
    
aeroProblems=[]
for i in range(nFlowCases):
    ap = AeroProblem(name='fc%d'%i, mach=mach_list[i],  altitude=11740.0, 
                    alpha=2.5, reynolds=Re_list[i],
                    areaRef=3.407014, chordRef=1.00,
                    xRef=1.20777, yRef=.007669, zRef=0, evalFuncs=['cd', 'cl', 'cmz'])
    # Add angle of attack variable
    ap.addDV('alpha', lower=1., upper=3., scale=1.0)
    aeroProblems.append(ap)

# ======================================================================
#         Functions:
# ======================================================================
def cruiseFuncs(x):
    if MPI.COMM_WORLD.rank == 0:
        print(x)
    # Set design vars
    DVGeo.setDesignVars(x)
    # Evaluate functions
    funcs = {}
    DVCon.evalFunctions(funcs)
        
    global currentx,currentcd
    currentcd = 0.0
    for i in range(nFlowCases):
        AP.Mach   = mach_list[i]
        AP.dvlist = Alldvlist[i]
        AP.funclist = Allfunclist[i]

        if i % nGroup == ptID: 
            AP.evalFunctions(x,funcs)
            temp_x = AP.recordx(x)
            currentcd += funcs['fc%d_cd'%i] * coefs_list[i]
            currentx[iflow] = temp_x[0]
            currentx[nFlowCases:] = temp_x[1:]
    
    if MPI.COMM_WORLD.rank == 0:
        print(currentcd,currentx)      
    return funcs

def cruiseFuncsSens(x, funcs):
    funcsSens = {}
    DVCon.evalFunctionsSens(funcsSens)
    for iflow in range(nFlowCases):
        AP.Mach   = mach_list[iflow]
        AP.dvlist = Alldvlist[iflow]
        AP.funclist = Allfunclist[iflow]

        if iflow%nGroup == ptID:
            AP.evalFunctionsSens(x,funcsSens)
    return funcsSens

def objCon(funcs, printOK):
    # Assemble the objective and any additional constraints:
    funcs['obj'] = 0.0
    for iflow in range(nFlowCases):
        funcs['obj'] += funcs['fc%d_cd'%iflow] * coefs_list[iflow]
        funcs['cl_con_'+ 'fc%d'%iflow] = funcs['fc%d_cl'%iflow] - cl_list[iflow]
        if iflow == 4:
            funcs['cmz_con_'+ 'fc%d'%iflow] = funcs['fc%d_cmz'%iflow] - cmcon
        # funcs['cmz_con_'+myname] = funcs[myname+'_cmz'] - cmcon
            
    if printOK:
        print('funcs in obj:', funcs)
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
# Add DVConstraints
DVCon.addConstraintsPyOpt(optProb)
# Add Objective
optProb.addObj('obj', scale=1e2)

# Aerodynamic constraints
for iflow in range(nFlowCases):
    optProb.addCon('cl_con_' + 'fc%d'%iflow, lower=0, upper=0, scale=1.0)
    if iflow == 4:
        optProb.addCon("cmz_con_" + 'fc%d'%iflow, lower=0.0, upper=10.0, scale=0.1)
        
# optProb.addCon('cmz_con', lower=0.0, upper=10.0, scale=1.0)
# optProb.addCon("cmz_con_fc4", lower=0.0, upper=10.0, scale=1.0)

# The MP object needs the 'obj' and 'sens' function for each proc set,
# the optimization problem and what the objcon function is:
MP.setProcSetObjFunc('cruise', cruiseFuncs)
MP.setProcSetSensFunc('cruise', cruiseFuncsSens)
MP.setObjCon(objCon)
MP.setOptProb(optProb)
optProb.printSparsity()

# Set up optimizer
if args.opt == "SLSQP":
    optOptions = {"IFILE": os.path.join(args.output, "SLSQP.out")}
elif args.opt == "SNOPT":
    optOptions = {
        "Major feasibility tolerance": 1e-4,
        "Major optimality tolerance": 1e-4,
        "Hessian full memory": None,
        "Function precision": 1e-8,
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
histFile = os.path.join('history/'+ args.opt +'_hist.hst')
sol = opt(optProb, MP.sens, storeHistory=os.path.join(args.output, "opt.hst"))#, hotStart=hotStart)
if comm.rank == 0:
    print(sol)

if currentcd < bestcd:
    bestcd = currentcd
    bestx  = currentx.copy()

f = open('optmum_HF.dat','w')
for i in range(dim + nFlowCases-1):
    f.write('%.15f\n'%(bestx[i]))
f.close()