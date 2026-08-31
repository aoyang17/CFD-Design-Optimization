'''
- Train a NN as a prediction model
'''
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Conv2D,LeakyReLU,Dropout,Flatten
from tensorflow.keras import activations
import tensorflow as tf
import os
from tensorflow.keras.models import load_model,save_model
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

para = np.loadtxt('nodes.txt')
nlevel = int(para[0])
nnode = int(para[1])

traindata = np.loadtxt('../../input/training.dat')
testdata = np.loadtxt('../../input/validating.dat')
bounds  = np.loadtxt('../../input/bounds.txt')

mincl = 0.15
maxcl = 0.72
mincd = 0.013
maxcd = 0.053
mincm = -0.3
maxcm = -0.03


ntest = testdata.shape[0]

ndim = bounds.shape[0]

def normalizeX(oldx):
    newx = oldx.copy()
    for i in range(ndim):
        newx[i] = 2.0*((oldx[i] - bounds[i,0])/(bounds[i,1]-bounds[i,0]) - 0.5)
    return newx

def normalizeCl(oldcl):
    return 2.0*((oldcl - mincl)/(maxcl-mincl) - 0.5)
    
def normalizeCd(oldcd):
    return 2.0*((oldcd - mincd)/(maxcd-mincd) - 0.5)

def normalizeCm(oldcm):
    return 2.0*((oldcm - mincm)/(maxcm-mincm) - 0.5)


def denormCl(newcl):
    oldcl = (newcl+1.0)*0.5*(maxcl-mincl)+mincl
    return oldcl

def denormCd(newcd):
    oldcd = (newcd+1.0)*0.5*(maxcd-mincd)+mincd
    return oldcd

def denormCm(newcm):
    oldcm = (newcm+1.0)*0.5*(maxcm-mincm)+mincm
    return oldcm


'''
print np.min(traindata[:,-3]),np.max(traindata[:,-3])
print np.min(testdata[:,-3]),np.max(testdata[:,-3])
stop
'''

Alldata = []
labelcl = []
labelcd = []
labelcm = []
for i in range(traindata.shape[0]):
    tempdata = normalizeX(traindata[i,:ndim])
    Alldata.append(tempdata)        
    labelcl.append(normalizeCl(traindata[i,ndim]))
    labelcd.append(normalizeCd(traindata[i,ndim+1]))
    labelcm.append(normalizeCm(traindata[i,ndim+2]))


testAlldata = []
testlabelcl = []
testlabelcd = []
testlabelcm = []
for i in range(testdata.shape[0]):
    tempdata = normalizeX(testdata[i,:ndim])
    testAlldata.append(tempdata)        
    testlabelcl.append(normalizeCl(testdata[i,ndim]))
    testlabelcd.append(normalizeCd(testdata[i,ndim+1]))
    testlabelcm.append(normalizeCm(testdata[i,ndim+2]))


modelcl = load_model('model_cl.h5')
modelcd = load_model('model_cd.h5')
modelcm = load_model('model_cm.h5')

'''
modelcl = Sequential()
modelcd = Sequential()
modelcm = Sequential()

for ilevel in range(nlevel):
    modelcl.add(Dense(nnode,activation=activations.tanh))
    modelcd.add(Dense(nnode,activation=activations.tanh))
    modelcm.add(Dense(nnode,activation=activations.tanh))

modelcl.add(Dense(1))
modelcd.add(Dense(1))
modelcm.add(Dense(1))
'''

# Compile the model.
modelcl.compile(
  optimizer='adam',
  loss='mae',
  metrics=['accuracy'],
)

# Compile the model.
modelcd.compile(
  optimizer='adam',
  loss='mae',
  metrics=['accuracy'],
)

# Compile the model.
modelcm.compile(
  optimizer='adam',
  loss='mae',
  metrics=['accuracy'],
)

#X_train,X_test,y_train,y_test=train_test_split(np.array(Alldata),np.array(labels),test_size=0.0,random_state=1)
X_train = np.array(Alldata)
X_cl    = np.array(labelcl)
X_cd    = np.array(labelcd)
X_cm    = np.array(labelcm)

X_test = np.array(testAlldata)
X_testcl    = np.array(testlabelcl)
X_testcd    = np.array(testlabelcd)
X_testcm    = np.array(testlabelcm)

nepoch = 10000

# Train the model.
historycl = modelcl.fit(
  X_train,
  X_cl,
  validation_data=(X_test, X_testcl),
  epochs=nepoch,
  batch_size=300,
)

# Train the model.
historycd = modelcd.fit(
  X_train,
  X_cd,
  validation_data=(X_test, X_testcd),
  epochs=nepoch,
  batch_size=300,
)

# Train the model.
historycm = modelcm.fit(
  X_train,
  X_cm,
  validation_data=(X_test, X_testcm),
  epochs=nepoch,
  batch_size=300,
)
#model = load_model('model.h5')



predictcl = modelcl.predict(np.array(testAlldata))
predictcd = modelcd.predict(np.array(testAlldata))
predictcm = modelcm.predict(np.array(testAlldata))

f = open('error_NN.txt','w')
for i in range(ntest):
    mycl = denormCl(testlabelcl[i])
    mycd = denormCd(testlabelcd[i])
    mycm = denormCm(testlabelcm[i])

    estcl = denormCl(predictcl[i,0])
    estcd = denormCd(predictcd[i,0])
    estcm = denormCm(predictcm[i,0])

    #print estcl,mycl
    #print estcd,mycl
    errcl = abs(mycl-estcl)
    errcd = abs(mycd-estcd)
    errcm = abs(mycm-estcm)
    
    f.write('%.15f %.15f %.15f %.15f %.15f %.15f\n'%(errcl,errcd,errcm,mycl,mycd,mycm))
f.close()    
    
errordata = np.loadtxt('error_NN.txt')

pertcl = np.linalg.norm(errordata[:,0])/np.linalg.norm(errordata[:,3])*100.0
pertcd = np.linalg.norm(errordata[:,1])/np.linalg.norm(errordata[:,4])*100.0
pertcm = np.linalg.norm(errordata[:,2])/np.linalg.norm(errordata[:,5])*100.0


f = open('percetage.txt','a')
f.write('%.5f\n%.5f\n%.5f\n'%(pertcl,pertcd,pertcm))
f.close()


modelcl.save('model_cl.h5')
modelcd.save('model_cd.h5')
modelcm.save('model_cm.h5')

hislosscl = historycl.history['loss']
hislossvalcl = historycl.history['val_loss']
hislosscd = historycd.history['loss']
hislossvalcd = historycd.history['val_loss']
hislosscm = historycm.history['loss']
hislossvalcm = historycm.history['val_loss']

oldloss = np.loadtxt('hisloss.dat')
nepochold = oldloss.shape[0]

f = open('hisloss.dat','a')
for ipc in range(nepoch):
    f.write('%.15f '%(ipc+1.+nepochold))
    f.write('%.15f '%(hislosscl[ipc]))
    f.write('%.15f '%(hislossvalcl[ipc]))
    f.write('%.15f '%(hislosscd[ipc]))
    f.write('%.15f '%(hislossvalcd[ipc]))
    f.write('%.15f '%(hislosscm[ipc]))
    f.write('%.15f '%(hislossvalcm[ipc]))
    f.write('\n')
f.close()

