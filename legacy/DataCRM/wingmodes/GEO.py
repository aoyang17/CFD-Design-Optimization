'''
Author: Dr. Jichao Li <cfdljc@gmail.com>
---------------------------------------------------------
 
This script is to set up the modal parameterization for the CRM wing. 

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

gridFile = 'input/L3_peter_rotat_mirror_bc.cgns'
FFDFile = 'input/rot.xyz'
nSpanwise = 8

DVGeo = DVGeometry(FFDFile)

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

DVGeo.addGeoDVLocal('shape', lower=-2.0, upper=2.0, scale=1.0)
DVGeo.addGeoDVGlobal('wing_twist', numpy.zeros(nSpanwise-1), twist, lower=-1., upper=1.)

nmode = 50
modedata = np.loadtxt('input/modes.dat')
modes = modedata[:nmode,:].copy()

# for example, if your wing mode coefficients are testcoef, you can specify the FFD local design varaibles in this way:

testcoef = np.zeros(nmode)
DVList={'shape':np.dot(testcoef,modes),'wing_twist':np.zeros(7)}
DVGeo.setDesignVars(DVList)    






