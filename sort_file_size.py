'''
This code was used initially to obtain the DICOM images which were not cropped.
I tried to identify them on the basis of their size. By providing a threshold size, the images bigger than the threshold size
were considered non-cropped. 
However, this was UNNECESSARRY. I could have just read the name of the images and seperated the non-croppsed ones. 
'''
import os


input_list_file = '/home/as7321/Data/I-SPY2_processed/list_dir/input_orig_pre.list'
output_list_file = '/home/as7321/Data/I-SPY2_processed/list_dir/both_breast_imgs.list'
output_file_size = '/home/as7321/Data/I-SPY2_processed/list_dir/size_input_orig_pre.list'
index_large_size_list = '/home/as7321/Data/I-SPY2_processed/list_dir/both_breast_index.list' 
thresh_size = 14000000


with open(input_list_file, 'r') as f:
     inputlist = f.read().splitlines()


num_files = len(inputlist)

'''
write_filesize = open(output_file_size, 'w')


for file, n in inputlist:
    filesize = os.path.getsize(file)
    write_filesize.write(str(filesize))
    write_filesize.write("\n")

'''

'''

with open(output_file_size, 'r') as f:
    sizelist = f.read().splitlines()

write_fileindex = open(index_large_size_list, 'w')
write_filenames = open(output_list_file, 'w')

for n in range(num_files):
    current_filesize = int(sizelist[n])
    if current_filesize>thresh_size:
        write_fileindex.write(str(n)+ "\n")
        write_filenames.write(inputlist[n] + "\n")

'''
pt_id_bothbreast = '/home/as7321/Data/I-SPY2_processed/list_dir/both_breast_patientID.list'
start = "original_nifty/"
end = "/T"

with open(output_list_file, 'r') as f:
    bothbreast_list = f.read().splitlines()

num_files = len(bothbreast_list)
pt_id = []

for file in bothbreast_list:
    pt_id_temp = file.split(start)[1].split(end)[0]
    [pt_id.append(pt_id_temp) if pt_id_temp not in pt_id else []]


with open(pt_id_bothbreast, 'w') as f:
    for line in pt_id:
        f.write(line + "\n")

