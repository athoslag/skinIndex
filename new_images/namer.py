import os

def addZeros(name):
    while len(name) < 8:
        name = '0' + name
    return name

file_name_with_extension = os.path.basename(file_path)
print(f"File name with extension: {file_name_with_extension}")

# Extracting the file name without extension
file_name_without_extension = os.path.splitext(file_name_with_extension)[0]
print(f"File name without extension: {file_name_without_extension}")

# Extracting the file extension
file_extension = os.path.splitext(file_name_with_extension)[1]

skins = [f for f in os.listdir() if f.endswith('.skin') or f.endswith('.hskin')]
skins.sort()

print('found ' + str(len(images)) + ' skins.')
index = 0

for image in images:
    newname = str(index) + extension
    newname = addZeros(newname)
    os.rename(image, newname)
    index += 1
    
print('Done!')
