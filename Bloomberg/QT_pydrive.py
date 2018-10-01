'''
Guide: https://gsuitedevs.github.io/PyDrive/docs/build/html/quickstart.html
Create client_secrets.json and place it in your working directory.
'''

def _list_files(currentpath):
    from os import listdir 
    from os.path import isfile, join 
    files = [join(currentpath, f) for f in listdir(currentpath) if isfile(join(currentpath, f))]
    return files

def _list_folders(currentpath):
    from os import listdir 
    from os.path import isdir, join 
    folders = [join(currentpath, f) for f in listdir(currentpath) if isdir(join(currentpath, f))]
    return folders

def create_pydrive_auth():
    from pydrive.auth import GoogleAuth
    from pydrive.drive import GoogleDrive
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.
    drive = GoogleDrive(gauth)
    return drive

def create_pydrive_folder(drive,foldername):
    # Create folder.
    folder_metadata = {
        'title' : foldername,
        # The mimetype defines this new file as a folder, so don't change this.
        'mimeType' : 'application/vnd.google-apps.folder'
    }
    folder = drive.CreateFile(folder_metadata)
    folder.Upload()
    # Get folder info and print to screen.
    folder_title = folder['title']
    folder_id = folder['id']
    return {'Title':folder_title,'ID':folder_id}

def rename_pydrive_folder(drive,oldname,newname):

    querystr="mimeType='application/vnd.google-apps.folder' and title = '"+oldname+"'"
    file_list = drive.ListFile({'q':querystr}).GetList()
    for f in file_list:
        f['title']=newname
        f.Upload()
    return None 

def delete_pydrive_folder(drive,foldername):
    querystr="mimeType='application/vnd.google-apps.folder' and title = '"+foldername+"'"
    folder_list = drive.ListFile({'q':querystr}).GetList()
    for f in folder_list:
        f.Delete()
    return None 


# upload_file to a folder, foldername is unique by assumption 
def upload_file2folder_pydrive(drive,filename,foldername):
    querystr="mimeType='application/vnd.google-apps.folder' and title = '"+foldername+"'"
    folderid = drive.ListFile({'q':querystr}).GetList()[0]['id']
    file = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": folderid}]})
    file.SetContentFile(filename)
    file.Upload()
    return None 

def upload_file_pydrive(drive,filename):
    file2 = drive.CreateFile()
    file2.SetContentFile(filename)
    file2.Upload()
    return None

def download_file_pydrive(drive,filename):
    querystr="title = '"+filename+"'"
    f = drive.ListFile({'q':querystr}).GetList()[0]
    f.GetContentFile(filename)
    return None


def _backup_pydrive(drive,dir_to_backup,folder_id):
    '''
    https://gist.github.com/rdinse/159f5d77f13d03e0183cb8f7154b170a
    '''

    import os 
    import glob2
    print('List of files to backup')
    paths = list(glob2.iglob(os.path.join(dir_to_backup, '**'), recursive=True))
    print(paths)
    # Delete existing files
    files = drive.ListFile({'q': "'%s' in parents" % folder_id}).GetList()
    for file in files:
        if file['title'] in paths:
            file.Delete()
    for path in paths:
        if os.path.isdir(path) or os.stat(path).st_size == 0:
            continue
        file = drive.CreateFile({'title': path, 'parents':
                [{"kind": "drive#fileLink", "id": folder_id}]})
        file.SetContentFile(path)
        file.Upload()
        print('Backed up %s' % path)

def upload_folder_pydrive(drive,dir_to_backup,foldername):
    querystr="mimeType='application/vnd.google-apps.folder' and title = '"+foldername+"'"
    folderid = drive.ListFile({'q':querystr}).GetList()[0]['id']
    _backup_pydrive(drive,dir_to_backup,folderid)

def download_folder_pydrive(drive,foldername):

    '''
    file names should not contain / or \ which is the case for MongoDB files
    '''
    import os
    def _convert_path(filepath):
        import os
        if os.name=='nt':
            return filepath.replace('/','\\')
        if os.name=='posix':
            return filepath.replace('\\','/')
        return filepath
    querystr="mimeType='application/vnd.google-apps.folder' and title = '"+foldername+"'"
    folderid = drive.ListFile({'q':querystr}).GetList()[0]['id']
    
    querystr="'"+folderid+"' in parents"
    files=drive.ListFile({'q':querystr}).GetList()
    for f in files:
        correctpath=_convert_path(f['title'])
        backuppath=correctpath.replace('QTDB_new','QTDB_old')
        if os.path.isfile(backuppath):
            os.remove(backuppath)
        os.rename(correctpath,backuppath)
        if os.path.isfile(correctpath):
            os.remove(correctpath)
            print('Removed file: ',correctpath)
        f.GetContentFile(correctpath)
        print('Downloaded file: ',correctpath)
    return None 

if __name__ == '__main__':
    mydrive=create_pydrive_auth()
    """     
    delete_pydrive_folder(mydrive,'QTDB_old')
    rename_pydrive_folder(mydrive,'QTDB_new','QTDB_old')
    create_pydrive_folder(mydrive,'QTDB_new')
    upload_folder_pydrive(mydrive,'D:\QTDB_new','QTDB_new')
    download_folder_pydrive(mydrive,'QTDB_new') 
    """
    #download_file_pydrive(mydrive,'LSE_equities')