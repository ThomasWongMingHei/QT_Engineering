# Example of google spreadsheet 

""" import oauth2client.client, oauth2client.file, oauth2client.tools
import gspread
import pandas as pd

client_id = ''
client_secret = ''

flow = oauth2client.client.OAuth2WebServerFlow(client_id, client_secret, 'https://spreadsheets.google.com/feeds')
storage = oauth2client.file.Storage('D:\QT_Engineering\Calculation\credentials.dat')
credentials = storage.get()
if credentials is None or credentials.invalid:
    import argparse
    flags = argparse.ArgumentParser(parents=[oauth2client.tools.argparser]).parse_args([])
    credentials = oauth2client.tools.run_flow(flow, storage, flags)

gc = gspread.authorize(credentials)

spread = gc.open_by_url("https://docs.google.com/spreadsheets/d/1TIAyQJ_bT3j1R3uR_4sv7JT1FVonir4gekGvLW8oGes/edit?usp=sharing")
sheet  = spread.worksheet('Sheet6')
print(sheet.get_all_values())
df = pd.DataFrame(sheet.get_all_values())
print(df) """

def gspread_client(token='spreadsheettoken.json',credentials='spreadsheetcredentials.json',SCOPES='https://spreadsheets.google.com/feeds'):
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


import pandas as pd


def googlesheetapi_setup(token='spreadsheettoken.json',credentials='spreadsheetcredentials.json',SCOPES='https://www.googleapis.com/auth/spreadsheets.readonly'):
    """ Retrieve sheet data using OAuth credentials and Google Python API. """
    from apiclient.discovery import build
    from httplib2 import Http
    from oauth2client import file, client, tools
    # Setup the Sheets API
    store = file.Storage(token)
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(credentials, SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))
    return service

def gsheet2df(service,spreadsheet_id,range_name="A1:Z20"):
    """ Converts Google sheet data to a Pandas DataFrame.
    Note: This script assumes that your data contains a header file on the first row!
    Also note that the Google API returns 'none' from empty cells - in order for the code
    below to work, you'll need to make sure your sheet doesn't contain empty cells,
    or update the code to account for such instances.
    """
    gsheet = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    header = gsheet.get('values', [])[0]   # Assumes first line is header!
    values = gsheet.get('values', [])[1:]  # Everything else is data.
    if not values:
        print('No data found.')
    else:
        all_data = []
        for col_id, col_name in enumerate(header):
            column_data = []
            for row in values:
                try:
                    column_data.append(row[col_id])
                except IndexError:
                    column_data.append('')
            ds = pd.Series(data=column_data, name=col_name)
            all_data.append(ds)
        df = pd.concat(all_data, axis=1)
        return df


myservice=googledriveapi_setup()
df = gsheet2df(myservice,'1-3oXy_ppVS64bkmxZ08vvTB_ASv2euMqs8RicjZJ01Y')
print('Dataframe size = ', df.shape)
print(df)

