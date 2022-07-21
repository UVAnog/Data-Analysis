##
## File: assignment11.py (STAT 3250)
## Topic: Assignment 11
##

##  The file Stocks.zip is a zip file containing nearly 100 sets of price
##  records for various stocks.  A sample of the type of files contained
##  in Stocks.zip is ABT.csv, which we have seen previously and is posted
##  in recent course materials. Each file includes daily data for a specific
##  stock, with stock ticker symbol given in the file name. Each line of
##  a file includes the following:
##
##   Date = date for recorded information
##   Open = opening stock price
##   High = high stock price
##   Low = low stock price
##   Close = closing stock price
##   Volume = number of shares traded
##   Adj Close = closing price adjusted for stock splits (ignored for this assignment)

##   The time interval covered varies from stock to stock. For many files
##   there are dates when the market was open but the data is not provided, so
##   those records are missing. Note that some dates are not present because the
##   market is closed on weekends and holidays.  Those are not missing records.

##  The Gradescope autograder will be evaluating your code on a subset
##  of the set of files in the folder Stocks.  Your code needs to automatically
##  handle all assignments to the variables q1, q2, ... to accommodate the
##  reduced set, so do not copy/paste things from the console window, and
##  take care with hard-coding values.

##  The autograder will contain a folder Stocks containing the stock data sets.
##  This folder will be in the working directory so your code should be written
##  assuming that is the case.


import pandas as pd  # load pandas
import numpy as np  # load numpy
import zipfile
import glob
pd.set_option('display.max_columns', 10)  # Display 10 columns in console

filelist = glob.glob('Stocks/*.csv') # 'glob.glob' is the directory search
stocks = pd.DataFrame()  # empty dataframe
for file in filelist:
    newdf = pd.read_csv(file)  # read in the file
    newdf['File Name'] = file
    stocks = pd.concat([stocks, newdf])


stocks['Stock Name'] = stocks['File Name'].str.split('/').str[1].str.split('.').str[0]

## 1.  Find the mean for the Open, High, Low, and Close entries for all
##     records for all stocks.  Give your results as a Series with index
##     Open, High, Low, Close (in that order) and the corresponding means
##     as values.
# get the mean for entries
stock_means = stocks[['Open', 'High', 'Low', 'Close']].mean()
q1 = pd.Series(stock_means)  # Series of means of Open, High, Low, and Close
print(q1)

## 2.  Find all stocks with an average Close price less than 30.  Give your
##     results as a Series with ticker symbol as index and average Close price.
##     price as value.  Sort the Series from lowest to highest average Close
##     price.  (Note: 'MSFT' is the ticker symbol for Microsoft.  'MSFT.csv',
##     'Stocks/MSFT.csv' and 'MSFT ' are not ticker symbols.)

# get the average close price for each unique stock
mean_close_prices = stocks['Close'].groupby(stocks['Stock Name']).mean()
# get averages under thirty
mean_close_prices_under_thirty = mean_close_prices[mean_close_prices < 30]
q2 = mean_close_prices_under_thirty.sort_values()  # Series of stocks with average close less than 30
print(q2)

## 3.  Find the top-10 stocks in terms of the day-to-day volatility of the
##     price, which we define to be the mean of the daily differences
##     High - Low for each stock. Give your results as a Series with the
##     ticker symbol as index and average day-to-day volatility as value.
##     Sort the Series from highest to lowest average volatility.

# make new column for volatility
stocks['Volatility'] = stocks['High'] - stocks['Low']

# group the volatility by each stock
stock_volatility = stocks['Volatility'].groupby([stocks['Stock Name']])

# sort the stocks high to low
mean_volatility = stock_volatility.mean().sort_values(ascending=False)

# get top 10 + ties
q3 = mean_volatility.loc[mean_volatility >= mean_volatility.iloc[9]]  # Series of top-10 mean volatility
print(q3)

## 4.  Repeat the previous problem, this time using the relative volatility,
##     which we define to be the mean of
##
##                       (High âˆ’ Low)/(0.5(Open + Close))
##
##     for each day. Provide your results as a Series with the same specifications
##     as in the previous problem.

# create new column of Relative Volatility with given equation
stocks['Relative Volatility'] = (stocks['High'] - stocks['Low']) / (0.5 * (stocks['Open'] + stocks['Close']))

# group the relative volatility of each stock
stock_relative_volatility = stocks['Relative Volatility'].groupby([stocks['Stock Name']])

