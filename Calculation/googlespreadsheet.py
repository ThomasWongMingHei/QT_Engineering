# Example of google spreadsheet 

import oauth2client.client, oauth2client.file, oauth2client.tools
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
print(df)

