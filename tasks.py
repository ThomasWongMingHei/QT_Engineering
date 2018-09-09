import pandas
from Calculation import datafeed


# Define the tasks in the script as a function 
# Configuration can be written in the tasks as a dictionary or dataframe 
# or import from the Configuration folder

def task1():
    from Calculation import datafeed
    print('Running task 1')
    datafeed.QT_mongoclient('localhost')
    return None 

