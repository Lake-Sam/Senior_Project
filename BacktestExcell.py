import stockerback 

import tensorflow as tf
import pandas as pd
                                         #Importing all the librarys and such I think I may need.
import yfinance as yf
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

from numba import jit, cuda
import numpy as np

import tkinter as tk                                    #GUI


from collections import OrderedDict

from datetime import date, timedelta
import datetime as dt
from pytz import timezone


from requests.exceptions import ConnectionError
import logging
tf.get_logger().setLevel(logging.ERROR)

fivehuna = ["MMM","ABT","ANF","ACN","ADBE","AMD","AES","AFL","A","GAS","APD","AKAM","AA","ATI","ALL","ANR","ALTR","MO","AMZN","AEE","AEP","AXP","AIG","AMT","AMP","ABC","AMGN","APH","ADI","AON","APA","AIV","AAPL","AMAT","ADM","AIZ","T","ADSK","ADP","AN","AZO","AVB","AVY","BAC","BK","BAX","BEAM","BDX","BBBY","BBY","BIG","BIIB","BLK","HRB","BA","BWA","BXP","BSX","BMY","CHRW","CPB","COF","CAH","KMX","CCL","CAT","CNP","CF","SCHW","CHK","CVX","CMG","CB","CI","CINF","CTAS","CSCO","C","CLF","CLX","CME","CMS","KO","CTSH","CL","CMCSA","CMA","CSC","CAG","COP","CNX","ED","STZ","GLW","COST","CCI","CSX","CMI","CVS","DHI","DHR","DRI","DVA","DE","DELL","XRAY","DVN","DV","DFS","DLTR","D","DOV","DOW","DTE","DD","DUK","DNB","EMN","ETN","EBAY","ECL","EIX","EW","EA","EMC","EMR","ETR","EOG","EQT","EFX","EQR","EL","EXC","EXPE","EXPD","XOM","FFIV","FAST","FDX","FIS","FITB","FHN","FSLR","FE","FISV","FLS","FLR","FMC","FTI","F","FOSL","BEN","FCX","GME","GCI","GPS","GD","GE","GIS","GPC","GNW","GILD","GS","GT","GOOG","GWW","HAL","HOG","HAR","HIG","HAS","HCP","HP","HES","HPQ","HD","HON","HRL","HST","HUM","HBAN","ITW","IR","TEG","INTC","ICE","IBM","IFF","IGT","IP","IPG","INTU","ISRG","IVZ","IRM","JBL","JNJ","JCI","JPM","JNPR","K","KEY","KMB","KIM","KMI","KLAC","KSS","KR","LLL","LH","LRCX","LEG","LEN","LIFE","LLY","LNC","LMT","L","LOW","LSI","MTB","M","MRO","MPC","MAR","MMC","MAS","MA","MAT","MKC","MCD","MCK","MDT","MRK","MET","MCHP","MU","MSFT","TAP","MON","MNST","MCO","MS","MOS","MSI","MUR","NBR","NDAQ","NOV","NTAP","NFLX","NWL","NEM","NWSA","NEE","NKE","NI","NE","JWN","NSC","NTRS","NOC","NRG","NUE","NVDA","ORLY","OXY","OMC","OKE","ORCL","OI","PCAR","PLL","PH","PDCO","PAYX","BTU","POM","PEP","PKI","PRGO","PFE","PCG","PM","PSX","PNW","PXD","PBI","PNC","RL","PPG","PPL","PFG","PG","PGR","PLD","PRU","PEG","PSA","PHM","PWR","QCOM","DGX","RRC","RF","RSG","RHI","ROK","COL","ROP","ROST","R","SAI","CRM","SLB","STX","SEE","SHLD","SRE","SHW","SPG","SLM","SJM","SNA","SO","LUV","SWN","SE","S","SWK","SBUX","STT","SRCL","SYK","SUN","STI","SYY","TROW","TGT","TEL","THC","TDC","TER","TXN","TXT","HSY","TRV","TMO","TJX","TRIP","TSN","USB","UNP","UNH","UPS","X","UNM","URBN","VFC","VLO","VTR","VRSN","VZ","V","VNO","VMC","WMT","DIS","WM","WAT","WFC","WDC","WU","WY","WHR","WMB","WEC","WYNN","XEL","XRX","XL","XYL","YUM","ZION"]
overall =  [None] * len(fivehuna)       #Overall comparision
predicted = [None] * len(fivehuna)      #Declaring necasarry arrays
current = [None] * len(fivehuna)
DiffTot = [None] * len(fivehuna)

count = len(fivehuna)

start_date = date(2021, 3, 1)                               #defining the date range start and stop dates
end_date = date(2021, 4, 1)
speed = 1
global purse 
global countBought
purse = 116654.69334719334
countBought = 0

global masterFrame
masterFrame = pd.DataFrame(columns=['Symbol', 'Predicted Return', 'Buy Price', 'Predicted Sell Price', 'Error', 'Date', 'Sell Price', 'Actual Return', 'Running Total', 'Column11'])


