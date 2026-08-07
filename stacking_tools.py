from iskay2 import paramfile
from iskay2 import maptools
from iskay2 import rcfile
from iskay2 import catalogtools
from iskay2 import ap_photo
import pandas as pd
import os, sys
import multiprocessing as mp
import numpy as np
from pixell import reproject, enmap
from itertools import repeat
from scipy.ndimage import rotate
rng = np.random.default_rng()

# spinoff of get_reprojection from iskay2.ap_photo that uses multiprocessing to get all submaps.
# returns the submaps so that we can stack them
def get_reprojection_full_cat(df_cat, themap, params, rc):
    global R_RAD_SUBMAP
    global OVERSAMPLE
    global THEMAP
    global Nproc
    global MAP_FNAME
    
    ras_rad = np.deg2rad(df_cat.ra.values)
    decs_rad = np.deg2rad(df_cat.dec.values)
    coords_decs_ras_rad = np.vstack([decs_rad, ras_rad]).T
    
    R_RAD_SUBMAP = rc['R_RAD_SUBMAP']
    OVERSAMPLE = rc['OVERSAMPLE']
    THEMAP = themap
    Nproc = len(os.sched_getaffinity(0))#rc['NPROC_AP_PHOTO']
    print(f'launching {Nproc} threads')
    MAP_FNAME = params['MAP_FNAME']
    
    # below is the multiprocessing part
    # generates a pool of workers, each of which will execute the "run" function on coords and return a submap
    with mp.Pool(processes=Nproc) as pool:
        res = pool.map(run, coords_decs_ras_rad)
    return res # returns all submaps from all workers

# this is the function that actually gets the submaps (equivalent to iskay2.ap_photo.get_reprojection but with global variables instead of args)
def run(coords):
    if OVERSAMPLE is None:
        res = None
    else:
        if 'HATLAS' in MAP_FNAME: # set pixel scales: 6, 8, and 12 arcsec/pix for 250, 350, 500 microns, respectively
            if '250' in MAP_FNAME:
                res = np.deg2rad(6/60./60.)
            if '350' in MAP_FNAME:
                res = np.deg2rad(8/60./60.)
            if '500' in MAP_FNAME:
                res = np.deg2rad(12/60./60.)
                # res = np.deg2rad(THEMAP.wcs.wcs.cdelt[1])
        else:
            res = min(np.abs(THEMAP.wcs.wcs.cdelt))*enmap.utils.degree/(2*OVERSAMPLE)

    submap = reproject.thumbnails(THEMAP, coords, R_RAD_SUBMAP, res)

    return submap

# same as above two functions but applies a random rotation to each submap
def get_reprojection_full_cat_rotate(df_cat, themap, params, rc):
    global R_RAD_SUBMAP
    global OVERSAMPLE
    global THEMAP
    global Nproc
    global MAP_FNAME
    
    ras_rad = np.deg2rad(df_cat.ra.values)
    decs_rad = np.deg2rad(df_cat.dec.values)
    coords_decs_ras_rad = np.vstack([decs_rad, ras_rad]).T
    
    R_RAD_SUBMAP = rc['R_RAD_SUBMAP']
    OVERSAMPLE = rc['OVERSAMPLE']
    THEMAP = themap
    Nproc = len(os.sched_getaffinity(0))#rc['NPROC_AP_PHOTO']
    print(f'launching {Nproc} threads')
    MAP_FNAME = params['MAP_FNAME']
    
    # below is the multiprocessing part
    # generates a pool of workers, each of which will execute the "run" function on coords and return a submap
    with mp.Pool(processes=Nproc) as pool:
        res = pool.map(run_rotate, coords_decs_ras_rad)
    return res # returns all submaps from all workers

def run_rotate(coords):
    if OVERSAMPLE is None:
        res = None
    else:
        if 'HATLAS' in MAP_FNAME: # set pixel scales: 6, 8, and 12 arcsec/pix for 250, 350, 500 microns, respectively
            if '250' in MAP_FNAME:
                res = np.deg2rad(6/60./60.)
            if '350' in MAP_FNAME:
                res = np.deg2rad(8/60./60.)
            if '500' in MAP_FNAME:
                res = np.deg2rad(12/60./60.)
                # res = np.deg2rad(THEMAP.wcs.wcs.cdelt[1])
        else:
            res = min(np.abs(THEMAP.wcs.wcs.cdelt))*enmap.utils.degree/(2*OVERSAMPLE)

    submap = rotate(reproject.thumbnails(THEMAP, coords, R_RAD_SUBMAP, res), angle=rng.integers(0,360), reshape=False, mode='constant', cval=np.nan)

    return submap
