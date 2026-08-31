import numpy as np
import segment as sg
from math import exp,sqrt,cos,asin
import csv
import pickle
import pandas as pd
import pprint as pp
import matplotlib.pyplot as plt
import ast
import os

folder_name = "1pt-ADODG"
directory = "./mission_analysis_database/" + folder_name

if not os.path.exists(directory):
    os.makedirs(directory)
    print("Folder '{}' created successfully.".format(folder_name))
else:
    print("Folder '{}' already exists.".format(folder_name))

nsegments = 11

Data = []

for i in range(nsegments):
    data_segment = sg.Segment()
    Data.append(data_segment)

def initialization(Mach,h,v):
    Data[0].segType = 'TGroundRoll'
    Data[0].Weight = [2500000.0,300000.0] # 186kts
    Data[0].Mach = [0.0,0.2]
    Data[0].Altitude = [0.0,0.0]
    Data[0].segTime = 0
    Data[0].throttle = [1.0]
        

    Data[1].segType= 'acceleratedClimb' #accelerate to 210kts at 1500ft
    Data[1].Weight = [3000000.0,300000.0]
    Data[1].Velocity = [95.963,110.369] #200 cas
    Data[1].Altitude = [0,457.2]
    Data[1].segTime = 0
    Data[1].throttle = [1.0]


    Data[2].segType= 'acceleratedClimb' #accelerate velocity to 10,000ft
    Data[2].Weight = [3000000.0,300000.0]
    Data[2].Velocity = [110.369,189.266] #250 cas
    Data[2].Altitude = [457.2,3048]
    Data[2].segTime = 0
    Data[2].throttle = [0.8]


    Data[3].segType= 'acceleratedClimb' #constant velocity to h
    Data[3].Weight = [3000000.0,300000.0]
    Data[3].Velocity = [189.266,v] #310 cas
    Data[3].Altitude = [3048,h]
    Data[3].segTime = 0
    Data[3].throttle = [0.8]

    Data[4].segType = 'CMachClimb'
    Data[4].Weight = [2500000.0,300000.0]
    Data[4].Mach = [Mach,Mach]
    Data[4].Altitude = [h,10668] #35,000ft 
    Data[4].segTime = 0
    Data[4].throttle = [0.8]

    Data[5].segType = 'cruise' 
    Data[5].Weight = [350000.0,330000.0]
    Data[5].Mach = [Mach,Mach]
    Data[5].Altitude = [10668,10668]
    Data[5].segTime = 0
    Data[5].throttle = [0.4]

    Data[6].segType = 'CMachDescent' 
    Data[6].Weight = [360000,300000]
    Data[6].Mach = [Mach,Mach]
    Data[6].Altitude = [10668,h]
    Data[6].segTime = 0
    Data[6].throttle = [0.015]

    Data[7].segType = 'acceleratedDescent' 
    Data[7].Weight = [350000,300000]
    Data[7].Velocity = [v,189.266] 
    Data[7].Altitude = [h,3048.0] 
    Data[7].segTime = 0
    Data[7].throttle = [0.07]  

    Data[8].segType = 'acceleratedDescent' 
    Data[8].Weight = [350000,300000]
    Data[8].Velocity = [189.266,110.369] 
    Data[8].Altitude = [3048.0,457.2] 
    Data[8].segTime = 0
    Data[8].throttle = [0.01 ]


    Data[9].segType = 'acceleratedDescent'
    Data[9].Weight = [3500000.0,457.2]
    Data[9].Velocity = [110.369,96.1136]
    Data[9].Altitude = [457.2,0]
    Data[9].segTime = 0
    Data[9].throttle = [0.01]

    Data[10].segType = 'LGroundRoll' 
    Data[10].Weight = [350000,300000]
    Data[10].Mach = [0.2,0]
    Data[10].Altitude = [0,0]
    Data[10].segTime = 0
    Data[10].throttle = [0.01]

    


    for i in range(nsegments):
        if Data[i].segType == 'cruise':
            Data[i].nInt=30

        else:
            Data[i].nInt=10

        Data[i].CD=[100 for j in range(Data[i].nInt)]
        Data[i].CL=[100 for j in range(Data[i].nInt)]
        Data[i].D=[49750 for j in range(Data[i].nInt)]
        Data[i].L=[49750 for j in range(Data[i].nInt)]
        Data[i].intVelocity=[100 for j in range(Data[i].nInt)]
        Data[i].T=[100 for j in range(Data[i].nInt)]
        Data[i].TSFC=[100 for j in range(Data[i].nInt)]
        Data[i].intAltitude=[0 for j in range(Data[i].nInt)]
        Data[i].intDist=[0 for j in range(Data[i].nInt)]
        Data[i].intFuel=[0 for j in range(Data[i].nInt)]
        Data[i].intTime=[0 for j in range(Data[i].nInt)]
        Data[i].alpha=[0 for j in range(Data[i].nInt)]
        Data[i].intMach=[0.23 for j in range(Data[i].nInt)]
        Data[i].segFuel=0
        Data[i].segDist=0
        Data[i].throttle = [Data[i].throttle[0] for j in range(Data[i].nInt)]

        

        if Data[i].segType in ['CMachClimb', 'CMachDescent', 'acceleratedClimb', 'acceleratedDescent','CVelClimb','CVelDescent']:
            Data[i].dvdh = [-1.18e-3 for j in range(Data[i].nInt)]
            Data[i].gamma = [0 for j in range(Data[i].nInt)]
            Data[i].RC = [0 for j in range(Data[i].nInt)]
        
        if Data[i].segType in ['cruise','loiter']:
            Data[i].intWeight = [500000 for j in range(Data[i].nInt)]
        else:
            Data[i].intWeight = [500000 for j in range(Data[i].nInt)]
    
    return Data

