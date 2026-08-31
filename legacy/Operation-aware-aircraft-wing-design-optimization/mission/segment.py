#%%
import interval
from prettytable import PrettyTable

class Segment: 
    def _init_(self):
        self.segType=None
        self.nInt=None
        self.Weight=[]
        self.Mach=[]
        self.Altitude=[]
        self.intWeight=[]
        self.intAltitude=[]
        self.intMach=[]
        self.intVelocity=[]
        self.alpha=[]
        self.CD=[]
        self.CL=[]
        self.D=[]
        self.L=[]
        self.intDist=[]
        self.intTime=None
        self.intFuel=[]
        self.segDist=None
        self.segTime=None
        self.segFuel=None
        self.T=[]
        self.TSFC=[]
        self.throttle=[]
        self.gamma=None
        self.RC=None
        self.dvdh=None  
        
def cruiseRange(Data, segmentNum):
    cruiseWfuel = Data[segmentNum].Weight[1] - Data[segmentNum].Weight[0]
    dW = cruiseWfuel/Data[segmentNum].nInt

    for i in range(Data[segmentNum].nInt):
        Data[segmentNum].intWeight[i] = Data[segmentNum].Weight[0] + i*dW
        Data[segmentNum].intAltitude[i] = Data[segmentNum].Altitude[0]
        Data[segmentNum].intMach[i] = Data[segmentNum].Mach[0]

    Data[segmentNum].segDist = 0
    Data[segmentNum].segTime = 0

    for i in range(Data[segmentNum].nInt):
        dsdw, dtdw = interval.computeCruise_dW(Data, segmentNum,i)
        Data[segmentNum].intDist[i] = round(dsdw * dW,6)
        Data[segmentNum].intTime[i] = round(dtdw * dW,6)
        Data[segmentNum].intFuel[i] = round(-dW,6)

        Data[segmentNum].segDist += Data[segmentNum].intDist[i]
        Data[segmentNum].segTime += Data[segmentNum].intTime[i]
  

    Data[segmentNum].segFuel = round(-cruiseWfuel,6)

def CMachClimbRange(Data, segmentNum):
    climbAlt = Data[segmentNum].Altitude[1] - Data[segmentNum].Altitude[0]
    dh = climbAlt/Data[segmentNum].nInt

    Data[segmentNum].segDist = 0
    Data[segmentNum].segTime = 0
    Data[segmentNum].segFuel = 0

    Data[segmentNum].intWeight[0] = Data[segmentNum].Weight[0]

    for i in range(Data[segmentNum].nInt):
        Data[segmentNum].intAltitude[i] = Data[segmentNum].Altitude[0] + i * dh
        Data[segmentNum].intMach[i] = Data[segmentNum].Mach[0]
        
        rho, soundspeed = interval.atmospherics(Data, segmentNum,i)
        velocity1 = soundspeed * Data[segmentNum].intMach[i]
        fdStep = 0.0001
        Data[segmentNum].intAltitude[i] += fdStep
        rho, soundspeed = interval.atmospherics(Data, segmentNum,i)
        velocity2 =  soundspeed * Data[segmentNum].intMach[i]
        dvdh = (velocity2 - velocity1)/fdStep
        Data[segmentNum].dvdh[i] = round(dvdh,6)
        
        Data[segmentNum].intAltitude[i] -= fdStep
        dsdh, dtdh, dwdh = interval.computeClimb_dh(Data, segmentNum,i)

        Data[segmentNum].intDist[i] = round(dsdh*dh,6)
        Data[segmentNum].intTime[i] = round(dtdh*dh,6)
        Data[segmentNum].intFuel[i] = round(-dwdh*dh,6)

        Data[segmentNum].segDist += Data[segmentNum].intDist[i]
        Data[segmentNum].segTime += Data[segmentNum].intTime[i]
        Data[segmentNum].segFuel += Data[segmentNum].intFuel[i]
        
        if i < Data[segmentNum].nInt-1:
            Data[segmentNum].intWeight[i+1] = Data[segmentNum].intWeight[i] - Data[segmentNum].intFuel[i]

    Data[segmentNum].Weight[1] = round(Data[segmentNum].intWeight[0]-Data[segmentNum].segFuel,6)

