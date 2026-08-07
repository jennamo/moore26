# Code adapted from https://github.com/rhenryliu/Thumbstack_new/blob/master/scripts/ThumbStack_DustDeproject_zenodo.py (see Liu et al. 2025 Appendix C)
# Functions for single-frequency dust+CIB deprojection 
import numpy as np
from astropy import units as u
import scipy
import scipy.constants
from scipy.optimize import minimize
import emcee

freq = np.array([90e9, 150e9, 220e9]) # Hz

# Fundamental Constants
Tcmb = 2.726   # K
h = 6.63e-34   # SI
kB = 1.38e-23  # SI
c = scipy.constants.c

# CIB Deprojection constants (fiducial)
beta = 1.6
T_CIB = 10.7

# CIB and tSZ frequency dependence functions (in temperature units)
def f(nu):
    """frequency dependence for tSZ temperature
    """
    x = h*nu/(kB*Tcmb)
    return x*(np.exp(x)+1.)/(np.exp(x)-1.) -4.

def dB_dT(nu, T):
    x = h * nu / (kB * T)
    numerator = 2 * h * nu**3 / c**2 * x * np.exp(x)
    denominator = T * (np.exp(x) - 1)**2
    return numerator / denominator

def f_CIB(nu, beta, Tcib):
    term1 = (nu)**(3 + beta)/(np.exp(h*nu/(kB*Tcib)) - 1)    
    return term1 * dB_dT(nu, Tcmb)
    # return term1 / dB_dT(nu, Tcmb)

def CIB_scale(beta, nu, T_CIB=T_CIB):
    return (f_CIB(nu, beta, T_CIB) / f_CIB(220e9, beta, T_CIB))  

def T_to_y(nu):
    factor = (180.*60./np.pi)**2 # unit conversion from sr to arcmin^2
    return 1.0 / (Tcmb * f(nu) * 1.e6)

# Chi-squared calculator
def chi2(beta, y1, y2, y3, C1, C2, C3, nu1, nu2):
    H1 = T_to_y(nu1)
    H2 = T_to_y(nu2)
    G1 = CIB_scale(beta, nu1)
    G2 = CIB_scale(beta, nu2)

    # Residual
    r = H1 * (y1 - G1 * y3) - H2 * (y2 - G2 * y3)

    # Covariance: scaled by squared H terms, which ensures positive definiteness
    Cr = H1**2 * C1 + H2**2 * C2 + (H1 * G1 - H2 * G2)**2 * C3
    Cr_inv = np.linalg.inv(Cr)

    return r.T @ Cr_inv @ r


# Emcee sampling priors and posteriors:

def log_prior(beta):
    if 0.01 < beta < 10.0:
        return 0.0  # log(1)
    return -np.inf
    
def log_likelihood(beta, y1, y2, y3, C1, C2, C3, nu1, nu2):
    return -0.5 * chi2(beta, y1, y2, y3, C1, C2, C3, nu1, nu2)

def log_posterior(beta, y1, y2, y3, C1, C2, C3, nu1, nu2):
    lp = log_prior(beta)
    if not np.isfinite(lp):
        return -np.inf
    return lp + log_likelihood(beta, y1, y2, y3, C1, C2, C3, nu1, nu2)

def compute_profile(y, Cy, nu):
    # factor for converting T to y
    H = T_to_y(nu)

    # Compute f
    f = H * (y)
    
    # Propagate covariance
    Cf = H**2 * (Cy)
    
    # 1σ uncertainty per element
    sigma_f = np.sqrt(np.diag(Cf))
    
    return f, sigma_f

def compute_deproj_profile(beta, y, y3, Cy, C3, nu):
    # factor for converting T to y
    H = T_to_y(nu)
    # scaling factor for 220 GHz CIB signal
    G = CIB_scale(beta, nu)

    # Compute f
    f = H * (y - G * y3)
    
    # Propagate covariance
    Cf = H**2 * (Cy + G**2 * C3)
    
    # 1σ uncertainty per element
    sigma_f = np.sqrt(np.diag(Cf))
    
    return f, sigma_f

def compute_dust_profile(beta, y, y3, Cy, C3, nu):
    # factor for converting T to y
    H = T_to_y(nu)
    # scaling factor for 220 GHz CIB signal
    G = CIB_scale(beta, nu)

    # Compute f
    f = H * (G * y3)
    
    # Propagate covariance
    Cf = H**2 * (G**2 * C3)
    
    # 1σ uncertainty per element
    sigma_f = np.sqrt(np.diag(Cf))
    
    return f, sigma_f