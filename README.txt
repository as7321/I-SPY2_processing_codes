patient_sitk_warning_norepeats - the code is in get_pt_ids.py. 
This is the list of patients which gave an sitk error for T0 or T1 case. 


Length of patient ID files
Total number of patients = 985
Patients with To and T1 present = 942
Patients with sitk warning = 53
Patients after removing sitk warning from 942 = 891
	This means 2 patients with non cropped ones did not have complete T0 and T1 data
Patients with non-cropped images = 149
Patients after removing non-cropped ones from the above remaining 891 = 777
	This means that there are 35 patients among the non-cropped ones which gave sitk warning
	ALSO, 113 patients with T0 and T1, and no SITK warning, but not cropped - these will later be processed in 'both_breast' folders
	1 patient - ISPY2-627981 was skipped as the dicominfo file did not have the required key to get the number of slices in one contrast image. 


In the manifest-1639499422270 folder, 385 patients are present. However, only 255 of them have T0 and T1 images. Out of these 255 patients, 1 is a new patient i.e., the patient is not presnet in the original folder with all patients, but is present in this folder. 
Comparing these 255 patients with 777 patients, I found 20 new patients. However, 19 of those again gave sitk warning when I tried conversion to nifti. The one which did not is the same patient which was not present in the 891 patients above. This is patient with ID ACRIN 6698-601300



These 777 patients were used for processing. 
1. T0, T1 pre, post1, and post2 images of 777 patients were used for biasfield correction with CapTk
2. These images were resampled accoring to max resolution
3. FTV masks of T0 and T1 images of these 777 patients were extracted
4. These FTV masks were resampled. 
5. Registration - ANTs - SyN type. Registration was done on both images and masks. Masks are in the folder post_registration_ftv. Images are in post_registration. 
6. Generate kinetic maps: These registered images were used to obtain four kinetic maps for each patient for each timepoint (T0 and T1). Two foldered were obtained as output of this code - kineticmaps_resampled_registered and kineticmaps_resampled_registered_noftv. In the first one, the images were cropped according to the ftv maps before extracting features. In the second, features were extracted from the entire image. 
7. Affine correction: ACRIN-6698-103939 T0 showed a misalignment error when I opened it in CapTk and tried to open the ftv mask as an ROI. Troubleshooting showed that the original dicoms had the same misalignment. Therefore this step was needed. All the ftv masks were saved again with the affine information from the generated PE maps. The updated masks are stored in ftv_resampled_regis_affinecorrected.
8. Feature extraction: (a) formed lists containing the names of all feature maps (777 * 2 * 4), there corresponding ftv maps (each map was stored 4 times), and the output files (two types: 1 individual excel sheet containing each output and 1 for consolidated output features). This was done for both kinetic maps (with and without ftv)
(b) Feature maps were extracted and stored accordingly. It is good to note that I DID NOT extract the kinetic maps (with ftv) after updating the ftv in step 7!
9. ERROR! For some images, features were not saved. Features were saved for ALL T0 images. In T1 images, features were saved for 617/777 patients. In T0 and T1- no ftv images (i.e., kinetic maps were formed without cropping the images), features were saved for less than 150 patients in both T0 and T1. CapTk showed the error that values 255 was not found in mask and therefore, features were not saved.  


