%import the list files. 
% Run Captk biasfield command.

clc;
clear;

list_dir_path = "/home/as7321/Data/I-SPY2_processed/list_dir/";
list_lab = 'biasfield';

fileinput=fullfile(list_dir_path + "input_"+ list_lab + ".list"); %Input before biasfield
fileoutput=fullfile(list_dir_path + "output_"+ list_lab + ".list"); %Output after biasfield

%Define CapTk bias correction command
captk_bias_cmd = '/opt/CaPTk/1.9.0/Preprocessing';
input_files = importdata(fileinput);
output_files = importdata(fileoutput);
num_files = numel(input_files);

for k = 1453:num_files
    input_k = cell2mat(input_files(k));
    output_k = cell2mat(output_files(k));
    disp(["Running biasfield correction on " + num2str(k) + " out of " + num2str(num_files) + " case..."])
    cmd = [captk_bias_cmd ' -i ' input_k ' -o ' output_k ' -n4 ']
    system(cmd);
    disp(["Saving output in" + output_k])
end
