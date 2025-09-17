clc;
clear;

list_dir_path = "/home/as7321/Data/I-SPY2_processed/list_dir/";
%output_dir_name_v01 = "/data/cbig/I-SPY2/shared/pre_resampling_ftv_affinecorrected/"
%output_dir_name_v02 = "/data/cbig/I-SPY2/shared/post_resampling_ftv_affinecorrected/"
output_dir_name_v03 = "/data/cbig/I-SPY2/shared/pre_resampling_ftv_affinecorrected_mask/"
patientID_to_process_list = "patientID_to_processv03.txt"
pt_id_info = readcell(list_dir_path + patientID_to_process_list);

%list_lab_current = 'resampled_ftv_masks_affinecorrected';%corresponding to post resampling
list_lab_prev = 'resampling'; %This is to get the file names easily. With biasfield, a lot of changes in filenames would be needed
%list_lab_between = 'ftv_masks_affinecorrected';%Corresponding to pre-resampling (only affine correction)
list_lab_between02 = 'ftv_masks_affinecorrected_extracted'; %Corresponding to pre-resampling after mask extraction 

filemask_input = importdata(list_dir_path + 'mask_' + list_lab_prev + ".list");
%filemask_output_namev02 = fullfile(list_dir_path + "mask_" + list_lab_current + ".list");
%filemask_output_namev01 = fullfile(list_dir_path + "mask_" + list_lab_between + ".list");
filemask_output_namev03 = fullfile(list_dir_path + "mask_" + list_lab_between02 + ".list");


%fileoutputv01 = fopen(filemask_output_namev01, 'w')
%fileoutputv02 = fopen(filemask_output_namev02, 'w');
fileoutputv03 = fopen(filemask_output_namev03, 'w');
num_files = length(filemask_input);

for i = 1:num_files
    file_path_prev = cell2mat(filemask_input(i, :));
    %file_path_current = strrep(file_path_prev, 'post_resampling', 'post_resampling_ftv_affinecorrected');
    %file_path_between = strrep(file_path_prev, 'post_resampling', 'pre_resampling_ftv_affinecorrected');
    file_path_between02 = strrep(file_path_prev, 'post_resampling', 'pre_resampling_ftv_affinecorrected_mask');
    %fprintf(fileoutputv02, '%s\n', file_path_current);
    %fprintf(fileoutputv01, '%s\n', file_path_between);
    fprintf(fileoutputv03, '%s\n', file_path_between02);
end

num_patients = size(pt_id_info, 1);
if ~exist(output_dir_name_v03, "dir")
    mkdir(output_dir_name_v03);
end
for pt = 1:num_patients
    output_path_current = output_dir_name_v03 + cell2mat(pt_id_info(pt));
    if ~exist(output_path_current, "dir")
        mkdir(output_path_current);
    end
    % output_path_between = output_dir_name_v01 + cell2mat(pt_id_info(pt));
    % if ~exist(output_path_between, "dir")
    %     mkdir(output_path_between);
    % end
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

patientID_to_process_list = "patientID_bothbreast_to_processv01.txt"
pt_id_info = readcell(list_dir_path + patientID_to_process_list);

list_lab_prev = 'resampling_bothbreast'
filemask_input = importdata(list_dir_path + 'mask_' + list_lab_prev + ".list");
num_files = length(filemask_input);

for i = 1:num_files
    file_path_prev = cell2mat(filemask_input(i, :));
    %file_path_current = strrep(file_path_prev, 'post_resampling', 'post_resampling_ftv_affinecorrected');
    %file_path_between = strrep(file_path_prev, 'post_resampling', 'pre_resampling_ftv_affinecorrected');
    file_path_between02 = strrep(file_path_prev, 'post_resampling', 'pre_resampling_ftv_affinecorrected_mask');
    %fprintf(fileoutputv02, '%s\n', file_path_current);
    %fprintf(fileoutputv01, '%s\n', file_path_between);
    fprintf(fileoutputv03, '%s\n', file_path_between02);
end

num_patients = size(pt_id_info, 1);
for pt = 1:num_patients
    output_path_current = output_dir_name_v03 + cell2mat(pt_id_info(pt));
    if ~exist(output_path_current, "dir")
        mkdir(output_path_current);
    end
    % output_path_between = output_dir_name_v01 + cell2mat(pt_id_info(pt));
    % if ~exist(output_path_between, "dir")
    %     mkdir(output_path_between);
    % end
end