'''
---------------------------------------------------------
This script is to used to generate warped mesh after mode parameterization 
---------------------------------------------------------
'''

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
from pyoptsparse import Optimization, OPT, History
from pyspline import *
from pathlib import Path
import sys

_ROOT = Path(__file__).resolve().parents[1] / "Mode_based_ASO"
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from DVGeometry_MODE_update import DVGeometry_MODE

# Use Python's built-in Argument parser to get commandline options
parser = argparse.ArgumentParser()
parser.add_argument("--output", type=str, default="output_single")
parser.add_argument("--opt", type=str, default="SLSQP", choices=["IPOPT", "SLSQP", "SNOPT"])
parser.add_argument("--gridFile", type=str, default="/home/aobo/MACH-Aero/input/L3_peter_rotat_mirror_bc.cgns")
parser.add_argument("--FFDFile", type=str, default="/home/aobo/MACH-Aero/input/rot.xyz")
parser.add_argument("--optOptions", type=ast.literal_eval, default={}, help="additional optimizer options to be added")
args = parser.parse_args()

MP = multiPointSparse(MPI.COMM_WORLD)
MP.addProcessorSet("cruise", nMembers=1, memberSizes=MPI.COMM_WORLD.size)
comm, setComm, setFlags, groupFlags, ptID = MP.createCommunicators()

if not os.path.exists(args.output):
    if comm.rank == 0:
        os.mkdir(args.output)

#load data


alpha = 0.0
twists = np.zeros(7)
mode_coeff = np.zeros(50)
modedata = np.loadtxt('/home/aobo/MACH-Aero/input/modes.dat')
modes = modedata[:50,:].copy()


# data = np.loadtxt("/home/aobo/MACH-Aero/Operate_mission_ASO/Data_driven_ASO/optmum_k_means_opt.dat")

# mode_coeff = data[37:87]
# print(mode_coeff.shape)

# # mode_coeff = np.random.rand(50,)
# # print(mode_coeff.shape)
# twists = data[30:37]
# print(twists)
# # mode_coeff[k] = 1.0
# # print(mode_coeff)

hist = History("/home/aobo/MACH-Aero/Operate_mission_ASO/Mode_based_ASO/opeartion_mode_based/opt.hst", flag="r")
DVnames = hist.getDVNames()
print(DVnames)

dict = {}
for name in DVnames:
    A = hist.getValues(names=name, major=True)
    dict[name] = A[name][-1]
    
    
mode_coeff = dict['shapey']
twists = dict['twist']



meshOptions = {
    "gridFile":args.gridFile,
    "fileType":'CGNS',
    "symmetryPlanes":None,
    'aExp': 3.0,
    'bExp': 5.0,
    'LdefFact':100.0,     # affects how far the deformations are pushed away from the surface
    'alpha':0.1,
    'errTol':1e-5
    }
mesh = USMesh(options=meshOptions)

coords0 = mesh.getSurfaceCoordinates()

DVGeo = DVGeometry(args.FFDFile)
DVGeo.addRefAxis("wing", xFraction=0.25, alignIndex="j")

nSpanwise = 8

def twist(val, geo):
    # Set all the twist values
    for i in range(nSpanwise-1):
        geo.rot_z['wing'].coef[i+1] = val[i]

DVGeo.addLocalDV('shape', lower=-2.0, upper=2.0, scale=1.0)
DVGeo.addGlobalDV('wing_twist', np.zeros(nSpanwise-1), twist, lower=-1., upper=1.)


DVList={'shape':np.dot(mode_coeff, modes),
        'wing_twist':twists}  

DVGeo.addPointSet(coords0, "coords")
DVGeo.setDesignVars(DVList)
newcoords = DVGeo.update("coords")
DVGeo.writePlot3d("ffd_deformed_operation_mode_based.xyz")
DVGeo.writePointSet("coords", "surf")
mesh.setSurfaceCoordinates(newcoords)
mesh.warpMesh()
mesh.writeGrid('L3_mirror_warped_CGNS_operation_mode_based.cgns')
