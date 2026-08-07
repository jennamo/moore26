from iskay2 import paramfile
from iskay2 import maptools
from iskay2 import rcfile
from iskay2 import catalogtools
from iskay2 import ap_photo
import pandas as pd
import os, sys
import multiprocessing as mp
import numpy as np
from stacking_tools import get_reprojection_full_cat
from astropy.io import fits

map_dir = '/hpc/group/cosmology/jem189/scratch/data/maps'
cat_dir = '/work/jem189/scratch/data/catalogs'
outdir = '/work/jem189/scratch/data/stacks'

# load param and rc files, update relevant params
params = paramfile.load_paramfile()
rc = rcfile.load_rcfile()
newparams = paramfile.load_paramfile(sys.argv[1])
params['MAP_FNAME'] = os.path.join(map_dir, newparams['map_name'])+'.fits'
params['CAT_FNAME'] = os.path.join(cat_dir, newparams['cat_name'])+'.csv'
# load map and catalog
themap = maptools.load_map(params, rc=rc)
df = catalogtools.load_catalog(params, rc=rc)

# access the desired sources
query = newparams['query']
df_queried = df.query(query, inplace=False)

# use small chunk of catalog if testing script                                                                                                                   
isTest = sys.argv[2]
if isTest == 'True':
    df_queried = df_queried.head(1000)

# get stacked submaps
print(f'N: {len(df_queried)}')
submaps = get_reprojection_full_cat(df_queried, themap, params, rc)
submaps = np.dstack(submaps)
print(np.shape(submaps))

# compute average and save
avg = np.average(submaps, axis=2)
mapname = newparams['map_name']
catname = newparams['cat_name']

outname = os.path.splitext(os.path.split(newparams['stack_file'])[1])[0]
results_folder = os.path.join(outdir, catname)
if not os.path.exists(results_folder):
    os.mkdir(results_folder)
print(f'saving stack to {results_folder}')
if isTest == 'True':
    fits.writeto(os.path.join(results_folder, f'{outname}_test.fits'), avg, overwrite='True')

else:
    fits.writeto(os.path.join(results_folder, f'{outname}.fits'), avg, overwrite='True')

