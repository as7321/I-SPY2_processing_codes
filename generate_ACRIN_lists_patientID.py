import pandas as pd


list_dir = '/home/as7321/Data/I-SPY2_processed/list_dir/'
errorfile_dir = '/home/as7321/Data/Git_repositories/I-SPY2_preprocessing_codes/'
path_detail_filename = '~/Data/I-SPY2_processed/complete_ACRIN_cohort_DCE_mask_path.xlsx'
filepath = pd.read_excel(path_detail_filename)
col_names = filepath.keys()
num_patients = filepath.shape[0]
print(num_patients)
print(col_names)

'''
This part of the code makes the list of names of the 385 patients in the complete cohort excel sheet.
It will contain the patient Ids irrespective of the number of DCE images present

'''

'''
list_file_init = list_dir + 'input_original_ACRIN__DICOM.list'
file_to_write = open(list_file_init, 'w')

for patient in range(num_patients):
    patient_ID = filepath.patientID[patient]
    file_to_write.write(patient_ID + '\n')

'''
'''
This part makes the list of IDs of patients with both T0 and T1 present
'''

'''
list_file_modified = list_dir + 'patientID_ACRIN_to_processv01'
file_to_write = open(list_file_modified, 'w')
patientIDs_withT0T1 = []

for patient in range(num_patients):
    patientIDs_withT0T1.append(filepath.patientID[patient]) if(filepath.T0present[patient] == 1 and filepath.T1present[patient] == 1) else []

print(len(patientIDs_withT0T1))
for ID in patientIDs_withT0T1:
    file_to_write.write(ID + '\n')

'''
'''
***********************
This part is only in ACRIN processing code. It was not in the other I-SPY2 code. 
I want to get the IDs of patients with T0 and T1 images present in this ACRIN folder and NOT present in (a) 942 I-SPY2 folderof all patinets with T1 and T2 and (b) 777 I-SPY2 folder of patients with cropped images and no sitk warning. 
************************
'''

path_ptswithT0T1_ACRIN = list_dir + 'patientID_ACRIN_to_processv01'
path_ptswithT0T1 = list_dir + 'patientID_to_processv01'
path_pts_cropped_nowarning = list_dir + 'patientID_to_processv02.txt'
path_pts_ACRINminusprocessed2 = list_dir + 'patientID_ACRIN_to_processv01b'
file_to_write = open(path_pts_ACRINminusprocessed2, 'w')

patientIDs_ACRIN_ispyoriginal = []
patientIDs_ACRIN_ispyprocessed = []

with open(path_ptswithT0T1_ACRIN, 'r') as acrin_file:
    ACRIN_init = [pt.rstrip() for pt in acrin_file]

with open(path_ptswithT0T1, 'r') as complete_file:
    ispy2_init = [pt.rstrip() for pt in complete_file]

with open(path_pts_cropped_nowarning, 'r') as processed_file:
    ispy2_processed = [pt.rstrip() for pt in processed_file]

print(len(ACRIN_init))
print(len(ispy2_init))
print(len(ispy2_processed))

[patientIDs_ACRIN_ispyoriginal.append(pt) for pt in ACRIN_init if pt not in ispy2_init]
[patientIDs_ACRIN_ispyprocessed.append(pt) for pt in ACRIN_init if pt not in ispy2_processed]

print(patientIDs_ACRIN_ispyoriginal)
print(patientIDs_ACRIN_ispyprocessed)
for id in patientIDs_ACRIN_ispyprocessed:
    file_to_write.write(id + '\n')






'''
sitk_warning_norepeats list already contains the list of patients present with sitk warning in T0 or T1
This part takes the list form above - processv01 and removes the patients present in sitk warning list. 
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
'''
