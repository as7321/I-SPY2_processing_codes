clc;
clear;

list_dir_path = "/home/as7321/Data/I-SPY2_processed/list_dir/";
list_lab_inputv01 = "feature_files_compiled_v03";
list_lab_inputv02 = "feature_files_noftv_compiled_v03";

fileinputv01 = strcat(list_dir_path, list_lab_inputv01, '.list');
fileinputv02 = strcat(list_dir_path, list_lab_inputv02, '.list');
input_compiled_names = [fileinputv01, fileinputv02];

output_dir = "/data/cbig/I-SPY2/shared/features_processed_v03/";
save_table = 1; %Whether the results should be saved or not
if ~exist(output_dir, "dir")
    mkdir(output_dir);
end


feats_to_remove = {} %{'T1_E_Histogram_Bins_128_Bins_128_QuartileCoefficientOfVariation'};


feats_to_SA = {}; %Sign adjust
%feats_to_SA = {'T1_E_NGTDM_Strength','T1_E_GLCM_Bins_128_Radius_1_Homogeneity','T1_E_GLCM_Bins_128_Radius_1_Entropy','T1_E_GLSZM_Bins_128_Radius_1_ZoneSizeMean',...
%    'T1_E_GLSZM_Bins_128_Radius_1_LargeZoneEmphasis', 'T1_E_GLSZM_Bins_128_Radius_1_LargeZoneHighGreyLevelEmphasis', 'T1_E_GLSZM_Bins_128_Radius_1_LargeZoneLowGreyLevelEmphasis',...
%    'T1_E_GLRLM_Bins_128_Radius_1_LongRunEmphasis', 'T1_E_GLRLM_Bins_128_Radius_1_LongRunHighGreyLevelEmphasis', 'T1_E_GLRLM_Bins_128_Radius_1_LongRunLowGreyLevelEmphasis'};
visFigs = 1; %Whether to view heatmap or not

% There are two types of files- with and without ftv
for session = 1:2 % One for with ftv and one without ftv
    input_files_compiled = importdata(input_compiled_names(session));
    num_files = size(input_files_compiled, 1);
    for k = 1%:num_files
        output_filename = strcat(output_dir, extractAfter(input_files_compiled{k}, "compiled_v03/"))
        processFeatures(input_files_compiled{k}, feats_to_remove, feats_to_SA, output_filename, visFigs, save_table)
    end
end


function processFeatures(feature_file, featsToRemove, featsToSA, outputfilename, visFigs, savetable)
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
%feature_values  = cell2mat(feature_values); % convert cell array of feature values to matrix for easier processing


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


%% Remove features with NaNs

disp("removing features or cases with NaNs...")
%Find cases (patient datasets) with NaNs
[R,C]=find(isnan(feature_values));
nan_cases= unique(R);
nan_feats = unique(C);

cases_nonan = cases;
feature_values_nonan = feature_values;

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

% now check for features that are all a constant value (IQR=0 for these)
disp("removing features with constant value (IRQ=0)...")
test_iqr = iqr(feature_values_nonan);
idx_iqr_zero = find(test_iqr==0);
feature_values_nonan(:,idx_iqr_zero)=[];
feature_labels(:,idx_iqr_zero+1) =[];

%Note: features with just one value all the way down will throw an error
%during harmonization, so you want to get rid of these! Plus they don't add
%information if they're just constant for all cases....
%}



%% Z-score the feature vector
disp("Z-score the features...")
feature_values_zscore = zscore(feature_values_nonan);


%% Sign-adjust the feature vector
disp("Sign adjust the features for increasing order of heterogeneity...")
feature_values_sa = feature_values_zscore; %sa = sign-adjust

%{
Here are features we want to sign-adjust (according to Belenky et al.):
Strength
- Homogeneity (not found)
- GLCM Entropy
- ZoneSizeMean
- LargeZoneEmphasis
- LargeZoneHighGreyLevelEmphasis
- LargeZoneLowGreyLevelEmphasis
- LongRunEmphasis
- LongRunHighGreyLevelEmphasis
- LongRunLowGreyLevelEmphasis

%}

if ~isempty(featsToSA)
    numfeats = numel(featsToSA);
    idxSA = [];
    for l = 1:numfeats
        idx_temp = find(contains(feature_labels,featsToSA{l}));
        idxSA = [idxSA, idx_temp];
    end
    feature_values_sa(:,idxSA-1) = feature_values_sa(:,idxSA-1).*(-1);
end


%% Remove features with featSkew > 10|| featIQR <= 1|| featKurtosis>15

