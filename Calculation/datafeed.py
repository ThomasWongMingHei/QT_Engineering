# QT Capital Engineering 

# help of arctic
# https://github.com/manahl/arctic/blob/master/howtos/how_to_use_arctic.py
# install mongodb windows
# https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/

# Need to run this in cmd for starting Local MongoDB at D drive
# "C:\Program Files\MongoDB\Server\3.6\bin\mongod.exe" --dbpath d:\qtdb\mongodb\data

from arctic import Arctic

import arctic

import os 
import pymongo
import pandas as pd

import timeit
import time
import json
import datetime
import random

# =============================================================================
# Configuration for QT Database scripts 
# =============================================================================



Dailycollection='QT_Daily'
TScollection='QT_TimeSeries'

Dailyprocessedcollection='Daily'
TSprocessedcollection='TimeSeries'

Datefield='DATE'
TSfield='DATE'
datafq='1min'

# =============================================================================
# Datafeed conversions 
# Mongodb, Arctic, csv, google spreadsheet 
# =============================================================================

def QT_df2gspread(df,gspath,worksheet):
    # Autheticate google account 
    # Upload dataframe 
    # https://github.com/burnash/gspread
    # https://github.com/robin900/gspread-dataframe

    return None
    
def QT_gspread2df(gspath,worksheet):
    # Autheticate google account 
    # Download dataframe 
    return None 

def QT_csv2gspread(csvpath,gspath,worksheet):
    return None


def QT_mongoclient(url):
    return pymongo.MongoClient(url)

def QT_csv2mongo(client,dbname,collectionname,filename):

    try:
        db = client.get_database(dbname)
        db_cm = db[collectionname]
        tlist = pd.read_csv(filename)
        db_cm.insert_many(tlist.to_dict('records'))
        client.close()
    except:
        print('File not uploaded ', filename)

def QT_df2mongo(client,dbname,collectionname,df):

    try:
        db = client.get_database(dbname)
        db_cm = db[collectionname]
        db_cm.insert_many(df.to_dict('records'))
        client.close()
    except:
        print('Not uploaded ', dbname,collectionname)
        
# Read dataframe from mongo, used for pricing data,
def QT_mongo2df(client,dbname,collectionname):
    
    db = client.get_database(dbname)
    df = pd.DataFrame(list(db[collectionname].find({})))
    try:
        df.drop(['_id'], axis=1,inplace=True)
        df.drop_duplicates(keep='last', inplace=True)
    except:
        print('Record not found',collectionname)
    client.close()
    return df 

def QT_mongo2csv(client,dbname,collectionname,filepath):
    
    db = client.get_database(dbname)
    df = pd.DataFrame(list(db[collectionname].find({})))
    try:
        df.drop(['_id'], axis=1,inplace=True)
        df.drop_duplicates(keep='last', inplace=True)
        df.to_csv(filepath,index=False)
    except:
        print('Record not found',collectionname)
    client.close()
    return df 


def QT_mongo2mongo(client1,dbname1,collectionname1,client2,dbname2,collectionname2):
    # Move a collection from a mongodb to another 
    return None 

def QT_arctichost(host):
    return Arctic(host)

# Download data to arctic db, try to append to existing table or create a bigger table 
def QT_df2arctic(df,store,arcticcollectionname,ticker,indexname=None,alternatename=''):
    # download df from mongo
    # remove duplicate documents(rows)
    # try to append to exisiting table in arctic 
    # if not possible then merge the existing tables to form a bigger table
    
    # Create collectionname if not exist
    try:
        library = store[arcticcollectionname]
    except:
        store.initialize_library(arcticcollectionname)       
    library = store[arcticcollectionname]

    # trying to append the data 
    try:
        library.append(ticker,df, metadata={'Name': alternatename})
        downloaded=True
    except:
        # Try to merge with the old dataframe
        try:
            temp=library.read(ticker)
            olddf=temp.data
            olddf.reset_index(inplace=True)
            df.reset_index(inplace=True)
            newdf=olddf.merge(df,how='outer')
            newdf.set_index(indexname,inplace=True)
            library.write(ticker,newdf, metadata={'Name': alternatename})
            downloaded=True
        except:
            print(ticker,' not updated')
            downloaded=False
    return [downloaded,ticker]

# Move data between arctic collections with option to drop duplicates
def QT_arctic2arctic(store1,arcticcollectionname1,ticker1,store2,arcticcollectionname2,ticker2,cleandata=True):
        
    library1 = store1[arcticcollectionname1]
    try:
        library2=store2[arcticcollectionname2]
    except:
        store2.initialize_library(arcticcollectionname2)
    library2=store2[arcticcollectionname2]

    df=library1.read(ticker1)
    if cleandata:
        newdf=df.drop_duplicates(keep='last')
    else:
        newdf=df
    library2.write(ticker2,newdf, metadata={'source': 'QT'})

# read historical data from arctic 
def QT_arctic2df(store,arcticcollectionname,ticker,start=None,end=None):
    # if start and end not provided, get the whole series
    # if end not provided, assume to get to latest data
    df=pd.DataFrame()
    return df 
    
# =============================================================================
# Database maintenance 
# =============================================================================

