clc;
clear;
addpath('utils/');
addpath('/home/as7321/Data/Git_repositories/NIfTI_20140122/');

list_dir_path = "/home/as7321/Data/I-SPY2_processed/list_dir/";
input_mask_list_name = 'post_registration_affine_ftv.list';
output_mask_list_name = 'post_reg_affine_binary_ftv.list';

%makelist(list_dir_path, input_mask_list_name, output_mask_list_name, 'affinecorrected', 'affine_binary')

input_masknames = importdata(strcat(list_dir_path, input_mask_list_name));
output_masknames = importdata(strcat(list_dir_path, output_mask_list_name));

num_files = size(input_masknames, 1);
mask_file = input_masknames{1};
input_folder_name = cell2mat(extractBetween(mask_file, 'shared/', '/'));


for k = 1:4:num_files
    in_k = input_masknames{k};
    out_k = output_masknames{k};
    [filepath, ~, ~] = fileparts(out_k);
    if ~exist(filepath, "dir")
        mkdir(filepath);
    end
    input_nii = load_nii(in_k);
    input_img = input_nii.img;
    img_binary = double(imbinarize(input_img));
    mask_info = niftiinfo(in_k);
    niftiwrite(img_binary, out_k, mask_info);
end