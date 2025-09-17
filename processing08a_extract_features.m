%This code makes list - containing the names of input and output files.
%Input consists of - PatientID + T0 or T1 + 4 kinetic feature maps i.e., 8
%for each patient while output consists of 8 excel sheets for each patient.
%Two types of input files will be processed, and hence two types of output
%lists will be formed - one (original) in which the features were extracted
% after removing the area outside the ftv mask and second (withoutftv) in
% which feaures from the entire image were extracted. 

clc;
clear;

input_maps_dirname = '/data/cbig/I-SPY2/shared/kineticmaps_resampled_registered_affinecorrected_withftv_v03/';
input_maps_dirname_withoutftv = '/data/cbig/I-SPY2/shared/kineticmaps_resampled_registered_withoutftv_v03/';
output_dir_name = '/data/cbig/I-SPY2/shared/features_kineticmaps_v03/';
output_dir_name_witoutftv = '/data/cbig/I-SPY2/shared/features_kineticmaps_withoutftv_v03/';
output_dir_name_compiled = '/data/cbig/I-SPY2/shared/features_kineticmaps_compiled_v03/';
mask_dir_name = '/data/cbig/I-SPY2/shared/post_registration_affine_ftv_dilateerode/';

list_dir_path = "/home/as7321/Data/I-SPY2_processed/list_dir/";
list_lab_inputv01 = "post_kineticmaps_v03";
list_lab_inputv02 = "post_kineticmaps_noftv_v03";
list_lab_outputv01 = "feature_files_v03";
list_lab_outputv02 = "feature_files_noftv_v03"
list_lab_mask = "post_registration_affine_ftv_dilateerode";
list_lab_outputcompiledv01 = "feature_files_compiled_v03";
list_lab_outputcompiledv02 = "feature_files_noftv_compiled_v03";

patientID_to_process_list = "patientID_to_processv04.txt";
pt_id_info = readcell(list_dir_path + patientID_to_process_list);

if ~exist(output_dir_name, "dir")
    mkdir(output_dir_name);
end
if ~exist(output_dir_name_witoutftv, "dir")
    mkdir(output_dir_name_witoutftv);
end
if ~exist(output_dir_name_compiled, "dir")
    mkdir(output_dir_name_compiled);
end

num_patients = size(pt_id_info, 1);
timepoints = ["T0", "T1"];
name_kinmaps = ["PE", "SER", "WIS", "WOS"];

fileinputv01 = fopen(strcat(list_dir_path, list_lab_inputv01, '.list'), 'w');
fileoutputv01 = fopen(strcat(list_dir_path, list_lab_outputv01, '.list'), 'w');
fileinputv02 = fopen(strcat(list_dir_path, list_lab_inputv02, '.list'), 'w');
fileoutputv02 = fopen(strcat(list_dir_path, list_lab_outputv02, '.list'), 'w');
filemask = fopen(strcat(list_dir_path, list_lab_mask, '.list'), 'w');
filecompiledv01 = fopen(strcat(list_dir_path, list_lab_outputcompiledv01, '.list'), 'w');
filecompiledv02 = fopen(strcat(list_dir_path, list_lab_outputcompiledv02, '.list'), 'w');


for pt = 1:num_patients
    current_pt = pt_id_info(pt);
    for tp = 1:length(timepoints)
        for kin = 1:length(name_kinmaps)
            input_pathv01 = fullfile(input_maps_dirname, pt_id_info(pt), timepoints(tp), name_kinmaps(kin)) + ".nii.gz";
            fprintf(fileinputv01, '%s\n', input_pathv01);
            output_pathv01 = fullfile(output_dir_name, pt_id_info(pt), timepoints(tp), name_kinmaps(kin) + ".csv");
            fprintf(fileoutputv01, '%s\n', output_pathv01);
            input_pathv02 = fullfile(input_maps_dirname_withoutftv, pt_id_info(pt), timepoints(tp), name_kinmaps(kin)) + ".nii.gz";
            fprintf(fileinputv02, '%s\n', input_pathv02);
            output_pathv02 = fullfile(output_dir_name_witoutftv, pt_id_info(pt), timepoints(tp), name_kinmaps(kin) + ".csv");
            fprintf(fileoutputv02, '%s\n', output_pathv02);
            % 1. Mask path remains the same irrespective of whether the input
            % is with or without ftv
            % 2. For each patient and timepoint, 4 same mask paths will be
            % corresponding to each feature map
            mask_path = fullfile(mask_dir_name, pt_id_info(pt), pt_id_info(pt) + "_" + timepoints(tp) + "_mask.nii.gz");
            fprintf(filemask, '%s\n', mask_path);
        end
    end
end

for tp = 1:length(timepoints)
    for kin = 1:length(name_kinmaps)
        output_pathv01 = fullfile(output_dir_name_compiled, timepoints(tp) + '_' + name_kinmaps(kin) + ".csv");
        fprintf(filecompiledv01, '%s\n', output_pathv01);
        output_pathv02 = fullfile(output_dir_name_compiled, timepoints(tp) + '_' + name_kinmaps(kin) + "noftv.csv");
        fprintf(filecompiledv02, '%s\n', output_pathv02);
    end
end
