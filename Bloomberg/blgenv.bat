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