def CMachDescentRange(Data, segmentNum):
    climbAlt = Data[segmentNum].Altitude[1] - Data[segmentNum].Altitude[0]
    dh = climbAlt/Data[segmentNum].nInt

    Data[segmentNum].segDist = 0
    Data[segmentNum].segTime = 0
    Data[segmentNum].segFuel = 0

    Data[segmentNum].intWeight[0] = Data[segmentNum].Weight[0]

    for i in range(Data[segmentNum].nInt):
        Data[segmentNum].intAltitude[i] = Data[segmentNum].Altitude[0] + i * dh
        Data[segmentNum].intMach[i] = Data[segmentNum].Mach[0]
        
        rho, soundspeed = interval.atmospherics(Data, segmentNum,i)
        velocity1 = soundspeed * Data[segmentNum].intMach[i]
        fdStep = 0.0001
        Data[segmentNum].intAltitude[i] += fdStep
        rho, soundspeed = interval.atmospherics(Data, segmentNum,i)
        velocity2 =  soundspeed * Data[segmentNum].intMach[i]
        dvdh = (velocity2 - velocity1)/fdStep
        Data[segmentNum].dvdh[i] = round(dvdh,6)
        
        Data[segmentNum].intAltitude[i] -= fdStep
        dsdh, dtdh, dwdh = interval.computeDescent_dh(Data, segmentNum,i)

        Data[segmentNum].intDist[i] = round(dsdh*dh,6)
        Data[segmentNum].intTime[i] = round(dtdh*dh,6)
        Data[segmentNum].intFuel[i] = round(-dwdh*dh,6)

        Data[segmentNum].segDist += Data[segmentNum].intDist[i]
        Data[segmentNum].segTime += Data[segmentNum].intTime[i]
        Data[segmentNum].segFuel += Data[segmentNum].intFuel[i]
        
        if i < Data[segmentNum].nInt-1:
            Data[segmentNum].intWeight[i+1] = Data[segmentNum].intWeight[i] - Data[segmentNum].intFuel[i]

    Data[segmentNum].Weight[1] = round(Data[segmentNum].intWeight[0]-Data[segmentNum].segFuel,6)

def acceleratedClimbRange(Data, segmentNum):
    climbAlt = Data[segmentNum].Altitude[1] - Data[segmentNum].Altitude[0]
    dh = climbAlt/Data[segmentNum].nInt
    dvdh = (Data[segmentNum].Velocity[1] - Data[segmentNum].Velocity[0])/climbAlt
    
    velocity = Data[segmentNum].Velocity[0]
    Data[segmentNum].intWeight[0] = Data[segmentNum].Weight[0]
    
    Data[segmentNum].segDist = 0
    Data[segmentNum].segTime = 0
    Data[segmentNum].segFuel = 0

    for i in range(Data[segmentNum].nInt):
        Data[segmentNum].dvdh[i] = round(dvdh,6)
        Data[segmentNum].intAltitude[i] = Data[segmentNum].Altitude[0] + i*dh

        rho, soundspeed = interval.atmospherics(Data, segmentNum,i)
        Data[segmentNum].intMach[i] = velocity / soundspeed
        
        dsdh, dtdh, dwdh = interval.computeClimb_dh(Data, segmentNum,i)
        Data[segmentNum].intDist[i] = round(dsdh*dh,6)
        Data[segmentNum].intTime[i] = round(dtdh*dh,6)
        Data[segmentNum].intFuel[i] = round(-dwdh*dh,6)

        Data[segmentNum].segDist += Data[segmentNum].intDist[i]
        Data[segmentNum].segTime += Data[segmentNum].intTime[i]
        Data[segmentNum].segFuel += Data[segmentNum].intFuel[i]
        
        if i < Data[segmentNum].nInt-1:
            Data[segmentNum].intWeight[i+1] = Data[segmentNum].intWeight[i] - Data[segmentNum].intFuel[i]
            velocity += dvdh*dh
    
    Data[segmentNum].Weight[1] = round(Data[segmentNum].intWeight[0]-Data[segmentNum].segFuel,6)

