
# Acting as a quantitative analyst create a function to detect market regime changes of the S&P 500 in python. 
# Source: https://chat.openai.com/c/2b6c9646-be0c-49cf-a180-7f6de7ee062a

# As a quantitative analyst, to detect market regime changes in the S&P 500, 
# I would suggest using a Hidden Markov Model (HMM). HMM is a popular choice 
# for modeling time series data and detecting regime changes. 
# We'll use the hmmlearn library, so make sure to install it first:

!pip3 install hmmlearn

# Here's a function to detect market regime changes in the S&P 500 using the Hidden Markov Model:

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from hmmlearn import hmm
from pandas_datareader import data as pdr

def get_sp500_data(start_date, end_date):
    sp500 = pdr.get_data_yahoo('^GSPC', start=start_date, end=end_date)
    return sp500



def preprocess_data(df):
    df['log_return'] = np.log(df['Adj Close'] / df['Adj Close'].shift(1))
    df.dropna(inplace=True)
    return df

def fit_hmm_model(data, n_states, n_iter):
    model = hmm.GaussianHMM(n_components=n_states, covariance_type='diag', n_iter=n_iter)
    model.fit(data.reshape(-1, 1))
    return model

def detect_market_regime_changes(start_date, end_date, n_states=2, n_iter=100):
    sp500 = get_sp500_data(start_date, end_date)
    sp500_preprocessed = preprocess_data(sp500)
    log_returns = sp500_preprocessed['log_return'].values

    model = fit_hmm_model(log_returns, n_states, n_iter)
    hidden_states = model.predict(log_returns.reshape(-1, 1))

    fig, ax = plt.subplots(figsize=(15, 8))
    for i in range(n_states):
        idx = (hidden_states == i)
        ax.plot(sp500_preprocessed.index[idx], sp500['Adj Close'][idx], 'o', label=f'Regime {i}', markersize=2)

    ax.set_xlabel('Date')
    ax.set_ylabel('S&P 500 Adjusted Close')
    ax.set_title('S&P 500 Market Regime Changes')
    ax.legend()
    plt.show()

# Example usage:
start_date = '2010-01-01'
end_date = '2021-09-30'

detect_market_regime_changes(start_date, end_date)


# This function performs the following steps:
# Fetches the S&P 500 historical data from Yahoo Finance using pandas_datareader.
# Preprocesses the data by calculating the log returns and removing missing values.
# Fits an HMM model to the log returns with a specified number of hidden states (default 2) and iterations (default 100).
# Predicts the hidden states (market regimes) using the fitted HMM model.
# Plots the S&P 500 adjusted close prices with the detected market regimes.
# Please note that this is a simple example, and the model can be improved by using more features, 
# tuning hyperparameters, or implementing additional preprocessing steps.
