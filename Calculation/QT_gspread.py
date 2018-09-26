'''
Gspread 

Setup: https://developers.google.com/sheets/api/quickstart/python
Download the credentials.json file to working directory 

'''

def gspread_client(token='token.json',credentials='credentials.json',SCOPES=['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']):
    """ Retrieve sheet data using OAuth credentials and Google Python API. """
    from oauth2client import file, client, tools
    import gspread
    # Setup the Sheets API
    store = file.Storage(token)
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(credentials, SCOPES)
        creds = tools.run_flow(flow, store)
    gc = gspread.authorize(creds)
    return gc 

def list_all_spreadsheet(gclient):
    list_spreadsheet=gclient.openall()
    for s in list_spreadsheet:
        print('Sheet ID: ',s.id)
        print('Sheet Name: ',s.title)

def csv2sheet(gclient,csvfilename,spreadsheetname,sheetname):
    from gspread_dataframe import set_with_dataframe
    import pandas as pd 
    df=pd.read_csv(csvfilename)
    currentsheet=gclient.open(spreadsheetname).worksheet(sheetname)
    set_with_dataframe(currentsheet, df)
    return None 

def sheet2df(gclient,spreadsheetname,sheetname,evaluate_formulas=True):
    from gspread_dataframe import get_as_dataframe
    currentsheet=gclient.open(spreadsheetname).worksheet(sheetname)
    df=get_as_dataframe(currentsheet,evaluate_formulas=evaluate_formulas)
    df.dropna(axis=0,how='all',inplace=True)
    df.dropna(axis=1,how='all',inplace=True)
    return df

def _current_date():
    from datetime import datetime
    return datetime.now().strftime("%Y_%m_%d_%H_%M_%S")


def _download_current_price(client,cfgfile,spreadsheet,sheet,email='qtengineeringcorestrats@gmail.com',output='D:\\QT_Engineering\\Calculation\Data\\',timesleep=5):
    import pandas as pd 
    size=pd.read_csv(cfgfile).shape
    try:
        sh=client.open(spreadsheet)
    except:
        sh=client.create(spreadsheet)
        sh.share(email, perm_type='user', role='writer')
    try:
        worksheet=sh.worksheet(sheet)
    except:
        worksheet=sh.add_worksheet(title=sheet,rows=str(size[0]),cols=str(size[1])) 
    csv2sheet(client,cfgfile,spreadsheet,sheet)
    import time 
    time.sleep(timesleep)
    df=sheet2df(client,spreadsheet,sheet)
    df.replace(to_replace=r"^#.*", value='', regex=True,inplace=True)
    outputfile=output+spreadsheet[14:]+_current_date()+'.csv'
    df.to_csv(outputfile,index=False)
    empty=df[df['tradetime']=='']
    return empty 

def download_current_price(client,tickerfile,cfgfile,spreadsheet,sheet,email='qtengineeringcorestrats@gmail.com',output='D:\\QT_Engineering\\Calculation\Data\\',timesleep=5):
    import googlefinance_cfg as gfcg 
    gfcg.generate_cfg(tickerfile,cfgfile)
    empty=_download_current_price(client,cfgfile,spreadsheet,sheet,email='qtengineeringcorestrats@gmail.com',output='D:\\QT_Engineering\\Calculation\Data\\',timesleep=5)
    print("Current data downloaded: ",tickerfile)
    return empty 

if __name__ == '__main__':
    myclient=gspread_client(credentials='D:\QT_Engineering\Calculation\credentials.json')
    #list_all_spreadsheet(myclient)
    empty1=download_current_price(myclient,'D:\QT_Engineering\Calculation\Config\Vanguard.csv','D:\QT_Engineering\Calculation\Config\Vanguardcfg.csv','Googlefinance_Vanguard','Current')
    empty2=download_current_price(myclient,'D:\QT_Engineering\Calculation\Config\LSE_ETF.csv','D:\QT_Engineering\Calculation\Config\LSE_ETFcfg.csv','Googlefinance_LSE_ETF','Current',timesleep=10)
    empty3=download_current_price(myclient,'D:\QT_Engineering\Calculation\Config\LSE_equities.csv','D:\QT_Engineering\Calculation\Config\LSE_equitiescfg.csv','Googlefinance_LSE_equities','Current',timesleep=10)
    import pandas as pd
    empty=pd.concat([empty1,empty2,empty3],ignore_index=True)
    print('Error tickers')
    print(empty[['Name','Ticker']])








