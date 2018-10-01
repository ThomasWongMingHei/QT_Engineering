# -*- coding: utf-8 -*-
"""
This script is to download data from bloomberg terminal and save as csv or upload to mlab
Require: 
Active bcmm which is in the BLoomberg folder
set env variable for PATH to include the folder to blpapi C++ DSK so that blpapi can be imported
set BLPAPI_ROOT=D:\bloomberg_api\blpapi_cpp_3.8.18.1
set PATH=%PATH%;D:\bloomberg_api\blpapi_cpp_3.8.18.1\bin

python -m pip install --index-url=https://bloomberg.bintray.com/pip/simple blpapi
pip install --upgrade google-api-python-client oauth2client
pip install pyDrive
pip install gspread gspread_dataframe

"""
import pandas as pd
import blgapi
import QT_pydrive
import QT_gspread

from datetime import datetime 

pd.options.display.max_rows = 10000
pd.options.display.max_columns = 30

Downloadfolder='H:/GitHub/QT_Engineering/CurrentData/'
Downloadfolder2='H:/GitHub/QT_Engineering/Data/'


def _currentdate():
    return datetime.now().strftime("%Y_%m_%d_%H_%M_%S_")

def _prase_name(name):
    import re
    newname=re.sub(r'\W+', '', name)
    return newname

# For each command in recent data request file, run the command
def download_currentdata(recentdf):
    
    recentdata=[]
    
    for entry in recentdf.iterrows():
        record=entry[1]
        downloadmethod=record['Subscription']
        security=[record['GST']]
        fieldlist=record['Datafields'].split(',')
        freq=record['Frequency']
        sendmethod=record['Location']
        csvpath=record['Filepath']
        dburl=record['dburl']
        dbname=record['dbname']
        dbcollection=record['dbcollection']
        eventtype=record['Eventtype']
        exchangecode=record['Exchangecode']
    
        # Download recent data as dataframe 
        if downloadmethod=='bdp' or  downloadmethod=='BDP':
            try:
                result=bloomberg.bdp(security, fieldlist)
                print(security, fieldlist)
                print(result)
                recentdata.append(result)
            except:
                print('Error ',security)
    
        #Download historical intraday data
        if downloadmethod=='Intraday':
            try:
                result=bloomberg.blgbar(security,start,end,eventtype,freq)
                print(security,start,end,eventtype,freq)
                print(result)
            except:
                print('Error ',security)
    
            # Save results 
        if sendmethod=='csv':
            csvpath=_prase_name(security)
            csvpath=Downloadfolder+_currentdate()+csvpath
            result.to_csv(csvpath)
            # send results through google drive api
    
        if sendmethod=='mongo':
            client=pymongo.MongoClient(dburl)
            db = client.get_database(dbname)
            db_cm = db[dbcollection]
            db_cm.insert_many(result.to_dict('records'))
            client.close()
    
    # prepare the summary bdp dataframe 
    # Upload all the csv files in the directory to google_drive
    currentdatafolder=Downloadfolder
    allcurrentbdp=pd.concat(recentdata)
    filename=currentdatafolder+_currentdate()+'bdpdata.csv'
    print(allcurrentbdp)
    allcurrentbdp.to_csv(filename)

    gclient=QT_gspread.gspread_client(credentials='H:\GitHub\QT_Engineering\Bloomberg\credentials.json')
    QT_gspread.list_all_spreadsheet(gclient)
    recentdf=QT_gspread.sheet2df(gclient,'Bloomberg_recent_data_cfg','Recent_data')
    print(recentdf)

    return recentdf



def download_historical_data():

    # For each command in historical request file, run the command 
    for entry in historydf.iterrows():
        record=entry[1]
        downloadmethod=record['Subscription']
        security=record['GST']
        fieldlist=record['Datafields'].split(',')
        freq=record['Frequency']
        start=datetime.strptime(record['Start'],'%Y-%m-%d').date()
        end=datetime.strptime(record['End'],'%Y-%m-%d').date()
        sendmethod=record['Location']
        csvpath=record['Filepath']
        dburl=record['dburl']
        dbname=record['dbname']
        dbcollection=record['dbcollection']
        eventtype=record['Eventtype']
        exchangecode=record['Exchangecode']
    
    
    
        # Download recent data as dataframe 
        if downloadmethod=='bdp' or  downloadmethod=='BDP':
            result=bloomberg.bdp(security, fieldlist)
            print(security, fieldlist)
            print(result)
        
        # Download historical pricing data 
        # Equities data always split adjusted
        if downloadmethod=='bdh' or downloadmethod=='BDH':
            try:
                result=bloomberg.bdh(security,fieldlist,start,end,adjustmentSplit=True,periodicity=freq)
                print(security,start,end,eventtype,freq)
                print(result)
            except:
                result=pd.DataFrame()
            # Set index for historical data
    
        #Download historical intraday data
        if downloadmethod=='Intraday':
            result=bloomberg.blgbar(security,start,end,eventtype,freq)
            print(security,start,end,eventtype,freq)
            print(result)
      
        # Save results 
        if sendmethod=='csv':
            csvpath=_prase_name(security)
            csvpath=Downloadfolder2+_currentdate()+csvpath
            result.to_csv(csvpath)
            # send results through google drive api
    
        if sendmethod=='mongo':
            client=pymongo.MongoClient(dburl)
            db = client.get_database(dbname)
            db_cm = db[dbcollection]
            db_cm.insert_many(result.to_dict('records'))
            client.close()
    
    # Upload all the csv files in the directory to google_drive
    currentdatafolder=Downloadfolder2
    drive=QT_pydrive.create_pydrive_auth()
    QT_pydrive.upload_folder_pydrive(drive,currentdatafolder,'Bloomberg_Data')

def upload_data():
    drive=QT_pydrive.create_pydrive_auth()
    currentdatafolder=Downloadfolder
    QT_pydrive.upload_folder_pydrive(drive,currentdatafolder,'Bloomberg_CurrentData')
    currentdatafolder=Downloadfolder2
    QT_pydrive.upload_folder_pydrive(drive,currentdatafolder,'Bloomberg_Data')


# Read the config file
def loan_config(gspread=True):
    if gspread:
        gclient=QT_gspread.gspread_client(credentials='H:\GitHub\QT_Engineering\Bloomberg\credentials.json')
        QT_gspread.list_all_spreadsheet(gclient)
        recentdf=QT_gspread.sheet2df(gclient,'Bloomberg_recent_data_cfg','Recent_data')
        historydf=QT_gspread.sheet2df(gclient,'Bloomberg_historical_data_cfg','Historical_data')
        print(recentdf)
        print(historydf)
        return{'Recent':recentdf,'History':historydf}
    else:
        # load from local file

if __name__ == '__main__':
    taskdf=load_config()
    # Start the bloomberg connection
    bloomberg = blgapi.BLP()
    switch1=raw_input('Download current data? Y/N ')
    switch2=raw_input('Download historical data? Y/N ')
    switch3=raw_input('Upload data to Google Drive? Y/N ')
    if switch1=='Y':
        download_currentdata(taskdf['Current'])
    if switch2=='Y':
        download_historical_data(taskdf['History'])
    if switch3=='Y':
        upload_data()
    # Close the bloomberg connection
    bloomberg.closeSession()


    # 

