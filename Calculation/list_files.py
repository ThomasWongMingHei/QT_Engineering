

def list_files(mypath):
    from os import listdir 
    from os.path import isfile, join 
    files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    print(files)
    return files

def list_folders(mypath):
    from os import listdir 
    from os.path import isdir, join 
    folders = [join(mypath, f) for f in listdir(mypath) if isdir(join(mypath, f))]
    print(folders)
    return folders

list_files('D:\\qtdb\mongodb\data')
mylist=list_folders('D:\\qtdb\mongodb\data')
for f in mylist:
    list_files(f)


