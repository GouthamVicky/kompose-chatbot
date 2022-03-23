import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

def iter_pd(df):
    for val in df.columns:
        yield val
    for row in df.to_numpy():
        for val in row:
            if pd.isna(val):
                yield ""
            else:
                yield val

def pandas_to_sheets(pandas_df, sheet, clear = True):
    # Updates all values in a workbook to match a pandas dataframe
    if clear:
        sheet.clear()
    (row, col) = pandas_df.shape
    cells = sheet.range("A1:{}".format(gspread.utils.rowcol_to_a1(row + 1, col)))
    for cell, val in zip(cells, iter_pd(pandas_df)):
        cell.value = val
    sheet.update_cells(cells)

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)

gc = gspread.authorize(credentials)


def gsheet_upload(sheetid,sheetname,collectioName):
    
    workbook = gc.open_by_key(sheetid)
    sheet = workbook.worksheet(sheetname)

    client = MongoClient(os.getenv('mongo_client_url'))
    db=client[collectioName]
    db=db.myCollection

    df = pd.DataFrame(list(db.find()))
    print(df)
    df.drop(columns=['_id'], inplace=True)
    print(df)
    pandas_to_sheets(df, workbook.worksheet(sheetname), clear=True)
