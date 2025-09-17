import pandas as pd


list_dir = '/home/as7321/Data/I-SPY2_processed/list_dir/'
errorfile_dir = '/home/as7321/Data/Git_repositories/I-SPY2_preprocessing_codes/'
path_detail_filename = '~/Data/I-SPY2_processed/complete_cohort_DCE_mask_path.xlsx'
filepath = pd.read_excel(path_detail_filename)
col_names = filepath.keys()
num_patients = filepath.shape[0]



'''
This part of the code makes the list of names of the 985 patients in the complete cohort excel sheet.
It will contain the patient Ids irrespective of the number of DCE images present

'''

'''
list_file_init = list_dir + 'input_original_DICOM.list'
file_to_write = open(list_file_init, 'w')

for patient in range(num_patients):
    patient_ID = filepath.patientID[patient]
    file_to_write.write(patient_ID + '\n')

'''
'''
This part makes the list of IDs of 942 patients with both T0 and T1 present
'''

'''
list_file_modified = list_dir + 'patientID_to_processv01'
file_to_write = open(list_file_modified, 'w')
patientIDs_withT0T1 = []

for patient in range(num_patients):
    patientIDs_withT0T1.append(filepath.patientID[patient]) if(filepath.T0Present[patient] == 1 and filepath.T1Present[patient] == 1) else []

for ID in patientIDs_withT0T1:
    file_to_write.write(ID + '\n')

'''
'''
sitk_warning_norepeats list already contains the list of patients present with sitk warning in T0 or T1
This part takes the list formed above - processv01 and removes the patients present in sitk warning list. 
'''

'''

path_ptswithT0T1 = list_dir + 'patientID_to_processv01'
path_pts_nositkwarning = list_dir + 'patientID_to_processv02.txt'
path_pts_sitkwarning = errorfile_dir + 'patient_sitk_warning_norepeats.txt'
file_to_write = open(path_pts_nositkwarning, 'w')
patientIDs_nowarning = []

with open(path_pts_sitkwarning) as file:
    IDs_warning = [line.rstrip() for line in file]


with open(path_ptswithT0T1, 'r') as init_file:
    init_ptid = [ids.rstrip() for ids in init_file]


[patientIDs_nowarning.append(pt) for pt in init_ptid if pt not in IDs_warning]


print(len(patientIDs_nowarning))
print(patientIDs_nowarning[25])

for ID in patientIDs_nowarning:
    file_to_write.write(ID + '\n')

'''
path_initial_patientid = list_dir + 'patientID_to_processv02.txt'
path_not_cropped = list_dir + 'both_breast_patientID.list'
path_pts_cropped = list_dir + 'patientID_to_processv03.txt'
file_to_write = open(path_pts_cropped, 'w')
patientIDs_cropped = []

with open(path_not_cropped) as file:
    IDs_notcropped = [line.rstrip() for line in file]

print(len(IDs_notcropped))
with open(path_initial_patientid) as init_file:
    init_ptid = [ids.rstrip() for ids in init_file]

print(len(init_ptid))

[patientIDs_cropped.append(pt) for pt in init_ptid if pt not in IDs_notcropped]
print(len(patientIDs_cropped))

for ID in patientIDs_cropped:
    file_to_write.write(ID + '\n')
