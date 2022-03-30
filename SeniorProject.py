import stocker

import tensorflow as tf
import pandas as pd
import statistics
import sys
import time
import os                                               #Importing all the librarys and such I think I may need.
import yfinance as yf
import smtplib

import concurrent.futures


from collections import OrderedDict

from datetime import datetime, timedelta
from pytz import timezone


from requests.exceptions import ConnectionError
import logging
tf.get_logger().setLevel(logging.ERROR)

fivehuna = ['AAPL', 'TSLA', 'ABT', 'ABBV', 'ACN', 'ADBE', 'ADT', 'AAP', 'AES', 'AFL', 'AMG', 'A', 'GAS', 'APD', 'AKAM', 'AA', 'ALXN', 'ALLE', 'ADS', 'ALL', 'ALTR', 'MO', 'AMZN', 'AEE', 'AAL', 'AEP', 'AXP', 'AIG', 'AMT', 'AMP', 'ABC', 'AME', 'AMGN', 'APH', 'ADI', 'AON', 'APA', 'AIV', 'AMAT', 'ADM', 'AIZ', 'T', 'ADSK', 'ADP', 'AN', 'AZO', 'AVGO', 'AVB', 'AVY', 'BLL', 'BAC', 'BK', 'BAX', 'BDX', 'BBBY', 'BRK-B', 'BBY', 'BLX', 'HRB', 'BA', 'BWA', 'BXP', 'BMY', 'BF-B', 'CHRW', 'COG', 'CPB', 'COF', 'CAH', 'HSIC', 'KMX', 'CCL', 'CAT', 'CNP', 'CERN', 'CF', 'SCHW', 'CVX', 'CMG', 'CB', 'CI', 'XEC', 'CINF', 'CTAS', 'CSCO', 'C', 'CTXS', 'CLX', 'CME', 'CMS', 'KO', 'CTSH', 'CL', 'CMCSA', 'CMA', 'CSC', 'CAG', 'COP', 'CNX', 'ED', 'STZ', 'GLW', 'COST', 'CCI', 'CSX', 'CMI', 'CVS', 'DHI', 'DHR', 'DRI', 'DVA', 'DE', 'DAL', 'XRAY', 'DVN',  'DFS', 'DISCA', 'DISCK', 'DG', 'DLTR', 'D', 'DOV', 'DOW', 'DTE', 'DD', 'DUK', 'DNB', 'EMN', 'ETN', 'EBAY', 'ECL', 'EIX', 'EW', 'EA', 'EMC', 'EMR', 'ENDP', 'ETR', 'EOG', 'EQT', 'EFX', 'EQIX', 'EQR', 'ESS', 'EL', 'ES', 'EXC', 'EXPE', 'EXPD', 'XOM', 'FFIV', 'FB', 'FAST', 'FDX', 'FIS', 'FITB', 'FSLR', 'FE', 'FLIR', 'FLS', 'FLR', 'FMC', 'FTI', 'F', 'FOSL', 'BEN', 'FCX', 'GME', 'GPS', 'GRMN', 'GD', 'GE', 'GIS', 'GM', 'GPC', 'GNW', 'GILD', 'GS', 'GT', 'GOOGL', 'GOOG', 'GWW', 'HAL', 'HBI', 'HOG', 'HAR', 'HIG', 'HAS', 'HCA', 'HP', 'HES', 'HPQ', 'HD', 'HON', 'HRL', 'HST', 'HUM', 'HBAN', 'ITW', 'IR', 'INTC', 'ICE', 'IBM', 'IP', 'IPG', 'IFF', 'INTU', 'ISRG', 'IVZ', 'IRM', 'JBHT', 'JNJ', 'JCI', 'JPM', 'JNPR', 'KSU', 'K', 'KEY', 'KMB', 'KIM', 'KMI', 'KLAC', 'KSS',  'KR', 'LB', 'LH', 'LRCX', 'LEG', 'LEN', 'LLY', 'LNC', 'LMT', 'L', 'LOW', 'LYB', 'MTB', 'MAC', 'M', 'MRO', 'MPC', 'MAR', 'MMC', 'MLM', 'MAS', 'MA', 'MAT', 'MKC', 'MCD', 'MCK', 'MDT', 'MRK', 'MET', 'MCHP', 'MU', 'MSFT', 'MHK', 'TAP', 'MDLZ', 'MNST', 'MCO', 'MS', 'MOS', 'MSI', 'MUR', 'NDAQ', 'NOV', 'NAVI', 'NTAP', 'NFLX', 'NWL', 'NEM', 'NWSA', 'NEE', 'NLSN', 'NKE', 'NI', 'JWN', 'NSC', 'NTRS', 'NOC', 'NRG', 'NUE', 'NVDA', 'ORLY', 'OXY', 'OMC', 'OKE', 'ORCL', 'OI', 'PCAR', 'PLL', 'PH', 'PDCO', 'PAYX', 'PNR', 'PBCT', 'POM', 'PEP', 'PKI', 'PRGO', 'PFE', 'PCG', 'PM', 'PSX', 'PNW', 'PXD', 'PBI', 'PCL', 'PNC', 'RL', 'PPG', 'PPL', 'PFG', 'PG', 'PGR', 'PLD', 'PRU', 'PEG', 'PSA', 'PHM', 'PVH', 'QRVO', 'PWR', 'QCOM', 'DGX', 'RRC', 'O', 'REGN', 'RF', 'RSG', 'RHI', 'ROK', 'COL', 'ROP', 'ROST', 'R', 'CRM', 'SCG', 'SLB', 'STX', 'SEE', 'SRE', 'SHW', 'SPG', 'SWKS', 'SLG', 'SJM', 'SNA', 'SO', 'LUV', 'SWN', 'SE', 'SWK', 'SBUX', 'HOT', 'STT', 'SRCL', 'SYK', 'SYY', 'TROW', 'TGT', 'TEL', 'TGNA', 'THC', 'TDC', 'TXN', 'TXT', 'HSY', 'TRV', 'TMO', 'TSCO', 'RIG', 'TRIP', 'FOXA', 'TSN', 'UA', 'UNP', 'UNH', 'UPS', 'URI', 'UHS', 'UNM', 'URBN', 'VFC', 'VLO', 'VAR', 'VTR', 'VRSN', 'VZ', 'VRTX', 'V', 'VNO', 'VMC', 'WMT', 'WBA', 'DIS', 'WM', 'WAT', 'ANTM', 'WFC', 'WDC', 'WU', 'WY', 'WHR', 'WMB', 'WEC', 'WYNN', 'XEL', 'XRX', 'XLNX', 'XL', 'XYL', 'YUM', 'ZBH', 'ZION', 'ZTS']
pe = [None] * len(fivehuna)             #profit equity
beta = [None] * len(fivehuna)           #beta
peg =  [None] * len(fivehuna)       #payout ratio
pTs =  [None] * len(fivehuna)           #PtS trailing 12 months
eps =  [None] * len(fivehuna)           #EPS
overall =  [None] * len(fivehuna)       #Overall comparision
predicted = [None] * len(fivehuna)      #Declaring necasarry arrays
current = [None] * len(fivehuna)
DiffTot = [None] * len(fivehuna)


