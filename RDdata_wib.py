import urllib.request as browser
import xlrd
import pandas as pd



url = 'http://api.worldbank.org/v2/en/indicator/GB.XPD.RSDV.GD.ZS?downloadformat=excel'
file_path = r'C:\Users\psach\Desktop\New project\rd_data.xls'

browser.urlretrieve(url,file_path)

wb = xlrd.open_workbook(file_path)
sheet = wb.sheet_by_index(0)

nrows = sheet.nrows

clmn_headers = sheet.row_values(3)

rows = []

for i in range(4,nrows):
    row = sheet.row_values(i)
    rows.append(row)

df = pd.DataFrame(rows,columns=clmn_headers)

for clmn in clmn_headers[4:]:
    df[clmn] = pd.to_numeric(df[clmn], errors='coerce')

df = df.drop(clmn_headers[1:40], axis = 1)
df = df.drop(['2019','2020'],axis = 1)
    
df = df.dropna()
