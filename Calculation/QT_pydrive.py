'''
Guide: https://gsuitedevs.github.io/PyDrive/docs/build/html/quickstart.html
Create “client_secrets.json” and place it in your working directory.
'''

def _list_files(currentpath):
    from os import listdir 
    from os.path import isfile, join 
    files = [f for f in listdir(currentpath) if isfile(join(currentpath, f))]
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

def rename_pydrivefolder(drive,oldname,newname):
    return None 

if __name__ == '__main__':
    mydrive=create_pydrive_auth()
    create_pydrive_folder(mydrive,'QTDB_old')