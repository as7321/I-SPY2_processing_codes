clc;
clear;

addpath('/home/as7321/Data/Git_repositories/NIfTI_20140122/');
list_dir_path = "/home/as7321/Data/I-SPY2_processed/list_dir/";
list_lab_prev = 'biasfield';
filemask_input = importdata(list_dir_path + 'mask_' + list_lab_prev + ".list");

num_files = length(filemask_input);
ptid = string();
tp = [];
pix_zero_t0 = [];
pix_zero_t1 = [];
pix_one_t0 = [];
pix_one_t1 = [];

for file_no = 1:2:num_files
    input_name = cell2mat(filemask_input(file_no, :));
    ptid_current = cell2mat(extractBetween(input_name, 'nifty/', '/T'));
    %tp_current = 'T0';
    mask_nii = load_untouch_nii(input_name);
    mask_img = mask_nii.img;
    nii_new = zeros(size(mask_img));
    nii_new(mask_img==0) = 1;
    pix_zero_current_t0 = sum(nii_new(:));
    nii_new(mask_img==1) = 1;
    pix_one_current_t0 = sum(nii_new(:));

    %tp_current = 'T1'
    input_name_t1 = cell2mat(filemask_input(file_no+ 1, :));
    mask_nii = load_untouch_nii(input_name_t1);
    mask_img = mask_nii.img;
    nii_new = zeros(size(mask_img));
    nii_new(mask_img==0) = 1;
    pix_zero_current_t1 = sum(nii_new(:));
    nii_new(mask_img==1) = 1;
    pix_one_current_t1 = sum(nii_new(:));


    ptid = [ptid; ptid_current];
    pix_zero_t0 = [pix_zero_t0; pix_zero_current_t0];
    pix_zero_t1 = [pix_zero_t1; pix_zero_current_t1];
    pix_one_t0 = [pix_one_t0; pix_one_current_t0];
    pix_one_t1 = [pix_one_t1; pix_one_current_t1];

end

list_lab_prev = 'biasfield_bothbreast';
filemask_input = importdata(list_dir_path + 'mask_' + list_lab_prev + ".list");
num_files = length(filemask_input);

for file_no = 1:2:num_files
    input_name = cell2mat(filemask_input(file_no, :));
    ptid_current = cell2mat(extractBetween(input_name, 'nifty/', '/T'));

    %tp_current = 'T0';
    mask_nii = load_untouch_nii(input_name);
    mask_img = mask_nii.img;
    nii_new = zeros(size(mask_img));
    nii_new(mask_img==0) = 1;
    pix_zero_current_t0 = sum(nii_new(:));
    nii_new(mask_img==1) = 1;
    pix_one_current_t0 = sum(nii_new(:));

    %tp_current = 'T1'
    input_name_t1 = cell2mat(filemask_input(file_no+ 1, :));
    mask_nii = load_untouch_nii(input_name_t1);
    mask_img = mask_nii.img;
    nii_new = zeros(size(mask_img));
    nii_new(mask_img==0) = 1;
    pix_zero_current_t1 = sum(nii_new(:));
    nii_new(mask_img==1) = 1;
    pix_one_current_t1 = sum(nii_new(:));


    ptid = [ptid; ptid_current];
    pix_zero_t0 = [pix_zero_t0; pix_zero_current_t0];
    pix_zero_t1 = [pix_zero_t1; pix_zero_current_t1];
    pix_one_t0 = [pix_one_t0; pix_one_current_t0];
    pix_one_t1 = [pix_one_t1; pix_one_current_t1];


end
ptid = ptid(2:end);
pix_numbers = table(ptid, pix_zero_t0, pix_zero_t1, pix_one_t0, pix_one_t1, 'VariableNames', ["PatientID","Num_zero_pix-t0","Num_zero_pix-t1", "Num_one_pix-t0", "Num_one_pix-t1"]);
table_name = 'No_zero_or_one_pixels_ftv.xlsx';
writetable(pix_numbers, list_dir_path + table_name, "Sheet",'pix_per_patient');