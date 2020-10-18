
import os, sys
import csv
from bs4 import BeautifulSoup
import urllib
from urllib.request import urlopen as browser
import xlsxwriter
import pdb

stock_list = [["DRREDDY"],["CIPLA"],["ADANIPORTS"],["BHARTIARTL"],["M&M"],
             ["HDFCBANK"],["SHREECEM"],["BAJAJFINSV"],["KOTAKBANK"],["MARUTI"]]
with open('stocks_bse.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(stock_list)
    file.close()
####Stats we are scraping 

key_stats =['ltpid','change','ChangePercent','Volume','MarketCap',
            'PE Ratios','EPS (Rs.)','Sales (Rs. Cr)',
            'Margin (%)','Last Dividend(%)','Average Equity']


stocks_arr =[]
# keep csv in same path as code
pfolio_file= open("stocks_bse.csv", "r")
for line in pfolio_file:
    indv_stock_arr = line.strip().split(',')
    stocks_arr.append(indv_stock_arr)

print(stocks_arr)


stock_info_arr = []

for stock in stocks_arr:
    stock_info = []
    ticker = stock[0]
    stock_info.append(ticker)

    url = "https://money.rediff.com/companies/{0}".format(ticker)


    innerHTML = browser(url)

    soup = BeautifulSoup(innerHTML.read(), 'html.parser')
    innerHTML.close()
   
    for stat in key_stats:
        try:
            try:
                 page_stat1 = soup.find(text=stat).find_parent("div")
                 page_row1 = page_stat1.find_parent("div")
                 page_statnum1 = page_row1.find('div',{"class": "floatR"}).get_text(strip=True)
                 print(page_statnum1)
            except:
                 page_statnum1 = soup.find("span", {"id": stat}).get_text(strip=True)
                 print(page_statnum1)
        except:
                 print('Invalid parent for this element')
                 page_statnum1 = "N/A"       

        stock_info.append(page_statnum1)

    
    stock_info_arr.append(stock_info)

print(stock_info_arr)
stat_clmn = [x.replace('ltpid', 'Current Price').replace('Margin (%)', 'Net Profit Margin (%)').replace('Average Equity', 'Return on Average Equity') for x in key_stats]
########## WRITING OUR RESULTS INTO EXCEL
# key_stats.extend(key_stats_on_stat)
workbook = xlsxwriter.Workbook('Portfolio Stat.xlsx')
worksheet = workbook.add_worksheet()
row = 0
col = 1

for stat in stat_clmn:
    worksheet.write(row, col, stat)
    col +=1

row = 1
col = 0
for our_stock in stock_info_arr:
    col = 0
    for info_bit in our_stock:
        worksheet.write(row, col, info_bit)
        col += 1
    row += 1
workbook.close()

print('Script completed')