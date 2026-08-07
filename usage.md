## Notes

We do not provide the finished catalogs.

The ACT DR6 maps are obtained from LAMBDA.

`iskay2` is required: [https://github.com/patogallardo/iskay2](link)

The `iskay2` pipeline is designed for pairwise kSZ analysis. For the tSZ analysis, we only use the aperture photometry functionality (see `stacking_tools.py`). `params.json` is the `iskay2` paramfile that contains the default iskay2 parameters that is generated when you first set up iskay2.



## Order of Operations

1. The catalogs from the kSZ analyses did not have radio source contamination flagged, so we first run `flag_radio_contamination.py` to identify sources within a specified radius of a known radio source. The call is `sbatch flag_radio_contamination.sh <cat path> <radius>` with radius in arcminutes
3. Then we use the `generate_paramfiles.ipynb` notebook to generate `.json` files for each binned subsample/map combination. These will be used in subsequent analysis steps to make running the code on all the different map/sample combinations more streamlined. We also have text files (`all_paramfiles.txt` (all samples+maps), `sf_paramfiles` (single-frequency only) that contain these paramfile paths to make it easy to run job arrays.
4. We then compute the aperture photometry for each catalog using `ap_photo.py`. This script takes in one of the parameter files generated in step 2. The paramfiles are listed in `ap_photo_config.txt`. The call is `sbatch --array=X ap_photo.sh` where X is either a single number (e.g. 1) or a range (e.g. 1-5). See the config file for the number/sample mapping.
5. You can generate a stacked image for a given subsample+map combination using the parameter files with the `stack_submaps.py` script. Using the `stack_submaps.sh` script with the `all_paramfiles.txt` config file, the call is `sbatch --array=X stack_submaps.sh` where X is either a single number (e.g. 1) or a range (e.g. 1-5). See the config file for number/sample mapping.
6. We compute radial profiles for each subsample+map combination using the parameter files with the `make_profile.py` script. This computes Compton-y (and temperature if using single-frequency maps) profiles and jackknife uncertainties for the AP disk, ring, and disk-ring. The results are saved as a `.csv` file in the `profiles` directory. Using the `make_profile.sh` script with the `all_paramfiles.txt` config file, the call is `sbatch --array=X make_profile.sh` where X is either a single number (e.g. 1) or a range (e.g. 1-5). See the config file for number/sample mapping.
7. The single-frequency profiles are deprojected following the method described in R.H. Liu et al. 2025 Appendix C. First, covariance matrices are computed using the `covariance.py` script. Then, the profiles are deprojected using the `deproj_cib_sf.py` script. Note the deprojection only works in cases where the 220 GHz profile is > 0 at all radii and there is a significant reduction in signal at 150 GHz relative to 90 GHz. The results are saved as a `.csv` file in the `profiles` directory. Using the `covariance.sh` script with the `sf_paramfiles.txt` config file, the call is `sbatch --array=X covariance.sh`. Using the `deproj_cib.sh` script with the `all_samples.txt` config file, the call is `sbatch --array=X deproj_cib.sh` where X is either a single number (e.g. 1) or a range (e.g. 1-5). See the config file for number/sample mapping. 
8. Ring-ring profiles are generated in `ring_ring.ipynb`
9. We do the y-tau analysis and scaling relation fitting in `y_tau.ipynb`
10. All figures and Tables are recreated in the `make_figures_and_tables.ipynb` notebook.