##This version forms kinetic maps using postcontrast 1 and post contrast 4 images (compared to v02 which uses 1 and 2)
#Additional changes are required as three scans do not have post 4, therefore post 3 will be used for those patients instead.# NOTE!!!! Instead of changinng the code, changes were made in files. i.e., I copied and renamed the post 3 image as post 4 in the two patients (ISPY2-422450 and ISPY2- 709559)


import glob
import os
import pandas as pd
import nibabel as nib
import numpy as np

np.seterr(divide='ignore', invalid='ignore')
scan_details_filename = '/home/as7321/Data/I-SPY2_processed/img_resolution_infov02.xlsx'
scan_details = pd.read_excel(scan_details_filename, sheet_name='scantimev02')

input_dir_name = '/data/cbig/I-SPY2/shared/post_registration/'
#input_mask_dir_name = '/data/cbig/I-SPY2/shared/post_registration_affine_ftv_erodedilate/'
#output_dir_name = '/data/cbig/I-SPY2/shared/kineticmaps_resampled_registered_affinecorrected_withftv/' #With FTV
output_dir_name = '/data/cbig/I-SPY2/shared/kineticmaps_resampled_registered_withoutftv_v03/' #Without FTV

contrast_time = ['pre', 'post1','post2', 'post3', 'post4']
scan_time = ['T0', 'T1']

for (ptpath, ptnames, ptfilenames) in os.walk(input_dir_name):
    break

#for (maskpath, ptnames_m, ptmasknames) in os.walk(input_mask_dir_name):
#    break

count = 0
def wis(img_pre, img_post1, img_post2, t1, t2, mask=None):
    '''
        Computes wash-in-slope of two/three DCE-MRI image time point within given mask.

        Parameteres
        -----------
        img_pre: numpy.array
            Baseline DCE-MRI (pre-contrast)
        img_post1: numpy.array
            First follow-up DCE_MRI (first post-contrast)
        img_post2: numpy.array
            Second follow-up DCE_MRI (second post-contrast)
        t1: int
            First time interval (T1-T0)
        t2: int
            Second time interval (T2-T0)
        mask: numpy.array
           Mask to compute WIS from. If not given, compute over entire array

        Reference
        ---------
        Khalifa, Fahmi, et al. "Models and methods for analyzing DCE-MRI: a review." Medical physics 41.12 (2014): 124301.
    '''
    if mask is not None:
        array0_m, array1_m, array2_m = [a * mask for a in [img_pre, img_post1 , img_post2]]
    else:
        array0_m = img_pre
        array1_m = img_post1
        array2_m = img_post2

    diff1 = (array1_m - array0_m) / array0_m
    diff2 = (array2_m - array0_m) / array0_m

    if_true = 0.5 * (diff1 / t1 + diff2 / (t1 + t2)) # This is what Walt and Rhea used
    #if_true = diff2 / t2
    if_false = diff1 / t1

    #Note: This does not account for cases where T0>T1 and T0>T2. Check if that ever happened i.e., if any value in wis was negative. In that case, those values should be 0.i
    wis_array = np.nan_to_num(np.where(array1_m < array2_m, if_true, if_false))
    #wis_array(wis_array<0) = 0
    return wis_array



def wos(img_pre, img_post1, img_post2, t1, t2, mask=None):
    '''
        Computes wash-out-slope of two/three DCE-MRI image time point within given mask.

        Parameteres
        -----------
        img_pre: numpy.array
            Baseline DCE-MRI (pre-contrast)
        img_post1: numpy.array
            First follow-up DCE_MRI (first post-contrast)
        img_post2: numpy.array
            Second follow-up DCE_MRI (second post-contrast)
        t1: int
            First time interval (T1-T0)
        t2: int
            Second time interval (T2-T0)
        mask: numpy.array
           Mask to compute WIS from. If not given, compute over entire array

        Reference
        ---------
        Khalifa, Fahmi, et al. "Models and methods for analyzing DCE-MRI: a review." Medical physics 41.12 (2014): 124301.
    '''
    if mask is not None:
        array0_m, array1_m, array2_m = [a * mask for a in [img_pre, img_post1, img_post2]]
    else:
        array0_m = img_pre
        array1_m = img_post1
        array2_m = img_post2

    diff1 = (array1_m - array0_m) / array0_m
    diff2 = (array2_m - array0_m) / array0_m

    if_true = np.zeros_like(array0_m)
    if_false = (diff1 - diff2) / (t2-t1)

    return np.nan_to_num(np.where(array1_m < array2_m, if_true, if_false))


