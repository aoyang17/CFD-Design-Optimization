"""
The script runs the GMM process on QAR data
"""

import glob
import ast
import os
import pandas as pd
import numpy as np
import seaborn as sns
import tensorflow as tf

from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.mixture import GaussianMixture
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import davies_bouldin_score
from matplotlib.colors import Normalize

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib.colors import LogNorm, Normalize

plt.rc('font',family='Times New Roman')
font1 = {'family': 'Times New Roman', 'weight': 'normal','size': 20}
font2 = {'family': 'Times New Roman', 'weight': 'normal','size': 50}

raw = np.array(
    [
        [
            2.000000000000000000e00,
            4.500000000000000111e-01,
            1.536799999999999972e-02,
            3.674239999999999728e-01,
            5.592279999999999474e-01,
            -1.258039999999999992e-01,
            -1.248699999999999984e-02,
        ],
        [
            3.500000000000000000e00,
            4.500000000000000111e-01,
            1.985100000000000059e-02,
            4.904470000000000218e-01,
            7.574600000000000222e-01,
            -1.615260000000000029e-01,
            8.987000000000000197e-03,
        ],
        [
            5.000000000000000000e00,
            4.500000000000000111e-01,
            2.571000000000000021e-02,
            6.109189999999999898e-01,
            9.497949999999999449e-01,
            -1.954619999999999969e-01,
            4.090900000000000092e-02,
        ],
        [
            6.500000000000000000e00,
            4.500000000000000111e-01,
            3.304200000000000192e-02,
            7.266120000000000356e-01,
            1.131138999999999895e00,
            -2.255890000000000117e-01,
            8.185399999999999621e-02,
        ],
        [
            8.000000000000000000e00,
            4.500000000000000111e-01,
            4.318999999999999923e-02,
            8.247250000000000414e-01,
            1.271487000000000034e00,
            -2.397040000000000004e-01,
            1.217659999999999992e-01,
        ],
        [
            0.000000000000000000e00,
            5.799999999999999600e-01,
            1.136200000000000057e-02,
            2.048760000000000026e-01,
            2.950280000000000125e-01,
            -7.882100000000000217e-02,
            -2.280099999999999835e-02,
        ],
        [
            1.500000000000000000e00,
            5.799999999999999600e-01,
            1.426000000000000011e-02,
            3.375619999999999732e-01,
            5.114130000000000065e-01,
            -1.189420000000000061e-01,
            -1.588200000000000028e-02,
        ],
        [
            3.000000000000000000e00,
            5.799999999999999600e-01,
            1.866400000000000003e-02,
            4.687450000000000228e-01,
            7.240400000000000169e-01,
            -1.577669999999999906e-01,
            3.099999999999999891e-03,
        ],
        [
            4.500000000000000000e00,
            5.799999999999999600e-01,
            2.461999999999999952e-02,
            5.976639999999999731e-01,
            9.311709999999999710e-01,
            -1.944160000000000055e-01,
            3.357500000000000068e-02,
        ],
        [
            6.000000000000000000e00,
            5.799999999999999600e-01,
            3.280700000000000283e-02,
            7.142249999999999988e-01,
            1.111707999999999918e00,
            -2.205870000000000053e-01,
            7.151699999999999724e-02,
        ],
        [
            0.000000000000000000e00,
            6.800000000000000488e-01,
            1.138800000000000055e-02,
            2.099310000000000065e-01,
            3.032230000000000203e-01,
            -8.187899999999999345e-02,
            -2.172699999999999979e-02,
        ],
        [
            1.500000000000000000e00,
            6.800000000000000488e-01,
            1.458699999999999927e-02,
            3.518569999999999753e-01,
            5.356630000000000003e-01,
            -1.257649999999999879e-01,
            -1.444800000000000077e-02,
        ],
        [
            3.000000000000000000e00,
            6.800000000000000488e-01,
            1.952800000000000022e-02,
            4.924879999999999813e-01,
            7.644769999999999621e-01,
            -1.678040000000000087e-01,
            6.023999999999999841e-03,
        ],
        [
            4.500000000000000000e00,
            6.800000000000000488e-01,
            2.666699999999999973e-02,
            6.270339999999999803e-01,
            9.801630000000000065e-01,
            -2.035240000000000105e-01,
            3.810000000000000192e-02,
        ],
        [
            6.000000000000000000e00,
            6.800000000000000488e-01,
            3.891800000000000120e-02,
            7.172730000000000494e-01,
            1.097855999999999943e00,
            -2.014620000000000022e-01,
            6.640000000000000069e-02,
        ],
        [
            0.000000000000000000e00,
            7.500000000000000000e-01,
            1.150699999999999987e-02,
            2.149069999999999869e-01,
            3.115740000000000176e-01,
            -8.498999999999999611e-02,
            -2.057700000000000154e-02,
        ],
        [
            1.250000000000000000e00,
            7.500000000000000000e-01,
            1.432600000000000019e-02,
            3.415969999999999840e-01,
            5.199390000000000400e-01,
            -1.251009999999999900e-01,
            -1.515400000000000080e-02,
        ],
        [
            2.500000000000000000e00,
            7.500000000000000000e-01,
            1.856000000000000011e-02,
            4.677589999999999804e-01,
            7.262499999999999512e-01,
            -1.635169999999999957e-01,
            3.989999999999999949e-04,
        ],
        [
            3.750000000000000000e00,
            7.500000000000000000e-01,
            2.472399999999999945e-02,
            5.911459999999999493e-01,
            9.254930000000000101e-01,
            -1.966150000000000120e-01,
            2.524900000000000061e-02,
        ],
        [
            5.000000000000000000e00,
            7.500000000000000000e-01,
            3.506800000000000195e-02,
            7.047809999999999908e-01,
            1.097736000000000045e00,
            -2.143069999999999975e-01,
            5.321300000000000335e-02,
        ],
        [
            0.000000000000000000e00,
            8.000000000000000444e-01,
            1.168499999999999921e-02,
            2.196390000000000009e-01,
            3.197160000000000002e-01,
            -8.798200000000000465e-02,
            -1.926999999999999894e-02,
        ],
        [
            1.250000000000000000e00,
            8.000000000000000444e-01,
            1.481599999999999931e-02,
            3.553939999999999877e-01,
            5.435950000000000504e-01,
            -1.317419999999999980e-01,
            -1.345599999999999921e-02,
        ],
        [
            2.500000000000000000e00,
            8.000000000000000444e-01,
            1.968999999999999917e-02,
            4.918299999999999894e-01,
            7.669930000000000359e-01,
            -1.728079999999999894e-01,
            3.756999999999999923e-03,
        ],
        [
            3.750000000000000000e00,
            8.000000000000000444e-01,
            2.785599999999999882e-02,
            6.324319999999999942e-01,
            9.919249999999999456e-01,
            -2.077100000000000057e-01,
            3.159800000000000109e-02,
        ],
        [
            5.000000000000000000e00,
            8.000000000000000444e-01,
            4.394300000000000289e-02,
            7.650689999999999991e-01,
            1.188355999999999968e00,
            -2.332680000000000031e-01,
            5.645000000000000018e-02,
        ],
        [
            0.000000000000000000e00,
            8.299999999999999600e-01,
            1.186100000000000002e-02,
            2.232899999999999885e-01,
            3.261100000000000110e-01,
            -9.028400000000000314e-02,
            -1.806500000000000120e-02,
        ],
        [
            1.000000000000000000e00,
            8.299999999999999600e-01,
            1.444900000000000004e-02,
            3.383419999999999761e-01,
            5.161710000000000464e-01,
            -1.279530000000000112e-01,
            -1.402400000000000001e-02,
        ],
        [
            2.000000000000000000e00,
            8.299999999999999600e-01,
            1.836799999999999891e-02,
            4.554270000000000262e-01,
            7.082190000000000429e-01,
            -1.642339999999999911e-01,
            -1.793000000000000106e-03,
        ],
        [
            3.000000000000000000e00,
            8.299999999999999600e-01,
            2.466899999999999996e-02,
            5.798410000000000508e-01,
            9.088819999999999677e-01,
            -2.004589999999999983e-01,
            1.892900000000000138e-02,
        ],
        [
            4.000000000000000000e00,
            8.299999999999999600e-01,
            3.700400000000000217e-02,
            7.012720000000000065e-01,
            1.097366000000000064e00,
            -2.362420000000000075e-01,
            3.750699999999999867e-02,
        ],
        [
            0.000000000000000000e00,
            8.599999999999999867e-01,
            1.224300000000000041e-02,
            2.278100000000000125e-01,
            3.342720000000000136e-01,
            -9.307600000000000595e-02,
            -1.608400000000000107e-02,
        ],
        [
            1.000000000000000000e00,
            8.599999999999999867e-01,
            1.540700000000000056e-02,
            3.551839999999999997e-01,
            5.433130000000000459e-01,
            -1.364730000000000110e-01,
            -1.162200000000000039e-02,
        ],
        [
            2.000000000000000000e00,
            8.599999999999999867e-01,
            2.122699999999999934e-02,
            4.854620000000000046e-01,
            7.552919999999999634e-01,
            -1.817850000000000021e-01,
            1.070999999999999903e-03,
        ],
        [
            3.000000000000000000e00,
            8.599999999999999867e-01,
            3.178899999999999781e-02,
            6.081849999999999756e-01,
            9.510380000000000500e-01,
            -2.252020000000000133e-01,
            1.540799999999999982e-02,
        ],
        [
            4.000000000000000000e00,
            8.599999999999999867e-01,
            4.744199999999999806e-02,
            6.846989999999999466e-01,
            1.042564000000000046e00,
            -2.333600000000000119e-01,
            2.035400000000000056e-02,
        ],
    ]
)