def acceleratedDescentRange(Data, segmentNum):
    climbAlt = Data[segmentNum].Altitude[1] - Data[segmentNum].Altitude[0]
    dh = climbAlt/Data[segmentNum].nInt
    dvdh = (Data[segmentNum].Velocity[1] - Data[segmentNum].Velocity[0])/climbAlt
    
    velocity = Data[segmentNum].Velocity[0]
    Data[segmentNum].intWeight[0] = Data[segmentNum].Weight[0]
    
    Data[segmentNum].segDist = 0
    Data[segmentNum].segTime = 0
    Data[segmentNum].segFuel = 0

    for i in range(Data[segmentNum].nInt):
        Data[segmentNum].dvdh[i] = round(dvdh,6)
        Data[segmentNum].intAltitude[i] = Data[segmentNum].Altitude[0] + i*dh

        rho, soundspeed = interval.atmospherics(Data, segmentNum,i)
        Data[segmentNum].intMach[i] = velocity / soundspeed
        
        dsdh, dtdh, dwdh = interval.computeDescent_dh(Data, segmentNum,i)
        Data[segmentNum].intDist[i] = round(dsdh*dh,6)
        Data[segmentNum].intTime[i] = round(dtdh*dh,6)
        Data[segmentNum].intFuel[i] = round(-dwdh*dh,6)

        Data[segmentNum].segDist += Data[segmentNum].intDist[i]
        Data[segmentNum].segTime += Data[segmentNum].intTime[i]
        Data[segmentNum].segFuel += Data[segmentNum].intFuel[i]
        
        if i < Data[segmentNum].nInt-1:
            Data[segmentNum].intWeight[i+1] = Data[segmentNum].intWeight[i] - Data[segmentNum].intFuel[i]
            velocity += dvdh*dh
    
    Data[segmentNum].Weight[1] = round(Data[segmentNum].intWeight[0]-Data[segmentNum].segFuel,6)

def CVelClimbRange(Data, segmentNum):
    climbAlt = Data[segmentNum].Altitude[1] - Data[segmentNum].Altitude[0]
    dh = climbAlt/Data[segmentNum].nInt
    dvdh = 0
    
    velocity = Data[segmentNum].Velocity[0]
    Data[segmentNum].intWeight[0] = Data[segmentNum].Weight[0]
    
    Data[segmentNum].segDist = 0
    Data[segmentNum].segTime = 0
    Data[segmentNum].segFuel = 0

    for i in range(Data[segmentNum].nInt):
        Data[segmentNum].dvdh[i] = round(dvdh,6)
        Data[segmentNum].intAltitude[i] = Data[segmentNum].Altitude[0] + i*dh

        rho, soundspeed = interval.atmospherics(Data, segmentNum,i)
        Mach = velocity / soundspeed
        Data[segmentNum].intMach[i] = Mach
        
        dsdh, dtdh, dwdh = interval.computeClimb_dh(Data, segmentNum,i)
        Data[segmentNum].intDist[i] = round(dsdh*dh,6)
        Data[segmentNum].intTime[i] = round(dtdh*dh,6)
        Data[segmentNum].intFuel[i] = round(-dwdh*dh,6)

        Data[segmentNum].segDist += Data[segmentNum].intDist[i]
        Data[segmentNum].segTime += Data[segmentNum].intTime[i]
        Data[segmentNum].segFuel += Data[segmentNum].intFuel[i]

        if i < Data[segmentNum].nInt-1:
            Data[segmentNum].intWeight[i+1] = Data[segmentNum].intWeight[i] - Data[segmentNum].intFuel[i]
            velocity += dvdh*dh

    Data[segmentNum].Weight[1] = round(Data[segmentNum].intWeight[0]-Data[segmentNum].segFuel,6)

