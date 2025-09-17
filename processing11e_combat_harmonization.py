import pandas as pd
import neuroCombat as nC
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
from scipy.stats import ranksums, ttest_ind, ttest_rel, ks_2samp
import os
import sys
import numpy as np
from itertools import permutations
# you may have to point python to the path where OPNested ComBat is located
sys.path.append('/home/as7321/Data/Git_repositories/I-SPY2_preprocessing_codes/utils')
import OPNestedComBat as nested
from sklearn.cluster import KMeans as kmeans


### The parts you need to change are all the file paths, spreadhsheet names, and results saving stuff
### Make sure you remove features that have a constant value for all cases as they throw an error!

############# USER INPUT #####################

#establish paths where your spreadsheets (features, clnical, and batch) and code are located
datapath = "/data/cbig/I-SPY2/shared/features_processed_v02_xlsx/"
#datapath = "H:/Work/git_repository/radiomics_captk_pipeline/Testing/features/"
codepath = "/home/as7321/Data/Git_repositories/I-SPY2_preprocessing_codes/utils/"
clinical_path = "/home/as7321/Data/I-SPY2_processed/"
#codepath = "Z:/home/slavkovk/Code/opnested-combat-main/"
#this is the spreadsheet that contains your z-scored, sign-adjusted, generally processed features (xls format)
datfile = "T0_PE.xlsx"
#datfile = "first_postcontrast_features_processed_n295_notfiltered.xls"
#sheetname_dat = 'processed_noHarm_features'
sheetname_dat = "Sheet1"
#this is the spreadsheet that contains your clinical and batch information in two different spreadsheets (xls format)
covfile = "combat_input_file.xlsx"
sheetname_cov='Covars'
sheetname_batch = 'T0_batch_effects'
#name of the file where your harmonized features will be saved
resultsfolder = "Results_after_harm_v02"
resultsfile = os.path.splitext(datfile)[0] + ".csv"
print(resultsfile)
#define which clinical variables are categorical and which are continuous
categorical_cols = ["HR", "HER"]
continuous_cols = []

############# CODE EXECUTES BELOW ##############

#read in feature data (change the sheet name as needed)
data_df = pd.read_excel(datapath+datfile, sheet_name=sheetname_dat)
data_df = data_df.rename(columns={"SubjectID": "case"})
#data_df.to_csv(codepath+"Results"+"data_df_check_vb.csv")
#data_df.to_csv(datapath+"Results_"+"data_df_check_vb.csv")

#read in clinical data (change the sheet name as needed)
covars_df = pd.read_excel(clinical_path+covfile, sheet_name=sheetname_cov)
#drop the 'case' column so that you only have the clinical values
covars_df = covars_df.drop(labels='Patient_ID',axis=1)


#read in batch effects to control for
batch_df = pd.read_excel(clinical_path+covfile, sheet_name=sheetname_batch)
batch_df = batch_df.drop(labels='patientID',axis=1)
#write any batch pre-processing you want to do for your specific example here
#batch_df.resolution = kmeans(n_clusters=3, random_state=0).fit(batch_df.resolution.to_numpy().reshape(-1,1)).labels_
batch_df["MagneticFieldStrength"] = (batch_df["MagneticFieldStrength"] <= 1.5).astype(int)
#batch_df.to_csv(datapath+"Results_"+"batch_df_after_categorizing_check.csv")
#define the batch variables here
batch_list = batch_df.keys().tolist()
#combine the clinical covars and batch effects into one dataframe called 'covars' 
covars = pd.concat([batch_df,covars_df],axis=1) 



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
# # FOR GMM COMBAT VARIANTS:
# # Adding GMM Split to batch effects
gmm_df = nested.GMMSplit(dat, caseno, codepath)
#gmm_df.to_csv(codepath+resultsfolder+"/gmm_check_vb.csv")
#gmm_df_merge = covars_df.merge(gmm_df, right_on='Patient',left_on='resolution')
#gmm_df_merge.to_csv(codepath+"Results"+"/gmm_merge_check_vb.csv")
covars['GMM'] = gmm_df['Grouping'] #gmm_df_merge['Grouping']
covars.to_csv(datapath+"Results_"+"covars_final_check.csv")


# EXECUTING OPNESTED-GMM COMBAT
# Here we add the newly generated GMM grouping to the list of categorical variables that will be protected during
# harmonization
categorical_cols = categorical_cols + ['GMM']

#print your categorical and batch info as a final check
print(categorical_cols)
print(continuous_cols)
print(batch_list)
print(datapath+resultsfolder)




# Completing Nested ComBat
output_df = nested.OPNestedComBat(dat, covars, batch_list, datapath+resultsfolder, categorical_cols=categorical_cols,
                                  continuous_cols=continuous_cols)
#write the results to a csv file
write_df = pd.concat([caseno, output_df], axis=1) 
write_df.to_csv(datapath+resultsfolder+'/'+resultsfile)

#Compute the AD test p-values to measure harmonziation performance
test = dat.T
#print("dat.T.shape = ",test.shape)
#print("output_df.shape = ",output_df.shape)
#print("covars.shape = ",covars.shape)
#print("batch_list = ",batch_list)

nested.feature_ad(dat.T, output_df, covars, batch_list, datapath+resultsfolder)
# Plot kernel density plots to visualize distributions before and after harmonization
nested.feature_histograms(dat.T, output_df, covars, batch_list, datapath+resultsfolder)
'''