long_haul = pd.read_csv('./QARdata/long_haul_data.csv')
medium_haul = pd.read_csv('./QARdata/medium_haul_data.csv')
short_haul = pd.read_csv('./QARdata/short_haul_data.csv')

short_medium = pd.concat([short_haul, medium_haul])
Hybrid = pd.concat([short_haul,medium_haul,long_haul])


def pandas_drop(data):
    result = data.drop(data[(data['mach']>0.88) | (data['mach']<0.6)].index)
    result = result.drop(result[(result['alt']>41338.583) | (result['alt']<9842.52)].index)
    result = result.drop(result[(result['aoa']>3.5) | (result['aoa']<0.5)].index)

    # result = data.drop(data[(data['mach']>0.88) | (data['mach']<0.8)].index)
    # result = result.drop(result[(result['alt']>41338.583) | (result['alt']<9842.52)].index)
    # result = result.drop(result[(result['aoa']>3.5) | (result['aoa']<0.5)].index)
    return result

def panda_filter(pd_haul):
    pd_haul = pd_haul[['mach','aoa','alt']]
    data = pd_haul[pd_haul.replace([np.inf, -np.inf], np.nan).notnull().all(axis=1)] 
    data = data.dropna(how = 'all') 
    return data

def panda_cruise_filter(data):
    data = data.drop(data[(data['mach']>0.88) | (data['mach']<0.77)].index)
    data = data.drop(data[(data['aoa']>3.02) | (data['aoa']<1.83)].index)
    data = data.drop(data[(data['alt']>41338.583) | (data['alt']<27790)].index)
    return data