def CVelDescentRange(Data, segmentNum):
    climbAlt = Data[segmentNum].Altitude[1] - Data[segmentNum].Altitude[0]
    dh = climbAlt/Data[segmentNum].nInt
    dvdh = 0
    
    velocity = Data[segmentNum].Velocity[0]
    Data[segmentNum].intWeight[0] = Data[segmentNum].Weight[0]
    
    Data[segmentNum].segDist = 0
    Data[segmentNum].segTime = 0
    Data[segmentNum].segFuel = 0

    for i in range(Data[segmentNum].nInt):
        Data[segmentNum].dvdh[i] = round(dvdh,6)
        Data[segmentNum].intAltitude[i] = Data[segmentNum].Altitude[0] + i*dh

        rho, soundspeed = interval.atmospherics(Data, segmentNum,i)
        Mach = velocity / soundspeed
        Data[segmentNum].intMach[i] = Mach
        
        dsdh, dtdh, dwdh = interval.computeDescent_dh(Data, segmentNum,i)
        Data[segmentNum].intDist[i] = round(dsdh*dh,6)
        Data[segmentNum].intTime[i] = round(dtdh*dh,6)
        Data[segmentNum].intFuel[i] = round(-dwdh*dh,6)

        Data[segmentNum].segDist += Data[segmentNum].intDist[i]
        Data[segmentNum].segTime += Data[segmentNum].intTime[i]
        Data[segmentNum].segFuel += Data[segmentNum].intFuel[i]

        if i < Data[segmentNum].nInt-1:
            Data[segmentNum].intWeight[i+1] = Data[segmentNum].intWeight[i] - Data[segmentNum].intFuel[i]
            velocity += dvdh*dh

    Data[segmentNum].Weight[1] = round(Data[segmentNum].intWeight[0]-Data[segmentNum].segFuel,6)


def loiterRange(Data, segmentNum):
    loiterTime = Data[segmentNum].segTime
    dt = loiterTime/Data[segmentNum].nInt

    Data[segmentNum].intWeight[0] = Data[segmentNum].Weight[0]

    velocity = Data[segmentNum].Velocity[0]
    rho, soundspeed = interval.atmospherics(Data, segmentNum,0)
    Mach = velocity/soundspeed

    Data[segmentNum].segDist = 0
    Data[segmentNum].segFuel = 0

    for i in range(Data[segmentNum].nInt):
        Data[segmentNum].intMach[i] = Mach
        Data[segmentNum].intVelocity[i] = velocity
        Data[segmentNum].intAltitude[i] = Data[segmentNum].Altitude[0]
        dsdt, dwdt = interval.computeLoiter_dt(Data, segmentNum,i, rho)

        Data[segmentNum].intDist[i] = round(dsdt*dt,6)
        Data[segmentNum].intTime[i] = round(dt,6)
        Data[segmentNum].intFuel[i] = round(-dwdt*dt,6)

        Data[segmentNum].segDist += 0        
        Data[segmentNum].segFuel += Data[segmentNum].intFuel[i]


        if i < Data[segmentNum].nInt-1:
            Data[segmentNum].intWeight[i+1] = Data[segmentNum].intWeight[i] - Data[segmentNum].intFuel[i]

    Data[segmentNum].Weight[1] = round(Data[segmentNum].intWeight[0]-Data[segmentNum].segFuel,6)



