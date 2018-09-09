import pymongo
import pandas as pd

# load configuration 
config=pd.read_csv('mongo_buffer_config.csv')
new=config[config['created']=='N']

new.sort_values('dburl',inplace=True)

# Add new entries to the database 
olddburl=''
for entry in new.iterrows():
    index=entry[0]
    record=entry[1]
    newdburl=record['dburl']
    if newdburl!=olddburl:
        client=pymongo.MongoClient(newdburl)
    db=client.get_database(record['dbname'])
    db.create_collection(record['dbname'],capped=True,max=record['size'])
    olddburl=newdburl
    config.loc[index,'created']='Y'

# Update configuration 
config.to_csv('mongo_buffer_config.csv')
