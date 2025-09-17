% Form list
% Input file path - T0(pre, post1, post2), T1 (pre, post1, post2)
clc;
clear;

list_dir_path = "/home/as7321/Data/I-SPY2_processed/list_dir/";
output_dir_name = "/data/cbig/I-SPY2/shared/post_biasfield_correction/"
input_orig_nii_list = "input_orig_pre.list";
patientID_to_process_list = "patientID_to_processv03.txt"
pt_id_info = readcell(list_dir_path + patientID_to_process_list);
list_lab = 'biasfield';

complete_nii_pre_filelist = importdata(list_dir_path + input_orig_nii_list);
fileinput_name = fullfile(list_dir_path + "input_" + list_lab + ".list");
fileoutput_name = fullfile(list_dir_path + "output_" + list_lab + ".list");
filemask_name = fullfile(list_dir_path + "mask_" + list_lab + ".list");
fileinput = fopen(fileinput_name, 'w');
fileoutput = fopen(fileoutput_name, 'w');
filemask = fopen(filemask_name, 'w');

num_files_orig = size(complete_nii_pre_filelist, 1);
for i = 1:num_files_orig
    patient_path_current = cell2mat(complete_nii_pre_filelist(i))
    patientID_current = cell2mat(extractBetween(patient_path_current, 'nifty/', '/T'))
    if ~isempty(find(ismember(patientID_current, pt_id_info)))
        current_timepoint = cell2mat(extractBetween(patient_path_current, '/T', '/'));
        if strcmp(current_timepoint, '0') || strcmp(current_timepoint, '1')
            fprintf(fileinput, '%s\n', patient_path_current); %T0 pre
            fprintf(fileinput, '%s\n', strrep(patient_path_current, 'pre', 'post1'));
            fprintf(fileinput, '%s\n', strrep(patient_path_current, 'pre', 'post2'));

            current_output = output_dir_name + patientID_current + "/" + patientID_current + "_T" + current_timepoint + "_pre.nii.gz"
            fprintf(fileoutput, '%s\n', current_output); %T0 pre
            fprintf(fileoutput, '%s\n', strrep(current_output, 'pre', 'post1'));
            fprintf(fileoutput, '%s\n', strrep(current_output, 'pre', 'post2'));

            current_mask = strrep(patient_path_current,'DCE_pre', 'mask');
            fprintf(filemask, '%s\n', current_mask);
        end
    end
end

num_patients = size(pt_id_info, 1);
for pt = 1:num_patients
    output_path_current = output_dir_name + cell2mat(pt_id_info(pt));
    if ~exist(output_path_current, "dir")
        mkdir(output_path_current);
    end
end



