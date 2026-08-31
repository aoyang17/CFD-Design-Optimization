
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
        
def data_filter(L2_input):
    L2_input[:, -1] = L2_input[:, -1] * (-1)

    L2_input = np.unique(L2_input,axis=0)
    np.random.shuffle(L2_input)
    has_nan = np.isnan(L2_input).any(axis=1)
    L2_input = L2_input[~has_nan]
    return L2_input

def min_max_print(data):
    # min_mach = np.min(data[:,0])
    # max_mach = np.max(data[:,0])
    # alt_min = np.min(data[:,1])
    # alt_max = np.max(data[:,1])
    # aoa_min = np.min(data[:,2])
    # aoa_max = np.max(data[:,2])
    cl_min = np.min(data[:,-3])
    cl_max = np.max(data[:,-3])
    cd_min = np.min(data[:,-2])
    cd_max = np.max(data[:,-2])
    cm_min = np.min(data[:,-1])
    cm_max = np.max(data[:,-1])
    bounds = np.array([[cl_min, cl_max],[cd_min, cd_max],[cm_min, cm_max]])  
    print(cl_min,cl_max,
          cd_min,cd_max,
          cm_min,cm_max)
    return bounds

L2_input = np.loadtxt("/home/aobo/MACH-Aero/NN_training/MF_training/L2_geo.txt")
L2_input = data_filter(L2_input)
L2_CFD_bounds = min_max_print(L2_input)


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
        print('Data-based models read!')
    
    def readDataModel(self):
        '''
        Read the data-based models
        '''
        # modelcl = Sequential()
        # modelcd = Sequential()
        # modelcm = Sequential()
        
        '''
        for ilevel in range(self.nlevel):
            modelcl.add(Dense(self.nnodes,activation=activations.tanh))
            modelcd.add(Dense(self.nnodes,activation=activations.tanh))
            modelcm.add(Dense(self.nnodes,activation=activations.tanh))

        modelcl.add(Dense(1))
        modelcd.add(Dense(1))
        modelcm.add(Dense(1))
        '''
        
        path_LF_cl =  '/home/aobo/MACH-Aero/input/model_cl.h5'
        path_LF_cd =  '/home/aobo/MACH-Aero/input/model_cd.h5'
        path_LF_cm =  '/home/aobo/MACH-Aero/input/model_cm.h5'
        

        path_LF2HF_cl = '/home/aobo/MACH-Aero/NN_training/MF_training/MF_models/Model_CL_LF2HF_NN.h5'
        path_LF2HF_cd = '/home/aobo/MACH-Aero/NN_training/MF_training/MF_models/Model_CD_LF2HF_NN.h5'
        path_LF2HF_cm = '/home/aobo/MACH-Aero/NN_training/MF_training/MF_models/Model_CM_LF2HF_NN.h5'
              
        model_cl_LF = load_model(path_LF_cl)
        model_cd_LF = load_model(path_LF_cd)
        model_cm_LF = load_model(path_LF_cm)

        model_cl_LF2HF = load_model(path_LF2HF_cl)
        model_cd_LF2HF = load_model(path_LF2HF_cd)
        model_cm_LF2HF = load_model(path_LF2HF_cm)



        self.mode_list_LF = [model_cl_LF, model_cd_LF, model_cm_LF]
        self.model_list_LF2HF = [model_cl_LF2HF, model_cd_LF2HF, model_cm_LF2HF]     

    def denormfunc(self,ifunc,newfunc,bounds_range):

        if bounds_range == "L3":
            funcrangs = [[0.15,0.72],[0.013,0.053],[-0.3, -0.03]]
        elif bounds_range == "L2":
            funcrangs = L2_CFD_bounds
        minvar,maxvar = funcrangs[ifunc][0],funcrangs[ifunc][1]
        npts = newfunc.shape[0]
        # print("****************")
        # print(npts)
        oldvars = np.zeros(npts)
        for i in range(npts):
            myvar = newfunc[i]
            oldvars[i] = (myvar+1.0)*0.5*(maxvar-minvar)+minvar
        #print '$$$$$$$$$$$$$$$$$',ifunc,newfunc,oldvars
        return oldvars

    def getfuncvalue(self,ifunc,thisvar):
        '''
        thisvar is a 2-D vector and has been normalized for predict
        "mach, altitude, alpha, 7 twists, 50 modes"
        
        '''

        npts = thisvar.shape[0]
        modelout_LF = self.mode_list_LF[ifunc].predict(thisvar)
        newvalues_LF = np.zeros(npts)
        for i in range(npts):
            newvalues_LF[i] = modelout_LF[i,0]
        orivalues_LF = self.denormfunc(ifunc, newvalues_LF, "L3")
        
        L2_funcrangs= L2_CFD_bounds
        
        # npts = orivalues_LF.shape[0]
        # newx = np.zeros((npts,self.ndim))
        # for ipt in range(npts):
        #     for i in range(self.ndim):
        L3_funcrangs = np.array([[0.15,0.72],[0.013,0.053],[-0.3, -0.03]])
        L3_norm_modelout_LF = 2.0*((orivalues_LF - L3_funcrangs[ifunc,0])/(L3_funcrangs[ifunc,1]-L3_funcrangs[ifunc,0]) - 0.5)
        L3_norm_modelout_LF = L3_norm_modelout_LF.reshape(-1,1)
        # L2_norm_modelout_LF = newx    
        
        thisvar_modelout = np.concatenate((thisvar[:,2:60], L3_norm_modelout_LF), axis=1)
        
        modelout = self.model_list_LF2HF[ifunc].predict(thisvar_modelout)

        newvalues = np.zeros(npts)
        for i in range(npts):
            newvalues[i] = modelout[i,0]
        orivalues = self.denormfunc(ifunc, newvalues, "L2")
        return orivalues
    
        # npts = thisvar.shape[0]
        # modelout = self.mode_list_LF[ifunc].predict(thisvar)

        # newvalues = np.zeros(npts)
        # for i in range(npts):
        #     newvalues[i] = modelout[i,0]
        # orivalues = self.denormfunc(ifunc,newvalues,"L3")
        # return orivalues
    
    
        
    def evalFunctions(self,xvar,funcs):

        thisvar = self.setupvar(xvar)
        # Evalute the functions and assemble them into the Funcs dict
        # Loop over all funcs
        for ifunc in range(self.nfunc):
            funcname = self.funclist[ifunc]
            funcs[funcname] = self.getfuncvalue(ifunc,thisvar)[0]
        print("****************")
        print(funcs)
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
    
    
    
