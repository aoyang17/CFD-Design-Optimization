'''
Author: Dr. Jichao Li <cfdljc@gmail.com>
---------------------------------------------------------
 
This script is to run CFD simulations for the CRM wing. 

---------------------------------------------------------
There are four scripts to perform EGO:
1. EGO.py -- the main script 
2. SUR.py -- the script to construct surrogates
3. CFD.py -- the script to run CFD
4. GEO.py -- the script for Geo and Mesh that can be directly loaded by EGO and CFD.
---------------------------------------------------------
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
from pyspline import *
from multipoint import *
from repostate import *
# Ignore deprecation warnings
import warnings
warnings.filterwarnings('ignore')


# ======================================================================
#         Create multipoint communication object
# ======================================================================
nGroup = 1
nProcPerGroup = 8
outputDirectory = './'

MP = multiPointSparse(MPI.COMM_WORLD)
MP.addProcessorSet('cruise', nMembers=nGroup, memberSizes=nProcPerGroup)
comm, setComm, setFlags, groupFlags, ptID = MP.createCommunicators()

# ======================================================================
#         Input Information
# ======================================================================

execfile('./GEO.py')

AEROSOLVER = ADFLOW
aeroOptions = {
    # Common Parameters
    'gridFile':gridFile,
    'outputDirectory':outputDirectory,
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
    'MGCycle':'2w',
    'MGStartLevel':-1,
    'nCyclesCoarse':20,
    'nCycles':6000,
    'nsubiterturb':7,
    'useNKSolver':True,
    'useANKSolver':True,
    'nkswitchtol':2e-5,
    'rkreset': False,
    'nrkreset': 90,
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

# New sample
samples=numpy.loadtxt('new.asm')
ncoef = samples.shape[0]
myMa    = samples[0]
myAltitude = samples[1]
myalpha = samples[2]
mytwist = samples[3:10].copy()
myshape = samples[10:].copy()

DVList={'shape':myshape,'wing_twist':mytwist}
DVGeo.setDesignVars(DVList)

# Create solver
CFDSolver = AEROSOLVER(options=aeroOptions, comm=comm)
CFDSolver.setMesh(mesh)
CFDSolver.setDVGeo(DVGeo)

span = 3.758150834
pos = numpy.array([0.0235, 0.267, 0.557, 0.695, 0.828, 0.944])*span
CFDSolver.addSlices('z', pos, sliceType='absolute')
CFDSolver.addLiftDistribution(100, 'z')


# ======================================================================
#         Run this CRM case
# ======================================================================

name='fc'
ap = AeroProblem(name=name, mach=myMa,  altitude=myAltitude, 
                 alpha=myalpha,
                 areaRef=3.407014, chordRef=1.00,
                 xRef=1.20777, yRef=.007669, zRef=0, evalFuncs=['cd', 'cl', 'cmz'])

funcs = {}
CFDSolver(ap)
CFDSolver.evalFunctions(ap, funcs)
CFDSolver.checkSolutionFailure(ap, funcs)
if not funcs['fail'] and MPI.COMM_WORLD.rank == 0:
    fobj=open('obj.txt','w')
    # write the sample itself out first
    for i in xrange(ncoef):
        fobj.write('%.15f\n'%(samples[i]))
    fobj.write('%.15f\n%.15f\n%.15f\n'%(funcs[name+'_cl'],funcs[name+'_cd'],-1.0*funcs[name+'_cmz']))
    fobj.close()
elif MPI.COMM_WORLD.rank == 0:
    fobj=open('obj.txt','w')
    for i in xrange(ncoef):
        fobj.write('%.15f\n'%(samples[i]))
    fobj.write('%.15f\n%.15f\n%.15f\n'%(1000.0,1000.0,1000.0))
    fobj.close()
    
