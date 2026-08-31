'''
This ADflow script runs the flow and adjoint for the ADODG5 case: the CRM wing-body-tail configuration

Objective function: CD
Design variables: Twists at nine spanwise locations and angle of attack
Mach number: 0.85
Reynolds number: 4.3e7
Lift coefficient: 0.5
Reference chord length: 7.00532 m
Reference area: 191.8448 m^2
Angle of attack: 2.04544325238 degree
Mesh cells: 10,358,373
Reference:
Gaetan Kenway, Charles Mader, Ping He, and Joaquim Martins. 
Effective adjoint approaches in Computational Fluid Dynamics,
Progress in Aerospace Sciences, 2019

Before running this script, make sure you have installed the required codes listed in Code_Version.txt.
Download the mesh ADODG5_Overset_Structured_Mesh.cgns and the FFD file ADODG5_FFD.xyz along with this script

Run this command for the flow and adjoint: "mpirun -np 96 python ADODG5_Run_Script.py adjoint".
This will compute CD and its derivatives wrt to the nine twist variables and angle of attack.

Run this command to verify the adjoint derivatives: "mpirun -np 96 python ADODG5_Run_Script.py complex twist 0".
This will compute the derivatives of dCD/dEta0 using the complex step method.
Here Eta0 is the twist variable at the first spanwise location (wing root).
To compute derivatives for all the twist locations, you need to call the above command nine times,
varying the last parameter from 0 to 8.
To verify the derivatives wrt the angle of attack, run this command: "mpirun -np 96 python ADODG5_Run_Script.py complex alpha".
NOTE: To verify derivatives, make sure your flow and adjoint converge tightly, set L2TolFlow and L2TolAdj to 1e-14.
'''

import sys
import numpy
from mpi4py import MPI
from baseclasses import *
from pygeo import *
from pyspline import *

# determine if it is a complex step run
try:
    task=sys.argv[1]
except:
    print("Specify a task to run. Options are: adjoint or complex")
    exit()

if task=='complex':
    from adflow import ADFLOW_C
    from idwarp import USMesh_C
    ADFLOW = ADFLOW_C
    USMesh = USMesh_C
    CS=True
    try:
        perturbVar = sys.argv[2]
    except:
        print("The second argument not found! Options are: twist or alpha.")
        exit()
    if not perturbVar in ['twist','alpha']:
        print("The second argument not valid! Options are: twist or alpha.")
        exit()
elif task=='adjoint':
    from adflow import ADFLOW
    from idwarp import USMesh
    CS=False
else:
    print("The first argument not valid! The options are: adjoint or complex")

if CS==True:
    useNK=False
    useANK=False
    L2TolFlow=1e-14
    L2TolAdj=1e-14
else:
    useNK=True
    useANK=True
    L2TolFlow=1e-10
    L2TolAdj=1e-8

# ======================================================================
#         Input Information
# ======================================================================

if task=='complex' and perturbVar=='twist':
    try:
        perturbIdx = sys.argv[3]
    except:
        print("The third argument not found! Options are integers fromm 0 to 8.")
        exit()
    if not int(perturbIdx) in range(9):
        print("The third argument not valid! Options are integers fromm 0 to 8")
        exit()

# we have nine twists, initialize them
nTwist = 9
twistList = [0,0,0,0,0,0,0,0,0]

# if complex step and we want to perturb alpha, add 1e-40 to the img part
if task=='complex' and perturbVar=='alpha':
    AoA0=2.04544325238+1e-40j
else:
    AoA0=2.04544325238

# initialize the flow problem
ap = AeroProblem(name='ADODG5', mach=0.85,
                 alpha=AoA0,altitude=37000*.3048,
                 areaRef=594720.0*.0254**2/2.0, chordRef=275.8*.0254,
                 zRef=177.95*.0254,
                 xRef=1325.90*.0254, evalFuncs=['cd'])

# add alpha as the design variables
ap.addDV('alpha')

