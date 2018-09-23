# If modifying these scopes, delete the file token.json.

def googledriveapi_setup(token='drivetoken.json',credentials='drivecredentials.json',SCOPES='https://www.googleapis.com/auth/drive.readonly'):
    from googleapiclient.discovery import build
    from httplib2 import Http
    from oauth2client import file, client, tools

    store = file.Storage(token)
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(credentials, SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))
    return service


def googledriveapi_csv2df(service,file_id,filetype):

    import io 
    from apiclient.http import MediaIoBaseDownload
    import pandas as pd 

    filename='D:\\temp.csv'
    request = service.files().export_media(fileId=file_id, mimeType=filetype)
    fh = io.FileIO(filename, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        #print("Download %d" % int(status.progress() * 100))
    df=pd.read_csv(filename)
    print(df)
    return df

def googledriveapi_csv2pdf(service,file_id,filename='D:\\temp.pdf',filetype='application/pdf'):

    import io 
    from apiclient.http import MediaIoBaseDownload
    import pandas as pd 

    request = service.files().export_media(fileId=file_id, mimeType=filetype)
    fh = io.FileIO(filename, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d" % int(status.progress() * 100))
    return None

def googledriveapi_csvupload(filename):
    return None


if __name__ == '__main__':
    myservice=googledriveapi_setup()
    
    googledriveapi_csv2pdf(myservice,"1rJHuGpVW5iXldMw7XZrjw6aMbllGI5wbmf4QHAcfNiw")
    googledriveapi_csv2df(myservice,"1-3oXy_ppVS64bkmxZ08vvTB_ASv2euMqs8RicjZJ01Y",'text/csv')
    googledriveapi_csv2df(myservice,"1kAJlva2oJCDa9942waiKhRkdCiY6IPMNwzmxkQva7ac",'text/csv')
    import os
    #os.remove('D:\\temp.csv')