def countStates(Data, states, ZFW):
    nstate = 0 
    for i in range(nsegments):
        if i == nsegments - 1:
            Data[i].Weight[0] = round(states[nstate],2)
            Data[i].Weight[1] = ZFW
            nstate += 1
            sg.LGroundRollRange(Data, i)
        elif Data[i].segType == 'TGroundRoll':
            Data[i].Weight[0] = round(states[nstate],2)
            nstate += 1
            sg.TGroundRollRange(Data, i)
        elif Data[i].segType == 'acceleratedClimb':
            Data[i].Weight[0] = round(states[nstate],2)
            nstate += 1
            sg.acceleratedClimbRange(Data, i)
        elif Data[i].segType == 'CVelClimb':
            Data[i].Weight[0] = round(states[nstate],2)
            nstate += 1
            sg.CVelClimbRange(Data, i)
        elif Data[i].segType == 'CMachClimb':
            Data[i].Weight[0] = round(states[nstate],2)
            nstate += 1
            sg.CMachClimbRange(Data, i)
        elif Data[i].segType == 'levelClimb':
            Data[i].Weight[0] = round(states[nstate],2)
            nstate += 1
            sg.levelClimbRange(Data, i)
        elif Data[i].segType == 'cruise':
            Data[i].Weight[0] = round(states[nstate],2)
            Data[i].Weight[1] = round(states[nstate+1],2)
            nstate += 1
            sg.cruiseRange(Data, i)
        elif Data[i].segType == 'CMachDescent':
            Data[i].Weight[0] = round(states[nstate],2)
            nstate += 1
            sg.CMachDescentRange(Data, i)
        elif Data[i].segType == 'CVelDescent':
            Data[i].Weight[0] = round(states[nstate],2)
            nstate += 1
            sg.CVelDescentRange(Data, i)
        elif Data[i].segType == 'acceleratedDescent':
            Data[i].Weight[0] = round(states[nstate],2)
            nstate += 1
            sg.acceleratedDescentRange(Data, i)
        elif Data[i].segType == 'loiter':
            Data[i].Weight[0] = round(states[nstate],2)
            nstate += 1
            sg.loiterRange(Data, i)
        elif Data[i].segType == 'TGroundRoll':
            Data[i].Weight[0] = round(states[nstate],2)
            nstate += 1
            sg.TGroundRollRange(Data, i)

    return Data, nstate