def K_means(df, scaler, n_clusters):

    # scaler = MinMaxScaler()
    df[['alt']] = df[['alt']] * 0.3048
    scale = scaler.fit_transform(df[['mach', 'aoa', 'alt']])
    df_scale = pd.DataFrame(scale, columns = ['mach','aoa', 'alt']);
    df_scale.head(5)

    kmeans = KMeans(init='k-means++', n_clusters=n_clusters, n_init=1)
    kmeans.fit(df_scale)

    value = scaler.inverse_transform(kmeans.cluster_centers_)

    k_means_cluster_data = {
        'mach':value[:, 0],
        'aoa':value[:, 1],
        'alt':value[:, 2],
    }
    k_means_pandas = pd.DataFrame(k_means_cluster_data)
    k_means_pandas.to_csv("K_means_points_clusters.csv")
    return kmeans

# def GMM(data, n_cluster, file_name):
#     data[['alt']] = data[['alt']] * 0.3048
#     scaler = MinMaxScaler()
#     scale = scaler.fit_transform(data[['mach', 'aoa', 'alt', 'CL']])
#     df_scale = pd.DataFrame(scale, columns = ['mach','aoa', 'alt', 'CL'])
#     df_scale.head(5)
    
#     gmm = GaussianMixture(n_components=n_cluster, init_params="kmeans", tol=1e-9, max_iter=0, covariance_type='full').fit(df_scale)

