%Input two excel sheets - 1) containing patient ID of all patients present
%in final feature extraction files, 2) containing manufacturer name and
%field strength corresponding to all these patients. Make an output excel
%file with sheet containing manufacturer and field strength corresponding
%to each patient. One sheet will be for T0 and one for T1. 

input_feature_filename = '/data/cbig/I-SPY2/shared/features_processed_v02/T0_PE.csv';
input_scanner_info_filename = '/home/as7321/Data/I-SPY2_processed/img_resolution_infov02.xlsx';
output_details_filename = '/home/as7321/Data/I-SPY2_processed/combat_input_file.xlsx';
output_sheet_name = ["T0_batch_effects", "T1_batch_effects"];
scantimept = ["T0", "T1"];

input_feature_file = readtable(input_feature_filename);
input_scanner_info = readtable(input_scanner_info_filename, "Sheet","ModelSpecs");

for i = 1:2
    new_sheet = input_scanner_info(strcmp(input_scanner_info.scantimept, scantimept(i)), ["patientID", "Manufacturer", "MagneticFieldStrength"]);
    new_sheet = new_sheet(ismember(new_sheet.patientID, input_feature_file.SubjectID), :);
    writetable(new_sheet, output_details_filename, "Sheet",output_sheet_name(i));
end
