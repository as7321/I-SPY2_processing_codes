import pandas as pd
import os
import sys
import numpy as np
from scipy import stats

### The parts you need to change are all the file paths, spreadhsheet names, and results saving stuff
### Make sure you remove features that have a constant value for all cases as they throw an error!

############# USER INPUT #####################

#establish paths where your spreadsheets (features, clnical, and batch) and code are located
datapath = "/data/cbig/I-SPY2/shared/features_processed_v03_xlsx/"
#codepath = "/home/as7321/Data/Git_repositories/I-SPY2_preprocessing_codes/utils/"
clinical_path = "/home/as7321/Data/I-SPY2_processed/"
#this is the spreadsheet that contains your z-scored, sign-adjusted, generally processed features (xls format)
datfile_T0 = ["T0_PE.xlsx","T0_PEnoftv.xlsx", "T0_SER.xlsx","T0_SERnoftv.xlsx" ,"T0_WIS.xlsx","T0_WISnoftv.xlsx" , "T0_WOS.xlsx", "T0_WOSnoftv.xlsx"]
datfile_T1 = ["T1_PE.xlsx","T1_PEnoftv.xlsx", "T1_SER.xlsx","T1_SERnoftv.xlsx" ,"T1_WIS.xlsx","T1_WISnoftv.xlsx" , "T1_WOS.xlsx", "T1_WOSnoftv.xlsx"]
sheetname_dat = "Sheet1"
#this is the spreadsheet that contains your clinical and batch information in two different spreadsheets (xls format)
covfile = "combat_input_file.xlsx"
sheetname_cov='Covars'
sheetname_batch_T0 = 'T0_batch_effects'
sheetname_batch_T1 = 'T1_batch_effects'
#name of the file where your pvalues will be saved
resultsfolder = "/data/cbig/I-SPY2/shared/Check_Kruskal_wallis/manufacturer_v03/"
if not os.path.exists(resultsfolder):
    os.mkdir(resultsfolder)


for datfile in datfile_T0:
    resultsfile = os.path.splitext(datfile)[0] + ".csv"
    print(resultsfile)

    ############# CODE EXECUTES BELOW ##############

    #read in feature data (change the sheet name as needed)
    data_df = pd.read_excel(datapath+datfile, sheet_name=sheetname_dat)


    #read in clinical data (change the sheet name as needed)
    covars_df = pd.read_excel(clinical_path+covfile, sheet_name=sheetname_cov)
    covars_df.rename(columns={'Patient_ID': 'SubjectID'}, inplace =True)

    #read in batch effects to control for
    batch_df = pd.read_excel(clinical_path+covfile, sheet_name=sheetname_batch_T0)
    batch_df.rename(columns={'patientID':'SubjectID'}, inplace = True)


    merged_df = pd.merge(batch_df, data_df, on='SubjectID')
    #unique_fieldstrength = merged_df['MagneticFieldStrength'].unique()
    unique_manufacturer = merged_df['Manufacturer'].unique()
    print(unique_manufacturer)
    feature_list = data_df.keys().tolist()

    output_file =  []


    for current_key in feature_list:
        '''
        sample_1 = merged_df[merged_df['MagneticFieldStrength'] == unique_fieldstrength[0]][current_key].values
        sample_2 = merged_df[merged_df['MagneticFieldStrength'] == unique_fieldstrength[1]][current_key].values
        h_val, p_val = stats.kruskal(sample_1, sample_2)
        row = {'Feature': current_key, 'H-value': h_val, 'p-value': p_val}
        '''
        sample_1 = merged_df[merged_df['Manufacturer'] == 'GE MEDICAL SYSTEMS'][current_key].values
        sample_2 = merged_df[merged_df['Manufacturer'] ==  'SIEMENS'][current_key].values
        sample_3 = merged_df[merged_df['Manufacturer'] ==  'Philips Medical Systems'][current_key].values 
        sample_4 = merged_df[merged_df['Manufacturer'] == 'Philips Healthcare'][current_key].values

        h_val, p_val = stats.kruskal(sample_1, sample_2, sample_3)
        h_val_2, p_val_2 = stats.kruskal(sample_1, sample_2, sample_3, sample_4)
        row = {'Feature':current_key, 'H-value': h_val, 'p-value': p_val, 'H-value_withPhilipsHealthcare': h_val_2, 'P-value_withPhilipsHealthcare': p_val_2}
        output_file.append(row)

    pvalue_df = pd.DataFrame(output_file)
    pvalue_df.to_csv(resultsfolder + resultsfile)

