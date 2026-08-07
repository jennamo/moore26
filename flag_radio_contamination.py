# call is sbatch flag_radio_contamination.sh <cat path> <radius>
import pandas as pd
from astropy.coordinates import SkyCoord
import astropy.units as u
import sys, os
import numpy as np

# import NVSS catalog and make SkyCoord instances of each source
# note: the catalog I load here has already converted the ra/dec from h:m:s format to degrees
radio_cat = pd.read_hdf('/hpc/group/cosmology/jem189/scratch/allnvss_sources.hdf', header=0)
radio_sc = SkyCoord(ra=radio_cat['ra_deg'].values*u.deg, dec=radio_cat['dec_deg'].values*u.deg)

# load source catalog and make SkyCoord instances of each source
cat_path = sys.argv[1] # provide catalog path in sbatch call
source_cat = pd.read_csv(cat_path)
source_sc = SkyCoord(ra=source_cat['ra'].values*u.deg, dec=source_cat['dec'].values*u.deg)

# cross-match catalogs within given radius
radius = float(sys.argv[2]) # provide radius (in arcmin) in sbatch call
cat_idx, radio_idx, sep, _ = radio_sc.search_around_sky(source_sc, radius*u.arcmin)
flag = np.ones(len(source_cat))
flag[cat_idx] = 0
col = f'valid_radio_{radius}'
source_cat[col] = flag
print(f'found {len(np.unique(cat_idx))} contaminated sources (r={radius})')

# save the updated dataframe 
outpath = os.path.splitext(cat_path)[0]+'_radioflagged.csv'
source_cat.to_csv(outpath, index=False)