import numpy as np
from pygeo import *
from pyspline import *
import warnings
warnings.filterwarnings("ignore")

nCP = 30
nPos = nCP-2

DVGeo = DVGeometry(FFDFile)

coef = DVGeo.FFD.vols[0].coef.copy()
coef_top, coef_bottom = map(np.array, zip(*coef))
coef_new = np.concatenate((coef_top,np.flipud(coef_bottom)), axis=0)
coef = coef_new
# print(coef)


nSpan = coef.shape[0]
ref = np.zeros((nSpan*2,3))

for k in xrange(nSpan):
    ref[k,0] = np.average(coef[k,:,0])
    ref[k,1] = np.average(coef[k,:,1])
    ref[k,2] = 0.0

    ref[k + nSpan,0] = np.average(coef[k,:,0])
    ref[k + nSpan,1] = np.average(coef[k,:,1])
    ref[k + nSpan,2] = 1.0

X = ref
c0 = pySpline.Curve(X=X, k=2)
DVGeo.addRefAxis('axis', c0)

def set_y(val, geo):
    C = geo.extractCoef('axis')   

    C[0,1] += -1.0*val[0]
    for i in xrange(1,nCP/2-1):
      C[i,1] += val[i]
      C[i + nCP, 1] += val[i]
    
    C[nCP/2-1, 1] += -1*val[nCP/2 - 1]
    C[nCP/2, 1] += 1*val[nCP/2- 1]
    
    for i in range(nCP/2 + 1, nCP - 1):
      C[i,1] += val[i-1]
      C[i + nCP, 1] += val[i-1]
    C[nCP-1,1] +=  val[0]
    
    for i in range(1,nCP+1):
			C[i-1+nCP,1] = C[i-1,1]

    geo.restoreCoef(C, 'axis')

variables=np.loadtxt('lastp.dat')

DVGeo.addGeoDVGlobal('set_y', variables, set_y, lower=-0.6, upper=0.6, scale=1e0)




