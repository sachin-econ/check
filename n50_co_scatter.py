import numpy as np
import pandas as pd
import pandas_datareader.data as web
import datetime as dt
from dateutil.relativedelta import relativedelta
import pickle
from bs4 import BeautifulSoup
from urllib.request import urlopen as browser
import matplotlib.pyplot as plt
import seaborn as sb
from matplotlib import style


style.use('ggplot')
plt.rcParams['axes.facecolor'] = 'white'

def nifty50_tickers():
    req = browser('https://en.wikipedia.org/wiki/NIFTY_50')
    soup = BeautifulSoup(req.read(), 'html.parser')
    table = soup.find('table', {'id': 'constituents'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[1].text
        tickers.append(ticker)

    with open("nifty50_tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)

    # print(tickers)

    return(tickers)


nifty50_tickers()


def nifty_50():
    with open("nifty50_tickers.pickle", "rb") as f:
        tickers = pickle.load(f)

    start_date = dt.datetime.now() - relativedelta(years=10)  # dt.datetime(2010, 9, 1)
    end_date = dt.date.today()
    combine_df = pd.DataFrame()

    for ticker in tickers:
        print(ticker)
        df = web.DataReader(ticker, 'yahoo', start_date, end_date)
        df.rename(columns={'Adj Close': ticker}, inplace=True)
        df.drop(['Open', 'High', 'Low', 'Close', 'Volume'], 1, inplace=True)
        if combine_df.empty:
            combine_df = df
        else:
            combine_df = combine_df.join(df, how='outer')
    combine_df.to_csv('n50_closes.csv')


nifty_50()


def corrl_heatmap():
    df = pd.read_csv('n50_closes.csv')
    df_corr = df.corr()
    mask = np.triu(np.ones_like(df_corr, dtype=np.bool))
    
    fig, ax = plt.subplots(figsize=(12,10))
    
    mask = mask[1:, :-1]
    corr = df_corr.iloc[1:,:-1].copy()
    
    sb.heatmap(corr, mask=mask, linewidths=1.5, fmt = ".2f", cmap="rocket",
               vmin=-1, vmax=1, cbar_kws={"shrink": .8}, square=True)  
    
    yticks = [i.upper() for i in corr.index]
    xticks = [i.upper() for i in corr.columns]
    
    plt.yticks(plt.yticks()[0],labels=yticks, rotation=0)
    plt.xticks(plt.xticks()[0],labels=xticks)
    
    title = 'Correlation Matrix\nNIFTY 50 Index\n'   
    plt.title(title, loc='left',fontsize=18)
    
    plt.show()


corrl_heatmap()