#     value = scaler.inverse_transform(gmm.means_)
#     gmm_para = pd.DataFrame()
#     gmm_para['mach_means'] = value[:, 0]
#     gmm_para['aoa_means'] = value[:, 1]
#     gmm_para['alt_means'] = value[:, 2]
#     gmm_para['CL_means'] = value[:, 3]
#     gmm_para['weights'] = gmm.weights_
#     # array_dict = {'_weights':gmm.weights_, '_means':gmm.means_}
#     gmm_para.to_csv(file_name)
#     return gmm, gmm_para

def GMM(data, n_cluster, file_name):
 
    gmm = GaussianMixture(n_components=n_cluster, init_params="kmeans", tol=1e-9, max_iter=0, covariance_type='full').fit(data)
    gmm_para = pd.DataFrame()
    gmm_para['mach_means'] = gmm.means_[:, 0]
    gmm_para['aoa_means'] = gmm.means_[:, 1]
    gmm_para['alt_means'] = gmm.means_[:, 2]
    gmm_para['CL_means'] = gmm.means_[:, 3]
    gmm_para['weights'] = gmm.weights_
    # array_dict = {'_weights':gmm.weights_, '_means':gmm.means_}
    gmm_para.to_csv(file_name)
    return gmm, gmm_para

def gmm_bic_score(estimator, X):
    """Callable to pass to GridSearchCV that will use the BIC score."""
    # Make it negative since GridSearchCV expects a score to maximize
    return -estimator.aic(X)

def Fuel_quantity(data):
    Initial_fuel = data['Total Fuel Quantity (kg)'].unique().max()  
    Final_fuel = data['Total Fuel Quantity (kg)'].unique().min()      
    fuel_cost = Initial_fuel - Final_fuel
    
    key = data['Phase of Flight'].unique()
    
    fuel_seg = []
    
    for i in key:
        min_fuel_seg = data.loc[data['Phase of Flight'] == key[i]]['Total Fuel Quantity (kg)'].dropna(axis=0,how='any').min()
        max_fuel_seg = data.loc[data['Phase of Flight'] == key[i]]['Total Fuel Quantity (kg)'].dropna(axis=0,how='any').max()
        fuel_cost_segment = max_fuel_seg - min_fuel_seg
        fuel_seg.append(fuel_cost_segment)
        
    
    
    # print(key.shape)
    
    a = data.loc[data['Phase of Flight'] == 'F) Climb']['Total Fuel Quantity (kg)'].dropna(axis=0,how='any').min() 
    b = data.loc[data['Phase of Flight'] == 'F) Climb']['Total Fuel Quantity (kg)'].dropna(axis=0,how='any').max() 
    # c = a['Total Fuel Quantity (kg)'].unique().min()  
    # b = data['F) Climb']
    # d = b['Total Fuel Quantity (kg)'].unique().max()  
    # print(Initial_fuel)
    # print(Final_fuel)
    # print("**************")
    # print(a)
    # print(b)    
    return

def get_rans_crm_wing(raw_data):
    # data structure:
    # alpha, mach, cd, cl, cmx, cmy, cmz

    deg2rad = np.pi / 180.0

    data = raw_data
    raw = data.drop(data[(data['mach']>0.88) | (data['mach']<0.6)].index)
    raw = raw.drop(raw[(raw['alpha']>3.5) | (raw['alpha']<0.5)].index)

    xt = np.array(raw[['alpha', 'mach']])
    yt = np.array(raw[['cd', 'cl']])
    xlimits = np.array([[0.5, 3.5], [0.6, 0.88]])

    xt[:, 0] *= deg2rad
    xlimits[0, :] *= deg2rad

    return xt, yt, xlimits

def nonlinear_function(x):
    return 1 / (1 + np.exp(-x))