count = len(fivehuna)

speed = 20


def ratios(symbols):
    iter = 0  
                                                                                                                      #Defining a function that will obtain the financial ratios about the specified stocks (symbols)
    ratio_data = pd.DataFrame(columns=['Symbol','PE', 'beta', 'PEG', 'EPS', 'PTS', 'Overall'])                         #Establishing a dataframe for storing ration data about the stocks

    peComp = 0 
    pegComp = 0
    betaComp = 0 
    ptsComp = 0
    epsComp = 0

    total = count/speed

    while iter < count:                                                                                         #while loop to get the PE for eachof the stocks
        GetInformation = yf.Ticker(symbols[iter])
        try:
            pe[iter] = GetInformation.info['trailingPE']
            peg[iter] = GetInformation.info['pegRatio']
            beta[iter] = GetInformation.info['beta']
            pTs[iter] = GetInformation.info['priceToSalesTrailing12Months']
            eps[iter] = GetInformation.info['trailingEps']
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
        
        try:
            peComp = peComp + int(pe[iter]) 
            pegComp = pegComp + int(peg[iter])
            betaComp = betaComp + int(beta[iter]) 
            ptsComp = ptsComp + int(pTs[iter]) 
            epsComp = epsComp + int(eps[iter]) 
        except TypeError:
            total = total - 1
            pass

        

        iter = iter + speed
    
    

    iter = 0

    peComp = peComp/total
    pegComp = pegComp/total
    betaComp = betaComp/total
    ptsComp = ptsComp/total
    epsComp = epsComp/total

    
    while iter < count:
        try:
            peAve = peComp/pe[iter]
            pegAve = pegComp/peg[iter]
            betaAve = beta[iter]/betaComp
            ptsAve = ptsComp/pTs[iter]
            epsAve = epsComp/eps[iter]
        except TypeError:
            pass
        except ZeroDivisionError:
            pass
        
        overall[iter] = peAve+pegAve+betaAve+ptsAve+epsAve

        ratio_data = ratio_data.append({
            'Symbol': fivehuna[iter],
            'PE': pe[iter],
            'beta': beta[iter],
            'PEG': peg[iter],
            'PTS': pTs[iter],
            'EPS': eps[iter],
            'Overall': overall[iter],
        }, ignore_index=True)

        iter = iter + speed

    ratio_data = ratio_data.sort_values(by=['Overall'], ascending=True)
    ratio_data = ratio_data.reset_index(drop=True)
        
    
    print(ratio_data[:10])
    return ratio_data[:10]



def get_ratings(symbols):

    comb = pd.DataFrame(columns=['symbol', 'percDiff', 'price', 'predictedPrice', 'error'])

    dow = 0
    
    while dow < count:
        try:
            predicted[dow] = stocker.predict.tomorrow(symbols[dow])  #ccomes up with the predicted price
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
            todays_data = ticker.history(period='1d')
            
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


        comb = comb.append({
            'symbol': symbols[dow],
            'percDiff': DiffTot[dow],
            'price': current[dow],
            'predictedPrice': predictedPrice,
            'error': error
        }, ignore_index=True)

        predictedPrice = 0
        

        dow = dow + 1

    
         
    comb = comb.sort_values(by=['percDiff'], ascending=False)
    comb = comb.reset_index(drop=True)
        
    
    print(comb[:10])
    return comb[:10]

        
get_ratings(fivehuna)
ratios(fivehuna)