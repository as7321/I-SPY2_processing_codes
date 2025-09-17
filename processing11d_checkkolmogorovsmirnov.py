import pandas as pd
from scipy.stats import ranksums, ttest_ind, ttest_rel, ks_2samp
import os
import sys
import numpy as np
from itertools import permutations
from sklearn.cluster import KMeans as kmeans
from scipy import stats

### The parts you need to change are all the file paths, spreadhsheet names, and results saving stuff
### Make sure you remove features that have a constant value for all cases as they throw an error!

############# USER INPUT #####################

#establish paths where your spreadsheets (features, clnical, and batch) and code are located
datapath = "/data/cbig/I-SPY2/shared/features_processed_v03_xlsx/"
clinical_path = "/home/as7321/Data/I-SPY2_processed/"
#this is the spreadsheet that contains your z-scored, sign-adjusted, generally processed features (xls format)
datfile_T0 = ["T0_PE.xlsx","T0_PEnoftv.xlsx", "T0_SER.xlsx","T0_SERnoftv.xlsx" ,"T0_WIS.xlsx","T0_WISnoftv.xlsx" , "T0_WOS.xlsx", "T0_WOSnoftv.xlsx"]
datfile_T1 = ["T1_PE.xlsx","T1_PEnoftv.xlsx", "T1_SER.xlsx","T1_SERnoftv.xlsx" ,"T1_WIS.xlsx","T1_WISnoftv.xlsx" , "T1_WOS.xlsx", "T1_WOSnoftv.xlsx"]
sheetname_dat = "Sheet1"
#this is the spreadsheet that contains your clinical and batch information in two different spreadsheets (xls format)
covfile = "combat_input_file.xlsx"
sheetname_batch_T0 = 'T0_batch_effects'
sheetname_batch_T1 = 'T1_batch_effects'
#name of the file where your pvalues will be saved
resultsfolder = "/data/cbig/I-SPY2/shared/Check_ks2samp/fieldstrength_v03/"
if not os.path.exists(resultsfolder):
    os.mkdir(resultsfolder)


for datfile in datfile_T1:
    resultsfile = os.path.splitext(datfile)[0] + ".csv"
    print(resultsfile)

    ############# CODE EXECUTES BELOW ##############

    #read in feature data (change the sheet name as needed)
    data_df = pd.read_excel(datapath+datfile, sheet_name=sheetname_dat)


    #read in batch effects to control for
    batch_df = pd.read_excel(clinical_path+covfile, sheet_name=sheetname_batch_T1)
    batch_df.rename(columns={'patientID':'SubjectID'}, inplace = True)


    merged_df = pd.merge(batch_df, data_df, on='SubjectID')
    unique_fieldstrength = merged_df['MagneticFieldStrength'].unique()
    #unique_manufacturer = merged_df['Manufacturer'].unique()
    #print(unique_manufacturer)
    feature_list = data_df.keys().tolist()

    output_file =  []


    for current_key in feature_list:
        
        sample_1 = merged_df[merged_df['MagneticFieldStrength'] == unique_fieldstrength[0]][current_key].values
        sample_2 = merged_df[merged_df['MagneticFieldStrength'] == unique_fieldstrength[1]][current_key].values
        res = stats.ks_2samp(sample_1, sample_2)
        

        row = {'Feature': current_key, 'Statistics': res.statistic, 'p-value': res.pvalue, 'location': res.statistic_location, 'sign': res.statistic_sign}
        
        output_file.append(row)

    pvalue_df = pd.DataFrame(output_file)
    pvalue_df.to_csv(resultsfolder + resultsfile)

#batch_df = batch_df.drop(labels='patientID',axis=1)
#write any batch pre-processing you want to do for your specific example here
#batch_df.resolution = kmeans(n_clusters=3, random_state=0).fit(batch_df.resolution.to_numpy().reshape(-1,1)).labels_
#batch_df["MagneticFieldStrength"] = (batch_df["MagneticFieldStrength"] <= 1.5).astype(int)
#batch_df.to_csv(datapath+"Results_"+"batch_df_after_categorizing_check.csv")
#define the batch variables here
#batch_list = batch_df.keys().tolist()
#combine the clinical covars and batch effects into one dataframe called 'covars' 
#covars = pd.concat([batch_df,covars_df],axis=1) 



'''
#remove nans from any clinical and batch effects (cases that are missing this information)
splitlen = len(batch_list)+len(categorical_cols)+len(continuous_cols)
a = pd.concat([covars,data_df],axis=1).dropna()
#a.to_csv(datapath+"Results_"+"a_check_vb.csv")
print(splitlen)
covars = a.iloc[:, :splitlen].reset_index(drop=True)
data_df = a.iloc[:, splitlen :].reset_index(drop=True)
caseno = data_df['case']
data_df = data_df.drop(labels='case',axis=1)
dat = data_df.T.apply(pd.to_numeric)
#dat.to_csv(datapath+"Results_"+"dat_final_check.csv")

print(batch_df['Manufacturer'].value_counts())
print(batch_df['MagneticFieldStrength'].value_counts())

'''
