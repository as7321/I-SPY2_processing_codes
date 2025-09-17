%This code writes the clinical details (i.e., pCR) and Covars (HR / HER2). It has nothing to do with Field strength and manufacturer


input_clinical_info_filename = '/home/as7321/Data/I-SPY2_processed/ISPY2-Imaging-Cohort-1-Clinical-Data-edited.xlsx';
input_feature_filename = '/data/cbig/I-SPY2/shared/features_processed_v02/T0_PE.csv';
output_details_filename = '/home/as7321/Data/I-SPY2_processed/combat_input_file.xlsx';

clinical_info = readtable(input_clinical_info_filename);
input_feature_file = readtable(input_feature_filename);

subjectID_final = input_feature_file.SubjectID;
num_final_patients = length(subjectID_final);
%subjectID_numeric = zeros(num_final_patients, 1);
count = 1;
for i = 1:num_final_patients
    if contains(subjectID_final(i), "ACRIN")
        subjectID_numeric(i) = str2double(extractAfter(cell2mat(subjectID_final(i)), "ACRIN-6698-"));
        count = count + 1;
    elseif contains(subjectID_final(i), "SPY")
        subjectID_numeric(i) = str2double(extractAfter(cell2mat(subjectID_final(i)), "ISPY2-"));
        count = count + 1;
    end
end
count = 1;
new_table = clinical_info(ismember(clinical_info.Patient_ID, subjectID_numeric), :);
[~, sorted_indices] = ismember(subjectID_numeric, new_table.Patient_ID);
new_table_sorted = new_table(sorted_indices, :);
new_table_sorted_covars = new_table(sorted_indices, ["Patient_ID", "HR", "HER2"]);
new_table_sorted_covars.Patient_ID = subjectID_final;
writetable(new_table_sorted, output_details_filename, "Sheet","clinicaldetails");
writetable(new_table_sorted_covars, output_details_filename, "Sheet","Covars", "WriteMode","overwritesheet");



