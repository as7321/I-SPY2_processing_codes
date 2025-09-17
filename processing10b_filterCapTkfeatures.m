clc;
clear;

list_dir_path = "/home/as7321/Data/I-SPY2_processed/list_dir/";
list_lab_inputv01 = "feature_files_compiled";
list_lab_inputv02 = "feature_files_noftv_compiled";

fileinputv01 = strcat(list_dir_path, list_lab_inputv01, '.list');
fileinputv02 = strcat(list_dir_path, list_lab_inputv02, '.list');
input_compiled_names = [fileinputv01, fileinputv02];

output_dir = "/data/cbig/I-SPY2/shared/features_processed_v01/";
save_table = 1; %Whether the results should be saved or not
if ~exist(output_dir, "dir")
    mkdir(output_dir);
end

feats_to_remove = {};
%feats_to_remove = {'T1_E_Histogram_Bins_128_Bins_128_QuartileCoefficientOfVariation'};


feats_to_SA = {}; %Sign adjust
%feats_to_SA = {'T1_E_NGTDM_Strength','T1_E_GLCM_Bins_128_Radius_1_Homogeneity','T1_E_GLCM_Bins_128_Radius_1_Entropy','T1_E_GLSZM_Bins_128_Radius_1_ZoneSizeMean',...
%    'T1_E_GLSZM_Bins_128_Radius_1_LargeZoneEmphasis', 'T1_E_GLSZM_Bins_128_Radius_1_LargeZoneHighGreyLevelEmphasis', 'T1_E_GLSZM_Bins_128_Radius_1_LargeZoneLowGreyLevelEmphasis',...
%    'T1_E_GLRLM_Bins_128_Radius_1_LongRunEmphasis', 'T1_E_GLRLM_Bins_128_Radius_1_LongRunHighGreyLevelEmphasis', 'T1_E_GLRLM_Bins_128_Radius_1_LongRunLowGreyLevelEmphasis'};

% There are two types of files- with and without ftv
for session = 1:2 % One for with ftv and one without ftv
    input_files_compiled = importdata(input_compiled_names(session));
    num_files = size(input_files_compiled, 1);
    for k = 1:num_files
        output_filename = strcat(output_dir, "NaNdetails.xlsx");
        sheetname = cell2mat(extractBetween(input_files_compiled{k}, "compiled/", ".csv"));
        findNaNs(input_files_compiled{k}, feats_to_remove, output_filename, sheetname, save_table)
    end
end


function findNaNs(feature_file, featsToRemove, outputfilename, sheetname, savetable)
%purpose: to remove undesired features, remove nans and constant features,
%z-score, sign-adjust, and filter on kurtosis/skewness/iqr
%output: saved csv file in savedir with processed features!

% feature_file:
% each column is a different feature, and each row is a different case

feature_xlsx = readtable(feature_file); %read in the spreadsheet
cases = feature_xlsx.SubjectID; % case numbers are first column

feature_labels = feature_xlsx.Properties.VariableNames; % headers of the xlsx file: {case, feature 1, etc...};

feature_values = readmatrix(feature_file);
feature_values = feature_values(:,2:end); % just the feature values without cases or headers
feature_values(isnan(feature_values)) = nan; % ensure all cells same data type ('NaN' -> nan)


%% Remove features that aren't desired
disp("Remove features that aren't relevant")
if ~isempty(featsToRemove)
    numfeats = numel(featsToRemove);
    idxremove = [];
    for l = 1:numfeats
        idx_temp = find(contains(feature_labels,featsToRemove{l}));
        idxremove = [idx_temp,idxremove];
    end
    feature_values(:,idxremove-1) =[];
    feature_labels(:,idxremove) = [];
end


%% Find features with NaNs

disp("Finding features and cases with NaNs...")

nan_sheet = isnan(feature_values);
cases_nonan = cases;
feature_values_nonan = feature_values;
%Find cases (patient datasets) with NaNs
%{
[R,C]=find(isnan(feature_values));
nan_cases= unique(R);
nan_feats = unique(C);

nans_in_feats = sum(nan_sheet);
nans_in_pts = sum(nan_sheet, 2);

% right now, these next two lines assume that you want to get rid of any
% feature that has a NaN value for any case.
feature_values_nonan(:,nan_feats)=[];
feature_labels(:,nan_feats+1) =[];

% this commented part removes NaNs in a bit of a more creative way (like if
% a feature is NaN for less than 10% of cases, remove those cases but keep
% the feature

%{
if numel(nan_cases) >= numel(cases)*0.1
    disp("removing features for which 10%> of cases have NaNs...")
    feature_values_nonan(:,nan_feats)=[];
    feature_labels(:,nan_feats+1) =[];
elseif numel(nan_cases) < numel(cases)*0.1
    disp("removing cases with NaNs...")
    cases_nonan(:,nan_cases)=[];
    feature_values_nonan(nan_cases,:)=[];
end
%}

%{
[nan_count, feat_idx] = groupcounts(C); %number of nan cases for each feature
idxremove = feat_idx(nan_count > 0.05*numel(cases));
feature_values(:,idxremove) =[];
feature_labels(:,idxremove+1) = [];
%}



feature_values_selected = finalFeatures1;
feature_labels_selected = finalFeatureLabels;

%}

cs_new = strings(numel(cases_nonan), 1);
for pt = 1:numel(cases_nonan)
    cs_new(pt) = string(cases_nonan(pt));
end
%temp_array = [cs_new,feature_values_selected];
%features_vals_final_table = array2table(temp_array,'VariableNames',feature_labels_selected);

%% Save the processed features as a table
temp_array = [cs_new, nan_sheet];
nan_table = array2table(temp_array, 'VariableNames',feature_labels);

if savetable ==1
    disp("saving processed features as csv...")
    writetable(nan_table, outputfilename, "Sheet",sheetname);
end

end