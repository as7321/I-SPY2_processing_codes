clc;
clear;
full_data_folder_path = '/data/cbig/I-SPY2/Data/manifest-1639499422270/ACRIN-6698';
patients_path_file_name = '/home/as7321/Data/I-SPY2_processed/complete_ACRIN_cohort_DCE_mask_path.xlsx';
col = ["patientID","T0present","T0Path" "T0DCEpath","T0MaskPath","T1present","T1Path","T1DCEpath","T1MaskPath","T2present","T2Path", "T2DCEpath", "T2MaskPath","T3present","T3path", "T3DCEPath", "T3MaskPath"];
DCE_time = [{'T0'}, {'T1'}, {'T2'}, {'T3'}];
patient_count = 0;


%patients_folder_struct = dir(cell2mat(fullfile(full_data_folder_path))); %Patient IDs
patients_folder_struct = dir(full_data_folder_path)
patients_folder_names = {patients_folder_struct(3:end-1).name};
num_patients = size(patients_folder_names, 2);
path_details_table = cell(num_patients, 17);
disp(num_patients)
for patients_num = 1:num_patients %Patient folder
    patient_count = patient_count +1;
    row = cell(1,17);
    count = 0;
    patient_ID = patients_folder_names(patients_num);
    patient_folder_name = cell2mat(fullfile(full_data_folder_path, patient_ID));
    patient_folder_files = dir(patient_folder_name);
    row(1,1) = {patient_ID};
    for time_point = 1:size(DCE_time, 2)
        mri_time = DCE_time(time_point);
        if any(contains({dir(patient_folder_name).name}, mri_time))
            patient_time_file = patient_folder_files(contains({dir(patient_folder_name).name}, mri_time)).name;
            patient_time_path = fullfile(patient_folder_name, patient_time_file);
            temp_files = {dir(patient_time_path).name};
            DCE_file_name = temp_files(contains(temp_files, 'original DCE'));
            Mask_file_name = temp_files(contains(temp_files, 'Analysis'));
            img_present = 1;
            if (isempty(DCE_file_name))
                DCE_file_name = {'NA'};
                Mask_file_name = {'NA'};
                img_present = 0;
            end
            row(1,2+count:2+count+3) = [img_present, patient_time_path, DCE_file_name, Mask_file_name];
        else
            row(1,2+count:2+count+3) = [{0}, {0}, {0}, {0}];
        end
        count = count + 4;
    end
path_details_table(patient_count, :) = [row];
end

T = cell2table(path_details_table, "VariableNames", col);
writetable(T, patients_path_file_name);

