# This will be a python file only to correct affine of the masks. 
# Masks from original_nifty folder (present in the list directory mask_biasfield and mask_biasfield_bothbreasts) will be taken along with corresponding DCE_pre images. The masks will be transformed accoridng to the affine of DCE_pre images.

import nibabel as nib
import numpy as np
from scipy.ndimage import affine_transform
import os
import ants


list_dir_path = '/home/as7321/Data/I-SPY2_processed/list_dir/'


input_masks_listname01 = 'mask_biasfield.list'
input_masks_listname02 = 'mask_biasfield_bothbreast.list'
output_masks_listname = 'mask_ftv_masks_affinecorrected.list'

string_base = '_mask'
string_moving = '_DCE_pre'

with open(os.path.join(list_dir_path, input_masks_listname01)) as f:
    input_mask_files01 = f.read().splitlines()

with open(os.path.join(list_dir_path, input_masks_listname02)) as f:
    input_mask_files02 = f.read().splitlines()

with open(os.path.join(list_dir_path, output_masks_listname)) as f:
    output_mask_files = f.read().splitlines()

input_mask_files = input_mask_files01 +  input_mask_files02
num_files = len(input_mask_files)
#for i, mask_loc in enumerate(input_mask_files01[1378:1379]):
for i in range(num_files):
    mask_loc = input_mask_files[i]
    print(mask_loc)
    output_mask_loc = output_mask_files[i]
    img_loc = mask_loc.replace('_mask', '_DCE_pre')
    
    
    '''
    base_file = ants.image_read(img_loc)
    moving_file = ants.image_read(mask_loc)
    #mask_file = ants.get_mask(moving_file, 0, 0)
    mask_numpy = moving_file.numpy()
    ftv_numpy = np.zeros(mask_numpy.shape)
    ftv_numpy[mask_numpy == 0] = 1
    #ftv_ants = ants.from_numpy(ftv_numpy)
    #mytx1 = ants.registration(base_file, moving_file, type_of_transform="Affine")
    ants.image_write(mask_file, output_mask_loc)
    #ants.image_write(ants.apply_transforms(base_file, mask_file, mytx1['fwdtransforms'], interpolator='nearestNeighbor'), output_mask_loc)

    '''
    mask_nifti = nib.load(mask_loc)
    img_nifti = nib.load(img_loc)

    mask_scan = mask_nifti.get_fdata()
    mask_affine = mask_nifti.affine
    ftv_scan = np.zeros(mask_scan.shape)
    ftv_scan[mask_scan == 0] = 1

    img_scan = img_nifti.get_fdata()
    img_affine = img_nifti.affine

    transformed_mask_init = []
    transformed_mask_init.append(mask_scan)
    mask_affine_inverse = np.linalg.inv(mask_affine)
    transformation_matrix = mask_affine_inverse.dot(img_affine)
    rotation = transformation_matrix[:3, :3]
    translation = transformation_matrix[:3, 3]
    output_shape = img_scan.shape
    ftv_scan = ftv_scan.squeeze(axis=-1)
    transformed_mask = affine_transform(ftv_scan, rotation, offset=translation, output_shape=output_shape, order=0, mode='nearest')
    transformed_mask_init.append(transformed_mask)
    transformed_mask_nifti = nib.Nifti1Image(transformed_mask, img_affine)
    nib.save(transformed_mask_nifti, output_mask_loc)

