%Input three excel sheets - 1) containing patient ID of all patients present
%in final feature extraction files, 2) containing manufacturer name and
%field strength corresponding to all these patients, 3) containing z-axis slice thickness of patients. Make an output excel
%file with sheet containing manufacturer, field strength,  corresponding
%to each patient. One sheet will be for T0 and one for T1.

input_feature_filename = '/groups/dk3360_gp/projects/I-SPY2/shared/features_processed_v02/T0_PE.csv';
input_scanner_info_filename = '/groups/dk3360_gp/projects/I-SPY2/shared/Documents/img_resolution_infov02.xlsx';
input_resolution_filename = '/groups/dk3360_gp/projects/I-SPY2/shared/Documents/img_resolution_info.xlsx';
input_resolution_sheetnames = ["ResolutionInfo-T0", "ResolutionInfo-T1"];
output_details_filename = '/groups/dk3360_gp/projects/I-SPY2/shared/Documents/combat_input_file.xlsx';
output_sheet_name = ["T0_batch_effects_v02", "T1_batch_effects_v02"];
scantimept = ["T0", "T1"];

input_feature_file = readtable(input_feature_filename);
input_scanner_info = readtable(input_scanner_info_filename, "Sheet","ModelSpecs");

for i = 1:2
	input_res_file = readtable(input_resolution_filename, "Sheet", input_resolution_sheetnames(i));
	input_res_file = input_res_file(:, ["subjectID", "pixdim_z"]);
	new_sheet = input_scanner_info(strcmp(input_scanner_info.scantimept, scantimept(i)), ["patientID", "Manufacturer", "MagneticFieldStrength"]);
	new_sheet = new_sheet(ismember(new_sheet.patientID, input_feature_file.SubjectID), :);
	new_sheet_combined = innerjoin(new_sheet, input_res_file, 'LeftKeys', 'patientID', 'RightKeys', 'subjectID');
	writetable(new_sheet_combined, output_details_filename, "Sheet",output_sheet_name(i));
end
