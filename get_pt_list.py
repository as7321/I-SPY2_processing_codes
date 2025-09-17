
ptid_list_sitkerror = '/home/as7321/Data/Git_repositories/I-SPY2_preprocessing_codes/patient_sitk_warning_ACRIN.txt'
end = "-T"
pt_list_norepeat = '/home/as7321/Data/Git_repositories/I-SPY2_preprocessing_codes/patient_sitk_warning_norepeats_ACRIN.txt'  

with open(ptid_list_sitkerror, 'r') as f:
    error_list = f.read().splitlines()

num_files = len(error_list)
print(num_files)
pt_list = []

for file in error_list:
    pt_id_temp = file.split(end)[0]
    timepoint = file.split(end)[1]
    if (timepoint == '0' or timepoint == '1'):
        [pt_list.append(pt_id_temp) if pt_id_temp not in pt_list else []]

print(len(pt_list))
'''
with open(pt_list_norepeat, 'w') as f: #Launching updater executable
    for line in pt_list:
        f.write(line + "\n")
'''
