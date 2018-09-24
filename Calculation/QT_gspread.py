# Example of google spreadsheet 

def gspread_client(token='spreadsheettoken.json',credentials='spreadsheetcredentials.json',SCOPES=['https://spreadsheets.google.com/feeds',
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
    print(df)
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

if __name__ == '__main__':
    myclient=gspread_client()
    list_all_spreadsheet(myclient)
    csv2sheet(myclient,'LSE_equitiescfg.csv','Googlefinance_currentprice','Current')
    import time
    time.sleep(2)
    mydf=sheet2df(myclient,'Googlefinance_currentprice','Current')
    print(mydf)
    mydf.to_csv('Googlefinanceoutput.csv',index=False)

    import pandas as pd 
    mydf=sheet2df(myclient,'LSE_Equities','Shares')
    df=pd.DataFrame()
    df['Name']=mydf['Issuer Name']
    df['Ticker']=['LON:'+ x for x in mydf['TIDM']]
    df.to_csv('LSE_equities.csv',index=False)







