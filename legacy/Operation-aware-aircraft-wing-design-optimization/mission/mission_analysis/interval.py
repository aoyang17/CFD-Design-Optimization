#%%
from surrogateAero2D_new import *
from surrogateEngine import *
from math import exp,sqrt,cos,asin
import numpy as np
import pprint as pp
from smt.surrogate_models import RMTB

#wing span
s = 436.8
units = "SI"

def atmospherics(Data, segmentNum, intervalNum):
    K = 34.163195e0
    units = 'SI'
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

    H = C1*Data[segmentNum].intAltitude[intervalNum]/(1.e0 + C1*Data[segmentNum].intAltitude[intervalNum]/6356.766e0)

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
    CKNOTS = a*1942.56e0 #Speed of Sound in Knots

    soundspeed = a
    return rho, soundspeed

def getCD(Data, alpha, Mach, CLtarget, segmentNum, intervalNum):
        
        iter = 0 
        x = np.zeros((1, 2))
        
        while True:
            x[0, 0] = alpha
            x[0, 1] = Mach
            
            CL = SurrogateAero(x)[0]
            f = CL - CLtarget
            gradient = SurrogateAero(x)[2]
            iter += 1
            
            if abs(f) < 0.0001:
                break
            if iter > 100:
                #print(segmentNum,intervalNum,'CL can not converged')
                break
            alpha -= f/gradient

        CD =  SurrogateAero(x)[1] #0.020

        Data[segmentNum].CL[intervalNum] =  round(CL,6) #CLtarget
        Data[segmentNum].CD[intervalNum] = round(CD,6)
        Data[segmentNum].alpha[intervalNum] = round(alpha,6)
        
        return CD

def engine(Data, segmentNum, intervalNum):
        '''input variables: Mach, altitute, throttle'''
        if units == 'English':
            altitudeSI = Data[segmentNum].intAltitude[intervalNum]/3280.8
        elif units == 'SI':
            altitudeSI = Data[segmentNum].intAltitude[intervalNum]/1000.0

        x = np.zeros((1,3))
        x[0,0] = Data[segmentNum].intMach[intervalNum]
        x[0,1] = altitudeSI
        x[0,2] = Data[segmentNum].throttle[intervalNum]

        T = SurrogareEngine(x)[0]*2  #*0.2248089431
        TSFC = SurrogareEngine(x)[1] #*9.8
        gradient = SurrogareEngine(x)[2]

        Data[segmentNum].T[intervalNum] = round(T,6)
        Data[segmentNum].TSFC[intervalNum] = round(TSFC,6)
        return T, TSFC, gradient

def computeCruise_dW(Data, segmentNum, intervalNum):
    rho, soundspeed = atmospherics(Data, segmentNum, intervalNum)
    velocity = Data[segmentNum].intMach[intervalNum] * soundspeed
    Data[segmentNum].intVelocity[intervalNum] = round(velocity,6)
    
    gamma = 0 
    L = Data[segmentNum].intWeight[intervalNum]*cos(gamma)
    CLtarget = L/(0.5*rho*s*(velocity**2))
    
    Data[segmentNum].alpha[intervalNum] = 0
    CD= getCD(Data, Data[segmentNum].alpha[intervalNum], Data[segmentNum].intMach[intervalNum], CLtarget, segmentNum, intervalNum)
    # qar corrected
    D = 0.5*rho*s*(velocity**2)*(CD*1.302)
    # D = 0.5*rho*s*(velocity**2)*(CD*1.27)

# auto throttle
    Data[segmentNum].throttle[intervalNum] = 1.0
    err = 10
    while True:
        if abs(err) < 1:
            break
        T, TSFC, gradient = engine(Data, segmentNum, intervalNum)
        err = T - D
        Data[segmentNum].throttle[intervalNum] -= err/gradient/1.5

