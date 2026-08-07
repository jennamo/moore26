import json
import numpy as np
import pandas as pd
import sys
from astropy.constants import c, h, k_B

def do_jackknife(data, N, axis=None):
    jk_avgs = []
    if axis != None:
        data_split = np.array_split(data, N, axis=axis)
        avg = np.average(data, axis=axis)
        for i in range(len(data_split)):
            subsample = [x for j, x in enumerate(data_split) if j != i]
            jk_avgs.append(np.average(np.concatenate(subsample), axis=0))
    else:
        data_split = np.array_split(data, N)
        avg = np.average(data)
        for i in range(len(data_split)):
            subsample = [x for j, x in enumerate(data_split) if j != i]
            jk_avgs.append(np.average(np.concatenate(subsample)))
    return jk_avgs, avg

def calc_uncertainty(jk_avgs, avg, N, axis=None):
    if axis != None:
        return np.sqrt((N-1)*np.sum(((jk_avgs-avg)**2)/N, axis=axis))
    else:
        return np.sqrt((N-1)*np.sum(((jk_avgs-avg)**2)/N))

def do_JK_mult(data, N, axis=0):
    jk_avgs, avg = do_jackknife(data, N, axis=0)
    unc = calc_uncertainty(jk_avgs, avg, N, axis=0)
    return avg, unc

def fsz(freq):
    x = (h.value*freq)/(k_B.value*2.725)
    return x*((np.exp(x)+1)/(np.exp(x)-1))-4

def y_from_T(T, freq):
    return (T*1e-6)/(fsz(freq)*2.725)

def make_profile_df(vals, params, outpath):
    radii, dT, dT_err, T, T_err, R, R_err = vals
    profile_df = pd.DataFrame()
    profile_df['radius'] = radii
    if 'ilc' in params['map_id']:
        profile_df['dy'] = dT
        profile_df['dy_err'] = dT_err
        profile_df['ydisk'] = T
        profile_df['ydisk_err'] = T_err
        profile_df['yring'] = R
        profile_df['yring_err'] = R_err
    else:
        profile_df['dT'] = dT
        profile_df['dT_err'] = dT_err
        profile_df['Tdisk'] = T
        profile_df['Tdisk_err'] = T_err
        profile_df['Tring'] = R
        profile_df['Tring_err'] = R_err
        profile_df['dy'] = y_from_T(dT, params['freq'])
        profile_df['dy_err'] = np.abs(y_from_T(dT_err, params['freq']))
        profile_df['ydisk'] = y_from_T(T, params['freq'])
        profile_df['ydisk_err'] = np.abs(y_from_T(T_err, params['freq']))
        profile_df['yring'] = y_from_T(R, params['freq'])
        profile_df['yring_err'] = np.abs(y_from_T(R_err, params['freq']))
        profile_df['dT_bc'] = profile_df['dT'].values/np.asarray(params['beam_corr'])
        profile_df['dT_err_bc'] = profile_df['dT_err'].values/np.asarray(params['beam_corr'])
    profile_df['dy_bc'] = profile_df['dy'].values/np.asarray(params['beam_corr'])
    profile_df['dy_err_bc'] = profile_df['dy_err'].values/np.asarray(params['beam_corr'])
    profile_df.to_csv(outpath)
    

if __name__ == '__main__':
    paramfile = sys.argv[1]
    
    with open(paramfile, 'r') as f:
        params = json.load(f)
    
    catalog = pd.read_hdf(params['ap_path'], header=0)
    catalog_queried = catalog.query(params['query'], inplace=False)
    
    radii = np.arange(params['min_r'], params['max_r'], 0.5)
    cols = [("dT_%1.2f_arcmin" % r).replace('.', 'p') for r in radii]
    disk_cols = [("T_disk_%1.2f_arcmin" % r).replace('.', 'p') for r in radii]
    ring_cols = [("T_ring_%1.2f_arcmin" % r).replace('.', 'p') for r in radii]

    dT, dT_err = do_JK_mult(catalog_queried[cols].values, N=2000)
    T, T_err = do_JK_mult(catalog_queried[disk_cols].values, N=2000)
    R, R_err = do_JK_mult(catalog_queried[ring_cols].values, N=2000)

    vals = [radii, dT, dT_err, T, T_err, R, R_err]

    outpath = f'profiles/{params["instance_name"]}_profiles.csv'
    make_profile_df(vals, params, outpath)
    
    


