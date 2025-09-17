import nibabel as nib
import cv2
import os
import numpy as np


list_dir_path = '/home/as7321/I-SPY2_processed/list_dir'
input_ftv_mask_dir = '/data/cbig/I-SPY2/shared/post_registration_ftv_affinecorrected/'
output_ftv_mask_dir = '/data/cbig/I-SPY2/shared/post_registration_affine_ftv_dilateerode/'
timepoints = ['T0', 'T1']
kernel = np.ones((3,3), np.uint8)

if not os.path.exists(output_ftv_mask_dir):
        os.mkdir(output_ftv_mask_dir)

for ptpath, ptnames, ptfiles in os.walk(input_ftv_mask_dir):
    break

count = 1

for pt in ptnames:
    print("Processing " + str(count) + " out of 1780 cases")
    if not os.path.exists(os.path.join(output_ftv_mask_dir, pt)):
        os.mkdir(os.path.join(output_ftv_mask_dir, pt))
    for tp in timepoints:
        init_ftv_mask = os.path.join(input_ftv_mask_dir, pt, pt + '_' + tp + '_mask.nii.gz')
        output_ftv_name = os.path.join(output_ftv_mask_dir, pt, pt + '_' + tp + '_mask.nii.gz')

        ftv_orig = nib.load(init_ftv_mask)
        mask_init = ftv_orig.get_fdata()
        affine = ftv_orig.affine
        
        #mask_eroded = cv2.erode(mask_init, kernel, iterations=1)
        mask_dilated = cv2.dilate(mask_init, kernel, iterations=1)
        mask_eroded = cv2.erode(mask_dilated, kernel, iterations=1)

        ftv_new = nib.Nifti1Image(mask_eroded, affine)
        nib.save(ftv_new, output_ftv_name)
        count = count + 1
      
