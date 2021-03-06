
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


import datetime 

pd.options.display.max_rows = 10000
pd.options.display.max_columns = 30

Downloadfolder='H:/QT_Engineering/CurrentData/'
Downloadfolder2='H:/QT_Engineering/Data/'


def _currentdate():
    return datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_")
    
def _prasename(x):
    y=x.replace('/','')
    return y

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
        #exchangecode=record['Exchangecode']
    
        # Download recent data as dataframe 
        if downloadmethod=='bdp' or  downloadmethod=='BDP':
            try:               
                print(security, fieldlist)
                result=bloomberg.bdp(security, fieldlist)
                result['Download_Time']=datetime.datetime.now()
                recentdata.append(result)
                print(result)
            except:
                print('Error ',security)
    
        #Download historical intraday data
        if downloadmethod=='Intraday':
            try:
                print(security,start,end,eventtype,freq)
                result=bloomberg.blgbar(security,start,end,eventtype,freq)
                print(result)
            except:
                print('Error ',security)
    
            # Save results 
        if sendmethod=='csv':
            csvpath=_prase_name(security)+'.csv'
            csvpath=Downloadfolder+_currentdate()+csvpath
            result.to_csv(csvpath)
            # send results through google drive api
    
    
    # prepare the summary bdp dataframe 
    # Upload all the csv files in the directory to google_drive
    currentdatafolder=Downloadfolder
    allcurrentbdp=pd.concat(recentdata)
    filename=currentdatafolder+_currentdate()+'bdpdata.csv'
    print(allcurrentbdp)
    allcurrentbdp.to_csv(filename)
    
    print(recentdf)
    return recentdf



def download_historical_data(historydf):

    # For each command in historical request file, run the command 
    for entry in historydf.iterrows():
        record=entry[1]
        downloadmethod=record['Subscription']
        security=record['GST']
        fieldlist=record['Datafields'].split(',')
        freq=record['Frequency']
        start=datetime.datetime.strptime(record['Start'],'%d/%m/%Y').date()
        end=datetime.datetime.strptime(record['End'],'%d/%m/%Y').date()
        sendmethod=record['Location']
        csvpath=record['Filepath']
        dburl=record['dburl']
        dbname=record['dbname']
        dbcollection=record['dbcollection']
        eventtype=record['Eventtype']
        #exchangecode=record['Exchangecode']
    
    
    
        # Download historical pricing data 
        # Equities data always split adjusted
        if downloadmethod=='bdh' or downloadmethod=='BDH':
            try:
                print(security,start,end,eventtype,freq)
                result=bloomberg.bdh(security,fieldlist,start,end,adjustmentSplit=True,periodicity=freq)
                print(result)
            except:
                result=pd.DataFrame()
            # Set index for historical data
    
        #Download historical intraday data
        if downloadmethod=='Intraday':
            try:
                print(security,start,end,eventtype,freq)
                result=bloomberg.blgbar(security,start,end,eventtype,freq)
                print(result)
            except:
                print('Error ',security)
      
        # Save results 
        if sendmethod=='csv':
            csvpath=_prase_name(security)+'.csv'
            csvpath=Downloadfolder2+_prasename(record['Start'])+' '+_prasename(record['End'])+csvpath
            result.to_csv(csvpath)
            # send results through google drive api
    



# Read the config file
def load_config():
    # load from local file
    recentdf=pd.read_csv('H:/QT_Engineering/Bloomberg/recentcfg.csv')
    historydf=pd.read_csv('H:/QT_Engineering/Bloomberg/historycfg.csv')
    print(recentdf)
    print(historydf)
    return{'Recent':recentdf,'History':historydf}

if __name__ == '__main__':
    taskdf=load_config()
    # Start the bloomberg connection
    bloomberg = blgapi.BLP()
    switch1=input('Download current data? Y/N ')
    switch2=input('Download historical data? Y/N ')
    if switch1=='Y':
        download_currentdata(taskdf['Recent'])
    if switch2=='Y':
        download_historical_data(taskdf['History'])
    # Close the bloomberg connection
    bloomberg.closeSession()


  