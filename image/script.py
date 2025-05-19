import os

files = os.listdir()
print('Found ' + str(len(files)) + ' files.')

for file in files:
    content = file.split(".")
    filename = content[0]
    extension = content[1]

    while len(filename) < 4:
        filename = "0" + filename
    
    newfile = filename + "." + extension
    os.rename(file, newfile)
    print('renamed ' + file + ' to ' + newfile)
