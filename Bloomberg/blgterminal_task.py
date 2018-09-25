# -*- coding: utf-8 -*-
"""
This script is to download data from bloomberg terminal and save as csv or upload to mlab
Require: 
Active Bloomberg terminal login
set env variable for PATH to include the folder to blpapi C++ DSK so that blpapi can be imported

Need to refer to QT_pydrive 

set BLPAPI_ROOT=D:\bloomberg_api\blpapi_cpp_3.8.18.1
set PATH=%PATH%;D:\bloomberg_api\blpapi_cpp_3.8.18.1\bin
conda install cython
python -m pip install --index-url=https://bloomberg.bintray.com/pip/simple blpapi

pip install pymongo
pip install git+https://github.com/manahl/arctic.git

pip install --upgrade google-api-python-client oauth2client
pip install pyDrive
pip install gspread gspread_dataframe

"""

import blgapi

import pandas as pd
import pymongo 
import pydrive
import QT_pydrive
import QT_gspread

from datetime import datetime 

def _current_date():
    return datetime.now().strftime("%Y_%m_%d_%H_%M_%S_")


# Read the config file or download from mlab 
gclient=QT_gspread.gspread_client(credentials='D:\\QT_Engineering\\Bloomberg\\credentials.json')
recentdf=QT_gspread.sheet2df(gclient,'Bloomberg_recent_data_cfg','Recent_data')
historydf=QT_gspread.sheet2df(gclient,'Bloomberg_historical_data_cfg','Historical_data')

bloomberg = blgapi.BLP()

# For each command in recent data request file, run the command

recentdata=[]

for entry in recentdf.iterrows():
    record=entry[1]
    downloadmethod=record['Subscription']
    security=record['GST']
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
        result=bloomberg.bdp(security, fieldlist)
        recentdata.append(result)

    #Download historical intraday data
    if downloadmethod=='Intraday':
        result=bloomberg.blgbar(security,start,end,eventtype,freq)

        # Save results 
    if sendmethod=='csv':
        csvpath='Data/'+_currentdate()+csvpath
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
currentdatafolder='D:\\QT_Engineering\\Bloomberg\\CurrentData\\'
allcurrentbdp=pd.concat(recentdata)
filename=currentdatafolder+_currentdate()+'bdpdata.csv'
allcurrentbdp.to_csv(filename)
drive=QT_pydrive.create_pydrive_auth()
QT_pydrive.upload_folder_pydrive(drive,currentdatafolder,'Bloomberg_CurrentData')




# For each command in historical request file, run the command 
for entry in historydf.iterrows():
    record=entry[1]
    downloadmethod=record['Subscription']
    security=record['GST']
    fieldlist=record['Datafields'].split(',')
    freq=record['Frequency']
    start=datetime.strptime(record['Start'],'%Y%m%d').date()
    end=datetime.strptime(record['End'],'%Y%m%d').date()
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
    
    # Download historical pricing data 
    # Equities data always split adjusted
    if downloadmethod=='bdh' or downloadmethod=='BDH':
        result=bloomberg.bdh(security,fieldlist,start,end,adjustmentSplit=True,periodicity=freq)
        # Set index for historical data

    #Download historical intraday data
    if downloadmethod=='Intraday':
        result=bloomberg.blgbar(security,start,end,eventtype,freq)
  
    # Save results 
    if sendmethod=='csv':
        csvpath='Data/'+_currentdate()+csvpath
        result.to_csv(csvpath)
        # send results through google drive api

    if sendmethod=='mongo':
        client=pymongo.MongoClient(dburl)
        db = client.get_database(dbname)
        db_cm = db[dbcollection]
        db_cm.insert_many(result.to_dict('records'))
        client.close()

# Upload all the csv files in the directory to google_drive
currentdatafolder='D:\\QT_Engineering\\Bloomberg\\Data'
drive=QT_pydrive.create_pydrive_auth()
QT_pydrive.upload_folder_pydrive(drive,currentdatafolder,'Bloomberg_Data')




# Close the bloomberg connection
bloomberg.closeSession()


# 