def computeResidual(Data, R, states,ZFW,Time):
    Data, nstate = countStates(Data, states,ZFW)

    computeTime = 0
    cruiseCounter = 0

    for i in range(nsegments):
        
        if Data[i].segType == 'cruise': #cruise segment
            if cruiseCounter == 0: 
                firstCruise = i 
                refTime = Data[i].segTime
                cruiseCounter += 1
            else:
                newR = (refTime - Data[i].segTime)/refTime*100
                R[i] = newR
                cruiseCounter += 1

        elif i == nsegments-1: 
            newR = (ZFW - Data[i].Weight[1])/ZFW*100 
            R[i] = newR
        else:
            newR = (Data[i+1].Weight[0] - Data[i].Weight[1])/Data[i+1].Weight[0]*100
            R[i] = newR
        
        computeTime += Data[i].segTime

    newR = (computeTime - Time)/Time*100

    R[firstCruise] = newR
    # print('residual:', R)

    return  Data, nstate, R, states

def getJacobian():
    # the initial weight of each segment
    Data = initialization(Mach,h,v)

    R = [1 for i in range(nsegments)]
    states = [assume - i*(assume - ZFW)/nsegments for i in range(nsegments)]

    Data, nstate, R, states = computeResidual(Data, R, states,ZFW,Time)
    iter = 1
    err = sum(np.absolute(np.array(R)))
    np.set_printoptions(precision=10)

    while err > 1:
        states_old = states.copy()
        R_old = R.copy()
        mR_old = np.array(R_old)    
        
        deltaW = 10.
        J = np.empty((nstate,nstate))

        for i in range(nstate):
            state_ref = states[i]
            states[i] = state_ref + deltaW
            Data, nstate, R, states = computeResidual(Data, R, states,ZFW,Time)
            
            mR = np.array(R)            

            Jt = (mR - mR_old).dot(1/deltaW)
            J[:,i] = Jt
            states[i] = state_ref

        Jinv = np.linalg.inv(J)
        # Jinv = np.linalg.pinv(J)
        delta = np.dot(Jinv, mR_old)
        mStates_old = np.array(states_old)
        mStates = mStates_old - delta
        a = mStates.tolist()
        
        for i in range(nstate):
            states[i] = a[i]
        Data, nstate, R, states = computeResidual(Data, R, states,ZFW,Time)
        err = sum(abs(np.array(R)))

        iter += 1
        print('iter:', iter,'err:',err,'\n','states:', states,'\n','residual', R)
    
    return Data, nsegments

# connect to real data
def atmos(altitude):
    units = 'SI'
    K = 34.163195e0

    if units == 'SI':
        C1 = 1e-3
        TL = 288.15e0
        PL = 101325.e0
        RL = 1.225e0
        AL = 340.294e0
        ML = 0.000017894e0
        BT = 1.458e-6
    elif units == 'English':
        C1 = 0.0003048e0
        TL = 518.67e0
        PL = 2116.22e0
        RL = 0.0023769e0
        AL = 1116.45e0
        ML = 3.7373e-7
        BT = 0.000000030450963e0

    H = C1*altitude/(1.e0 + C1*altitude/6356.766e0)

    if H <= 11.e0:
        T = 288.15e0 - 6.5e0*H
        PP = (288.15e0/T)**(-K/6.5e0)
    elif H > 11.e0 and H <= 20.e0:
        T = 216.65e0
        PP = 0.22336e0*exp(-K*(H-11.e0)/216.65e0)
    elif H > 20.e0 and H <= 32.e0:
        T = 216.65e0 + (H-20.e0)
        PP = 0.054032e0*(216.65e0/T)**K
    elif H > 32.e0 and H <= 47.e0:
        T = 228.65e0 + 2.8e0*(H-32.e0)
        PP = 0.0085666e0*(228.65e0/T)**(K/2.8e0)
    elif H > 47.e0 and H <= 51.e0:
        T = 270.65e0
        PP = 0.0010945e0*exp(-K*(H-47.e0)/270.65e0)
    elif H > 51.e0 and H <= 71.e0:
        T = 270.65e0 - 2.8e0*(H-51.e0)
        PP = 0.00066063e0*(270.65e0/T)**(-K/2.8e0)
    elif H > 71.e0 and H <= 84.852e0:
        T = 214.65e0 - 2.e0*(H-71.e0)
        PP = 0.000039046e0*(214.65e0/T)**(-K/2.e0)

    RR = PP/(T/288.15e0)
    mu = BT*(T**1.5e0)/(T+110.4e0)
    TS = T/288.15e0
    a = AL*sqrt(TS)
    T = TL*TS
    rho = RL*RR
    P = PL*PP
    RM = rho*a/mu
    QM = 0.7e0*P
    F = T - 459.69e0
    C = T - 273.15e0
    VELRAT = sqrt(TS)
    nu = mu/rho
    SQRR = sqrt(RR)
    SQRTS = sqrt(TS)
    CKNOTS = a*1.9438445 #Speed of Sound in Knots

    return rho,P,CKNOTS,a

