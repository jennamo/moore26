import numpy as np
import pandas as pd
import os, sys, json, secrets

# calculate covariance matrix
def bootstrap_resample(dTs, seed, N=10000):
    rng = np.random.default_rng(seed=seed)
    profiles = np.zeros((N, len(cols)))
    for i in range(N):
        choices = rng.choice(len(dTs), len(dTs), replace=True)
        data = dTs.values[choices]
        profiles[i] = np.average(data, axis=0)
    covariance = np.cov(profiles.T)
    return covariance

if __name__ == '__main__':
    seed = secrets.randbits(128) # random seed
    paramfile = sys.argv[1]
    with open(paramfile, 'r') as f:
        params = json.load(f)

    catalog = pd.read_hdf(params['ap_path'], header=0)
    catalog_queried = catalog.query(params['query'], inplace=False)
    radii = np.arange(params['min_r'], params['max_r'], 0.5)
    cols = [("dT_%1.2f_arcmin" % r).replace('.', 'p') for r in radii]

    dTs = catalog_queried[cols]
    covariance = bootstrap_resample(dTs, seed)
    covariance/=np.outer(params["beam_corr"], params["beam_corr"]) # beam correct the cov
    outpath = f'/hpc/home/jem189/code/moore26/covariances/{params["instance_name"]}.npy'
    np.save(outpath, covariance)