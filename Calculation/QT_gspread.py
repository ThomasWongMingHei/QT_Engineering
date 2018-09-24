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
    import gspread_dataframe
    return None 






