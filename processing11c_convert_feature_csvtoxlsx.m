input_folder_name = "/data/cbig/I-SPY2/shared/features_processed_v03/";
output_folder_name = "/data/cbig/I-SPY2/shared/features_processed_v03_xlsx/";

if ~exist(output_folder_name, 'dir')
    mkdir(output_folder_name);
end

csv_files = dir(fullfile(input_folder_name, '*.csv'));
for i = 1:length(csv_files)
    csv_file = fullfile(input_folder_name, csv_files(i).name);
    data = readtable(csv_file);
    [~, base_name, ~] = fileparts(csv_files(i).name); % Extract the file name without extension
    xlsx_file = fullfile(output_folder_name, [base_name, '.xlsx']);
    writetable(data, xlsx_file);
end