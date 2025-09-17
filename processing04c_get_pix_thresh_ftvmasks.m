clc;
clear;

addpath('/home/as7321/Data/Git_repositories/NIfTI_20140122/');
list_dir_path = "/home/as7321/Data/I-SPY2_processed/list_dir/";
list_lab_prev = 'biasfield';
filemask_input = importdata(list_dir_path + 'mask_' + list_lab_prev + ".list");

num_files = length(filemask_input);
ptid = string();
tp = [];
pix_zero = [];
pix_one = [];

for file_no = 1:num_files
    input_name = cell2mat(filemask_input(file_no, :));
    ptid_current = cell2mat(extractBetween(input_name, 'nifty/', '/T'));
    if rem(file_no, 2) == 0
        tp_current = 'T1';
    else
        tp_current = 'T0';
    end
    mask_nii = load_nii(input_name);
    mask_img = mask_nii.img;
    nii_new = zeros(size(mask_img));
    nii_new(mask_img==0) = 1;
    pix_zero_current = sum(nii_new(:));

    nii_new(mask_img==1) = 1;
    pix_one_current = sum(nii_new(:));

    ptid = [ptid; ptid_current];
    tp = [tp; tp_current];
    pix_zero = [pix_zero; pix_zero_current];
    pix_one = [pix_one; pix_one_current];

end

list_lab_prev = 'biasfield_bothbreast';
filemask_input = importdata(list_dir_path + 'mask_' + list_lab_prev + ".list");
num_files = length(filemask_input);

for file_no = 1:num_files
    input_name = cell2mat(filemask_input(file_no, :));
    ptid_current = cell2mat(extractBetween(input_name, 'nifty/', '/T'));
    if rem(file_no, 2) == 0
        tp_current = 'T1';
    else
        tp_current = 'T0';
    end
    mask_nii = load_untouch_nii(input_name);
    mask_img = mask_nii.img;
    nii_new = zeros(size(mask_img));
    nii_new(mask_img==0) = 1;
    pix_zero_current = sum(nii_new(:));

    nii_new(mask_img==1) = 1;
    pix_one_current = sum(nii_new(:));

    ptid = [ptid; ptid_current];
    tp = [tp; tp_current];
    pix_zero = [pix_zero; pix_zero_current];
    pix_one = [pix_one; pix_one_current];

end
ptid = ptid(2:end);
pix_numbers = table( ptid,  tp, pix_zero, pix_one, 'VariableNames', ["PatientID","TimePoints", "Num_zero_pix","Num_one_pix"]);
table_name = 'No_zero_or_one_pixels_ftv.xlsx';
writetable(pix_numbers, list_dir_path + table_name);