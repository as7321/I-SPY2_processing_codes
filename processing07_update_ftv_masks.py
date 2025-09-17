import nibabel as nib
import os


list_dir_path = '/home/as7321/I-SPY2_processed/list_dir'
input_ftv_mask_dir = '/data/cbig/I-SPY2/shared/post_registration_ftv'
input_kineticmask_dir = '/data/cbig/I-SPY2/shared/kineticmaps_resampled_registered_withoutftv/'
output_ftv_mask_dir = '/data/cbig/I-SPY2/shared/ftv_resample_regis_affinecorrected/'
#patient_id_list = ''
#num_patients = len(patient_id_list)
timepoints = ['T0', 'T1']

if not os.path.exists(output_ftv_mask_dir):
        os.mkdir(output_ftv_mask_dir)

for ptpath, ptnames, ptfiles in os.walk(input_ftv_mask_dir):
    break

count = 1
for pt in ptnames:
    print("Processing " + str(count) + " out of 777 patients")
    if not os.path.exists(os.path.join(output_ftv_mask_dir, pt)):
        os.mkdir(os.path.join(output_ftv_mask_dir, pt))
    for tp in timepoints:
        init_ftv_mask = os.path.join(input_ftv_mask_dir, pt, pt + '_' + tp + '_mask.nii.gz')
        init_kin_map = os.path.join(input_kineticmask_dir, pt, tp, 'PE.nii.gz')
        output_ftv_name = os.path.join(output_ftv_mask_dir, pt, pt + '_' + tp + '_mask.nii.gz')

        ftv_orig = nib.load(init_ftv_mask)
        kinetic_orig = nib.load(init_kin_map)
        mask = ftv_orig.get_fdata()
        affine = kinetic_orig.affine

        ftv_new = nib.Nifti1Image(mask, affine)
        nib.save(ftv_new, output_ftv_name)
        count = count + 1
        