def plot_rans_crm_wing(xt, yt, limits, gmm_para, interp, name):

    rad2deg = 180.0 / np.pi

    num = 500
    num_a = 50
    num_M = 50

    x = np.zeros((num, 2))
    colors = ["b", "g", "r", "c", "m", "k", "y"]

    nrow = 3
    ncol = 2

    fig, axs = plt.subplots(1, 1, figsize=(26, 18), dpi=180)
    plt.rcParams['font.family'] = 'Times New Roman'
    # -----------------------------------------------------------------------------

    legend_entries = []

    # alpha_sweep = np.linspace(0.5, 3.5, num)
    x = np.zeros((num_a, num_M, 2))
    x[:, :, 0] = np.outer(np.linspace(0.5, 3.5, num_a), np.ones(num_M)) / rad2deg
    x[:, :, 1] = np.outer(np.ones(num_a), np.linspace(0.6, 0.88, num_M))
    CD = interp.predict_values(x.reshape((num_a * num_M, 2)))[:, 0].reshape(
        (num_a, num_M)
    )
    CL = interp.predict_values(x.reshape((num_a * num_M, 2)))[:, 1].reshape(
        (num_a, num_M)
    )

    # axs.plot(xt[:, 1], xt[:, 0] * rad2deg, "o")
    CS = axs.contour(x[:, :, 1], x[:, :, 0] * rad2deg, CL, 20)
    pcm2 = axs.pcolormesh(
        x[:, :, 1],
        x[:, :, 0] * rad2deg,
        CL,
        cmap=plt.get_cmap("rainbow"),
        shading="auto",
    )
    cbar = fig.colorbar(pcm2, ax=axs)
    cbar.ax.set_ylabel(r'$C_L$',fontsize=30)
    cbar.ax.tick_params(labelsize=25)

    axs.set(xlabel="Mach number", ylabel="alpha (deg)")
    axs.tick_params(axis='both', which='major', labelsize=30)
    axs.set_xlabel('Mach number', font2)
    axs.set_ylabel('Angle of attack ($^\circ$)', font2)
    axs.tick_params(axis='both', which='major', labelsize=30)
    axs.clabel(CS, inline=1, fontsize=20)
    axs.set_title(r'$C_L$',font2)
    # axs.scatter(value_k[:,0], value_k[:,1])
    scaler = MinMaxScaler(feature_range=(1, 5))
    w_values = scaler.fit_transform(np.array(gmm_para['weights']).reshape(-1, 1)).flatten()
    w_values = [x * 200 for x in w_values]
    
    # scatter = axs.scatter(gmm_para["mach_means"], gmm_para["aoa_means"], s= 1000 * norm(gmm_para['weights']), c="orangered", alpha=1)
    scatter = axs.scatter(gmm_para["mach_means"], gmm_para["aoa_means"], s= w_values, c="red", alpha=1)

    # handles, labels = scatter.legend_elements(prop="sizes")
    # print(labels)
    
    # selected_indices = [1, 3, 5, 7, 9]  
    # selected_labels = [labels[i] for i in selected_indices] 
    # selected_handles = [handles[i] for i in selected_indices]
    # try:
    #     selected_labels = [str(int(label) // 1000) for label in selected_labels]
    # except ValueError:
    #     selected_labels = [label.replace('$\\mathdefault{', '').replace('}$', '') for label in selected_labels]

    # legend = axs.legend(selected_handles, selected_labels, loc="lower left", title="Sizes", prop = font1)
    
    # legend.get_title().set_fontsize(25)
    
    # legend.get_texts()[0].set_text('0.02')
    # legend.get_texts()[1].set_text('0.04')
    # legend.get_texts()[2].set_text('0.06')
    # legend.get_texts()[3].set_text('0.08')
    # legend.get_texts()[4].set_text('0.1')


    # legend.legendHandles[0].set_color('red')
    # legend.legendHandles[1].set_color('red')
    # legend.legendHandles[2].set_color('red')
    # legend.legendHandles[3].set_color('red')
    # legend.legendHandles[4].set_color('red')

    plt.savefig('CL_contour_with_gmm%s.pdf'%name,bbox_inches='tight',dpi=fig.dpi,pad_inches=0.2)
    # plt.savefig('CL_contour_with_gmm%s.png'%name,bbox_inches='tight',dpi=fig.dpi,pad_inches=0.2)
    
    plt.show()


