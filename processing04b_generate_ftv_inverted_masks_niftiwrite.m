clc;
clear;

addpath('/home/as7321/Data/Git_repositories/NIfTI_20140122/');
list_dir_path = "/home/as7321/Data/I-SPY2_processed/list_dir/";
list_lab_between = 'ftv_masks_inverted';
list_lab_prev = 'biasfield';
list_lab_current = 'resampled_ftv_masks_inverted';

filemask_input = importdata(list_dir_path + 'mask_' + list_lab_prev + ".list");
filemask_between = importdata(list_dir_path + "mask_" + list_lab_between + ".list");
filemask_output = importdata(list_dir_path + "mask_" + list_lab_current + ".list");

%Define CapTk bias correction command
captk_resampling_cmd = '/opt/CaPTk/1.9.0/Utilities';

num_files = length(filemask_input);

for file_no = 1:num_files
    input_name = cell2mat(filemask_input(file_no, :));
    between_name = cell2mat(filemask_between(file_no, :));
    mask_nii = load_nii(input_name);
    mask_img = mask_nii.img;
    mask_hdr = mask_nii.hdr;
    mask_info = niftiinfo(input_name);

    nii_new = zeros(size(mask_img));
    nii_new(mask_img==1) = 1;
    nii_new = im2uint8(nii_new);
    niftiwrite(nii_new, between_name, mask_info);

    output_name = cell2mat(filemask_output(file_no, :));
    disp(["Running CaPTk resampling on " + num2str(file_no) + " out of " + num2str(num_files) + " case..."])
    cmd = [captk_resampling_cmd ' -i ' between_name ' -o ' output_name ' -rr 1.4,1.4,2.6 -ri LINEAR']
    system(cmd);
    disp(["Saving output in" + output_name])

end