def get_ratings(symbols, sdate):
    comb = pd.DataFrame(columns=['Symbol', 'Predicted Return', 'Buy Price', 'Predicted Sell Price', 'Error', 'Date', 'Sell Price', 'Actual Return'])
    dow = 0
    while dow < count:
        try:            
            predicted[dow] = stockerback.predict.tomorrow(symbols[dow], sdate)  #ccomes up with the predicted price
        except KeyError:
            pass
        except ConnectionError as e:
            pass
        except TimeoutError:
            pass
        except IndexError:
            pass
        except ValueError:
            pass
        except AttributeError:
            pass
        except KeyError: 'HistoricalPriceStore'
        #if(dow % 20 == 0):
        print(dow)
        dow = dow + speed
    dow = 0
    while dow < count:
        try:
            ticker = yf.Ticker(symbols[dow])
            todays_data = ticker.history("1d","1d",sdate.strftime('%Y-%m-%d'))
            #real = stocker.get_data.data.get_last_iex(symbols[dow])   #Extracts the current price 
            current[dow] = todays_data['Close'][0]
        except KeyError:
            pass
        except IndexError:
            pass

        if(dow % 20 == 0):
            print(dow)
        dow = dow + speed
    dow = 0
    while dow < count:  #Percent differance
        predictedPrice = 0
        error = 0
        try:
            servant = predicted[dow]
            servant = str(servant)
            intern = servant.split(", ")
            intern.remove(intern[2])
            intern.remove(intern[0])
            error = (intern.pop(0))
            error = float(error)
        except IndexError:
            pass
        try:
            predicted[dow] = str(predicted[dow])
            intern = predicted[dow].split(", ")
            intern.remove(intern[2])
            predictedPrice = (intern.pop(0))
            predictedPrice = predictedPrice[1:]
            predictedPrice = float(predictedPrice)
        except IndexError:
            pass
        if predictedPrice != 0:
            try:
                PercDif = ((predictedPrice - current[dow]) / current[dow] * 100)
                PercDif = round(PercDif, 3)
                DiffTot[dow] = PercDif
            except TypeError:
                pass
        else:
            DiffTot[dow] = 0
        #comb = pd.concat([comb, pd.DataFrame.from_records([{ 
        #                'symbol': symbols[dow],
         #               'percDiff': DiffTot[dow],
          #              'price': current[dow],
           #             'predictedPrice': predictedPrice,
            #            'error': error
             #           }])])
        comb = comb.append({
            'Symbol': symbols[dow],
            'Predicted Return': DiffTot[dow],
            'Buy Price': current[dow],
            'Predicted Sell Price': predictedPrice,
            'Error': error,
            'Date': sdate
        }, ignore_index=True)
        predictedPrice = 0
        #comb['symbol'] = comb['symbol'].astype('|S8')
        dow = dow + 1
    comb = comb.sort_values(by=['Predicted Return'], ascending=False)
    comb = comb.reset_index(drop=True)
    
    buy(comb, sdate)
    


def buy(comb, single_date):                                                      #defining the buy function which splits the current portfolio ten ways and buys and calculates the gain/loss and adds it back together
    global purse
    global masterFrame 
    global countBought

    print("Start of Day", single_date, purse)
    split = purse/20
    tomorrow = single_date + dt.timedelta(days=1)
    temppurse = 0
    
    i=0
    j=20
    running = purse
    while i < 20:
        try:
            error = comb.at[i,'Error']
            predicted_return = comb.at[i, 'Predicted Return']
            if error > predicted_return:
                comb = comb.drop([i])

                temppurse = split + temppurse 
                j = j - 1
                i = i + 1
                continue
        except KeyError:
            continue
       
        

        #print("buy ", comb.at[i,'symbol'], "at", comb.at[i, 'price'])
        try:
            
            ticker = yf.Ticker(comb.at[i,'Symbol'])
            tomorrows_data = ticker.history("1d","1d",tomorrow.strftime('%Y-%m-%d'))
            tomorrow_close = tomorrows_data['Close'][0]
            PercDif = (((tomorrow_close - comb.at[i,'Buy Price']) / comb.at[i,'Buy Price']))
        except IndexError:
            PercDif = 0
            continue
        except UnboundLocalError:
            continue
        except KeyError:
            continue
        #print(tomorrow_close)
        #print(PercDif)
        temppurse = (split * PercDif) + temppurse + split
        running = (split * PercDif) + running
        #print( temppurse)
        comb.at[i, 'Sell Price'] = tomorrow_close
        comb.at[i, 'Actual Return'] = PercDif
        comb.at[i, 'Running Total'] = running
        comb.at[i, 'Column11'] = countBought
        countBought = countBought + 1
        i = i + 1
        
    masterFrame = pd.concat([comb[:j], masterFrame])
    purse = temppurse
    print(masterFrame[:j])

    print("end of day", single_date, "account value:", purse)
    
    

    

def daterange(start_date, end_date):            
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)
        


for single_date in daterange(start_date, end_date):       #Base level loop, Starts the iteration through the days in the date range                                                             
    if single_date.weekday() == 5 or single_date.weekday() == 6:
        single_date = single_date + dt.timedelta(days=1)
    else:
        get_ratings(fivehuna, single_date)


print("end of period account value:", purse)

writer = pd.ExcelWriter('march21.xlsx')
# write dataframe to excel
masterFrame.to_excel(writer)
# save the excel
writer.save()











