#%%
from smt.surrogate_models import RMTB
import numpy as np
import pandas as pd

def get_rans_crm_wing():
    # data structure:
    # upper surface a4, lower surface a3, mach number, angle of attack
    # a4 a3 mach alpha cd cl

    # data = pd.read_csv('/home/aobo/MACH-Aero/Operate_mission_ASO/Analyze_warpped_CGNS/data_driven_K_means_optimized_3rd.csv')
    # data = pd.read_csv("/home/aobo/MACH-Aero/Operate_mission_ASO/Analyze_warpped_CGNS/Optimized_wing_Kmeans.csv")
    data = pd.read_csv("./wing_aeroparameter_file/Optimized_wing_Analyze_L3_gmm_entire_20.csv")
    # data = pd.read_csv("/home/aobo/MACH-Aero/Operate_mission_ASO/Analyze_warpped_CGNS/Optimized_wing_single_pt.csv")
    # data = pd.read_csv("/home/aobo/MACH-Aero/Operate_mission_ASO/Analyze_warpped_CGNS/Optimized_wing_ninepts.csv")
    # p2-Yuan-Dell
    # Optimization-1500
    raw = np.array([data[item] for item in data.head()])
        
    deg2rad = np.pi / 180

    xt = data[['alpha','mach']].to_numpy()
    yt = data[['cl','cd']].to_numpy()
    xlimits = np.array([
    [0,8], # Angle of attack
    [0,0.86], # Mach number
    ])    
    xt[:,0] *= deg2rad
    xlimits[0, :] *= deg2rad

    
    return xt, yt, xlimits
    
xt, yt, xlimits = get_rans_crm_wing()

def calculateSurrogate(xt, yt,xlimits):

    interp = RMTB(num_ctrl_pts=20, xlimits=xlimits, nonlinear_maxiter=100, energy_weight=1e-12,print_global=True)
    interp.set_training_values(xt, yt)
    interp.train()
    return interp

surrogateA = calculateSurrogate(xt,yt,xlimits)


def SurrogateAero(x):
    cd = surrogateA._predict_values(x)[0,1]
    cl = surrogateA._predict_values(x)[0,0]
#     clNew = surrogateA._predict_values(x)[1,1]
    gradient = surrogateA._predict_derivatives(x,0)[0,0]
    
    return cl, cd, gradient



# %%
