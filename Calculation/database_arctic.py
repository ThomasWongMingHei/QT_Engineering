import arctic 
import pandas as pd 
import datafeed

def start_library(connection,libname):
    store = Arctic('localhost')

# load configuration 
config=pd.read_csv('arctic_config,csv')
new=config[config['created']=='N']

# Add new entries to the database 
for entry in new.iterrows():
    index=entry[0]
    record=entry[1]
     

    config.loc[index,'created']='Y' 

# Update configuration