def calTAS(altitude, CAS):
    rho,P,k,a = atmos(altitude)
    rho0,P0,k0,a0 = atmos(0)
    mu = 1/3.5
    TAS = ((2/mu)*(P/rho)*((1+((P0/P)*((1+(mu/2)*(rho0/P0)*CAS**2)**(1/mu)-1)))**(mu)-1))**(1/2)

    return TAS

def calPoint(Mach):
    alt = 3048
    CAS = 320*0.514444
    err = 10
    while abs(err) >1 :
        speed = Mach*atmos(alt)[3]
        olderr = calTAS(alt,CAS) - speed
        err = calTAS(alt+10,CAS) - Mach*atmos(alt+10)[3]
        gradient = (err - olderr)/10
        alt -= err/gradient
    return alt,speed




# ZFW = 223402*2.20462 
# Range = 7167.85*6076.12 #HKG - JFK
# Mach = 0.747882 
# h,v = calPoint(Mach)
# assume = 800000 
# ISADev = 3

# getJacobian()
#     # pp.pprint(R)
#     # pp.pprint(Data)

# totalFuel = 0
# totalTime = 0 
# for j in range (nsegments):
#     if Data[j].segType == 'loiter':
#         totalTime += Data[j].segTime
#         loiter =  Data[j].segFuel
#     else:
#         totalFuel += Data[j].segFuel
#         totalTime += Data[j].segTime

# # df = pd.DataFrame(Data[j])
# # df.to_csv(f"results/tempResult_{i}_{j}.csv")

# print(totalFuel,totalTime) 
# print(loiter)
# print(Data[1].CD) 


# f = open('HKG-JFK13.csv')


def readCSV(fileName):
    f = open(fileName)
    reader = csv.reader(f)
    headers = next(reader,None)
    column = {}
    for h in headers:
        column[h] = []
    for row in reader:
        for h,v in zip(headers,row):
            column[h].append(v)
    return column

############################################
column = readCSV('./mission_analysis_database/JFK0103.csv')
rI = readCSV('./mission_analysis_database/recordInterval.csv')
# rS = readCSV('recordSegment.csv')
############################################