def TGroundRollRange(Data, segmentNum):
    # set the stall speed here, 215mph, convert unit: m/s
    vStall = 95.963 #- 34.029
    dv = vStall/(Data[segmentNum].nInt-1)
    dthrottle = (1.0 - Data[segmentNum].throttle[0])/Data[segmentNum].nInt
    
    Data[segmentNum].intWeight[0] = Data[segmentNum].Weight[0]

    Data[segmentNum].segDist = 0
    Data[segmentNum].segTime = 0
    Data[segmentNum].segFuel = 0 

    for i in range(Data[segmentNum].nInt):
        Data[segmentNum].intVelocity[i] = i*dv #+ 34.029
        Data[segmentNum].throttle[i] = Data[segmentNum].throttle[0] #+ i*dthrottle
        dsdv, dtdv, dwdv = interval.computeTGroundRoll_dv(Data, segmentNum, i)

        Data[segmentNum].intDist[i] = round(dsdv*dv,6)
        Data[segmentNum].intTime[i] = round(dtdv*dv,6)
        Data[segmentNum].intFuel[i] = round(-dwdv*dv,6)

        Data[segmentNum].segDist += Data[segmentNum].intDist[i]
        Data[segmentNum].segTime += Data[segmentNum].intTime[i]
        Data[segmentNum].segFuel += Data[segmentNum].intFuel[i]

        if i < Data[segmentNum].nInt-1:
            Data[segmentNum].intWeight[i+1] = Data[segmentNum].intWeight[i] - Data[segmentNum].intFuel[i]

    Data[segmentNum].Weight[1] = round(Data[segmentNum].intWeight[0] - Data[segmentNum].segFuel,6)
    Data[segmentNum].Mach[1] = round(Data[segmentNum].intMach[Data[segmentNum].nInt-1], 6)

def LGroundRollRange(Data, segmentNum):
    vStall = 35
    dv = -vStall/Data[segmentNum].nInt

    Data[segmentNum].intWeight[0] = Data[segmentNum].Weight[0]
    
    Data[segmentNum].segDist = 0
    Data[segmentNum].segTime = 0
    Data[segmentNum].segFuel = 0 

    for i in range(Data[segmentNum].nInt):
        Data[segmentNum].intVelocity[i] = vStall + i*dv
        dsdv, dtdv, dwdv = interval.computeLGroundRoll_dv(Data, segmentNum,i)

        Data[segmentNum].intAltitude[i] = Data[segmentNum].Altitude[0]

        Data[segmentNum].intDist[i] = round(dsdv*dv,6)
        Data[segmentNum].intTime[i] = round(dtdv*dv,6)
        Data[segmentNum].intFuel[i] = round(-dwdv*dv,6)

        Data[segmentNum].segDist += Data[segmentNum].intDist[i]
        Data[segmentNum].segTime += Data[segmentNum].intTime[i]
        Data[segmentNum].segFuel += Data[segmentNum].intFuel[i]

        if i < Data[segmentNum].nInt-1:
            Data[segmentNum].intWeight[i+1] = Data[segmentNum].intWeight[i] - Data[segmentNum].intFuel[i]

    Data[segmentNum].Weight[1] = round(Data[segmentNum].Weight[0] - Data[segmentNum].segFuel,6)
    Data[segmentNum].Mach[1] = round(Data[segmentNum].intMach[Data[segmentNum].nInt-1], 6)

