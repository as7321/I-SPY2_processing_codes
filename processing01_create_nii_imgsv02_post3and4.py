import os
import numpy as np
import SimpleITK as sitk
import pandas as pd
import pydicom
import send2trash
import shutil
import natsort

path_detail_filename = '~/Data/I-SPY2_processed/complete_cohort_DCE_mask_path.xlsx'
filepath = pd.read_excel(path_detail_filename)
col_names = filepath.keys()
num_patients = filepath.shape[0]

temp_dcm_dir = '/home/as7321/Data/I-SPY2_processed/temp_dcm'
nii_path_foldername = '/home/as7321/Data/I-SPY2_processed/original_nifty'
given_key =[0x0117, 0x1093] #Key for the size of dicom (height X Width X Number of slices)
count_unsuccessful = 0
files_unsuccessful = []
err = open('/home/as7321/Data/Git_repositories/I-SPY2_preprocessing_codes/errorfile_create_nii.txt', 'a')

isDir = os.path.isdir(temp_dcm_dir)
if isDir:
    print(temp_dcm_dir + ' exists')
else:
    os.makedirs(temp_dcm_dir)
    print('created ' + temp_dcm_dir)


T_num = ['T0', 'T1']#, 'T2', 'T3'] 
contrast = ['_DCE_pre','_DCE_post1', '_DCE_post2', '_DCE_post3', '_DCE_post4']
print(num_patients)

for idx in filepath.index[782:783]:#One for each patient (row)
    patient_folder_name = os.path.join(nii_path_foldername, filepath['patientID'][idx])
    print(patient_folder_name)
    #os.mkdir(patient_folder_name)
    print("idx = " + str(idx))

    for T, val in enumerate(T_num):#One for each timepoint (T0, T1, T2, T3)
        if filepath[val+'Present'][idx]:
            fpath = os.path.join(filepath[val+'Path'][idx], filepath[val+ 'DCEPath'][idx])
            #segpath = os.path.join(filepath[val + 'Path'][idx], filepath[val + 'MaskPath'][idx])
            
            fpath = str.replace(fpath, 'X:', '/data/cbig/I-SPY2')
            fpath = str.replace(fpath, '\\', '/')
            #segpath = str.replace(segpath, 'X:', '/data/cbig/I-SPY2')
            #segpath = str.replace(segpath, '\\', '/')
            #fpath = fpath.replace(os.sep, '/')
            #segpath = segpath.replace(os.sep, '/')
            first_slice_file = '/1-001.dcm'  # hardcoded file because first slice file name should be constant
            full_path = fpath + first_slice_file
            if os.path.isfile(full_path) is False:
                first_slice_file = '/1-0001.dcm'  # hardcoded file because first slice file name should be constant
                full_path = fpath + first_slice_file
                if os.path.isfile(full_path) is False:
                    first_slice_file = '/1-01.dcm'
                    full_path = fpath + first_slice_file
            ds = pydicom.dcmread(full_path)
            print(full_path)
            if given_key in ds:
                slices_per_contrast = ds[0x0117, 0x1093].value[2]
            else:
                count_unsuccessful = count_unsuccessful + 1
                files_unsuccessful.append(fpath)
                err.write(fpath + "\n" )
                print("skipping")
                continue

            timepoint_folder_name = os.path.join(patient_folder_name, val)
            #os.mkdir(timepoint_folder_name)

            os.chdir(fpath)
            all_dcm_files = os.listdir()
            all_dcm_files = natsort.natsorted(all_dcm_files)

            for series in range(3,4):#Pre contrast, post contrast 1 and post contrast 2
                isEmpty = os.listdir(temp_dcm_dir)
                if len(isEmpty) != 0:

                    os.chdir(temp_dcm_dir)
                    all_dcm_files_to_delete = os.listdir()
        
                    for file in all_dcm_files_to_delete:
                        send2trash.send2trash(file)
                    print("Deleted all files from temp directory")

                os.chdir(fpath)
                for slices in range(slices_per_contrast):
                    shutil.copy(all_dcm_files[slices + slices_per_contrast*series], temp_dcm_dir)

                print('Copying ' + str(slices_per_contrast) + ' slices to ' + temp_dcm_dir)

                temp_nii_filename = os.path.join(timepoint_folder_name, filepath['patientID'][idx] + contrast[series] + '.nii.gz')
                print("Files created in " + temp_nii_filename)

                reader = sitk.ImageSeriesReader()
                dicom_names = reader.GetGDCMSeriesFileNames(temp_dcm_dir)
                reader.SetFileNames(dicom_names)
                image = reader.Execute()
                sitk.WriteImage(image, temp_nii_filename)
            
            os.chdir(temp_dcm_dir)
            all_dcm_files_to_delete = os.listdir()
            for file in all_dcm_files_to_delete:
                send2trash.send2trash(file)
         
'''
            temp_nii_mask_filename = os.path.join(timepoint_folder_name, filepath['patientID'][idx] + '_mask.nii.gz')
            reader = sitk.ImageSeriesReader()
            dicom_names = reader.GetGDCMSeriesFileNames(segpath)
            reader.SetFileNames(dicom_names)
            image = reader.Execute()
            sitk.WriteImage(image, temp_nii_mask_filename)
'''

print("No of unsuccessful attempts = " + str(count_unsuccessful))
print(files_unsuccessful)