% Note: this step is done after harmonization now, so I've excluded it from
% this script but left the code commented in case someone wants to do this
% filtering along with all the other processing before harmonzition. 
% 
% 
%%
% *IF SOMEONE WANTS TO INLUDE IT, CHANGE THE IF STATMENT BELOW*


disp("Manually filter features based on skewness, kurtosis, and IQR...")

finalFeatures1=[];
finalFeatureLabels = {};
finalFeatureLabels{1,1} = feature_labels{1,1};
Include=[];
doNotInclude=[];
[R, C]= size(feature_values_zscore);
count=1;
for i=1:C
    Feature= feature_values_sa(:,i);
    featIQR= iqr(Feature);
    featKurt= kurtosis(Feature);
    featSkew= abs(skewness(Feature));
    %if  featSkew > 10|| featIQR >= 1|| featKurt>15
    if  featSkew < 0 %featSkew > 10|| featKurt>15
        doNotInclude= [doNotInclude; i];

    else
        count = count+1;
        Include=[Include; i];
        finalFeatures1 = [finalFeatures1, Feature];
        finalFeatureLabels{1,count} = feature_labels{1,i+1};
    end

end
%}
feature_values_selected = finalFeatures1;
feature_labels_selected = finalFeatureLabels;



%% Plot a heatmap of the features
cs_new = strings(numel(cases_nonan), 1);
for pt = 1:numel(cases_nonan)
    cs_new(pt) = string(cases_nonan(pt));
end
temp_array = [cs_new,feature_values_selected];
features_vals_final_table = array2table(temp_array,'VariableNames',feature_labels_selected);
if visFigs

    disp("Plot heatmaps of final features...")
    % plot all the features
    figure('Renderer', 'painters', 'Position', [10 10 1900 1000])
    h = heatmap(feature_values_selected.','YDisplayLabels',feature_labels_selected(2:end));
    %colormap(mymap)
    colormap('jet')
    Ax = gca;
    Ax.XDisplayLabels = nan(size(Ax.XDisplayData));
    caxis([-5 5])
    title('All Features')

    % plot just the intensity features (manually check indices)
    idx = find(contains(feature_labels_selected,'Intensity'));
    intens_feats = feature_values_selected(:,idx-1);
    figure('Renderer', 'painters', 'Position', [10 10 1900 700])
    h = heatmap(intens_feats.','YDisplayLabels',feature_labels_selected(1,idx));
    %colormap(mymap)
    colormap('jet')
    Ax = gca;
    Ax.XDisplayLabels = nan(size(Ax.XDisplayData));
    title('Intensity Features')


    % plot just the histogram features (manually check indices)
    figure('Renderer', 'painters', 'Position', [10 10 1900 1000])
    idx = find(contains(feature_labels_selected,'Histogram'));
    idx = idx(idx<size(feature_values_selected, 2));
    hist_feats = feature_values_selected(:,idx-1);
    h = heatmap(hist_feats.','YDisplayLabels',feature_labels_selected(1,idx));
    %colormap(mymap)
    colormap('jet')
    Ax = gca;
    Ax.XDisplayLabels = nan(size(Ax.XDisplayData));
    title('Histogram Features')

    % plot just the morphologic features (manually check indices)
    figure('Renderer', 'painters', 'Position', [10 10 1900 700])
    idx = find(contains(feature_labels_selected,'Morphologic'));
    idx = idx(idx<size(feature_values_selected, 2));
    hist_feats = feature_values_selected(:,idx-1);
    h = heatmap(hist_feats.','YDisplayLabels',feature_labels_selected(1,idx));
    %colormap(mymap)
    colormap('jet')
    Ax = gca;
    Ax.XDisplayLabels = nan(size(Ax.XDisplayData));
    title('Morphologic Features')

    % plot just the GLSZM features
    figure('Renderer', 'painters', 'Position', [10 10 1900 700])
    idx = find(contains(feature_labels_selected,'GLSZM'));
    idx = idx(idx<size(feature_values_selected, 2));
    hist_feats = feature_values_selected(:,idx-1);
    h = heatmap(hist_feats.','YDisplayLabels',feature_labels_selected(1,idx));
    %colormap(mymap)
    colormap('jet')
    Ax = gca;
    Ax.XDisplayLabels = nan(size(Ax.XDisplayData));
    title('GLSZM Features')

end
%% Save the processed features as a table

if savetable ==1
    disp("saving processed features as csv...")
    writetable(features_vals_final_table, outputfilename);
    %writetable(features_vals_final_table,fullfile(savedir,sprintf("%s_features_processed.csv",savelab)));
end

end