# Use OS to walk through the input directory. View all files in each patient folder. 
#If the file contains T0, save it as it is in the output folder. If the file contains T1, transform it and save it.  

import os
import ants

input_imgs_dir_name = '/data/cbig/I-SPY2/shared/post_resampling/'
input_mask_dir_name = '/data/cbig/I-SPY2/shared/post_resampling_ftv_affinecorrected/'
output_imgs_dir_name = '/data/cbig/I-SPY2/shared/post_registration/'
output_mask_dir_name = '/data/cbig/I-SPY2/shared/post_registration_ftv_affinecorrected/'

string_base = 'T0_pre'
string_moving = 'T1_pre'

for (dirpath, all_pt_ids, filenames) in os.walk(input_imgs_dir_name):
    break

count = 1
for patient in all_pt_ids:
    print("processing " + str(count) + " out of 890 patients")
    count = count + 1
    for (ptfolderpath, folder, files) in os.walk(os.path.join(dirpath, patient)):
        break
    print(os.path.join(dirpath, patient))
    base_filename = moving_filename = files[0]
    for f in files:
        base_filename = f if string_base in f else base_filename
        moving_filename = f if string_moving in f else moving_filename
    base_file = ants.image_read(os.path.join(ptfolderpath, base_filename))
    moving_file = ants.image_read(os.path.join(ptfolderpath, moving_filename))
    mytx1 = ants.registration(base_file, moving_file, type_of_transform="SyN")
    
    output_imgs_foldername = os.path.join(output_imgs_dir_name, patient)
    output_masks_foldername = os.path.join(output_mask_dir_name, patient)
    if not os.path.exists(output_imgs_foldername):
        os.mkdir(output_imgs_foldername)
    if not os.path.exists(output_masks_foldername):
        os.mkdir(output_masks_foldername)

    for current_file in files:
        current_input_filepath = os.path.join(ptfolderpath, current_file)
        current_output_filepath = os.path.join(output_imgs_foldername, current_file)
        current_input = ants.image_read(current_input_filepath)
        if "T0" in current_file:
            ants.image_write(current_input, current_output_filepath)
        if "T1" in current_file:
            ants.image_write(ants.apply_transforms(base_file, current_input, mytx1['fwdtransforms']), current_output_filepath)


    for (ptmaskfolder, folder, mask_files) in os.walk(os.path.join(input_mask_dir_name, patient)):
        break

    for current_mask in mask_files:
        mask_input_filepath = os.path.join(ptmaskfolder, current_mask)
        mask_output_filepath = os.path.join(output_masks_foldername, current_mask)
        mask_input = ants.image_read(mask_input_filepath)
        if "T0" in current_mask:
            ants.image_write(mask_input, mask_output_filepath)
        if "T1" in current_mask:
            ants.image_write(ants.apply_transforms(base_file, mask_input, mytx1['fwdtransforms'], interpolator='nearestNeighbor'), mask_output_filepath)
    