def plot_mach_cl_distribution(df,name):
    # plt.rc('font', family='serif',size=10)
    fig, ax = plt.subplots(figsize = (12, 9), dpi=180)
    plt.rcParams['font.family'] = 'Times New Roman'
    font2 = {'family': 'Times New Roman', 'weight': 'normal','size': 30}
    ax.scatter(df['mach'].values, df['CL'].values, s=df['weights'].values, alpha=0.5)

    ax.ticklabel_format(style='sci', scilimits=(-1,2), axis='both')
    ax.set_xlabel('Mach', font2)
    ax.set_ylabel(r'$C_{L}$', font2)

    # plt.savefig('mach_cl_distribution%s.png'%name,bbox_inches='tight',dpi=fig.dpi,pad_inches=0.2)
    plt.savefig('mach_cl_distribution%s.pdf'%name,bbox_inches='tight',dpi=fig.dpi,pad_inches=0.2)

def plot_gmm_clusters_within_distribution(gmm_para, full_data, name):

    fig, axs = plt.subplots(1, 1, figsize=(26, 18), dpi=180)
    plt.rcParams['font.family'] = 'Times New Roman'
    font2 = {'family': 'Times New Roman', 'weight': 'normal','size': 50}
    font1 = {'family': 'Times New Roman', 'weight': 'normal','size': 20}

    scaler = MinMaxScaler(feature_range=(1, 3))
    w_values = scaler.fit_transform(np.array(gmm_para['weights']).reshape(-1, 1)).flatten()
    w_values = [x * 500 for x in w_values]
    
    h = axs.hist2d(full_data["mach"], full_data["aoa"], norm=LogNorm(),density=True,bins=30,cmap='viridis')
    scatter = axs.scatter(gmm_para["mach_means"], gmm_para["aoa_means"], s= w_values, c="orangered", alpha=1) 
    
    handles, labels = scatter.legend_elements(prop="sizes")
    print("*************")
    print(handles)
    print(labels)    
    
    # selected_indices = [1, 3, 5, 7, 9]  
    # selected_labels = [labels[i] for i in selected_indices] 
    # selected_handles = [handles[i] for i in selected_indices]


    
    # try:
    #     selected_labels = [str(int(label) // 1000) for label in selected_labels]
    # except ValueError:
    #     selected_labels = [label.replace('$\\mathdefault{', '').replace('}$', '') for label in selected_labels]

    # # selected_labels = [str(int(label) // 1000) for label in selected_labels]
    
    # legend = axs.legend(selected_handles, selected_labels, loc="lower left", title="Sizes", prop = font1)
    
    # legend.get_title().set_fontsize(25)
    # legend.get_texts()[0].set_text('0.02')
    # legend.get_texts()[1].set_text('0.04')
    # legend.get_texts()[2].set_text('0.06')
    # legend.get_texts()[3].set_text('0.08')
    # legend.get_texts()[4].set_text('0.1')


    # legend.legendHandles[0].set_color('red')
    # legend.legendHandles[1].set_color('red')
    # legend.legendHandles[2].set_color('red')
    # legend.legendHandles[3].set_color('red')
    # legend.legendHandles[4].set_color('red')


    # ax.plot([0],[0], marker="o", markersize=10)
    # axs[0].ticklabel_format(style='sci', scilimits=(-1,2), axis='both', labelsize=30)
    axs.tick_params(axis='both', which='major', labelsize=30)
    axs.set_xlabel('Mach number', font2)
    axs.set_ylabel('Angle of attack ($^\circ$)', font2)

    cbar = plt.colorbar(h[3], ax=axs)
    cbar.ax.set_ylabel('LogNorm of flight condition counts',fontsize=30)
    cbar.ax.tick_params(labelsize=25)
    # cbar.ax.set_yticklabels(fontdict=font1,)

    # for text in legend.get_texts():
    #     text.set_fontsize(20)

    # # 调整图例的大小
    # plt.gcf().set_size_inches(6, 4)

    plt.savefig('GMM_full_plot_distribution%s.pdf'%name,bbox_inches='tight',dpi=fig.dpi,pad_inches=0.2)
    # plt.savefig('GMM_full_plot_distribution%s.png'%name,bbox_inches='tight',dpi=fig.dpi,pad_inches=0.2)
    plt.show()


