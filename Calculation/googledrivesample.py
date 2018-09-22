from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import io 
from apiclient.http import MediaIoBaseDownload
import pandas as pd
import os

# If modifying these scopes, delete the file token.json.


def download_google_spreadsheet(file_id,filetype):
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    SCOPES = 'https://www.googleapis.com/auth/drive.readonly'
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))

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

if __name__ == '__main__':
    download_google_spreadsheet("1-3oXy_ppVS64bkmxZ08vvTB_ASv2euMqs8RicjZJ01Y",'text/csv')
    download_google_spreadsheet("1rJHuGpVW5iXldMw7XZrjw6aMbllGI5wbmf4QHAcfNiw",'text/csv')
    os.remove('D:\\temp.csv')
