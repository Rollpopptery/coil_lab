
import numpy as np
import scipy.optimize




# The exponential decay function
def exp_decay(x, tau, init):
    return init * np.e ** (-x / tau)


y_dataSetIn = None
y_curveFitOut = None
tauValue = 0

def test():

    global y_dataSetIn
    global y_curveFitOut
    global tauValue

    x = np.arange(0, len(y_dataSetIn), 1)

    # Use scipy.optimize.curve_fit to fit parameters to noisy data
    popt, pcov = scipy.optimize.curve_fit(exp_decay, x, y_dataSetIn)
    fit_tau, fit_init = popt

    # Sample exp_decay with optimized parameters
    y_curveFitOut = exp_decay(x, fit_tau, fit_init)

    tauValue = fit_tau



if __name__ == "__main__":

    # Parameters for the exp_decay function
    real_tau = 30
    real_init = 250


    # Sample exp_decay function and add noise
    np.random.seed(100)

    x = np.arange(0, 100, 1)
    noise = np.random.normal(scale=50, size=x.shape[0])
    y = exp_decay(x, real_tau, real_init)
    y_dataSetIn= y + noise
    test()
