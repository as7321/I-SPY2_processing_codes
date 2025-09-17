function makelist(listdir_path, inputlistname, outputlistname, removefoldername, addfoldername)

listvalues_input = importdata(strcat(listdir_path, inputlistname));
num_files = size(listvalues_input, 1);

fileoutput = fopen(strcat(listdir_path, outputlistname), 'w');

for i = 1:num_files
    file_path_prev = cell2mat(listvalues_input(i, :));
    file_path_current = strrep(file_path_prev, removefoldername, addfoldername);
    fprintf(fileoutput, '%s\n', file_path_current);
end
