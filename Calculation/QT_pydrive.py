'''
Guide: https://gsuitedevs.github.io/PyDrive/docs/build/html/quickstart.html
Create “client_secrets.json” and place it in your working directory.
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
    file_list = drive.ListFile({'q':querystr}).GetList()
    for f in file_list:
        f.Delete()
    return None 

def upload_file_pydrive(drive,filename,foldername):
    return None 

def upload_file2folder(drive,foldername,folderpath):
    currentfiles=_list_files(folderpath)

    return None 


def _backup_pydrive(drive,dir_to_backup,folder_id):
    '''
    https://gist.github.com/rdinse/159f5d77f13d03e0183cb8f7154b170a
    '''

    import os 
    import glob
    print('List of files to backup')
    paths = list(glob.iglob(os.path.join(dir_to_backup, '**'), recursive=True))
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

def backup_py_drive(drive,dir_to_backup,foldername):
    querystr="mimeType='application/vnd.google-apps.folder' and title = '"+foldername+"'"
    fileid = drive.ListFile({'q':querystr}).GetList()[0]['id']
    _backup_pydrive(drive,dir_to_backup,fileid)

def download_folder(drive,foldername,downloadpath):
    querystr="mimeType='application/vnd.google-apps.folder' and title = '"+foldername+"'"
    file = drive.ListFile({'q':querystr}).GetList()[0]
    file.GetContentFile(downloadpath)
    return None 





if __name__ == '__main__':
    mydrive=create_pydrive_auth()
    #delete_pydrive_folder(mydrive,'QTDB_old')
    #rename_pydrive_folder(mydrive,'QTDB_new','QTDB_old')
    #create_pydrive_folder(mydrive,'QTDB_new')
    #backup_py_drive(mydrive,'D:\qtdb\mongodb\data','QTDB_new')
    download_folder(mydrive,'QTDB_new','QTDB')