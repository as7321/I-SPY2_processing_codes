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
sys.path.append('/users/as7321/workstation222-MRI/Git_repositories/mamamia-AS/')
import OPNestedComBat as nested
from sklearn.cluster import KMeans as kmeans


### The parts you need to change are all the file paths, spreadhsheet names, and results saving stuff
### Make sure you remove features that have a constant value for all cases as they throw an error!

############# USER INPUT #####################

#establish paths where your spreadsheets (features, clnical, and batch) and code are located
datapath = "/groups/dk3360_gp/projects/I-SPY2/shared/features_processed_v02_xlsx/"
codepath = "/users/as7321/workstation222-MRI/Git_repositories/mamamia-AS/"
clinical_path = "/groups/dk3360_gp/projects/I-SPY2/shared/Documents/"
resultpath = "/groups/dk3360_gp/projects/I-SPY2/shared/features_harmonized_v02_withouthrher2/"
if not os.path.exists(resultpath):
    os.mkdir(resultpath)


#this is the spreadsheet that contains your z-scored, sign-adjusted, generally processed features (xls format)
timepoints = ["T0", "T1"]
kin_maps = ["PE", "SER", "WIS", "WOS"]
sheetname_dat = "Sheet1"
#this is the spreadsheet that contains your clinical and batch information in two different spreadsheets (xls format)
covfile = "combat_input_file.xlsx"
sheetname_cov='Covars'
#define which clinical variables are categorical and which are continuous
categorical_cols = []# ["HR", "HER2"]
continuous_cols = []

#read in clinical data (change the sheet name as needed) - HR and HER2
covars_df = pd.read_excel(clinical_path+covfile, sheet_name=sheetname_cov)
print(covars_df.head())

############# CODE EXECUTES BELOW ##############
for tp in timepoints:
    sheetname_batch = tp + "_batch_effects"
    #read in batch effects to control for
    batch_df = pd.read_excel(clinical_path+covfile, sheet_name=sheetname_batch)
    #batch_df = batch_df.drop(labels='patientID',axis=1)
    #write any batch pre-processing you want to do for your specific example here
    batch_df["MagneticFieldStrength"] = (batch_df["MagneticFieldStrength"] <= 1.5).astype(int)
    manufacturer_map = {'GE MEDICAL SYSTEMS': 0, 'SIEMENS': 1, 'Philips Medical Systems': 2, 'Philips Healthcare': 2}
    batch_df['Manufacturer'] = batch_df['Manufacturer'].map(manufacturer_map)
    #define the batch variables here
    batch_list = batch_df.keys().tolist()[1:]
    #combine the clinical covars and batch effects into one dataframe called 'covars'
    #covars_tp = pd.merge(batch_df, covars_df, left_on="patientID", right_on="Patient_ID")
    #covars_tp = covars_tp.drop(labels = "Patient_ID", axis =1)
    covars_tp = batch_df

    for kinmap in kin_maps:
        datfile = tp + "_" + kinmap + "noftv.xlsx"
        resultsfile = os.path.splitext(datfile)[0] + ".csv" #name of the file where your harmonized features will be saved
        #read in feature data (change the sheet name as needed) - features
        data_df = pd.read_excel(datapath+datfile, sheet_name=sheetname_dat)
        data_df = data_df.rename(columns={"SubjectID": "case"})

        #remove nans from any clinical and batch effects (cases that are missing this information)
        splitlen = len(batch_list)+len(categorical_cols)+len(continuous_cols) + 1#1 is due to patient_ID
        a = pd.merge(covars_tp, data_df, left_on="patientID", right_on="case")
        a = a.dropna()
        #a.to_csv(datapath+"Results_"+"a_check_vb.csv")
        covars = a.iloc[:, :splitlen].reset_index(drop=True)
        covars = covars.drop(labels="patientID", axis=1)
        data_df = a.iloc[:, splitlen :].reset_index(drop=True)
        caseno = data_df['case']
        data_df = data_df.drop(labels='case',axis=1)
        dat = data_df.T.apply(pd.to_numeric)
        #dat.to_csv(datapath+"Results_"+"dat_final_check.csv")
        #print(covars['Manufacturer'].value_counts())

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

        '''
        
        #print your categorical and batch info as a final check
        print(categorical_cols)
        print(batch_list)
        print(resultpath + resultsfile)
        print(covars.head())

        
        # Completing Nested ComBat
        output_df = nested.OPNestedComBat(dat, covars, batch_list, resultpath, categorical_cols=categorical_cols,continuous_cols=continuous_cols)
        
        #write the results to a csv file
        write_df = pd.concat([caseno, output_df], axis=1) 
        write_df.to_csv(os.path.join(resultpath, resultsfile))
        
        #Compute the AD test p-values to measure harmonziation performance
        test = dat.T
        print("dat.T.shape = ",test.shape)
        print("output_df.shape = ",output_df.shape)
        print("covars.shape = ",covars.shape)
        print("batch_list = ",batch_list)
        
        resultpath_pval = os.path.join(resultpath, os.path.splitext(datfile)[0]) + "/"
        if not os.path.exists(resultpath_pval):
            os.mkdir(resultpath_pval)

        nested.feature_ad(dat.T, output_df, covars, batch_list, resultpath_pval)
        # Plot kernel density plots to visualize distributions before and after harmonization
        nested.feature_histograms(dat.T, output_df, covars, batch_list, resultpath_pval)
        
