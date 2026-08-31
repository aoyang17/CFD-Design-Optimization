'''
Author: Dr. Jichao Li <cfdljc@gmail.com>
---------------------------------------------------------
 
This script is to set up the geo and mesh for the CRM wing. 

---------------------------------------------------------
'''
# ======================================================================
#         Import modules
# ======================================================================
from __future__ import print_function
import os
import argparse
import numpy
from baseclasses import *
from pygeo import *
from repostate import *
from idwarp import USMesh
# Ignore deprecation warnings
import warnings
import numpy as np
from pyspline import *

warnings.filterwarnings('ignore')

gridFile = './input/L3_peter_rotat_mirror_bc.cgns'
FFDFile = './input/rot.xyz'
nSpanwise = 8

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

DVGeo = DVGeometry_FFD_MODE(FFDFile)

# Create the Ref line
coef = DVGeo.FFD.vols[0].coef.copy()
X = numpy.zeros((nSpanwise,3))
for ispan in range(nSpanwise):
    Lep = 0.5*(coef[0,ispan,0,:]+coef[0,ispan,1,:])
    Tep = 0.5*(coef[-1,ispan,0,:]+coef[-1,ispan,1,:]) 
    X[ispan,:] = Lep + 0.25*(Tep - Lep)

c1 = pySpline.Curve(X=X, k=2)
DVGeo.addRefAxis('wing', c1)


def twist(val, geo):
    # Set all the twist values
    for i in range(nSpanwise-1):
        geo.rot_z['wing'].coef[i+1] = val[i]

optbounds = np.loadtxt('./input/bounds.txt')
nmode = 50

modedata = np.loadtxt('./input/modes.dat')
modes = modedata[:nmode,:].copy()

DVGeo.addGeoDVLocal_Mode('shape', modes, lower=optbounds[10:,0], upper=optbounds[10:,1], scale=1.0)
DVGeo.addGeoDVGlobal('wing_twist', numpy.zeros(nSpanwise-1), twist, lower=optbounds[3:10,0], upper=optbounds[3:10,1])

'''
dvlist=[
{'DVname':'alpha_fc','DVnumber':1},
{'DVname':'wing_twist','DVnumber':7},
{'DVname':'shape','DVnumber':nmode}
]
'''
