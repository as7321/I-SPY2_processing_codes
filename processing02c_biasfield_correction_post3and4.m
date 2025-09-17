% Form list
% Input file path - T0(post3, post4), T1 (pre, post3, post4)
clc;
clear;

list_dir_path = "/home/as7321/Data/I-SPY2_processed/list_dir/";
%The new List files being formed
list_lab = 'biasfield_post3and4';
fileinput_name = fullfile(list_dir_path + "input_" + list_lab + ".list");
fileoutput_name = fullfile(list_dir_path + "output_" + list_lab + ".list");
fileinput = fopen(fileinput_name, 'w');
fileoutput = fopen(fileoutput_name, 'w');

%The old list files which will be read and modified
list_lab_prev01 = 'biasfield';
list_lab_prev02 = 'biasfield_bothbreast';
fileinput_prev01=fullfile(list_dir_path + "input_"+ list_lab_prev01 + ".list"); %Input before biasfield
fileinput_prev02=fullfile(list_dir_path + "input_"+ list_lab_prev02 + ".list"); %Input before biasfield
fileoutput_prev01=fullfile(list_dir_path + "output_"+ list_lab_prev01 + ".list"); %Output after biasfield
fileoutput_prev02=fullfile(list_dir_path + "output_"+ list_lab_prev02 + ".list"); %Output after biasfield

inputfiles_prev01 = importdata(fileinput_prev01);
inputfiles_prev02 = importdata(fileinput_prev02);
inputfiles_prevcombined = [inputfiles_prev01; inputfiles_prev02];

outputfiles_prev01 = importdata(fileoutput_prev01);
outputfiles_prev02 = importdata(fileoutput_prev02);
outputfiles_prevcombined = [outputfiles_prev01; outputfiles_prev02];

ptid_nopost4 = ['ISPY2-422450', 'ISPY2-709559'];

num_files = numel(inputfiles_prevcombined);
for k = 1:num_files
    input_k = cell2mat(inputfiles_prevcombined(k));
    output_k = cell2mat(outputfiles_prevcombined(k));
    patientID_current = cell2mat(extractBetween(input_k, 'nifty/', '/T'))
    contrast_tp = cell2mat(extractBetween(input_k, '_DCE_', '.nii.gz'));
    if ~isempty(find(ismember(patientID_current, ptid_nopost4)))
        if strcmp(contrast_tp, 'post1')
            fprintf(fileinput, '%s\n', strrep(input_k, 'post1', 'post3'));
            fprintf(fileoutput, '%s\n', strrep(output_k, 'post1', 'post3'));
            
        elseif strcmp(contrast_tp, 'post2')
            fprintf(fileinput, '%s\n', strrep(input_k, 'post2', 'post4'));
            fprintf(fileoutput, '%s\n', strrep(output_k, 'post2', 'post4'));

        end
    else
        if strcmp(contrast_tp, 'post1')
            fprintf(fileinput, '%s\n', strrep(input_k, 'post1', 'post3'));
            fprintf(fileoutput, '%s\n', strrep(output_k, 'post1', 'post3'));
            
        elseif strcmp(contrast_tp, 'post2')
            fprintf(fileinput, '%s\n', strrep(input_k, 'post2', 'post3'));
            fprintf(fileoutput, '%s\n', strrep(output_k, 'post2', 'post3'));

        end
    end
end