if __name__ == "__main__":

    import matplotlib.pyplot as plt
    from matplotlib.pyplot import figure

    from smt.surrogate_models import RMTB
    from sklearn.decomposition import PCA
    # GMM based on QAR data

    Hybrid = pandas_drop(Hybrid)
    Hybrid = panda_filter(Hybrid)
    # Hybrid = panda_cruise_filter(Hybrid)
    # Hybrid_sample = Hybrid[:1000]
    Hybrid_sample = Hybrid.sample(n=10000,random_state=None,axis=0)
    # print(Hybrid_sample)
    CRM_2D_raw = pd.read_csv("CRM_raw_data.csv")
    xt, yt, xlimits = get_rans_crm_wing(CRM_2D_raw)

    interp = RMTB(
        num_ctrl_pts=20, xlimits=xlimits, nonlinear_maxiter=100, energy_weight=1e-12
    )
    interp.set_training_values(xt, yt)
    interp.train()

    rad2deg = 180.0 / np.pi


    hybrid_x_sample = Hybrid_sample[['aoa','mach']].to_numpy()
    hybrid_x_sample[:, 0] /= rad2deg
    CD_sample = interp.predict_values(hybrid_x_sample)[:, 0]
    CL_sample = interp.predict_values(hybrid_x_sample)[:, 1]

    hybrid_x_sample_para = pd.DataFrame()
    hybrid_x_sample_para['mach'] =  Hybrid_sample[['mach']]
    hybrid_x_sample_para['aoa'] = Hybrid_sample[['aoa']]
    hybrid_x_sample_para['alt'] = Hybrid_sample[['alt']] * 0.3048
    hybrid_x_sample_para['CL'] = CL_sample

    name = '_mission_40'
    n_clusters = 40
    hybrid_x_sample_para.to_csv('hybrid_full_data_extend_%s.csv'%name)


    
    hybrid_GMM_data_x = hybrid_x_sample_para[['mach','CL','aoa','alt']]
    pca = PCA(n_components=4)

    # 对数据进行维度变换
    # hybrid_GMM_data = pca.fit_transform(hybrid_GMM_data_x)
    hybrid_GMM_data = hybrid_GMM_data_x
    gmm_with_pca = GaussianMixture(n_components=n_clusters)

    gmm_with_pca.fit(hybrid_GMM_data)
    # gmm_with_pca, gmm_para = GMM(hybrid_GMM_data, n_clusters, 'pca_gmm')


    # labels_with_pca = gmm_with_pca.predict(hybrid_GMM_data)
    # cluster_centers_pca = pca.inverse_transform(gmm_with_pca.means_)
    # cluster_weights_pca = gmm_with_pca.weights_

    # labels_with_pca = gmm_with_pca.predict(hybrid_GMM_data)
    cluster_centers_pca = gmm_with_pca.means_
    cluster_weights_pca = gmm_with_pca.weights_

    print(cluster_centers_pca)
    print(cluster_weights_pca)
    
    data = {
        'mach': cluster_centers_pca[:, 0],
        'cl': cluster_centers_pca[:, 1],
        'aoa': cluster_centers_pca[:, 2],
        'alt': cluster_centers_pca[:, 3],
        'w':cluster_weights_pca,
    }
    df = pd.DataFrame(data)

    # 将 DataFrame 存储到 CSV 文件
    df.to_csv('Points_csv/GMM_entire_%spts_2.csv'%n_clusters, index=False)

    
    # hybrid_GMM, gmm_para = GMM(hybrid_GMM_data, n_clusters)
    
    
    
    
    # full_data = pd.read_csv("full_data_distribution.csv")
    # plot_gmm_clusters_within_distribution(gmm_para, full_data, name)
    
    # CRM_2D_raw = pd.read_csv("CRM_raw_data.csv")
    # xt, yt, xlimits = get_rans_crm_wing(CRM_2D_raw )
    # interp = RMTB(
    #     num_ctrl_pts=20, xlimits=xlimits, nonlinear_maxiter=100, energy_weight=1e-12
    # )
    # interp.set_training_values(xt, yt)
    # interp.train()
    # plot_rans_crm_wing(xt, yt, xlimits, gmm_para, interp, name)

    # print(gmm_with_pca.means_)
    # print(gmm_with_pca.weights_)