# -*- coding: utf-8 -*-
"""
This script is to download data from bloomberg terminal and save as csv or upload to mlab
Require: 
Active Bloomberg terminal login
set env variable for PATH to include the folder to blpapi C++ DSK so that blpapi can be imported

CSV download method is for one off tasks
Mongo download method is for daily/weekly updates

"""

import blgapi
import pandas as pd
import pymongo 
from datetime import datetime 


# Read the config file or download from mlab 

configdf=pd.read_csv('cfg_blgterminal.csv')
bloomberg = blgapi.BLP()

# For each command in config file, run the command 
for entry in configdf.iterrows():
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

    # Download recent data as string 
    if downloadmethod=='bdp' or  downloadmethod=='BDP':
        result=bloomberg.bdp(security, fieldlist)
    
    # Download historical pricing data 
    # Equities data always split adjusted
    if downloadmethod=='bdh' or downloadmethod=='BDH':
        result=bloomberg.bdh(security,fieldlist,start,end,adjustmentSplit=True,periodicity=freq)
        # Set index for historical data
  
    # Save results 
    if sendmethod=='csv':
        csvpath='Data/'+csvpath
        result.to_csv(csvpath)

    if sendmethod=='mongo':
        client=pymongo.MongoClient(dburl)
        db = client.get_database(dbname)
        db_cm = db[dbcollection]
        db_cm.insert_many(df.to_dict('records'))
        client.close()

# Close the bloomberg connection
bloomberg.closeSession()


# 

