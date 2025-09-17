clc;
clear;

addpath('/home/as7321/Data/Git_repositories/NIfTI_20140122/');
list_dir_path = "/home/as7321/Data/I-SPY2_processed/list_dir/";
list_lab_prev = 'ftv_masks_affinecorrected';
%list_lab_orig01 = 'biasfield'; %Original nifti before registration
%list_lab_orig02 = 'biasfield_bothbreast';%Original nifti before registration
%list_lab_between = 'ftv_masks_affinecorrected_extracted';
list_lab_current = 'resampled_ftv_masks_affinecorrected';

%filemask_orig01 = importdata(list_dir_path + 'mask_' + list_lab_orig01 + ".list");
%filemask_orig02 = importdata(list_dir_path + 'mask_' + list_lab_orig02 + ".list");
%filemask_orig = [filemask_orig01; filemask_orig02];
filemask_input = importdata(list_dir_path + 'mask_' + list_lab_prev + ".list");
%filemask_between = importdata(list_dir_path + "mask_" + list_lab_between + ".list");
filemask_output = importdata(list_dir_path + "mask_" + list_lab_current + ".list");

%Define CapTk bias correction command
captk_resampling_cmd = '/opt/CaPTk/1.9.0/Utilities';

num_files = length(filemask_input);

for file_no = 1:num_files
    input_name = cell2mat(filemask_input(file_no, :));
    %between_name = cell2mat(filemask_between(file_no, :));
    %orig_mask_name = cell2mat(filemask_orig(file_no, :));
    %mask_nii = load_nii(input_name);
    %mask_img = mask_nii.img;
    %mask_hdr = mask_nii.hdr;
    


    %new_hdr= mask_hdr;
    %nii_to_save.hdr = new_hdr;


    %niftiwrite(nii_new, between_name, mask_info);
    %disp(between_name)
    %save_nii(nii_to_save, between_name);

    %resampled_img_name = strrep(strrep(out_name, 'post_resampling_ftv_affinecorrected', 'post_resampling'), '_mask', '_pre');
    %img_info = niftiinfo(resampled_img_name);

    output_name = cell2mat(filemask_output(file_no, :));
    disp(["Running CaPTk resampling on " + num2str(file_no) + " out of " + num2str(num_files) + " case..."])
    cmd = [captk_resampling_cmd ' -i ' input_name ' -o ' output_name ' -rr 1.4,1.4,2.6 -rm 1']
    system(cmd);
    disp(["Saving output in" + output_name])
end