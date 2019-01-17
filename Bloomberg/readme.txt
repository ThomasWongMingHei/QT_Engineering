# QT Engineering 

Tasks to do:

1. Add option to take files to remote drive, useful when downloading huge amount of data, 
we can add download to remote drive option to the current and history data option

2. Configuration of current data, how to determine start and end date for the intraday and historical data request

3. Schedule for downloading current data at regular time intervals to generate intraday snapshot of non-pricing data

4. Subscription to security: what to do when there is updates in pricing, design buffer to save the file 

5. 
(Optional) Make sure Anaconda2 and git is on the computer,  get it through Software Hub 


Start bbcomm it is in the blg folder

1. Download the folder for QT_Engineering
H:\QT_Engineering should be the path 


2. Set env variables 
set BLPAPI_ROOT=H:\QT_Engineering\Bloomberg\bloomberg_api\blpapi_cpp_3.8.18.1
set PATH=%PATH%H:\QT_Engineering\Bloomberg\bloomberg_api\blpapi_cpp_3.8.18.1\bin;



3. Install packages using Anaconda prompt 
conda install python=3.6
python -m pip install --index-url=https://bloomberg.bintray.com/pip/simple blpapi
pip install --upgrade google-api-python-client oauth2client
pip install pyDrive
pip install gspread
pip install gspread_dataframe

4. Test running 

python 
import blpapi
import QT_pydrive

5. change directory to H:\QT_Engineering\Bloomberg
   Run the srcipt to download data

6. After checking the data is downloaded, please delete the existing files 

python H:/QT_Engineering/Bloomberg/blgterminal_task.py


C:\ProgramData\Anaconda3\Scripts\activate.bat
conda create -n env_blg
conda activate env_blg
conda install python=3.6
python -m pip install --index-url=https://bloomberg.bintray.com/pip/simple blpapi==3.9.2
pip install --upgrade google-api-python-client oauth2client
pip install pyDrive
pip install gspread
pip install gspread_dataframe
conda install pandas


C:\ProgramData\Anaconda3\Scripts\activate.bat
conda activate env_blg
python H:/QT_Engineering/Bloomberg/blg_task.txt




qtengineeringcorestrats@gmail.com >> bloomberg









(Optional) Make sure Anaconda2 and git is on the computer,  get it through Software Hub 


(Optional) Download and unzip blpapi_cpp_3.8.18.1 and save at any suitable path

https://www.bloomberg.com/professional/support/api-library/

Login to bloomberg terminal
Start bbcomm

1. Download the folder for QT_Engineering
H:\QT_Engineering should be the path 


2. Set env variables 
set BLPAPI_ROOT=H:\QT_Engineering\Bloomberg\bloomberg_api\blpapi_cpp_3.8.18.1
set PATH=%PATH%H:\QT_Engineering\Bloomberg\bloomberg_api\blpapi_cpp_3.8.18.1\bin;



3. Install packages using Anaconda prompt 
conda install cython
python -m pip install --index-url=https://bloomberg.bintray.com/pip/simple blpapi

# pip install git+https://github.com/cuemacro/findatapy.git ## require [ython>3.4 does not work on Imperial computers
pip install pymongo
pip install git+https://github.com/manahl/arctic.git
pip install --upgrade google-api-python-client oauth2client
pip install pyDrive



4. Test running 

python 

import blpapi

import pymongo






import findatapy
import QT_pydrive
5. Run the srcipt to download data

(*) 
Windows
Locate the directory for the conda environment in your Anaconda Prompt by running in the command shell %CONDA_PREFIX%.

Enter that directory and create these subdirectories and files:

cd C:\Users\Thomas\AppData\Local\conda\conda\envs\env_prod
mkdir .\etc\conda\activate.d
mkdir .\etc\conda\deactivate.d
type NUL > .\etc\conda\activate.d\env_vars.bat
type NUL > .\etc\conda\deactivate.d\env_vars.bat

Edit .\etc\conda\activate.d\env_vars.bat as follows: (Replace D drive with the suitable drive 

set BLPAPI_ROOT=H:\QT_Engineering\Bloomberg\bloomberg_api\blpapi_cpp_3.8.18.1
set PATH=%PATH%H:\QT_Engineering\Bloomberg\bloomberg_api\blpapi_cpp_3.8.18.1\bin;

Edit .\etc\conda\deactivate.d\env_vars.bat as follows:
set BLPAPI_ROOT=

When you run activate analytics, the environment variables are set to the values you wrote into the file. When you run deactivate, those variables are erased.




