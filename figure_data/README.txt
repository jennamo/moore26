Here I provide descriptions of the files containing the data used in the figures/tables in Moore et al. 2026. We provide figure data for all figures except Figure 1 -- this figure requires the refined sample catalogs, which we have not released to the public.

################################################################################
"figure2.csv" contains the data for the redshift histogram. 
Load using pd.read_csv('figure2.csv')
The df columns are:
"zbin": left edge of bin, same for all samples
"N_lrg_f150": number of LRG sources (f150 footprint)
"N_lrg_ilc": number of LRG sources (ILC footprint)
"N_bgs": number of BGS sources
"N_optical": number of eROMaPPer sources
################################################################################
################################################################################
"figure3_XXX.npz" contains the image data for the f090/f150 and ILC stacks. There is one file for each sample.
View keys by using np.load('figure3_XXX.npz').files (there are 5 per)
Then load data by using np.load('figure3_XXX.npz')[key]
Each key contains a 161x161 array containing the image data.
Plot one image using plt.imshow(data, origin='lower')
The scale may be converted from pixels to arcmin by dividing by the pixel size:
r_rad_submap = np.deg2rad(10./60.) # each image has 10' radius
pixel_size = (2*r_rad_submap/np.shape(data)[0])*10800/np.pi # approx 0.124 arcmin per pixel
################################################################################
################################################################################
"figure4_XXX.npz" contains the data for the f090/f150 beam-corrected profiles. There is one file for each sample.
View keys by using np.load('figure4_XXX.npz').files (there are 2 per)
Then load data by using np.load('figure4_XXX.npz')[key]
Each key contains a 3x13 array containing:
[key][0]: radii
[key][1]: Compton-y
[key][2]: jackknife uncertainty
################################################################################
################################################################################
"figure5_XXX.npz" contains the data for the ILC beam-corrected profiles. There is one file for each sample.
View keys by using np.load('figure5_XXX.npz').files (there are 3 per)
Then load data by using np.load('figure5_XXX.npz')[key]
Each key contains a 3x13 array containing:
[key][0]: radii
[key][1]: Compton-y
[key][2]: jackknife uncertainty
################################################################################
################################################################################
"figure6_XXX.npz" contains the data for the ring-ring beam-corrected profiles. There is one file for each sample.
View keys by using np.load('figure6_XXX.npz').files (there are 2 per)
Then load data by using np.load('figure6_XXX.npz')[key]
Each key contains a 3x13 array containing:
[key][0]: radii
[key][1]: Compton-y
[key][2]: jackknife uncertainty
################################################################################
################################################################################
"figure7_profiles.npz" contains the data for the 220 GHz profiles.
View keys by using np.load('figure7_profiles.npz').files (there are 3)
Then load data by using np.load('figure7_profiles.npz')[key]
Each key contains a 3x13 array containing:
[key][0]: radii
[key][1]: delta T (uK)
[key][2]: jackknife uncertainty
"figure7_images.npz" contains the image data for the 220 GHz stacks.
View keys by using np.load('figure7_images.npz').files (there are 3 per)
Then load data by using np.load('figure7_images.npz')[key]
Each key contains a 161x161 array containing the image data.
Plot one image using plt.imshow(data, origin='lower')
The scale may be converted from pixels to arcmin by dividing by the pixel size:
r_rad_submap = np.deg2rad(10./60.) # each image has 10' radius
pixel_size = (2*r_rad_submap/np.shape(data)[0])*10800/np.pi # approx 0.124 arcmin per pixel
################################################################################
################################################################################
"figure8_XXX.npz" contains the data for the deprojected single-frequency profiles. There is one file for each sample.
View keys by using np.load('figure8_XXX.npz').files (there are 2 per)
Then load data by using np.load('figure8_XXX.npz')[key]
Each key contains a 4x13 array containing:
[key][0]: radii
[key][1]: Compton-y (deprojected)
[key][2]: bootstrap covariance
[key][3]: Compton-y (raw, beam-corrected)
################################################################################
################################################################################
"figure9_XXX.npz" contains the image data for the full sample and radio-stacks. There is one file for each sample.
View keys by using np.load('figure9_XXX.npz').files (there are 6 per)
Then load data by using np.load('figure9_XXX.npz')[key]
Each key contains a 3x161x161 array containing:
key[0]: image data for the full sample stack
key[1]: image data for the radio-clean stack (sources with NVSS source w/in 1' removed)
key[2]: image data for the radio-clean stack (sources with NVSS source w/in R_AP ' removed)
Plot one image using plt.imshow(data, origin='lower')
The scale may be converted from pixels to arcmin by dividing by the pixel size:
r_rad_submap = np.deg2rad(10./60.) # each image has 10' radius
pixel_size = (2*r_rad_submap/np.shape(data)[0])*10800/np.pi # approx 0.124 arcmin per pixel
################################################################################
################################################################################
"figure10_XXX.npz" contains the data for the full sample and radio-clean profiles for all maps. There is one file for each sample.
Here, "radio-clean" means that all sources with an NVSS source w/in R_AP have been removed.
View keys by using np.load('figure10_XXX.npz').files (there are 6 per)
Then load data by using np.load('figure10_XXX.npz')[key]
Each key contains a 5x13 array containing:
[key][0]: radii
[key][1]: Compton-y for full sample (or dT (uK) for f220)
[key][2]: jackknife uncertainty for full sample
[key][3]: Compton-y for radio-clean sample (or dT (uK) for f220)
[key][4]: jackknife uncertainty for radio-clean sample
################################################################################
################################################################################
"figure11.npz" contains the data for the deprojected single-frequency profiles for the radio-clean eROMaPPer L5 and L10 bins.
Here, "radio-clean" means that all sources with an NVSS source w/in 2.4' have been removed.
View keys by using np.load('figure11.npz').files (there are 4 per)
Then load data by using np.load('figure11.npz')[key]
Each key contains a 4x13 array containing:
[key][0]: radii
[key][1]: Compton-y (deprojected)
[key][2]: bootstrap uncertainty
[key][3]: Compton-y (raw, beam-corrected)
################################################################################
################################################################################
"figure12.csv" contains the data for the Compton-y plot. This data is also tabulated in Table X.
Load using pd.read_csv('figure12.csv', index_col=0)
The df columns (one set for each map) are:
<map>_dy: final corrected Compton-y AP measurement within the fiducial aperture 
<map>_dy_err: error on above measurement
There is an entry for each full sample and radio clean sample (denoted with '_rc')
################################################################################
################################################################################
"figure13.csv" contains the data for the LRG y-tau plot. See y_tau.ipynb for analysis.
We plot the measurements for the f150 map and both deprojected ILC maps.
Load using pd.read_csv('figure13.csv', index_col=0)
The df columns (one set for each map) are:
<map>_y: Compton-y AP measurement within the fiducial aperture* 
<map>_y_err: error on above measurement
<map>_tau: kSZ optical depth within the fiducial aperture (from Gong. et al. 2026)
<map>_tau_err: error on above measurement
There is an entry for each full sample and radio clean sample (denoted with '_rc')
*Note here we do not use the beam-corrected measurements.
"figure13_model.npz" contains the model y-tau scaling relation that Yulin developed from simulations
View keys by using np.load('figure13_model.npz').files (there are 3)
Then load data by using np.load('figure13_model.npz')[key] OR load entire file with
data = np.load('figure13.npz') and then access keys via
key = data['key']
'y_model': np array containing model Compton-y values
'tau_model': np array containing model tau values
'tau_err_model': np array containing model tau error
################################################################################
################################################################################
"figure14.csv" contains the data for the BGS y-tau plot. See y_tau.ipynb for analysis.
We plot the measurements for both deprojected ILC maps.
Load using pd.read_csv('figure14.csv', index_col=0)
The df columns (one set for each map) are:
<map>_y: Compton-y AP measurement within the fiducial aperture* 
<map>_y_err: error on above measurement
<map>_tau: kSZ optical depth within the fiducial aperture (from Hadzhiyska. et al. 2025)
<map>_tau_err: error on above measurement
There is an entry for each full sample and radio clean sample (denoted with '_rc')
*Note here we do not use the beam-corrected measurements.
"figure14_model.npz" contains the SIMBA y-tau points and the y-tau scaling relation that was fit to them
View keys by using np.load('figure14_model.npz').files (there are 10)
Then load data by using np.load('figure14_model.npz')[key] OR load entire file with
data = np.load('figure14.npz') and then access keys via
key = data['key']
'simba_y': np array containing SIMBA Compton-y values
'simba_y_err': np array containing error on simba_y
'simba_tau': np array containing SIMBA tau values
'simba_tau_err': np array containing error on simba_tau
'y_model': np array containing Compton-y values of fit
'taufit': np array containing tau values of fit
't_low': np array containing lower 1 sigma bound of fit
't_high': np array containing upper 1 sigma bound of fit
'popt': np array containing fit [lnt0, m] parameters
'stds': np array containing 1 sigma errors on [lnt0, m]
################################################################################
################################################################################
"figure15.csv" contains the data for the optical y-tau plot using the original (cumulative) binned samples (full sample measurements). See y_tau.ipynb for analysis.
We use only the dB-deprojected ILC map here since measurements are very consistent across all maps for this sample.
Load using pd.read_csv('figure15.csv', index_col=0)
The df columns are:
<map>_y: Compton-y AP measurement within the fiducial aperture* 
<map>_y_err: error on above measurement
<map>_tau: kSZ optical depth within the fiducial aperture* (from Hsu. et al. in prep)
<map>_tau_err: error on above measurement
*Note here we do not use the beam-corrected measurements.
################################################################################
################################################################################
"figure16.csv" contains the data for the optical y-tau plot using the disjoint binned samples. See y_tau.ipynb for analysis.
We use only the dB-deprojected ILC map here since measurements are very consistent across all maps for this sample.
Load using pd.read_csv('figure16.csv', index_col=0)
The df columns are:
<map>_y: Compton-y AP measurement within the fiducial aperture* 
<map>_y_err: error on above measurement
<map>_tau: kSZ optical depth within the fiducial aperture (from Hsu. et al. in prep)
<map>_tau_err: error on above measurement
There is an entry for each full sample and radio clean sample (denoted with '_rc')
*Note here we do not use the beam-corrected measurements.
"figure16_model_full_sample.npz" and "figure16_model_radio_clean.npz" contain the y-tau scaling relation that was fit to the samples
View keys by using np.load('figure16_model_{samp}.npz').files (there are 6)
Then load data by using np.load('figure16_model_{samp}.npz')[key] OR load entire file with
data = np.load('figure14.npz') and then access keys via
key = data['key']
'y_model': np array containing Compton-y values of fit
'popt': np array containing fit [lnt0, m] parameters
'stds': np array containing 1 sigma errors on [lnt0, m]
'taufit': np array containing tau values of fit
't_low': np array containing lower 1 sigma bound of fit
't_high': np array containing upper 1 sigma bound of fit
################################################################################
################################################################################
"figure18.npz" contains the image data for the nonrotated/rotated/difference images (LRG L36 f150)
View keys by using np.load('figure18.npz').files (there are 3)
Then load data by using np.load('figure18.npz')[key]
Each key contains a 161x161 array containing the image data.
The difference image is equal to (nonrotated-rotated)/nonrotated. In the figure we multiply this by 100 to convert to percentage.
Plot one image using plt.imshow(data, origin='lower')
The scale may be converted from pixels to arcmin by dividing by the pixel size:
r_rad_submap = np.deg2rad(10./60.) # each image has 10' radius
pixel_size = (2*r_rad_submap/np.shape(data)[0])*10800/np.pi # approx 0.124 arcmin per pixel
################################################################################
################################################################################
"figure19.json" contains the f090/f150 beam-corrected profiles for all binned samples
Load data by using:
with open('figure19.json', 'r') as file:
    profile_data = json.load(file)
The file is a nested dictionary with the following structure:
profile_data[sample][map][bin][key]
where
[sample] = 'lrg', 'bgs', or 'opt'
[map] = 'f090' or 'f150'
[bin] = bin label
[key] = 'radii', 'dy', or 'dy_err'
################################################################################
################################################################################
"figure20.json" contains the ILC beam-corrected profiles for all binned samples
Load data by using:
with open('figure20.json', 'r') as file:
    profile_data = json.load(file)
The file is a nested dictionary with the following structure:
profile_data[sample][map][bin][key]
where
[sample] = 'lrg', 'bgs', or 'opt'
[map] = 'ilc', 'ilc_cib_1.6_10.7', 'ilc_db_1.6_10.7'
[bin] = bin label
[key] = 'radii', 'dy', or 'dy_err'
################################################################################
################################################################################
"figure21_XXX.npz" contains the data for the deprojected ILC profiles (using different values of beta). There is one file for each sample.
View keys by using np.load('figure6_XXX.npz').files (there are 7 per)
Then load data by using np.load('figure6_XXX.npz')[key]
Each key contains a 3x13 array containing:
[key][0]: radii
[key][1]: Compton-y
[key][2]: jackknife uncertainty
################################################################################
################################################################################
"figure22_XXX.npz" contains the data for the deprojected ILC profiles (using different values of Tcib). There is one file for each sample.
View keys by using np.load('figure22_XXX.npz').files (there are 5 per)
Then load data by using np.load('figure22_XXX.npz')[key]
Each key contains a 3x13 array containing:
[key][0]: radii
[key][1]: Compton-y
[key][2]: jackknife uncertainty
################################################################################
################################################################################
"table1.csv" contains the sample characteristics for the LRG binned samples. 
Load data using pd.read_csv('table1.csv', index_col=0)
Some of this data is also shown in Gong et al. 2026 Table I.
The df columns are:
Lmin/10^10Lsun: lower luminosity bound of bin
Lmax/10^10Lsun: upper luminosity bound of bin (None for cumulative bins)
Mvir_min/10^13Msun: lower halo mass bound of bin
Mvir_max/10^13Msun: upper halo mass bound of bin (None for cumulative bins)
<logM*/Msun>: average log10 stellar mass of bin
<L/10^10Lsun>: average luminosity of bin
<z>: average redshift of bin
N_ilc: number of sources in bin (ILC map footprint)
N_f150: number of sources in bin (f150 map footprint)
################################################################################
################################################################################
"table2.csv" contains the sample characteristics for the BGS binned samples.
Load data using pd.read_csv('table2.csv', index_col=0)
Some of this data is also shown in Hadzhiyska et al. 2025 Table I.
The df columns are:
<logM*/Msun>: average log10 stellar mass of bin
<logMh>: average log10 halo mass of bin
<z>: average redshift of bin
N: number of sources in bin
################################################################################
################################################################################
"table3.csv" contains the sample characteristics for the eROMaPPer binned samples.
Load data using pd.read_csv('table3.csv', index_col=0)
The df columns are:
<lambda_DES>: average richness of bin
<logM200>: average log10 halo mass (units of h^-1 Msun) of bin
<z>: average redshift of bin
N: number of sources in bin
################################################################################
################################################################################
"table5.csv" contains the sample characteristics and Compton-y aperture photometry for the disjoint eROMaPPer binned samples.
Load data using pd.read_csv('table5.csv', index_col=0)
The df columns are:
<N>: number of sources in bin
<z>: average redshift of bin
<lambda_DES>: average richness of bin
ilc_cib_1.6_10.7_y/10^-7: Compton-y aperture photometry measurement using CIB-deprojected ILC map
ilc_cib_1.6_10.7_y_err/10^-7: jackknife uncertainty on above measurement
ilc_db_1.6_10.7_y/10^-7: Compton-y aperture photometry measurement using dB-deprojected ILC map
ilc_db_1.6_10.7_y_err/10^-7: jackknife uncertainty on above measurement
################################################################################
################################################################################
Data for Tables 7-9 can be found in the Figure 17 data files.
################################################################################
################################################################################