# ADflow options    
aeroOptions = {
    'isosurface':{'shock':1.0, 'vx':-0.001},
    'outputDirectory':'./',
    'gridFile':'./ADODG5_Overset_Structured_Mesh.cgns',
    'discretization':'central plus scalar dissipation',
    'equationType':'RANS',
    'loadbalanceiter':40,
    'liftIndex':3,
    'smoother':'dadi',
    'nsubiterturb':4,
    'nsubiter':2,
    'mgcycle': 'sg',
    'mgstartlevel':-1,
    'useqcr':True,
    'CFL':2.0,
    'vis4':0.018,
    'vis2':0.25,
    'resaveraging':'noresaveraging',
    'setMonitor':True,
    'ADPC':True,
    'viscpc':False,
    'ILUFill':2,
    'ASMOverlap':2,
    'nCycles':100000,
    'outerpreconits':3,
    'adjointmaxiter':1500,
    'turbresscale':20000.0,
    'nkasmoverlap':2,
    'L2Convergence':L2TolFlow,
    'adjointsubspacesize':200,
    'adjointl2convergence':L2TolAdj,
    'matrixordering':'rcm',
    'preconditionerside':'right',
    'applyadjointpcsubspacesize':20,
    'usenksolver':useNK,
    'nkouterpreconits':3,
    'nksubspacesize':200,
    'rkreset':True,
    'nrkreset':100,
    'nkjacobianlag':4,
    'nkswitchtol':1e-5,
    'nkadpc':True,
    'nkls':'cubic',
    'usematrixfreedrdw':True,
    'sepSensorOffset':-0.10,
    'useANKSolver':useANK,
    'ankswitchtol':1E-2}

# IDWarp options
meshOptions = {'gridFile':'./ADODG5_Overset_Structured_Mesh.cgns'}

# Create twist design variables
DVGeo = DVGeometry('ADODG5_FFD.xyz',complex=CS)

# We will use the FFD coordinates to create the reference axis
# automatically, this will ensure everything lines up exactly as we
# want.

# First extract the coefficients of the FFD that corresponds to the
# wing. This happens to be vol zero: the 'i' direction is 'x'
# (streamwise), the 'j' direction is out the wing and the 'k'
# direction is 'up'
coef = DVGeo.FFD.vols[0].coef.copy()

# First determine the reference chord lengths:
nTwist = coef.shape[1]
sweep_ref = numpy.zeros((nTwist+1, 3))
for j in xrange(nTwist):
    max_x = numpy.max(coef[:, j, :, 0])
    min_x = numpy.min(coef[:, j, :, 0])
    sweep_ref[j+1, 0] = min_x + 0.25*(max_x-min_x)
    sweep_ref[j+1, 1] = numpy.average(coef[:, j, :, 1])
    sweep_ref[j+1, 2] = numpy.average(coef[:, j, :, 2])

# Now add on the first point which is just the second one, projected
# onto the sym plane
sweep_ref[0, :] = sweep_ref[1, :].copy()
sweep_ref[0, 1] = 0.0

# Create the actual reference axis
c1 = Curve(X=sweep_ref, k=2)
DVGeo.addRefAxis('wing', c1, volumes=[0, 5])

# Now the tail reference axis
x = numpy.array([2365.0, 2365.0])*.0254
y = numpy.array([0, 840/2.0])*.0254
z = numpy.array([255.0, 255.0])*.0254
c2 = Curve(x=x, y=y, z=z, k=2)
DVGeo.addRefAxis('tail', c2, volumes=[25])

def twist(val, geo):
    # Set all the twist values
    for i in xrange(nTwist):
        geo.rot_y['wing'].coef[i+1] = val[i]

    # Also set the twist of the root to the SOB twist
    geo.rot_y['wing'].coef[0] = val[0]

# We always have shape and twist
DVGeo.addGeoDVGlobal('twist', numpy.zeros(nTwist), twist,
                     lower=-10, upper=10, scale=1.0)


# if we run complex step for twist DVs, add 1e-40 perturbation here
if task=='complex' and perturbVar=='twist':
    twistList[int(perturbIdx)] = 0+1e-40j
    DVGeo.setDesignVars({'twist':twistList})

# Create solver
comm = MPI.COMM_WORLD
CFDSolver = ADFLOW(options=aeroOptions, comm=comm)
CFDSolver.setDVGeo(DVGeo)
mesh = USMesh(options=meshOptions, comm=comm)
CFDSolver.setMesh(mesh)

# output slices
CFDSolver.addFamilyGroup('wing', ['wingu', 'wingl', 'wingte'])
CFDSolver.addFamilyGroup('output', ['wing', 'fuse', 'tail', 'sym'])
CFDSolver.addFamilyGroup('wingfuse', ['wing', 'fuse'])
CFDSolver.addFamilyGroup('fusetail', ['fuse', 'tail'])

# wing is from 3.016 to 29.468
CFDSolver.addSlices('y',[3.637622,17.749764,27.986688], groupName='wing')

# call the flow
funcs={}
CFDSolver(ap)
CFDSolver.evalFunctions(ap,funcs)
if comm.rank==0:
    print ("\nComputed objective function value:")
    print (funcs)

# call the adjoint    
if not CS:
    funcsSens = {}
    CFDSolver.evalFunctionsSens(ap, funcsSens, ['cd'])

    if comm.rank==0:
        print ("\nComputed objective function derivatives:")
        numpy.set_printoptions(precision=16)
        print (funcsSens)

    CFDSolver.writeSurfaceSensitivity('sensitivity.dat', 'cd')


