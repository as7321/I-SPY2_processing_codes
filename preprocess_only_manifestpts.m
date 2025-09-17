clc;
clear;
ACRIN_patients_path_file_name = '/home/as7321/Data/I-SPY2_processed/complete_ACRIN_cohort_DCE_mask_path.xlsx';
complete_patients_path_file_name = '/home/as7321/Data/I-SPY2_processed/complete_cohort_DCE_mask_path.xlsx';
acrin_pts = readtable(ACRIN_patients_path_file_name);
total_pts = readtable(complete_patients_path_file_name);

acrin_ptIDs = acrin_pts.patientID;
all_ptIDs = total_pts.patientID;

count_newpts = 0;
idx_newpts = [];
idx_newpts_withT0T1 = [];
count_newpts_withT0T1 = 0;

for i = 1:size(acrin_pts, 1)
    idx = find(strcmp(acrin_ptIDs(i), all_ptIDs));
    if(isempty(idx))
        count_newpts = count_newpts + 1;
        idx_newpts = [idx_newpts, i];
        if acrin_pts.T0present(i) == 1 && acrin_pts.T1present(i) == 1
            idx_newpts_withT0T1 = [idx_newpts_withT0T1, i];
            count_newpts_withT0T1 = count_newpts_withT0T1 + 1;
        end
    end
end