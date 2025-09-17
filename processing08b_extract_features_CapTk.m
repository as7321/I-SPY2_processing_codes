clc;
clear;

list_dir_path = "/home/as7321/Data/I-SPY2_processed/list_dir/";
list_lab_inputv01 = "post_kineticmaps_v03";
list_lab_inputv02 = "post_kineticmaps_noftv_v03";
list_lab_outputv01 = "feature_files_v03";
list_lab_outputv02 = "feature_files_noftv_v03"
list_lab_mask = "post_registration_affine_ftv_dilateerode";
list_lab_outputcompiledv01 = "feature_files_compiled_v03";
list_lab_outputcompiledv02 = "feature_files_noftv_compiled_v03";


fileinputv01 = strcat(list_dir_path, list_lab_inputv01, '.list');
fileoutputv01 = strcat(list_dir_path, list_lab_outputv01, '.list');
fileinputv02 = strcat(list_dir_path, list_lab_inputv02, '.list');
fileoutputv02 = strcat(list_dir_path, list_lab_outputv02, '.list');
filemask = strcat(list_dir_path, list_lab_mask, '.list');
filecompiledv01 = strcat(list_dir_path, list_lab_outputcompiledv01, '.list');
filecompiledv02 = strcat(list_dir_path, list_lab_outputcompiledv02, '.list');

input_file_names = [fileinputv01, fileinputv02];
output_file_names = [fileoutputv01, fileoutputv02];
output_compiled_names = [filecompiledv01, filecompiledv02];
str_before_id = ["v03/", "v03/"];

%Define CapTk feature extraction command
captk_cmd_featurextract = '/opt/CaPTk/1.9.0/FeatureExtraction';
param_file_texture_features = '/home/as7321/Data/I-SPY2_processed/params_ISPY2_texturefeatures_370_Arunima_v01.csv'

% Case 1: each patiemt has a folder. Each folder has two sub-folders - T0 and
% T1. Each subfolder has 4 excel sheets, one for each kinetic map.
for session = 1:2 % One for with ftv and one without ftv
    input_files = importdata(input_file_names(session));
    output_files = importdata(output_file_names(session));
    mask_files = importdata(filemask);
    num_files = numel(input_files);
    output_files_compiled = importdata(output_compiled_names(session));

    for k = 1:num_files %Eight for each patient
        img_k = input_files{k};
        mask_k = mask_files{k};
        id_k = cell2mat(extractBetween(img_k, str_before_id(session), "/T"));
        out_k = output_files{k};

        [filepath, ~, ~] = fileparts(out_k);
        if ~exist(filepath, "dir")
            mkdir(filepath)
        end

        disp(['Extracting features for case ' img_k '...'])
        cmd=[captk_cmd_featurextract ' -n ' id_k ' -i ' img_k ' -o ' out_k  ' -t T1 ' ' -r 1 -m ' mask_k ' -l E -p ' param_file_texture_features];
        system(cmd)
        disp(['Saving featues in ' out_k '...'])


        %Compiled excel sheet features
        filetype = rem(k, 8);
        if filetype == 0
            filetype = 8;
        end
        out_compiled_k = output_files_compiled{filetype};
        disp(['Extracting features for case ' img_k '...'])
        cmd=[captk_cmd_featurextract ' -n ' id_k ' -i ' img_k ' -o ' out_compiled_k  ' -t T1 ' ' -r 1 -m ' mask_k ' -l E -p ' param_file_texture_features];
        system(cmd)
        disp(['Saving featues in ' out_compiled_k '...'])

    end
end

