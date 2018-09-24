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
    currentsheet=gclient.open(spreadsheetname).worksheet(sheetname)
    set_with_dataframe(currentsheet, df)
    return None 

if __name__ == '__main__':
    myclient=gspread_client()
    list_all_spreadsheet(myclient)
    csv2sheet(myclient,)






