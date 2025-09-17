%import the list files. 
% Run Captk resampling command.

clc;
clear;

list_dir_path = "/home/as7321/Data/I-SPY2_processed/list_dir/";
list_lab_prev = 'biasfield';
list_lab_current = 'resampling';

fileinput=fullfile(list_dir_path + "output_"+ list_lab_prev + ".list"); %Input before resampling
fileoutput=fullfile(list_dir_path + "output_"+ list_lab_current + ".list"); %Output after resampling

%Define CapTk bias correction command
captk_resampling_cmd = '/opt/CaPTk/1.9.0/Utilities';
input_files = importdata(fileinput);
output_files = importdata(fileoutput);
num_files = numel(input_files);

for k = 1:num_files
    input_k = cell2mat(input_files(k));
    output_k = cell2mat(output_files(k));
    disp(["Running CaPTk resampling on " + num2str(k) + " out of " + num2str(num_files) + " case..."])
    cmd = [captk_resampling_cmd ' -i ' input_k ' -o ' output_k ' -rr 1.4,1.4,2.6 -ri LINEAR']
    system(cmd);
    disp(["Saving output in" + output_k])
end

maskinput=fullfile(list_dir_path + "mask_"+ list_lab_prev + ".list"); %Input before resampling
maskoutput=fullfile(list_dir_path + "mask_"+ list_lab_current + ".list"); %Output after resampling

input_masks = importdata(maskinput);
output_masks = importdata(maskoutput);
num_files = numel(input_masks);

for k = 1:num_files
    input_k = cell2mat(input_masks(k));
    output_k = cell2mat(output_masks(k));
    disp(["Running CaPTk resampling on " + num2str(k) + " out of " + num2str(num_files) + " case..."])
    cmd = [captk_resampling_cmd ' -i ' input_k ' -o ' output_k ' -rr 1.4,1.4,2.6 -ri LINEAR']
    system(cmd);
    disp(["Saving output in" + output_k])
end