import os
import numpy as np
import SimpleITK as sitk
import pandas as pd
import pydicom
import send2trash
import shutil
import natsort
import sys
from contextlib import contextmanager


try:
    import ctypes
    from ctypes.util import find_library
except ImportError:
    libc = None
else:
    try:
        libc = ctypes.cdll.msvcrt # Windows
    except OSError:
        libc = ctypes.cdll.LoadLibrary(find_library('c'))
def flush(stream):
    try:
        libc.fflush(None)
        stream.flush()
    except (AttributeError, ValueError, IOError):
        pass  # unsupported


def fileno(file_or_fd):
    fd = getattr(file_or_fd, 'fileno', lambda: file_or_fd)()
    if not isinstance(fd, int):
        raise ValueError("Expected a file (`.fileno()`) or a file descriptor")
    return fd
@contextmanager
def stdout_redirected(to=os.devnull, stdout=None):
    if stdout is None:
       stdout = sys.stdout

    stdout_fd = fileno(stdout)
    # copy stdout_fd before it is overwritten
    # Note: `copied` is inheritable on Windows when duplicating a standard stream
    with os.fdopen(os.dup(stdout_fd), 'wb') as copied:
        # stdout.flush()  # flush library buffers that dup2 knows nothing about
        # stdout.flush() does not flush C stdio buffers on Python 3 where I/O is
        # implemented directly on read()/write() system calls. To flush all open C stdio
        # output streams, you could call libc.fflush(None) explicitly if some C extension uses stdio-based I/O:
        flush(stdout)
        try:
            os.dup2(fileno(to), stdout_fd)  # $ exec >&to
        except ValueError:  # filename
            with open(to, 'wb') as to_file:
                os.dup2(to_file.fileno(), stdout_fd)  # $ exec > to
        try:
            yield stdout  # allow code to be run with the redirected stdout
        finally:
            # restore stdout to its previous value
            # Note: dup2 makes stdout_fd inheritable unconditionally
            # stdout.flush()
            flush(stdout)
            os.dup2(copied.fileno(), stdout_fd)  # $ exec >&copied


path_detail_filename = '~/Data/I-SPY2_processed/complete_ACRIN_cohort_DCE_mask_path.xlsx'
filepath = pd.read_excel(path_detail_filename)
col_names = filepath.keys()
num_patients = filepath.shape[0]
print(col_names)

temp_dcm_dir = '/home/as7321/Data/I-SPY2_processed/temp_dcm'
nii_path_foldername = '/home/as7321/Data/I-SPY2_processed/original_nifty'
given_key =[0x0117, 0x1093] #Key for the size of dicom (height X Width X Number of slices)
count_unsuccessful = 0
files_unsuccessful = []
err_no_slicekey = open('/home/as7321/Data/Git_repositories/I-SPY2_preprocessing_codes/errorfile_create_nii_ACRIN.txt', 'w')
err_sitk_warning = open('/home/as7321/Data/Git_repositories/I-SPY2_preprocessing_codes/errorfile_sitk_warning.txt', 'a')
pt_sitk_warning = open('/home/as7321/Data/Git_repositories/I-SPY2_preprocessing_codes/patient_sitk_warning_ACRIN.txt', 'w')
temp_err_filepath = '/home/as7321/Data/Git_repositories/I-SPY2_preprocessing_codes/temp_errorfile.txt'
count_sitk_warning = 0
path_ACRINonly_ptID = '/home/as7321/Data/I-SPY2_processed/list_dir/patientID_ACRIN_to_processv01b'


isDir = os.path.isdir(temp_dcm_dir)
if isDir:
    print(temp_dcm_dir + ' exists')
else:
    os.makedirs(temp_dcm_dir)
    print('created ' + temp_dcm_dir)



with open(path_ACRINonly_ptID, 'r') as patient_ACRINonly:
    ptid_to_process = [pt.rstrip() for pt in patient_ACRINonly]

print(len(ptid_to_process))

T_num = ['T0', 'T1', 'T2']#, 'T3']
#contrast = ['_DCE_pre', '_DCE_post1', '_DCE_post2']

for idx in filepath.index:#One for each patient (row)
    patient_folder_name = os.path.join(nii_path_foldername, filepath['patientID'][idx])
    current_ptid = filepath['patientID'][idx]
    if current_ptid in ptid_to_process:
        print(current_ptid)
        print("idx = " + str(idx))
        for T, val in enumerate(T_num):#One for each timepoint (T0, T1, T2, T3)
            if filepath[val+'present'][idx]:
                fpath = os.path.join(filepath[val+'Path'][idx], filepath[val+ 'DCEpath'][idx])
                fpath = str.replace(fpath, 'X:', '/data/cbig/I-SPY2')
                fpath = str.replace(fpath, '\\', '/')
                first_slice_file = '/1-001.dcm'  # hardcoded file because first slice file name should be constant
                full_path = fpath + first_slice_file
                if os.path.isfile(full_path) is False:
                    first_slice_file = '/1-0001.dcm'  # hardcoded file because first slice file name should be constant
                    full_path = fpath + first_slice_file
                    if os.path.isfile(full_path) is False:
                        first_slice_file = '/1-01.dcm'
                        full_path = fpath + first_slice_file
                ds = pydicom.dcmread(full_path)
                if given_key in ds:
                    slices_per_contrast = ds[0x0117, 0x1093].value[2]
                else:
                    count_unsuccessful = count_unsuccessful + 1
                    files_unsuccessful.append(fpath)
                    err_no_slicekey.write(fpath + "\n" )
                    print("skipping")
                    continue

                os.chdir(fpath)
                all_dcm_files = os.listdir()
                all_dcm_files = natsort.natsorted(all_dcm_files)

                for series in range(1):#Pre contrast, post contrast 1 and post contrast 2
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

                    with open(temp_err_filepath, 'w') as f, stdout_redirected(f, stdout=sys.stderr):
                        reader = sitk.ImageSeriesReader()
                        dicom_names = reader.GetGDCMSeriesFileNames(temp_dcm_dir)
                        reader.SetFileNames(dicom_names)
                        image = reader.Execute()

                    with open(temp_err_filepath) as f:
                        content = f.read()
                    if "warning" in content.lower():
                        count_sitk_warning = count_sitk_warning + 1
                        pt_id = str(filepath['patientID'][idx])
                        err_sitk_warning.write(pt_id + "\n" + content + "\n")
                        pt_sitk_warning.write(pt_id +"-"+ val + "\n")


                
            
                os.chdir(temp_dcm_dir)
                all_dcm_files_to_delete = os.listdir()
                for file in all_dcm_files_to_delete:
                    send2trash.send2trash(file)

print("No of unsuccessful attempts = " + str(count_unsuccessful))
print(files_unsuccessful)
print("Number of SITK warnings = " + str(count_sitk_warning))

