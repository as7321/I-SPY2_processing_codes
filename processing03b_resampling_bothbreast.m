clc;
clear;

list_dir_path = "/home/as7321/Data/I-SPY2_processed/list_dir/";
output_dir_name = "/data/cbig/I-SPY2/shared/post_resampling/"
list_lab_prev = 'biasfield_bothbreast';
list_lab_current = 'resampling_bothbreast';


complete_biasfield_corrected_filelist = importdata(list_dir_path + 'output_' + list_lab_prev + ".list");
filemask_input = importdata(list_dir_path + 'mask_' + list_lab_prev + ".list");

fileoutput_name = fullfile(list_dir_path + "output_" + list_lab_current + ".list");
filemask_output = fullfile(list_dir_path + "mask_" + list_lab_current + ".list");

fileoutput = fopen(fileoutput_name, 'w');
filemask = fopen(filemask_output, 'w');

num_files_orig = size(complete_biasfield_corrected_filelist, 1);
for i = 1:num_files_orig
    patient_path_prev = cell2mat(complete_biasfield_corrected_filelist(i));
    patient_path_current = strrep(patient_path_prev, 'post_biasfield_correction', 'post_resampling');
    fprintf(fileoutput, '%s\n', patient_path_current);
end

num_files_mask = size(filemask_input, 1);
for i = 1:num_files_mask
    mask_path_input = cell2mat(filemask_input(i));
    patientID_current = cell2mat(extractBetween(mask_path_input, 'nifty/', '/T'));
    current_timepoint = cell2mat(extractBetween(mask_path_input, '/T', '/'));
    mask_path_output = output_dir_name + patientID_current + '/' + patientID_current + "_T" + current_timepoint + "_mask.nii.gz";
    fprintf(filemask, '%s\n', mask_path_output);
end

pt_id_filename = 'patientID_bothbreast_to_processv01.txt';
pt_id_info = readcell(list_dir_path + pt_id_filename);
num_patients = size(pt_id_info, 1);
for pt = 1:num_patients
    output_path_current = output_dir_name + cell2mat(pt_id_info(pt));
    if ~exist(output_path_current, "dir")
        mkdir(output_path_current);
    end
end
