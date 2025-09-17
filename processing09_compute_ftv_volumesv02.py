import os
import scipy.stats as stats
import numpy as np
import nibabel as nib
import pandas as pd


input_ftv_dir_name = '/data/cbig/I-SPY2/shared/post_registration_affine_ftv_dilateerode/'
#input_ftv_dir_name = '/data/cbig/I-SPY2/shared/pre_resampling_ftv/'
processed_excel_dirname = '/data/cbig/I-SPY2/shared/processed_excelsheets/'
processed_ftv_vol_dirname = os.path.join(processed_excel_dirname, 'ftv_volumev02')
filename = os.path.join(processed_ftv_vol_dirname, input_ftv_dir_name.split('shared/')[1].split('/')[0] + '.csv')


if not os.path.exists(processed_excel_dirname):
    os.mkdir(processed_excel_dirname)

if not os.path.exists(processed_ftv_vol_dirname):
    os.mkdir(processed_ftv_vol_dirname)

for(ftvpath, ptnames, ptfiles) in os.walk(input_ftv_dir_name):
    break

ptnames.sort()
num_patients = len(ptnames)
timepoints = ['T0', 'T1']
count = 0

def ld(nii):
    '''
        Calculate longest diameter in mm
    '''
    from skimage.morphology import binary_erosion
    from scipy.spatial.distance import pdist

    data = nii.get_fdata().astype(np.uint8)
    if data.sum() > 2: # at lease 8 voxel to have contour after erosion
        pixdim = nii.header.get_zooms()
        contour = data - binary_erosion(data)
        contour_indices = np.nonzero(contour)
        contour_coord = np.vstack(contour_indices).T * pixdim

        # poor man's mapReduce
        limit = 10000
        length = contour_coord.shape[0]
        if length > limit:
            multiplier = np.floor(length / limit).astype(int)
            dist = np.zeros(multiplier)
            for i in range(multiplier):
                dist[i] = pdist(contour_coord[i*limit:(i*limit+limit)]).max()
            dist[-1] = pdist(contour_coord[(multiplier)*limit:]).max()
            return dist.max()
        else:
            return pdist(contour_coord).max()
    else:
        return 0

def vol(nii):
    '''
        Calculate mask volume in mm^3 ## tested.
    '''
    data = nii.get_fdata().astype(np.uint8)
    unit_vol = np.prod(nii.header.get_zooms())

    return np.count_nonzero(data)*unit_vol

def clinical_tumor_size(nii):
    '''
        Calculate clinical tumor size in mm ## tested
    '''
    data = nii.get_fdata().astype(np.uint8)
    pixdim_x, pixdim_y, pixdim_z = nii.header.get_zooms()[0:3]
    length_x = np.count_nonzero(data.sum(axis=(1,2))) * pixdim_x
    length_y = np.count_nonzero(data.sum(axis=(0,2))) * pixdim_y
    length_z = np.count_nonzero(data.sum(axis=(0,1))) * pixdim_z

    return np.max([length_x, length_y, length_z])


ftv_volumes = pd.DataFrame(columns = ['Diameter-mm-T0', 'Volume-mm^3-T0', 'TumorSize-mm-T0', 'Diameter-mm-T1', 'Volume-mm^3-T1', 'TumorSize-mm-T1'], index = ptnames)
pt_id = timeofscan = tumordiameter = tumorvolume = tumorsize = []
for patient in ptnames:
    print("processing " + str(count) + " out of " +  str(num_patients) + " cases")
    count = count + 1
    pt_tumormetrics = []
    for tp in timepoints:
        current_ftv_filename = os.path.join(input_ftv_dir_name, patient, patient + '_' + tp + '_mask.nii.gz')
        print(current_ftv_filename)
        ftv_nii = nib.load(current_ftv_filename)
        pt_tumormetrics = pt_tumormetrics + [ld(ftv_nii), vol(ftv_nii), clinical_tumor_size(ftv_nii)]
        
        
    ftv_volumes.loc[patient] = pt_tumormetrics
print(ftv_volumes.head())
print("Saving to " + filename)
ftv_volumes.to_csv(filename, index_label = 'PatientID')

