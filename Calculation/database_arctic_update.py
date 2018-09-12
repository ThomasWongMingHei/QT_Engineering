# Make sure MongoDB is running in the data folder 

import arctic 
import pandas as pd 
import datafeed
import datetime


# load configuration 
config=pd.read_csv('arctic_config,csv')
bloomberg=pd.read_csv('cfg_blgterminal.csv')
localstore = arctic.Arctic('localhost')
success=[]
fail=[]


# Add new entries to the database 
for entry in config.iterrows():
    index=entry[0]
    record=entry[1]
    sendmethod=record['method']
    csvpath=record['filepath']

    # Download data from Mongo or csv and set index for the dataframe
    if sendmethod=='csv':
        csvpath='Data/'+csvpath
        pricedata=pd.read_csv(csvpath,index_col=0)
    if sendmethod=='mongo':
        client=datafeed.QT_mongoclient(record['mongourl'])
        pricedata=datafeed.QT_mongo2df(client,record['mongoname'],record['mongocollection'])
        pricedata.set_index(record['indexname'],inplace=True)

    # Add data to Arctic 
    if record['host']=='localhost':
        [downloaded,ticker]=datafeed.QT_df2arctic(pricedata,localstore,record['library'],record['ticker'],record['indexname'],record['name'])
        datafeed.QT_arctic2arctic(localstore,record['library'],record['ticker'],localstore,record['library'],record['ticker'])
        if downloaded:
            success.append(ticker)
            if sendmethod=='mongo':
                datafeed.QT_mongoclean(client,record['mongoname'],record['mongocollection'])
        else:
            fail.append(ticker)

# Report on success and fail list to email 

successdf=pd.DataFrame({'success':success})
faildf=pd.DataFrame({'fail':fail})

# Generate inventory of database and the next config file for bloomberg terminal
# Generate list of dictionary for the dataframe
# 
# csv updates in bloomberg will not persist
updates=bloomberg[bloomberg['method']=='mongo'] 
config['Last Entry']=''
inventory=[]
for lib in localstore.list_libraries():
    for symbol in lib.list_symbols():
        buffer=lib.read(symbol)
        last=buffer.data.last_valid_index()
        name=buffer.metadata['Name']
        config.loc[name,'Last Entry']=pd.to_datetime(last).date
        record={'host':'localhost','library':lib,'symbol':symbol,'Name':name}
        inventory.append(record)

# bloomberg config updates       
configupdates=config[['name','Last Entry']].copy()
updates.drop(['Start'],axis=1,inplace=True)
updates=updates.join(configupdates,on='name',how='left')
updates['Start']=updates['Last Entry']+datetime.timedelta(days=1)

updatesurl=''
updatesdb=''
updatescollection='Bloomberg'
client=datafeed.QT_mongoclient(updatesurl)
datafeed.QT_df2mongo(client,updatesdb,updatescollection,updates)
        




