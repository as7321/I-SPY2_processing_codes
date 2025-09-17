% Form list
% Input file path - T0(post3, post4), T1 (pre, post3, post4)
% This function will take input from the output of biasfield correction.
% Therefore, input list will be biasfield output list. Here, we are making
% an output list, which contains the path and names of output after
% resampling. 

clc;
clear;

list_dir_path = "/home/as7321/Data/I-SPY2_processed/list_dir/";
output_dir_name = "/data/cbig/I-SPY2/shared/post_resampling/"
list_lab_prev = 'biasfield_post3and4';
list_lab_current = 'resampling_post3and4';


complete_biasfield_corrected_filelist = importdata(list_dir_path + 'output_' + list_lab_prev + ".list");
fileoutput_name = fullfile(list_dir_path + "output_" + list_lab_current + ".list");
fileoutput = fopen(fileoutput_name, 'w');

num_files_orig = size(complete_biasfield_corrected_filelist, 1);
for i = 1:num_files_orig
    patient_path_prev = cell2mat(complete_biasfield_corrected_filelist(i));
    patient_path_current = strrep(patient_path_prev, 'post_biasfield_correction', 'post_resampling');
    fprintf(fileoutput, '%s\n', patient_path_current);
end
