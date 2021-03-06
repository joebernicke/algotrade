# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 14:38:43 2020

@author: joebe
"""
import pandas as pd 
import matplotlib.pyplot as plt 
from pandas_datareader import data
start_date = '2001-01-01' 
end_date = '2018-01-01' 
SRC_DATA_FILENAME='goog_data_large.pkl'
try:  
    goog_data = pd.read_pickle(SRC_DATA_FILENAME)  
    print('File data found...reading GOOG data') 
except FileNotFoundError:  
    print('File not found...downloading the GOOG data')  
    goog_data = data.DataReader('GOOG', 'yahoo', start_date, end_date)  
goog_data.to_pickle(SRC_DATA_FILENAME)
goog_monthly_return = goog_data['Adj Close'].pct_change().groupby([goog_data['Adj Close'].index.year,goog_data['Adj Close'].index.month]).mean() 
goog_montly_return_list=[]
for i in range(len(goog_monthly_return)): 
    goog_montly_return_list.append({'month':goog_monthly_return.index[i][1],'monthly_return': goog_monthly_return[i]})
goog_montly_return_list=pd.DataFrame(goog_montly_return_list, columns=('month','monthly_return'))
goog_montly_return_list.boxplot(column='monthly_return', by='month')

ax = plt.gca() 
labels = [item.get_text() 
for item in ax.get_xticklabels()] 
labels=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
ax.set_xticklabels(labels) 
ax.set_ylabel('GOOG return') 
plt.tick_params(axis='both', which='major', labelsize=7) 
plt.title("GOOG Monthly return 2001-2018") 
plt.suptitle("") 
plt.show()

# Displaying rolling statistics 
#ts=goog_monthly_return
def plot_rolling_statistics_ts(ts, titletext,ytext, window_size=12):  
    ts.plot(color='red', label='Original', lw=0.5)  
    ts.rolling(window_size).mean().plot(color='blue',label='Rolling Mean')  
    ts.rolling(window_size).std().plot(color='black', label='Rolling Std')
    plt.legend(loc='best')  
#plt.ylabel(ytext)  
#plt.title(titletext)  
    plt.show(block=False)
plot_rolling_statistics_ts(goog_monthly_return[1:],'GOOG prices rolling mean and standard deviation','Monthly return')
plot_rolling_statistics_ts(goog_data['Adj Close'],'GOOG prices rolling mean and standard deviation','Daily prices',365)
plt.show()