# fixed throttle
    # T, TSFC, gradient = engine(Data, segmentNum, intervalNum)


    # TSFC += 7e-5
    T = D
    dsdw = -velocity/(TSFC * T)
    dtdw = -1/(TSFC * T)

    
    Data[segmentNum].L[intervalNum] = round(L,6)
    Data[segmentNum].D[intervalNum] = round(D,6) 
    
    return dsdw, dtdw

def computeClimb_dh(Data, segmentNum, intervalNum):
    rho, soundspeed = atmospherics(Data, segmentNum, intervalNum)
    velocity = Data[segmentNum].intMach[intervalNum] * soundspeed
    Data[segmentNum].intVelocity[intervalNum] = round(velocity,6)

    tol = 1e-10
    g = 9.80665

    gammaSeg = 0
    iter = 0

    while True:
        L = Data[segmentNum].intWeight[intervalNum]*cos(gammaSeg)
        CLtarget = L/(0.5*rho*s*(velocity**2)) 

        if Data[segmentNum].intMach[intervalNum] < 0.39:
            CD = CLtarget/20
            # CD = getCD(Data, Data[segmentNum].alpha[intervalNum], Data[segmentNum].intMach[intervalNum], CLtarget-0.5, segmentNum, intervalNum)
            
            # CL = CLtarget-0.5
            Data[segmentNum].CL[intervalNum] = round(CLtarget,6)
            Data[segmentNum].CD[intervalNum] = round(CD,6)
            Data[segmentNum].alpha[intervalNum] = round(0,6)
        else:
            CD = getCD(Data, Data[segmentNum].alpha[intervalNum], Data[segmentNum].intMach[intervalNum], CLtarget, segmentNum, intervalNum)
        
        # qar corrected
        D = 0.5*rho*s*(velocity**2)*CD*1.279
        # D = 0.5*rho*s*(velocity**2)*CD

        T, TSFC,gradient = engine(Data, segmentNum, intervalNum)
        
        if T < 1.1*D:
            T = 1.1*D

        RC =  ((T - D)*velocity)/(Data[segmentNum].intWeight[intervalNum]*(1+(velocity/g)*Data[segmentNum].dvdh[intervalNum])) 
        
        gammaNew = asin(max(min(RC/velocity,1.0),-1.0))

        deltaGamma = gammaNew - gammaSeg
        gammaSeg = gammaNew

        if abs(deltaGamma) < tol:
            break
        if iter > 50:
            print('gamma not converged', deltaGamma)
            break
        iter += 1

     
    dwdh = -TSFC*T/(RC)
    dsdh = velocity*cos(gammaSeg)/(RC)
    dtdh = 1/(RC)

    Data[segmentNum].gamma[intervalNum] = round(gammaSeg,6)
    Data[segmentNum].RC[intervalNum] = round(RC,6)
    Data[segmentNum].L[intervalNum] = round(L,6)
    Data[segmentNum].D[intervalNum] = round(D,6)

    return dsdh, dtdh, dwdh

