"""
This script is used to plot Kmeans elbow
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from matplotlib.colors import LogNorm, Normalize
from sklearn.metrics.pairwise import pairwise_distances_argmin

from sklearn import preprocessing
import sklearn.cluster as cluster
import sklearn.metrics as metrics
from sklearn.preprocessing import MinMaxScaler
import seaborn as sns
from smt.surrogate_models import RMTB
import matplotlib.font_manager as fm

font_path = '/home/aobo/Operation-aware/Times New Roman.ttf'
fm.fontManager.addfont(font_path)
# prop = fm.FontProperties(fname=font_path)

prop = fm.FontProperties(fname=font_path, weight='normal', size=30)

plt.rcParams['font.family'] = prop.get_family()
plt.rcParams['font.size'] = prop.get_size()

def K_means(df, n_clusters):

    # scaler = MinMaxScaler()
    df[['alt']] = df[['alt']] * 0.3048
    scaler = MinMaxScaler()
    scale = scaler.fit_transform(df[['mach', 'aoa', 'alt']])
    df_scale = pd.DataFrame(scale, columns = ['mach','aoa', 'alt']);
    # df_scale.head(5)

    kmeans = KMeans(n_clusters=n_clusters,init='k-means++',random_state=0)
    kmeans.fit(df_scale)

    value = scaler.inverse_transform(kmeans.cluster_centers_)

    k_means_cluster_data = {
        'mach':value[:, 0],
        'aoa':value[:, 1],
        'alt':value[:, 2],
    }
    k_means_pandas = pd.DataFrame(k_means_cluster_data)
    k_means_pandas.to_csv("K_means_points_clusters.csv")
    return kmeans, k_means_pandas

#     k_means_pandas.to_csv("k_means_data_2.csv")

def plot_K_means_wss(K, wss):

    fig, ax = plt.subplots(1, figsize = (26, 18), dpi=180)

    ax.ticklabel_format(style='sci', scilimits=(-1,2), axis='both')

    font1 = {'family': 'Times New Roman', 'weight': 'normal','size': 20}
    font2 = {'family': 'Times New Roman', 'weight': 'normal','size': 30}


    ax.plot(K, wss, linestyle='-', marker='o',linewidth=5.0, markersize=20.0, markerfacecolor='black')
    # ax.set_title('Altitude with time step', font2)
    ax.ticklabel_format(style='sci', scilimits=(-1,2), axis='both')
    ax.tick_params(axis='both', which='major', labelsize=30)

    # ax.scatter(K[3],wss[3],marker='o',edgecolors='r')

    # ax.annotate('K-WSS Elbow', xy=(K[3]+1.5, wss[3]+1.5), xytext=(50, 40),
    #             arrowprops=dict(facecolor='red', edgecolor='red',
    #                             arrowstyle='->',linewidth='5'),size=30)

    ax.annotate('K-WSS Elbow Area', xy=(K[3]+1.5, wss[3]+1.5), xytext=(35, 25), color='red',fontproperties=prop, fontsize=40)

    # ax.annotate('', xy=(K[2]+1.5, wss[3]+6.5), xytext=(50, 40),
    #             arrowprops=dict(facecolor='red', edgecolor='red',
    #                             arrowstyle='->',linewidth='5'),size=30)

    rect = plt.Rectangle((17, 10), 15, 12, edgecolor='red', facecolor='none', linewidth=4)

    ax.add_patch(rect)

    ax.set_xlabel('K value', font2, fontproperties=prop, fontsize=40)
    ax.set_ylabel('WSS score', font2, fontproperties=prop, fontsize=40)

    plt.savefig('K_means_WSS_new.pdf',bbox_inches='tight',dpi=fig.dpi,pad_inches=0.2)
    plt.savefig('K_means_WSS.png',bbox_inches='tight',dpi=fig.dpi,pad_inches=0.2)
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


def plot_rans_crm_wing(xt, yt, limits, k_means_df, interp):

    rad2deg = 180.0 / np.pi

    num = 500
    num_a = 50
    num_M = 50

    x = np.zeros((num, 2))
    colors = ["b", "g", "r", "c", "m", "k", "y"]

    nrow = 3
    ncol = 2

    fig, axs = plt.subplots(1, 1, figsize=(26, 18), dpi=180)

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
    cbar.ax.set_ylabel(r'$C_{L}$',fontsize=30)
    cbar.ax.tick_params(labelsize=25)

    axs.set(xlabel="Mach number", ylabel="alpha (deg)")
    axs.tick_params(axis='both', which='major', labelsize=30)
    axs.set_xlabel('Mach number', fontproperties=prop, fontsize=40)
    axs.set_ylabel('Angle of attack ($^\circ$)', fontproperties=prop, fontsize=40)
    axs.tick_params(axis='both', which='major', labelsize=30)
    axs.clabel(CS, inline=1, fontsize=20)
    axs.set_title(r'$C_{L}$', fontproperties=prop, fontsize=40)
    # axs.scatter(value_k[:,0], value_k[:,1])
    axs.scatter(k_means_df["mach"], k_means_df["aoa"], s= 22**2, c="orangered", alpha=1)
    
    plt.savefig('CL_contour_with_K_means.pdf',bbox_inches='tight',dpi=fig.dpi,pad_inches=0.2)
    plt.savefig('CL_contour_with_K_means.png',bbox_inches='tight',dpi=fig.dpi,pad_inches=0.2)
    
    plt.show()


def plot_K_means_clusters_within_distribution(k_means_df, full_data):



    fig, axs = plt.subplots(1, 1, figsize=(26, 18), dpi=180)

    font2 = {'family': 'Times New Roman', 'weight': 'normal','size': 50}
    font1 = {'family': 'Times New Roman', 'weight': 'normal','size': 20}

    h = axs.hist2d(full_data["mach"], full_data["aoa"], norm=LogNorm(),density=True,bins=30,cmap='viridis')
    axs.scatter(k_means_df["mach"], k_means_df["aoa"], s= 22**2, c="orangered", alpha=1)      
    # ax.plot([0],[0], marker="o", markersize=10)
    # axs[0].ticklabel_format(style='sci', scilimits=(-1,2), axis='both', labelsize=30)
    axs.tick_params(axis='both', which='major', labelsize=30)
    axs.set_xlabel('Mach number', font2)
    axs.set_ylabel('Angle of attack ($^\circ$)', font2)

    cbar = plt.colorbar(h[3], ax=axs)
    cbar.ax.set_ylabel('LogNorm of flight condition counts',fontsize=30)
    cbar.ax.tick_params(labelsize=25)
    # cbar.ax.set_yticklabels(fontdict=font1,)

    plt.savefig('K_means_full_plot_distribution.pdf',bbox_inches='tight',dpi=fig.dpi,pad_inches=0.2)
    plt.savefig('K_means_full_plot_distribution.png',bbox_inches='tight',dpi=fig.dpi,pad_inches=0.2)
    plt.show()





if __name__ == '__main__':

    # df = pd.read_csv("hybrid_full_data_extend.csv")
    # # df = pd.read_csv("hybrid_full_data.csv")
    # n_clusters = 30
    # k_means, k_means_df = K_means(df, n_clusters)

    # k_means_df.to_csv("new_Kmeans_clusters.csv", k_means_df)


    cluster_list = [5, 10, 20, 30, 40, 50, 60, 70, 80]
    wss = [73, 39, 19, 13, 10, 9.5, 9.2, 9.1, 9]
    # wss = []
    # for k in cluster_list: 
    #     k_means_iter, k_means_df_iter = K_means(df, scaler, k)
    #     wss_iter = k_means_iter.inertia_
    #     wss.append(wss_iter)

    plot_K_means_wss(cluster_list, wss)

    # full_data = pd.read_csv("/home/aobo/MACH-Aero/Operate_mission_ASO/Full_data_plot/full_data_distribution.csv")

    # plot_K_means_clusters_within_distribution(k_means_df, full_data)

    # CRM_2D_raw = pd.read_csv("CRM_raw_data.csv")
    # xt, yt, xlimits = get_rans_crm_wing(CRM_2D_raw )
    # interp = RMTB(
    #     num_ctrl_pts=20, xlimits=xlimits, nonlinear_maxiter=100, energy_weight=1e-12
    # )
    # interp.set_training_values(xt, yt)
    # interp.train()
    # plot_rans_crm_wing(xt, yt, xlimits, k_means_df, interp)



# # k_means = KMeans(init='k-means++', n_clusters=20, n_init=1)
# # k_means.fit(df_scale)
# # # KMeans(n_clusters=30)
# # print(k_means.cluster_centers_)

# # value = scaler.inverse_transform(k_means.cluster_centers_)

# # k_means_cluster_data = {
# #     'mach':value[:, 0],
# #     'aoa':value[:, 1]
# # }
# # k_means_pandas = pd.DataFrame(k_means_cluster_data)
# # k_means_pandas.to_csv("k_means_data_2.csv")

# # value_k = pd.read_csv("k_means_data_2.csv").to_numpy()
# # # print(value_k[:,2])
# # # plt.scatter(value[:,0], value[:,1])
# # # plt.savefig("k_means.png")
# # # print(value_k)





# def plot_rans_crm_wing(xt, yt, limits, interp):
#     import numpy as np
#     import matplotlib

#     matplotlib.use("Agg")
#     import matplotlib.pyplot as plt

#     rad2deg = 180.0 / np.pi

#     num = 500
#     num_a = 50
#     num_M = 50

#     x = np.zeros((num, 2))
#     colors = ["b", "g", "r", "c", "m", "k", "y"]

#     nrow = 3
#     ncol = 2

#     plt.close()
#     fig, axs = plt.subplots(1, 1, figsize=(15, 15))

#     # -----------------------------------------------------------------------------

#     legend_entries = []

#     # alpha_sweep = np.linspace(0.5, 3.5, num)
#     x = np.zeros((num_a, num_M, 2))
#     x[:, :, 0] = np.outer(np.linspace(1.5, 3.5, num_a), np.ones(num_M)) / rad2deg
#     x[:, :, 1] = np.outer(np.ones(num_a), np.linspace(0.6, 0.88, num_M))
#     CD = interp.predict_values(x.reshape((num_a * num_M, 2)))[:, 0].reshape(
#         (num_a, num_M)
#     )
#     CL = interp.predict_values(x.reshape((num_a * num_M, 2)))[:, 1].reshape(
#         (num_a, num_M)
#     )

#     # axs.plot(xt[:, 1], xt[:, 0] * rad2deg, "o")
#     axs.contour(x[:, :, 1], x[:, :, 0] * rad2deg, CL, 20)
#     pcm2 = axs.pcolormesh(
#         x[:, :, 1],
#         x[:, :, 0] * rad2deg,
#         CL,
#         cmap=plt.get_cmap("rainbow"),
#         shading="auto",
#     )
#     fig.colorbar(pcm2, ax=axs)
#     axs.set(xlabel="Mach number", ylabel="alpha (deg)")
#     axs.set_title("CL")
#     # axs.scatter(value_k[:,0], value_k[:,1])
#     axs.scatter(value_k[:,1], value_k[:,2],s=120.0, edgecolor='black')
    
#     plt.savefig('CL.pdf',bbox_inches='tight',dpi=fig.dpi,pad_inches=0.2)
#     plt.show()


# xt, yt, xlimits = get_rans_crm_wing()
# interp = RMTB(
#     num_ctrl_pts=20, xlimits=xlimits, nonlinear_maxiter=100, energy_weight=1e-12
# )
# interp.set_training_values(xt, yt)
# interp.train()
# plot_rans_crm_wing(xt, yt, xlimits, interp)


# K=[5, 10, 20, 30, 40, 50, 60, 70, 80]
# wss = []

# for k in K:
#     kmeans=cluster.KMeans(n_clusters=k)
#     kmeans=kmeans.fit(df_scale)
#     wss_iter = kmeans.inertia_
#     wss.append(wss_iter)

# # plt.xlabel('K')
# # plt.ylabel('Within-Cluster-Sum of Squared Errors (WSS)')
# # plt.plot(K,np.log(wss))
# # plt.savefig("k_means_WSS_score.png")


# import matplotlib.pyplot as plt
# from matplotlib.pyplot import figure

# plt.rc('font', family='serif',size=10)

# fig, ax = plt.subplots(1, figsize = (22, 18), dpi=180)
# # fig.suptitle('Axes values are scaled individually by default')
# ax.ticklabel_format(style='sci', scilimits=(-1,2), axis='both')

# font1 = {'family': 'Times New Roman', 'weight': 'normal','size': 20}
# font2 = {'family': 'Times New Roman', 'weight': 'normal','size': 30}


# ax.plot(K, wss, linestyle='-', marker='o',linewidth=5.0,markersize=20.0, markerfacecolor='black')
# # ax.set_title('Altitude with time step', font2)
# ax.ticklabel_format(style='sci', scilimits=(-1,2), axis='both')
# ax.tick_params(axis='both', which='major', labelsize=30)

# # ax.scatter(K[3],wss[3],marker='o',edgecolors='r')

# ax.annotate('K-WSS Elbow', xy=(K[3]+1.5, wss[3]+1.5), xytext=(50, 40),
#             arrowprops=dict(facecolor='red', edgecolor='red',
#                             arrowstyle='->',linewidth='5'),size=30)


# ax.set_xlabel('K value', font2)
# ax.set_ylabel('Within-Cluster-Sum of Squared Errors (WSS)', font2)

# plt.savefig('K_means_WSS.pdf',bbox_inches='tight',dpi=fig.dpi,pad_inches=0.2)
# plt.show()
