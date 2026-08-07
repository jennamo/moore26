# Performs the dust+CIB deprojection on the single-frequency radial profiles
# Methodology adapted from Liu et al. 2025
import numpy as np
import pandas as pd
import os, sys, json
import cib_deproj as cib
from scipy.optimize import minimize

freq_labels = ['f090', 'f150', 'f220']
freqs = [90e9, 150e9, 220e9]

def calc_beta(b0, profiles, covariances, inner_stop):
    ys_inner = [profiles[f]['dT_bc'].values[:inner_stop] for f in freq_labels]
    ys_outer = [profiles[f]['dT_bc'].values[inner_stop:] for f in freq_labels]
    covars_inner = [covariances[f][:inner_stop, :inner_stop] for f in freq_labels]
    covars_outer = [covariances[f][inner_stop:, inner_stop:] for f in freq_labels]

    def fit_beta(label, ys, covars):
        res = minimize(lambda x: cib.chi2(x[0],ys[0],ys[1],ys[2],covars[0],covars[1],covars[2],freqs[0],freqs[1],),
            x0=[b0],
            method="L-BFGS-B",
            bounds=[(0.01, 20.0)])

        if not res.success:
            raise RuntimeError(f"{label} optimization failed: {res.message}")

        beta = res.x[0]
        chi2 = res.fun
        n_dof = len(ys[0]) - 1

        print(f"{label}: Best-fit β = {beta:.4f}, " f"Minimum χ² = {chi2:.4f}, " f"χ²_red = {chi2 / n_dof:.4f}")
        return beta

    beta_inner = fit_beta("Inner", ys_inner, covars_inner)
    beta_outer = fit_beta("Outer", ys_outer, covars_outer)

    return ([ys_inner, ys_outer],[covars_inner, covars_outer],[beta_inner, beta_outer])

def do_deproj(ys, covars, betas, profiles, inner_stop):
    for i, f in enumerate(['f090', 'f150']):
        deproj_profile = np.ones_like(profiles[f]['dy_bc'].values)
        deproj_profile_err = np.ones_like(profiles[f]['dy_err_bc'].values)
        dust_profile = np.ones_like(profiles[f]['dy_bc'].values)
        dust_profile_err = np.ones_like(profiles[f]['dy_err_bc'].values)
        for j in range(len(betas)):
            prof, prof_err = cib.compute_deproj_profile(betas[j], ys[j][i], ys[j][2], covars[j][i], covars[j][2], freqs[i])
            dustprof, dustprof_err = cib.compute_dust_profile(betas[j], ys[j][i], ys[j][2], covars[j][i], covars[j][2], freqs[i])
            sl = slice(None, inner_stop) if j == 0 else slice(inner_stop, None)
            deproj_profile[sl] *= prof
            deproj_profile_err[sl] *= prof_err
            dust_profile[sl] *= dustprof
            dust_profile_err[sl] *= dustprof_err
        profiles[f]['dy_deproj'] = deproj_profile
        profiles[f]['dy_deproj_err'] = deproj_profile_err
        profiles[f]['dy_dust'] = dust_profile
        profiles[f]['dy_dust_err'] = dust_profile_err
    return profiles
        
if __name__ == '__main__':
    sample = sys.argv[1]
    params = {}
    profiles = {}
    covariances = {}
    for freq in freq_labels:
        paramfile = f'paramfiles/{freq}_{sample}.json'
        profile = f'profiles/{freq}_{sample}_profiles.csv'
        covariance = f'covariances/{freq}_{sample}.npy'
        with open(paramfile, 'r') as f:
            params[freq] = json.load(f)
        profiles[freq] = pd.read_csv(profile, index_col=0)
        covariances[freq] = np.load(covariance)

    b0 = 3.0
    ys, covars, betas = calc_beta(b0, profiles, covariances, inner_stop=2)
    profiles_deproj = do_deproj(ys, covars, betas, profiles, inner_stop=2)
    for freq in ['f090', 'f150']:
        profiles_deproj[freq].to_csv(f'profiles/{freq}_{sample}_profile_deproj.csv', index=False)
    