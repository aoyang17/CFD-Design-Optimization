import os
import numpy as np
from SUR import AeroSurrogate

dvlist=[
{'DVname':'alpha_fc','DVnumber':1},
{'DVname':'wing_twist','DVnumber':7},
{'DVname':'shape','DVnumber':50}
]


funclist=['fc_cl', 'fc_cd', 'fc_cmz']

allbounds = np.loadtxt('./input/bounds.txt')

myaltitude =11740.0

Mlist=[0.82,0.82,0.82,0.85,0.85,0.85,0.88,0.88,0.88]

data = np.loadtxt('optmum.dat')
# CFD of samples
for ins in range(9):
    # write this sampling point out to a file
    mymach = Mlist[ins]
    f = open('new.asm','w')
    f.write('%.15f\n'%(mymach))
    f.write('%.15f\n'%(myaltitude))
    f.write('%.15f\n'%(data[ins]))    
    for idim in range(9,data.shape[0]):
        f.write('%.15f\n'%(data[idim]))        
    f.close()
    
    os.system('rm obj.txt')
    os.system('mpirun -n 8 python CFD.py')
    
    try:
        thisamp = np.loadtxt('obj.txt')
        thiscm = thisamp[-1]
    except:
        thiscm = 10000.0
        
    if thiscm > 50.0:
        # this means unconverged
        pass
    else:
        fsam = open('CFDfuncs.dat','a')
        fsam.write('%.15f %.15f %.15f\n'%(thisamp[-3],thisamp[-2],thisamp[-1]))
        fsam.close()
    
    os.system('mv fc_000_slices.dat slice{0}.dat'.format(ins))
    os.system('mv fc_000_surf.cgns surf{0}.cgns'.format(ins))