def saveData(flightNum):
    rS = readCSV('./mission_analysis_database/recordSegment.csv')
    # rs1 = pd.DataFrame(rS)
    for segNum in range(nsegments):
        rS['segType'].append(Data[segNum].segType)
        rS['nInt'].append(Data[segNum].nInt)
        rS['Weight'].append(Data[segNum].Weight)
        rS['Altitude'].append(Data[segNum].Altitude)
        rS['intWeight'].append(Data[segNum].intWeight)
        rS['intAltitude'].append(Data[segNum].intAltitude)
        rS['intMach'].append(Data[segNum].intMach)
        rS['intVelocity'].append(Data[segNum].intVelocity)
        rS['alpha'].append(Data[segNum].alpha)
        rS['CD'].append(Data[segNum].CD)
        rS['CL'].append(Data[segNum].CL)
        rS['D'].append(Data[segNum].D)
        rS['L'].append(Data[segNum].L)
        rS['intDist'].append(Data[segNum].intDist)
        rS['intTime'].append(Data[segNum].intTime)
        rS['intFuel'].append(Data[segNum].intFuel)
        rS['segDist'].append(Data[segNum].segDist)
        rS['segTime'].append(Data[segNum].segTime)
        rS['segFuel'].append(Data[segNum].segFuel)
        rS['T'].append(Data[segNum].T)
        rS['TSFC'].append(Data[segNum].TSFC)
        rS['throttle'].append(Data[segNum].throttle)
        
        # rS['gamma'].append(Data[segNum].gamma)
        # rS['dvdh'].append(Data[segNum].dvdh)
        # rS['Mach'].append(Data[segNum].Mach)
        
        try:
            rS['gamma'].append(Data[segNum].gamma)
            rS['dvdh'].append(Data[segNum].dvdh)
            # rS['Mach'].append(Data[segNum].Mach)
        except AttributeError:
            rS['gamma'].append([0]*Data[segNum].nInt)
            rS['dvdh'].append([0]*Data[segNum].nInt)
            # rS['Mach'].append([0]*Data[segNum].nInt)
    
    df = pd.DataFrame.from_dict(rS,orient='index')
    df = df.transpose()
    df.to_csv("./mission_analysis_database/%s/p3_short_%d.csv"%name%flightNum, encoding='utf-8')
    # with open(f"results/{flightNum}_recordSegment.csv", 'w') as f:
    #     for key in rS.keys():
    #         f.write("%s,%s\n"%(key,rS[key]))

    # plotFigure(f"results/{flightNum}_recordSegment.csv",'intDist','intAltitude')
    return rS
    

if __name__ == '__main__':

    ####################################################################################
    i = 1
    g = 9.80665
    # ISADev = float(column['ISADev'][i])
    ZFW = 205023.75*g


    #

    sample_airlines = pd.read_csv("./sample_airlines_file/sample_airlines_MA.csv")
    new_data = {}

    for index, row in sample_airlines.iterrows():

            # parameter setting
        Time = row["total time"]
        Mach = row["mean mach"]   #float(column['Mach'][i]) - 0.03 #(float(column['errTime'][i])+4)*0.001

        h,v = calPoint(Mach)
        assume = 350000*g
        ####################################################################################
        getJacobian()
        # pp.pprint(R)


        totoalFuel = 0
        totoalDist = 0 
        for j in range (nsegments):
            if Data[j].segType == 'loiter':
                totoalDist += Data[j].segDist
                totoalFuel += Data[j].segFuel
                loiter =  Data[j].segFuel
            else:
                totoalFuel += Data[j].segFuel
                totoalDist += Data[j].segDist

        saveData(index)
        # plotSubFigure() 

        # for j in range(nsegments):
        #     sg.printCheck(Data,j)

        # column['calFuel'][i] = totoalFuel/g
        # column['calDist'][i] = totoalDist/1609.34
        # column['errFuel'][i] = (totoalFuel/g/float(column['tripFuel'][i])-1)*100.0
        # column['errDist'][i] = (column['calDist'][i]/float(column['Dist'][i]) - 1)*100

        # column['calFAF'][i] = totoalFuel - float(column['tripFuel'][i])
        print('case',index,'err',column['errFuel'][index],totoalFuel)

        new_data = pd.DataFrame({
            # 'Index':index,
            'Dep': row["Dep"],
            'Arr': row["Arr"],
            'Fuel': np.array(totoalFuel,dtype=object),
            'Flight time': np.array(row["total time"],dtype=object),
        },index=[0])
        new_data.to_csv("airlines_MA_fuel_%s.csv"%folder_name, mode='a', header=False, index=False)

# final = pd.concat(list(new_data.values()), ignore_index=True)
# new_data.to_csv("airlines_MA_fuel_all_GMM_optimized.csv", mode='a', header=False, index=False)
        # df = pd.DataFrame(column)
        # #df = df.transpose()
        # df.to_csv('data_driven.csv',encoding='utf-8')
    


