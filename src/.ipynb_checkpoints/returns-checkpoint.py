#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 14:45:05 2022

@author: potruso
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt


ticker = ['BTC-USD']
data = yf.download(ticker, start = '2017-01-01', end = '2019-01-01', period = 'max').reset_index(drop=True)

data = data['Close'].drop(columns = ['Date'], axis = 1)


returns = np.log(data/data.shift(1)).dropna()
plt.plot(returns)

cumret = returns.cumsum()
plt.plot(cumret)
plt.show()

print(len(data))

m_data = pd.read_csv('model_vars.csv').drop(columns = ['Unnamed: 0'], axis = 1)

m_returns = np.log(m_data/m_data.shift(1)).dropna()
plt.plot(m_returns)

m_cumret = m_returns.cumsum()
plt.plot(m_cumret)
plt.show()

plt.plot(returns)
plt.plot(m_returns)
plt.show()

#------------------------------------------------------------------------------

from sklearn.metrics import mean_absolute_error, r2_score

fig,ax = plt.subplots(figsize=(8,8))
ax.set_title('Returns Prediction',fontsize=16)
ax.set_ylabel('Model Returns',fontsize=12)
ax.set_xlabel('Actual Returns',fontsize=12)
ax.scatter(returns,m_returns)

score_r2 = r2_score(returns, m_returns)
score_mae = mean_absolute_error(returns, m_returns)
plt.text(0.15, 0.11, '$ R^{2} $=' + str(round(score_r2, 2)), fontsize=16)
plt.text(0.15, 0.10, 'MAE =' + str(round(score_mae)), fontsize=16)
plt.show()