def pe(img_pre, img_post1, img_post2, mask = None):
    '''
        Computes peak enhancement of two/three DCE-MRI image time point within given mask.

        Parameteres
        -----------
        img_pre: numpy.array
            Baseline DCE-MRI (pre-contrast)
        img_post1: numpy.array
            First follow-up DCE_MRI (first post-contrast)
        img_post2: numpy.array
            Second follow-up DCE_MRI (second post-contrast)
        mask: numpy.array
           Mask to compute PE from. If not given, compute over entire array

        Reference
        ---------
        Khalifa, Fahmi, et al. "Models and methods for analyzing DCE-MRI: a review." Medical physics 41.12 (2014): 124301.
    '''
    if mask is not None:
        array0_m, array1_m, array2_m = [a * mask for a in [img_pre, img_post1, img_post2]]
    else:
        array0_m = img_pre
        array1_m = img_post1
        array2_m = img_post2

    diff1 = (array1_m - array0_m) / array0_m
    diff2 = (array2_m - array0_m) / array0_m

    return np.nan_to_num(np.where(array1_m < array2_m, diff2, diff1))


def ser(img_pre, img_post1, img_post2, mask = None):
    '''
        Computes signal enhancemnet ratio of two/three DCE-MRI image time point within given mask.

        Parameteres
        -----------
        img_pre: numpy.array
            Baseline DCE-MRI (pre-contrast)
        img_post1: numpy.array
            First follow-up DCE_MRI (first post-contrast)
        img_post2: numpy.array
            Second follow-up DCE_MRI (second post-contrast)
        mask: numpy.array
           Mask to compute SER from. If not given, compute over entire array

        Reference
        ---------
        Khalifa, Fahmi, et al. "Models and methods for analyzing DCE-MRI: a review." Medical physics 41.12 (2014): 124301.
    '''
    if mask is not None:
        array0_m, array1_m, array2_m = [a * mask for a in [img_pre, img_post1, img_post2]]
    else:
        array0_m = img_pre
        array1_m = img_post1
        array2_m = img_post2

    if_true = np.zeros_like(array0_m)
    if_false = (array1_m - array0_m) / (array2_m - array0_m)

    return np.nan_to_num(np.where(array2_m == array0_m, if_true, if_false))



def make_kinetic_masks(images_path, t1, t2, FTV_mask_path=None):
    '''
        def make_masks(root, timings, tp):
        subj = os.path.basename(root)
        t1, t2 = timings[(subj, tp)]
        tp_root = os.path.join(root, subj + '-' + tp)
        niis = [nib.load(fname) for fname in sorted(glob.glob(os.path.join(tp_root, '*.nii')))]
    '''
    #niis = [nib.load(f_name) for f_name in [os.path.join(root, contrast_number) for contrast_number in images_path]]
    niis = [nib.load(f_name) for f_name in images_path]
    imgs = [nii.get_fdata() for nii in niis]
    affine = niis[0].affine

    if FTV_mask_path is not None:
        FTV_mask = nib.load(FTV_mask_path).get_fdata()
    else:
        FTV_mask = None
    masks = dict()
    masks['WIS'] = wis(imgs[0], imgs[1], imgs[2], t1, t2, mask=FTV_mask)
    masks['WOS'] = wos(imgs[0], imgs[1], imgs[2], t1, t2, mask=FTV_mask)
    masks['SER'] = ser(imgs[0], imgs[1], imgs[2], mask=FTV_mask)
    masks['PE'] = pe(imgs[0], imgs[1], imgs[2], mask=FTV_mask)

    return masks, affine

for patient in ptnames:
    print("Processed " + str(count) + " out of 890 patients")
    try:
        os.mkdir(os.path.join(output_dir_name, patient))
    except FileExistsError:
        pass
    
    for (pt_dir_name, ptfolders, ptfiles) in os.walk(ptpath+ patient):
        break
    #for (mask_dir_name, mkfolders, maskfiles) in os.walk(maskpath + patient):
    #    break

    for scan in scan_time:
        f_pre = f_post1 = f_post4 = f_ftv = None
        
        for f in ptfiles:
            f_pre = os.path.join(pt_dir_name, f) if scan in f and contrast_time[0] in f else f_pre
            f_post1 = os.path.join( pt_dir_name, f) if scan in f and contrast_time[1] in f else f_post1
            f_post4 = os.path.join(pt_dir_name, f) if scan in f and contrast_time[4] in f else f_post4
        #for f in maskfiles:
        #    f_ftv = os.path.join(mask_dir_name,f) if scan in f else f_ftv

        pt_details = scan_details[(scan_details['patientID'] == patient) & (scan_details['scantimept'] == scan)]
        t1 = pt_details.iloc[0]['time_post1']
        t2 = pt_details.iloc[0]['time_post4']

        images_path = [f_pre, f_post1, f_post4]
        #masks, affine = make_kinetic_masks(images_path, t1, t2, f_ftv)
        masks, affine = make_kinetic_masks(images_path, t1, t2)
        for k in masks.keys():
            mask = masks[k]

            # cap max and min values in masks
            mask[mask > 1000] = 1000
            mask[mask < -1000] = -1000
            nii = nib.nifti1.Nifti1Image(mask, affine)
            current_filename = scan + '_' +  k + '.nii.gz'
            out_file_name = os.path.join(output_dir_name, patient, current_filename)
            nib.save(nii, out_file_name)

    count = count + 1            

