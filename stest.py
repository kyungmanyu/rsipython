import numpy as np
import pandas as pd 
import pandas_datareader.data as web
import datetime

start=datetime.datetime(2019,10,1)
end=datetime.datetime(2019,11,6)
stock_ds=web.DataReader('035250.KS',"yahoo",start,end)
date_index=stock_ds.index.astype('str')

def calcRSI(df,period):
    #df.diff를 통해 (기준일 종가-기준일전일 종가)를 계산하여 0보다 크면 증가분을 감소했으면 0을 넣어줌
    U = np.where(df.diff(1)['Close'] > 0 , df.diff(1)['Close'],0)
    #df.diff를 통해 (기준일 종가-기준일 전일종가)를 계산하여 0보다작으면 감소분을 증가했으면 0을 넣어줌
    D = np.where(df.diff(1)['Close'] < 0 , df.diff(1)['Close']*(-1),0)
    #AU, period=14일 동안의 U의 평균
    AU = pd.DataFrame(U,index=date_index).rolling(window=period).mean()
    #AD, period=14일동안에 D의 평균
    AD = pd.DataFrame(D,index=date_index).rolling(window=period).mean()
    #0부터 1로 표현되는 RSI에 100을 곱함
    RSI = AU / (AD+AU)*100
    return RSI

#web.DataReader를 통해 받았던 원래 DataFrame에 'RSI'열을 추가
stock_ds.insert(len(stock_ds.columns),"RSI", calcRSI(stock_ds,14))
#RSI signal(RSI이동평균)을구해서 추가함
stock_ds.insert(len(stock_ds.columns),"RSI signal",stock_ds['RSI'].rolling(window=9).mean())
print(stock_ds)

