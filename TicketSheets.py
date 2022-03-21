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

workbook = gc.open_by_key("1AfmD71eoJmcWEyuLBXlHTeUnW7YXVvY1yFue1OC5-qw")
sheet = workbook.worksheet("Sheet1")

client = MongoClient(os.getenv('mongo_client_url'))
db=client['kompose_lead_form']
db=db.myCollection

df = pd.DataFrame(list(db.find()))
print(df)
df.drop(columns=['_id'], inplace=True)
pandas_to_sheets(df, workbook.worksheet("Sheet1"))
