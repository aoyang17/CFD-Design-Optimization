
from __future__ import division
import numpy as np
import math
from scipy.stats import norm
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Conv2D,LeakyReLU,Dropout,Flatten
from tensorflow.keras import activations
import tensorflow as tf
import os
from tensorflow.keras.models import load_model,save_model
try:
    from collections import OrderedDict
except ImportError:
    try:
        from ordereddict import OrderedDict
    except ImportError:
        print("Could not find any OrderedDict class. For 2.6 and earlier, "
              "use:\n pip install ordereddict")


class AeroSurrogate(object):

    def __init__(self,bounds,myMach,myAltitude,dvlist,funclist):
        '''
        bounds : bounds of each variables (both dv and flow parameters)
        nlevel : No. of levels in NN models
        nnodes : No. of nodes in each NN level
        
        dvlist : list of dict,  example=[
                                {'DVname':'alpha_fc','DVnumber':1},
                                {'DVname':'wing_twist','DVnumber':7},
                                {'DVname':'shape','DVnumber':192}
                                ]
        funclist: list,         example=
                                ['fc_cl', 'fc_cd', 'fc_cmy']
        ]
        '''
        self.bounds = bounds
        self.nlevel = 0#nlevel
        self.nnodes = 0#nnodes
        self.altitude = myAltitude
        self.Mach   = myMach
        ndv = 0 
        nfunc = len(funclist)
        for localdv in dvlist:
            ndv +=localdv['DVnumber']
        assert bounds.shape[0] == (ndv+2),'The number of items in bounds are not as expected'
        self.ndim = bounds.shape[0]
        self.nfunc = nfunc
        self.dvlist = dvlist
        self.funclist = funclist
        self.FDstep = 1.e-4
        self.readDataModel()
        print 'Data-based models read!'
    
    def readDataModel(self):
        '''
        Read the data-based models
        '''
        modelcl = Sequential()
        modelcd = Sequential()
        modelcm = Sequential()
        
        '''
        for ilevel in range(self.nlevel):
            modelcl.add(Dense(self.nnodes,activation=activations.tanh))
            modelcd.add(Dense(self.nnodes,activation=activations.tanh))
            modelcm.add(Dense(self.nnodes,activation=activations.tanh))

        modelcl.add(Dense(1))
        modelcd.add(Dense(1))
        modelcm.add(Dense(1))
        '''
        
        modelcl = load_model('./input/model_cl.h5')
        modelcd = load_model('./input/model_cd.h5')
        modelcm = load_model('./input/model_cm.h5')

        self.modelist= [modelcl,modelcd,modelcm]       

    def denormfunc(self,ifunc,newfunc):
        funcrangs = [[0.15,0.72],[0.013,0.053],[-0.3, -0.03]]
        minvar,maxvar = funcrangs[ifunc][0],funcrangs[ifunc][1]
        npts = newfunc.shape[0]
        oldvars = np.zeros(npts)
        for i in range(npts):
            myvar = newfunc[i]
            oldvars[i] = (myvar+1.0)*0.5*(maxvar-minvar)+minvar
        #print '$$$$$$$$$$$$$$$$$',ifunc,newfunc,oldvars
        return oldvars

    def getfuncvalue(self,ifunc,thisvar):
        '''
        thisvar is a 2-D vector and has been normalized for predict
        '''
        npts = thisvar.shape[0]
        modelout = self.modelist[ifunc].predict(thisvar)

        newvalues = np.zeros(npts)
        for i in range(npts):
            newvalues[i] = modelout[i,0]
        orivalues = self.denormfunc(ifunc,newvalues)
        return orivalues
        
    def evalFunctions(self,xvar,funcs):
        thisvar = self.setupvar(xvar)
        # Evalute the functions and assemble them into the Funcs dict
        # Loop over all funcs
        for ifunc in range(self.nfunc):
            funcname = self.funclist[ifunc]
            funcs[funcname] = self.getfuncvalue(ifunc,thisvar)[0]
        return    
    
    def evalFunctionsSens(self,xvar,funcsSens):
        FDvars = self.setFDvar(xvar)
        # Evalute the funcSens and assemble them into the funcsSens dict
        # Loop over all funcs
        for ifunc in range(self.nfunc):
            #thissurrogate = self.modelist[ifunc]
            funcname = self.funclist[ifunc]
            funcsSens[funcname] = OrderedDict()
            funcvars = self.getfuncvalue(ifunc,FDvars)
            indextemp = 0
            # Loop over all Dvs
            for localdv in self.dvlist:
                dvname = localdv['DVname']
                dvnumber = localdv['DVnumber']
                localgrad = np.zeros(dvnumber)
                for i in range(dvnumber):
                    localgrad[i] = (funcvars[indextemp+1] - funcvars[0])/self.FDstep
                    indextemp += 1
                funcsSens[funcname][dvname] = localgrad
        return

    def normlizevar(self,thisvars):
        npts = thisvars.shape[0]
        newx = np.zeros((npts,self.ndim))
        for ipt in range(npts):
            for i in range(self.ndim):
                newx[ipt,i] = 2.0*((thisvars[ipt,i] - self.bounds[i,0])/(self.bounds[i,1]-self.bounds[i,0]) - 0.5)
        return newx
        

    def setupvar(self,xvar):
        # set up the template of the input for surrogates
        thisvar = np.zeros((1,self.ndim))
        thisvar[0,0] = self.Mach
        thisvar[0,1] = self.altitude
        indextemp = 2
        for localdv in self.dvlist:
            dvname = localdv['DVname']
            dvnumber = localdv['DVnumber']
            thisvar[0,indextemp:indextemp+dvnumber] = xvar[dvname]
            indextemp += dvnumber
        normvar = self.normlizevar(thisvar)
        return normvar

    def setFDvar(self,xvar):
        # set up the template of the input for surrogates
        thisvar = np.zeros((self.ndim-1,self.ndim))

        thisvar[0,0] = self.Mach
        thisvar[0,1] = self.altitude
        indextemp = 2
        for localdv in self.dvlist:
            dvname = localdv['DVname']
            dvnumber = localdv['DVnumber']
            thisvar[0,indextemp:indextemp+dvnumber] = xvar[dvname]
            indextemp += dvnumber
        
        for idim in range(self.ndim-2):
            thisvar[idim+1,:] = thisvar[0,:]
            thisvar[idim+1,idim+2] = thisvar[0,idim+2] + self.FDstep
        
        normvar = self.normlizevar(thisvar)

        return normvar


    def recordx(self,xvar):
        # set up the template of the input for recording
        thisvar = np.zeros(self.ndim-2)
        indextemp = 0
        for localdv in self.dvlist:
            dvname = localdv['DVname']
            dvnumber = localdv['DVnumber']
            thisvar[indextemp:indextemp+dvnumber] = xvar[dvname]
            indextemp += dvnumber
        return thisvar
    
    
    