# sort the stocks high to low
mean_relative_volatility = stock_relative_volatility.mean().sort_values(ascending=False)

# get top 10 + ties
q4 = mean_relative_volatility.loc[
    mean_relative_volatility >= mean_relative_volatility[9]]  # Series of top-10 mean relative volatility
print(q4)

## 5.  For each day the market was open in October 2008, find the average
##     daily Open, High, Low, Close, and Volume for all stocks that have
##     records for October 2008.  (Note: The market is open on a given
##     date if there is a record for that date in any of the files.)
##     Give your results as a DataFrame with dates as index and columns of
##     means Open, High, Low, Close, Volume (in that order).  The dates should
##     be sorted from oldest to most recent, with dates formatted (for example)
##     2008-10-01, the same form as in the files.

# get data from the set that lies between the dates, and then get columns from date to volume
October_Market_2008 = stocks[(stocks['Date'] <= '2008-10-31') & (stocks['Date'] >= '2008-10-01')].loc[:,
                      'Date':'Volume']

# group by each day, and find the average open, high, low, close, and volume for that day
October_Market_2008_Averages = October_Market_2008.loc[:, 'Open':'Volume'].groupby(October_Market_2008['Date']).mean()

q5 = October_Market_2008_Averages  # DataFrame of means for each open day of Oct '08.
print(q5)

## 6. For 2011, find the date with the maximum average relative volatility
##    for all stocks and the date with the minimum average relative
##    volatility for all stocks. Give your results as a Series with
##    the dates as index and corresponding average relative volatility
##    as values, with the maximum first and the minimum second.

# add new column of date to datetime
stocks['Datetime'] = pd.to_datetime(stocks['Date'])

# subset to get stocks from 2011
Market_2011 = stocks[stocks['Datetime'].dt.year == 2011]

# get the relative volatility of each day
Market_2011_Relative_Volatility = Market_2011['Relative Volatility'].groupby(Market_2011['Date'])

# get the mean and sort
Market_2011_Mean_Relative_Volatility = Market_2011_Relative_Volatility.mean().sort_values(ascending=False)

# get first (max) and last (min) values
max_relative = Market_2011_Mean_Relative_Volatility.head(1)
min_relative = Market_2011_Mean_Relative_Volatility.tail(1)

new_frame = pd.concat([max_relative, min_relative], axis=0)
# merge max and min to series
q6 = pd.Series(new_frame)  # Series of average relative volatilities
print(q6)

## 7. For 2010-2012, find the average relative volatility for all stocks on
##    Monday, Tuesday, ..., Friday.  Give your results as a Series with index
##    'Mon','Tue','Wed','Thu','Fri' (in that order) and corresponding
##    average relative volatility as values.

# get market data from 2010 to 2012
Market_2010_2012 = stocks[(stocks['Datetime'].dt.year >= 2010) & (stocks['Datetime'].dt.year <= 2012)]

# group my day of the week, get relative volatility, take average
Daily_RV = Market_2010_2012.groupby(Market_2010_2012['Datetime'].dt.strftime('%A'))[['Relative Volatility']].mean()

# return series with appropriate indexing
# https://stackoverflow.com/questions/47741400/pandas-dataframe-group-and-sort-by-weekday
# days of the week to ensure correct order of series
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
ordered_days = Daily_RV.reindex(days)
q7 = ordered_days.squeeze()  # Series of average relative volatility by day of week
print(q7)

## 8.  For each month of 2009, determine which stock had the maximum average
##     relative volatility. Give your results as a Series with MultiIndex
##     that includes the month (month number is fine) and corresponding stock
##     ticker symbol (in that order), and the average relative volatility
##     as values.  Sort the Series by month number 1, 2, ..., 12.

# get market data for 2009
Market_2009 = stocks[(stocks['Datetime'].dt.year == 2009)]

# group by month and get relative volatility
Market_2009_Monthly = Market_2009['Relative Volatility'].groupby([Market_2009['Datetime'].dt.month,
                                                                  Market_2009['Stock Name']])

# get the largest average value for each group (month)
Market_2009_Monthly_Average = Market_2009_Monthly.mean().groupby(level=0, group_keys=False).nlargest(1)

q8 = Market_2009_Monthly_Average  # Series of maximum relative volatilities by month
print(q8)