def QT_mongoclean(client,dbname,collectionname):
    db = client.get_database(dbname)
    db_cm = db[collectionname]
    db_cm.delete_many({})
    client.close()

def QT_arcticclean(store,collection):

    library = store[collection]
    list=library.list_symbols()
    for sec in list:
        library.delete(sec)
        print('Security is deleted: ',sec)
        
def QT_arctic_list_all_document(store,collectionname):
    library=store[collectionname]
    symbollist=library.list_symbols()
    for sec in symbollist:
        df=library.read(sec)
        print('Security name ',sec,' Collection',collectionname)
        print(df.data.shape[0])
        print(df.data)


def QT_arctic_list_all(store):
    startofprocess = time.time()
    for i in store.list_libraries():
        list_all_document(store,i)
    print('Time used ',time.time()-startofprocess)

def QT_mongo_list_all_document(client,dbname,collectionname):
    return None

def QT_mongo_list_all(client,dbname):
    return None 

        
# =============================================================================
# Data Pre-pcoessing  
# For each data source, write a preprocess function to remove duplicate and set index 
# =============================================================================        

def QT_blghistory(df,indexname,fq):
        #723181 DateString = '01-Jan-1980'
    try:
        df.drop_duplicates(keep='last', inplace=True)
        df[fieldname]=df[fieldname]-723181
        df[fieldname]=df[fieldname].apply(lambda x: pd.to_datetime(x, unit='D',origin=pd.Timestamp('1980-01-01')) )
        df[fieldname]=df[fieldname].dt.round(fq)
        df.drop_duplicates(keep='last', inplace=True)
        df.set_index(fieldname,inplace=True)
        df.sort_index(inplace=True)
    except:
        try:
            df.drop_duplicates(keep='last', inplace=True)
            df.set_index(fieldname,inplace=True)
            df.sort_index(inplace=True)
        except:
            return df
        return df
    return df

# =============================================================================
# Datetime functions 
# Trading calendars 
# https://github.com/ThomasWongMingHei/pandas_market_calendars/blob/master/README.rst
# To create new calendars, need to fork the above github repo and add new exchange_calendar_qtcustom.py
# and then import this to  calendar_utils.py
# More details will be given on how to create new calendars 
# =============================================================================         

def QT_shiftdate(date,shift):
    date2=pd.to_datetime(date)+pd.Timedelta(datetime.timedelta(days=shift))
    print(date2)
    return date2

# shifttime('2018-06-05','09:00:00',1,'09:00:00')
def QT_shifttime(date,time,shiftdate,shifttime):
    time2=pd.to_datetime(date+' '+time)
    mydelta=pd.to_timedelta(str(shiftdate)+' days '+shifttime)
    time3=time2+mydelta 
    return time3


# =============================================================================
# Email functions 
# =============================================================================

# send an email with a list of attachments of csv/textfile/df

def QTEmail_attach(sender_mail, sender_password, receiver_db_url, 
                    receiver_db_name, receiver_list, text_file, attachments):
    
    df = QT_mongo2df(receiver_db_url, receiver_db_name, receiver_list)
    names = df['name']
    emails = df['email']

    html = ''
    for attachment in attachments:
        # Determine type of attachment
        # attach to the html message using suitable ways 
        df = pd.read_csv(attachment, engine = 'python')
        html = html + df.to_html()
    del df

    with open(text_file, 'r', encoding='utf-8') as message_file:
        message_file_content = message_file.read()
        message = Template(message_file_content)
    
    s = smtplib.SMTP(host = 'smtp.gmail.com', port = 587)
    s.starttls()
    s.login(sender_mail, sender_password)

    # now iterate the dataframe to get name and email     
    for name, email in zip(names, emails):
        msg = MIMEMultipart()
        _message = message.safe_substitute(PERSON_NAME = name)
        msg['From'] = 'QT Capital Engineering'
        msg['To'] = email
        msg['Subject'] = 'ALERT'
        part = MIMEText(_message + html, 'html')
        msg.attach(part)
        s.send_message(msg)
        del msg 
    s.quit()


# =============================================================================
# Flask functions 
# =============================================================================

def QT_df2csv_html(df,fname):
    from flask import make_response
    resp = make_response(df.to_csv())
    resp.headers["Content-Disposition"] = "attachment; filename="+fname
    resp.headers["Content-Type"] = "text/csv"
    return resp











# ============================================================================
# Pre-process functions 
# Maybe not relevant for new config
# ============================================================================

def QT_select_range(df,fieldname,start,end):
    
    #723181 DateString = '01-Jan-1980'
    df.sort_index(inplace=True)
    df=df.truncate(start,end)
    return df


def QT_check_unique(df):
    qtindex=df.index.get_values()
    temp=pd.Series(qtindex).unique()
    if len(qtindex)==len(temp):
        return True
    else:
        return False 

def QT_check_empty(df):
    if df.shape[0]==0:
        return True
    else:
        return False 

def QT_remove_nondata(df):
    # remove columns of all zero or na
    df.dropna(axis=1,how='all',inplace=True)
    df=df.loc[:, (df != 0).any(axis=0)]
    return df