def computeDescent_dh(Data, segmentNum, intervalNum):
    rho, soundspeed = atmospherics(Data, segmentNum, intervalNum)
    velocity = Data[segmentNum].intMach[intervalNum] * soundspeed
    Data[segmentNum].intVelocity[intervalNum] = round(velocity,6)

    tol = 1e-10
    g = 9.80665

    gammaSeg = 0
    iter = 0

    while True:
        L = Data[segmentNum].intWeight[intervalNum]*cos(gammaSeg)
        CLtarget = L/(0.5*rho*s*(velocity**2)) 

        if Data[segmentNum].intMach[intervalNum] < 0.39:
            CD = CLtarget/20
            # CD = getCD(Data, Data[segmentNum].alpha[intervalNum], Data[segmentNum].intMach[intervalNum], CLtarget-0.5, segmentNum, intervalNum)
            
            # CL = CLtarget-0.5
            Data[segmentNum].CL[intervalNum] = round(CLtarget,6)
            Data[segmentNum].CD[intervalNum] = round(CD,6)
            Data[segmentNum].alpha[intervalNum] = round(0,6)
        else:
            CD = getCD(Data, Data[segmentNum].alpha[intervalNum], Data[segmentNum].intMach[intervalNum], CLtarget, segmentNum, intervalNum)
        
        # qar corrected
        D = 0.5*rho*s*(velocity**2)*CD*1.5 
        # D = 0.5*rho*s*(velocity**2)*CD


        T, TSFC,gradient = engine(Data, segmentNum, intervalNum)

        RC =  ((T - D)*velocity)/(Data[segmentNum].intWeight[intervalNum]*(1+(velocity/g)*Data[segmentNum].dvdh[intervalNum])) 
        
        gammaNew = asin(max(min(RC/velocity,1.0),-1.0))

        deltaGamma = gammaNew - gammaSeg
        gammaSeg = gammaNew

        if abs(deltaGamma) < tol:
            break
        if iter > 50:
            print('gamma not converged', deltaGamma)
            break
        iter += 1

     
    dwdh = -TSFC*T/(RC)
    dsdh = velocity*cos(gammaSeg)/(RC)
    dtdh = 1/(RC)

    Data[segmentNum].gamma[intervalNum] = round(gammaSeg,6)
    Data[segmentNum].RC[intervalNum] = round(RC,6)
    Data[segmentNum].L[intervalNum] = round(L,6)
    Data[segmentNum].D[intervalNum] = round(D,6)

    return dsdh, dtdh, dwdh

def computeTGroundRoll_dv(Data, segmentNum, intervalNum):
    g = 9.80665
    velocity = Data[segmentNum].intVelocity[intervalNum]
    rho, soundspeed = atmospherics(Data, segmentNum, intervalNum)
    Data[segmentNum].intMach[intervalNum] = velocity/soundspeed

    # xInpute = np.array([[0,Data[segmentNum].intMach[intervalNum],Data[segmentNum].intAltitude[intervalNum]]])
    CL = 1.19/9*intervalNum
    # CL = SurrogateAero(xInpute)[1]
    L = 0.5*rho*s*(velocity**2)*CL
    CD = CL/20
    # CD = SurrogateAero(xInpute)[0]
    D = 0.5*rho*s*(velocity**2)*CD

    mu = 0.04
    T, TSFC,gradient= engine(Data, segmentNum, intervalNum)
    dsdv = velocity*Data[segmentNum].intWeight[intervalNum]/(g*(T - D - mu*(Data[segmentNum].intWeight[intervalNum] - L)))
    dtdv = Data[segmentNum].intWeight[intervalNum]/(g*(T - D - mu*(Data[segmentNum].intWeight[intervalNum] - L)))
    dwdv = -TSFC*T*Data[segmentNum].intWeight[intervalNum]/(g*(T - D - mu*(Data[segmentNum].intWeight[intervalNum] - L)))

    Data[segmentNum].CL[intervalNum] = round(CL,6)
    Data[segmentNum].CD[intervalNum] = round(CD,6)
    Data[segmentNum].L[intervalNum] = round(L,6)
    Data[segmentNum].D[intervalNum] = round(D,6)
    
    return dsdv, dtdv, dwdv

