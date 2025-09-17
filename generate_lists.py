import os 

input_dir = '/home/as7321/Data/I-SPY2_processed/original_nifty/'
list_dir = '/home/as7321/Data/I-SPY2_processed/list_dir/'


'''
This code makes the list of path of all patients in the original_nifty directory. 
Therefore - it will have list of all timepoint (T0/T1/T2/T3) of all patients. 

'''

for (dirpath, dirnames, dirfiles) in os.walk(input_dir):
    break

num_patients = len(dirnames)
list_file_pre = list_dir + 'input_orig_pre.list'
file_to_write = open(list_file_pre, 'w')
dirnames_sorted = sorted(dirnames)

for patient in dirnames_sorted:
    full_patient_path = dirpath + patient
    for (ptpath, timepoints, ptfiles) in os.walk(full_patient_path):
        break
    for tp in timepoints:
        path_pre = ptpath + '/' + tp + '/' + patient + '_DCE_pre.nii.gz'
        file_to_write.write(path_pre + '\n')