def levelClimbRange(Data, segmentNum):
    dv = (Data[segmentNum].Velocity[1]-Data[segmentNum].Velocity[0])/Data[segmentNum].nInt
    
    Data[segmentNum].intWeight[0] = Data[segmentNum].Weight[0]

    Data[segmentNum].segDist = 0
    Data[segmentNum].segTime = 0
    Data[segmentNum].segFuel = 0 

    for i in range(Data[segmentNum].nInt): 
        Data[segmentNum].intAltitude[i] = Data[segmentNum].Altitude[0]
        Data[segmentNum].intVelocity[i] = i*dv+Data[segmentNum].Velocity[0]
        dsdv, dtdv, dwdv = interval.level_dv(Data, segmentNum, i)

        Data[segmentNum].intDist[i] = round(dsdv*dv,6)
        Data[segmentNum].intTime[i] = round(dtdv*dv,6)
        Data[segmentNum].intFuel[i] = round(-dwdv*dv,6)

        Data[segmentNum].segDist += Data[segmentNum].intDist[i]
        Data[segmentNum].segTime += Data[segmentNum].intTime[i]
        Data[segmentNum].segFuel += Data[segmentNum].intFuel[i]

        if i < Data[segmentNum].nInt-1:
            Data[segmentNum].intWeight[i+1] = Data[segmentNum].intWeight[i] - Data[segmentNum].intFuel[i]

    Data[segmentNum].Weight[1] = round(Data[segmentNum].intWeight[0] - Data[segmentNum].segFuel,6)
    # Data[segmentNum].Mach[1] = round(Data[segmentNum].intMach[Data[segmentNum].nInt-1], 6)



#%%    
import numpy as np
def printCheck(Data,segmentNum):
    print('----------------------')
    print(Data[segmentNum].segType,'segment')
    print('Fuel burn: ', Data[segmentNum].segFuel/9.8,'kg')
    print('Distance:  ',Data[segmentNum].segDist*0.000621371,'nm',Data[segmentNum].segDist,'m')
    print('Time:      ',Data[segmentNum].segTime,'s',Data[segmentNum].segTime/60,'min')
    x = PrettyTable()
    x.field_names=['Time','Alt (ft)','Dist','Burnoff','Weight','Lift','Velocity','Mach','Thrust','Drag','RC','gamma','dvdh','Alpha','CL','CD','throttle','TSFC','Fuel Flow']
    for i in range(Data[segmentNum].nInt):
        try:
            x.add_row([round(Data[segmentNum].intTime[i],1),round(Data[segmentNum].intAltitude[i]*3.28084,1),round(Data[segmentNum].intDist[i],2),
            round(Data[segmentNum].intFuel[i],1),round(Data[segmentNum].intWeight[i],1),round(Data[segmentNum].L[i],1),
            round(Data[segmentNum].intVelocity[i],1),round(Data[segmentNum].intMach[i],2),round(Data[segmentNum].T[i],1),round(Data[segmentNum].D[i],1),
            round(Data[segmentNum].RC[i]*196.85,2),round(Data[segmentNum].gamma[i]/np.pi*180,2),round(Data[segmentNum].dvdh[i],3),round(Data[segmentNum].alpha[i]/np.pi*180,2),
            round(Data[segmentNum].CL[i],3),round(Data[segmentNum].CD[i],5),round(Data[segmentNum].throttle[i],5),round(Data[segmentNum].TSFC[i]*1e5,3),round(Data[segmentNum].T[i]*Data[segmentNum].TSFC[i]*3600/9.8,3)])
        except AttributeError:
            x.add_row([round(Data[segmentNum].intTime[i],1),round(Data[segmentNum].intAltitude[i]*3.28084,1),round(Data[segmentNum].intDist[i],2),
            round(Data[segmentNum].intFuel[i],1),round(Data[segmentNum].intWeight[i],1),round(Data[segmentNum].L[i],1),
            round(Data[segmentNum].intVelocity[i],1),round(Data[segmentNum].intMach[i],2),round(Data[segmentNum].T[i],1),round(Data[segmentNum].D[i],1),
            0,0,0,round(Data[segmentNum].alpha[i]/np.pi*180,2),
            round(Data[segmentNum].CL[i],3),round(Data[segmentNum].CD[i],5),round(Data[segmentNum].throttle[i],3),round(Data[segmentNum].TSFC[i]*1e5,5),round(Data[segmentNum].T[i]*Data[segmentNum].TSFC[i]*3600/9.8,3)])

    print(x)
#%%