## 9.  The â€œPython Indexâ€ is designed to capture the collective movement of
##     all of our stocks. For each date, this is defined as the average price
##     for all stocks for which we have data on that day, weighted by the
##     volume of shares traded for each stock.  That is, for stock values
##     S_1, S_2, ... with corresponding volumes V_1, V_2, ..., the average
##     weighted volume is
##
##           (S_1*V_1 + S_2*V_2 + ...)/(V_1 + V_2 + ...)
##
##     Find the Open, High, Low, and Close for the Python Index for each date
##     the market was open in January 2013.
##     Give your results as a DataFrame with dates as index and columns of
##     means Open, High, Low, Close (in that order).  The dates should
##     be sorted from oldest to most recent, with dates formatted (for example)
##     2013-01-31, the same form as in the files.

# subset data to january of 2013
Market_January_2013 = stocks[(stocks['Datetime'] >= '2013-01-01') &
                             (stocks['Datetime'] <= '2013-01-31')].loc[:, 'Date':'Volume']

# loop through each day and get open, high, low, close multiplied by volume
for i in Market_January_2013.columns[1:5]:
    Market_January_2013[i] = Market_January_2013[i] * Market_January_2013['Volume']

# group by date and get corresponding open, high, low, close
Market_January_2013_Values = Market_January_2013.loc[:, 'Open':'Volume'].groupby(Market_January_2013['Date']).sum()

# get one date per row, and divide open, high, low, close by volume
January_Values = Market_January_2013_Values[['Open', 'High', 'Low', 'Close']].div(
    Market_January_2013_Values['Volume'].values, axis=0)

q9 = January_Values  # DataFrame of Python Index values for each open day of Jan 2013.
print(q9)

## 10. For the years 2007-2012 determine the top-8 month-year pairs in terms
##     of average relative volatility of the Python Index. Give your results
##     as a Series with MultiIndex that includes the month (month number is
##     fine) and year (in that order), and the average relative volatility
##     as values.  Sort the Series by average relative volatility from
##     largest to smallest.

# subset data to get info from 2007 - 2012
Market_2007_2012 = stocks[(stocks['Datetime'].dt.year >= 2007) &
                          (stocks['Datetime'].dt.year <= 2012)].loc[:, 'Date':'Relative Volatility']

# extract these columns
Market_2007_2012_Subset = Market_2007_2012[['Date', 'Relative Volatility', 'Volume']]

# change to datetime
Market_2007_2012_Subset['Date'] = pd.to_datetime(Market_2007_2012_Subset['Date'])

# add new column of just the month
Market_2007_2012_Subset['Month'] = Market_2007_2012_Subset['Date'].dt.month

# add new column of just the year
Market_2007_2012_Subset['Year'] = Market_2007_2012_Subset['Date'].dt.year

Market_2007_2012_Data = Market_2007_2012_Subset[['Month', 'Year', 'Relative Volatility', 'Volume']]

# loop through relative volatility and volume
for i in Market_2007_2012_Data.columns[2:3]:
    # for each index of relative volatility multiply by the volume
    Market_2007_2012_Data[i] = Market_2007_2012_Data[i] * Market_2007_2012_Data['Volume']

# group relative volatility and volume by the year and month and then sum
Market_2007_2012_Values = Market_2007_2012_Data[['Relative Volatility', 'Volume']].groupby(
    [Market_2007_2012_Data['Year'], Market_2007_2012_Data['Month']]).sum()

# for each group divide relative volatility by the volume
Market_2007_2012_Pairs = Market_2007_2012_Values['Relative Volatility'].div(
    Market_2007_2012_Values['Volume'].values, axis=0)

# sort the values
Market_2007_2012_Sorted = Market_2007_2012_Pairs.sort_values(ascending=False)

# get the top 8
q10 = Market_2007_2012_Sorted.loc[Market_2007_2012_Sorted >= Market_2007_2012_Sorted.iloc[7]]  # Series of month-year pairs and average rel. volatilities
print(q10)

## 11. Each stock in the data set contains records starting at some date and
##     ending at another date.  In between the start and end dates there may be
##     dates when the market was open but there is no record -- these are the
##     missing records for the stock.  For each stock, determine the percentage
##     of records that are missing out of the total records that would be
##     present if no records were missing. Give a Series of those stocks
##     with less than 1.3% of records missing, with the stock ticker as index
##     and the corresponding percentage as values, sorted from lowest to
##     highest percentage.

q11 = None  # Series of stocks and percent missing
print(q11)