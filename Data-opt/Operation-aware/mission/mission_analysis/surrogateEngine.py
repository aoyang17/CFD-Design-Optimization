from smt.surrogate_models import RMTB
import numpy as np 
import os

# Rearranging engine data as the input of the surrogate model
# Input: none
# Output: xt = throttle(-), altitude(km), Mach(-) => 3 dimensional array
#         yt = thrust(x 1e6 N), SFC (x 1e-3 N/N/s) => 2 dimensional array
#         dyt_dxt = dthrust/dthrottle, dthrust/daltitude, dthrust/dMach, dSFC/dthrottle, dSFC/daltitude, dSFC/dMach => 2 * 3 dimensional array
#         xlimits = throttle(-), altitude(km), Mach(-) => 3 dimensional array
def get_b777_engine():
    this_dir = os.path.split(__file__)[0]

    nt = 12*11*8
    xt = np.loadtxt(os.path.join(this_dir, './B777_engine/b777_engine_inputs.dat')).reshape((nt, 3))
    yt = np.loadtxt(os.path.join(this_dir, './B777_engine/b777_engine_outputs.dat')).reshape((nt, 2))
    dyt_dxt = np.loadtxt(os.path.join(this_dir, './B777_engine/b777_engine_derivs.dat')).reshape((nt, 2, 3))

    xlimits = np.array([[0, 0.9], [0, 15], [0, 1.],])

    return xt, yt, dyt_dxt, xlimits


# Training and making engine surrogate model
# Input: xt = throttle(-), altitude(km), Mach(-) => 3 dimensional array
#        yt = thrust(x 1e6 N), SFC (x 1e-3 N/N/s) => 2 dimensional array
#        dyt_dxt = dthrust/dthrottle, dthrust/daltitude, dthrust/dMach, dSFC/dthrottle, dSFC/daltitude, dSFC/dMach => 2 * 3 dimensional array
#        xlimits = throttle(-), altitude(km), Mach(-) => 3 dimensional array
# Output: surrogateE = surrogate model
def calculateSurrogateEngine(xt, yt, dyt_dxt, xlimits):
    surrogateE = RMTB(num_ctrl_pts=15, xlimits=xlimits, nonlinear_maxiter=20, approx_order=2, energy_weight=0e-14, regularization_weight=0e-18, extrapolate=True,print_global=False)
    surrogateE.set_training_values(xt, yt)
    surrogateE.set_training_derivatives(xt, dyt_dxt[:, :, 0], 0)
    surrogateE.set_training_derivatives(xt, dyt_dxt[:, :, 1], 1)
    surrogateE.set_training_derivatives(xt, dyt_dxt[:, :, 2], 2)
    surrogateE.train()
    return surrogateE


# Calcuate thrust and TSFC using engine surrogate model
# Input: x = mach
# Output: thrust = thrust(x 1e6 N)
#         SFC = SFC (x 1e-3 N/N/s)
def SurrogareEngine(x):
    thrust = surrogateE._predict_values(x)[0,0]
    TSFC = surrogateE._predict_values(x)[0,1] #*1.03
    gradient = surrogateE._predict_derivatives(x,2)[0,0]
    return thrust,TSFC,gradient

xt, yt, dyt_dxt, xlimits = get_b777_engine()
surrogateE = calculateSurrogateEngine(xt, yt, dyt_dxt, xlimits)