def computeLGroundRoll_dv(Data, segmentNum, intervalNum):
    g = 9.80665
    velocity = Data[segmentNum].intVelocity[intervalNum]
    rho, soundspeed = atmospherics(Data, segmentNum, intervalNum)
    Data[segmentNum].intMach[intervalNum] = velocity/soundspeed
    Data[segmentNum].intMach[intervalNum] = Data[segmentNum].intMach[intervalNum]

    # xInpute = np.array([[0,Data[segmentNum].intMach[intervalNum],Data[segmentNum].intAltitude[intervalNum]]])
    # CL = SurrogateAero(xInpute)[1]
    # L = 0.5*rho*s*(velocity**2)*CL
    # CD = SurrogateAero(xInpute)[0]
    # D = 0.5*rho*s*(velocity**2)*CD

    CL = 1.19 - 1.19/9*intervalNum
    L = 0.5*rho*s*(velocity**2)*CL
    CD = CL/3
    D = 0.5*rho*s*(velocity**2)*CD

    mu = 0.048
    T, TSFC,gradient = engine(Data, segmentNum, intervalNum)
    dsdv = velocity*Data[segmentNum].intWeight[intervalNum]/(g*(T - D - mu*(Data[segmentNum].intWeight[intervalNum] - L)))
    dtdv = Data[segmentNum].intWeight[intervalNum]/(g*(T - D - mu*(Data[segmentNum].intWeight[intervalNum] - L)))
    dwdv = -TSFC*T*Data[segmentNum].intWeight[intervalNum]/(g*(T - D - mu*(Data[segmentNum].intWeight[intervalNum] - L)))
    
    Data[segmentNum].CD[intervalNum] = round(CD,6)
    Data[segmentNum].CL[intervalNum] = round(CL,6)
    Data[segmentNum].L[intervalNum] = round(L,6)
    Data[segmentNum].D[intervalNum] = round(D,6)

    return dsdv, dtdv, dwdv


def computeLoiter_dt(Data, segmentNum, intervalNum, rho):
    gammaSeg = 0
    #rho, soundspeed = atmospherics(Data, segmentNum, intervalNum)

    L = Data[segmentNum].intWeight[intervalNum]*cos(gammaSeg)
    CLtarget = L/(0.5*rho*s*(Data[segmentNum].intVelocity[intervalNum]**2))
    CD = getCD(Data, Data[segmentNum].alpha[intervalNum], Data[segmentNum].intMach[intervalNum], CLtarget, segmentNum, intervalNum)
    D = 0.5*rho*s*(Data[segmentNum].intVelocity[intervalNum]**2)*CD
    T, TSFC,gradient = engine(Data, segmentNum, intervalNum)
    dwdt = -TSFC * T
    velocity = Data[segmentNum].intVelocity[intervalNum]
    dsdt = velocity
    
    Data[segmentNum].L[intervalNum] = round(L,6)
    Data[segmentNum].D[intervalNum] = round(D,6)

    return dsdt, dwdt

def level_dv(Data, segmentNum, intervalNum):
    g = 9.80665
    velocity = Data[segmentNum].intVelocity[intervalNum]
    rho, soundspeed = atmospherics(Data, segmentNum, intervalNum)
    Data[segmentNum].intMach[intervalNum] = velocity/soundspeed

    gammaSeg = 0
    L = Data[segmentNum].intWeight[intervalNum]*cos(gammaSeg)
    CLtarget = L/(0.5*rho*s*(Data[segmentNum].intVelocity[intervalNum]**2))
    if Data[segmentNum].intMach[intervalNum] < 0.4:
        CD = CLtarget/11
        CL = CLtarget-0.5
        Data[segmentNum].CL[intervalNum] = round(CLtarget,6)
        Data[segmentNum].CD[intervalNum] = round(CD,6)
        Data[segmentNum].alpha[intervalNum] = round(0,6)
    else:
        CD = getCD(Data, Data[segmentNum].alpha[intervalNum], Data[segmentNum].intMach[intervalNum], CLtarget, segmentNum, intervalNum)
        
    D = 0.5*rho*s*(Data[segmentNum].intVelocity[intervalNum]**2)*CD
    T, TSFC,gradient = engine(Data, segmentNum, intervalNum)


    dsdv = velocity*Data[segmentNum].intWeight[intervalNum]/(g*(T - D))
    dtdv = Data[segmentNum].intWeight[intervalNum]/(g*(T - D))
    dwdv = -TSFC*T*Data[segmentNum].intWeight[intervalNum]/(g*(T - D ))

    
    Data[segmentNum].L[intervalNum] = round(L,6)
    Data[segmentNum].D[intervalNum] = round(D,6)
    
    return dsdv, dtdv, dwdv
