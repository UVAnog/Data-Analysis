##
## File: assignment09.py (STAT 3250)
## Topic: Assignment 9
##

##  This assignment requires the data file 'airline-stats.txt'.  This file
##  contains thousands of records of aggregated flight information, organized
##  by airline, airport, and month.  The first record is shown below.
##
##  The file is quite large (1.8M lines, 31MB) so may be difficult to open in
##  Spyder.  An abbreviated version 'airline-stats-brief.txt' is also
##  provided that has the same structure as the original data set but is
##  easier to open in Spyder.

##  Note: Some or all of the questions on this assignment can be done without the
##  use of loops, either explicitly or implicitly (apply). As usual, scoring
##  will take this into account.

##  The Gradescope autograder will be evaluating your code on a reduced
##  version of the airline-stats.txt data that includes only a fraction of the
##  records.  Your code needs to automatically handle all assignments
##  to the variables q1, q2, ... to accommodate the reduced data set,
##  so do not copy/paste things from the console window, and take care
##  with hard-coding values.

# =============================================================================
# airport
#     code: ATL
#     name: Atlanta GA: Hartsfield-Jackson Atlanta International
# flights
#     cancelled: 5
#     on time: 561
#     total: 752
#     delayed: 186
#     diverted: 0
# number of delays
#     late aircraft: 18
#     weather: 28
#     security: 2
#     national aviation system: 105
#     carrier: 34
# minutes delayed
#     late aircraft: 1269
#     weather: 1722
#     carrier: 1367
#     security: 139
#     total: 8314
#     national aviation system: 3817
# dates
#     label: 2003/6
#     year: 2003
#     month: 6
# carrier
#     code: AA
#     name: American Airlines Inc.
# =============================================================================

import numpy as np  # load numpy as np
import pandas as pd  # load pandas as pd

# Read in the test data as text one line at a time
airlines = open('airline-stats.txt').read().splitlines()
#airlines = open('/Users/nolan/Desktop/classes/stat3250/data/airline-stats.txt').read().splitlines()

# create a series of the data
airline_series = pd.Series(airlines)
# subset for totals
airline_totals = airline_series[airline_series.str.contains('total')]

## 1.  Give the total number of hours delayed for all flights in all records,
##     based on the entries in (minutes delayed)/total

# get total minutes
total_minutes = airline_totals[1::2].str.split().str[1].reset_index(drop=True).astype(float)

q1 = np.sum(total_minutes)/60  # total number of hours delayed for all flights in all records
print(q1)

## 2.  Which airlines appear in at least 500 records?  Give a Series with airline
##     names as index and record counts for values, in order of record count
##     from largest to smallest.

# subset data to get lines that contain 'name'
names = airline_series[airline_series.str.contains('name')]
# get the airline names
airline_names = names[1::2].str.split(':').str[-1].reset_index(drop=True)
# find the counts of how many each appears
airline_name_counts = airline_names.value_counts()
q2 = airline_name_counts[airline_name_counts > 500]  # Series of airline names and record counts
print(q2)

## 3.  The entry under 'flights/delayed' is not always the same as the total
##     of the entries under 'number of delays'.  (The reason for this is not
##     clear.)  Determine the percentage of records for which these two
##     values are different.

# LIST of reasons for delay
delay_list = ['delayed', 'late aircraft', 'weather', 'security', 'national aviation system', 'carrier:']

# create empty df, loop through airline file and add entries that include delays from the list
delayed_flights = pd.DataFrame()
for i in range(len(delay_list)):
    # subset to only entries that are delayed
    x = airline_series[airline_series.str.contains(delay_list[i])]
    # get the entry and number
    x = x[0::2].str.split(':').str[-1]
    # turn into a df and concat to add it as columns to the delayed flights df
    delay_flight = pd.DataFrame(x).reset_index(drop=True)
    delayed_flights = pd.concat([delayed_flights, delay_flight], axis=1)

# create column names that match the list in order they were added to df
delayed_flights.columns = ['delayed', 'late aircraft', 'weather', 'security', 'national aviation system', 'carrier']
# convert to floats
delayed_flights = delayed_flights.astype(float)
# sum the columns
delayed_flights['delay total'] = (delayed_flights['late aircraft'] + delayed_flights['weather'] +
                                  delayed_flights['security'] + delayed_flights['national aviation system'] +
                                  delayed_flights['carrier'])

# percentage of records with two values different
q3 = (sum(delayed_flights['delayed'] != delayed_flights['delay total'])/len(delayed_flights)) * 100
print(q3)

## 4.  Determine the percentage of records for which the number of delays due to
##     'late aircraft' exceeds the number of delays due to 'carrier'.

# subset the data to extract entries of late aircraft
late_aircraft = airline_series[airline_series.str.contains('late aircraft')]
# get the total number of late aircraft delays
late_aircraft_totals = late_aircraft[0::2].str.split(':').str[-1].astype(float).reset_index(drop=True)

# subset the data to extract entries of carrier
carrier = airline_series[airline_series.str.contains('carrier')]
# get the total number of delays due to carrier
carrier_totals = carrier[0::3].str.split(':').str[-1].astype(float).reset_index(drop=True)

q4 = (sum(late_aircraft_totals > carrier_totals) / len(delayed_flights)) * 100  # percentage of records as described above
print(q4)

## 5.  Find the top-8 airports in terms of the total number of minutes delayed.
##     Give a Series with the airport names (not codes) as index and the total
##     minutes delayed as values, sorted order from largest to smallest total.
##     (Include any ties for 8th position as usual)

# get all of the names of the airports
airport_names = names[0::2].str.split(':').str[-1].reset_index(drop=True)

# total the delays in minutes for each, group and get totals
airport_totals = pd.concat([airport_names, total_minutes], axis=1)
airport_totals = airport_totals[1].groupby(airport_totals[0])

# get the top 8 airports and remove heading of '0' from the series
top8 = pd.Series(airport_totals.sum().sort_values(ascending=False)).rename_axis(None, axis=0)

q5 = top8.loc[top8 >= top8.iloc[7]]  # Series of airport names and total minutes delayed
print(q5)

## 6.  Find the top-12 airports in terms of rates (as percentages) of on-time flights.
##     Give a Series of the airport names (not codes) as index and percentages
##     as values, sorted from largest to smallest percentage. (Include any
##     ties for 12th position as usual)

# get all of the ontime flights and totals
ontime_flights = airline_series[airline_series.str.contains('on time')]
ontime_flight_totals = ontime_flights.str.split(':').str[-1].astype(float).reset_index(drop=True)

# getting numerical totals
totals = airline_totals[0::2].str.split(':').str[-1].astype(float).reset_index(drop=True)

# making a df of ontime totals, total values and airport names
airport_df = pd.concat([names, ontime_flight_totals, totals], axis=1)

# group on time flights and flight totals by airport name and sum
ontime_group = airport_df[[1, 2]].groupby(airport_df[0]).sum()

# create new column to hold percentages
ontime_group['percentage'] = ontime_group[1] / ontime_group[2]

# sort the percentage totals from greatest to least, remove index title from df
ontime_rates = ontime_group.sort_values(by='percentage', ascending=False).rename_axis(None, axis=0) * 100

# transform to series
top_rates = pd.Series(ontime_rates['percentage'])

q6 = top_rates.loc[top_rates >= top_rates.iloc[11]]  # Series of airport names and percentages
print(q6)

## 7.  Find the top-10 airlines in terms of rates (as percentages) of on time flights.
##     Give a Series of the airline names (not codes) as index and percentages
##     as values, sorted from largest to smallest percentage. (Include any
##     ties for 10th position as usual)

# make new df of ontime flights, totals, and airline names
airline_df = pd.concat([ontime_flight_totals, totals, airline_names], axis=1)

# group ontime flights, totals by airline name and sum
airline_ontime_totals = (airline_df[[0, 1]].groupby(airline_df[2])).sum()

# create new column to hold percentages
airline_ontime_totals['percentage'] = airline_ontime_totals[0] / airline_ontime_totals[1] * 100

# sort the percentage totals from greatest to least, remove index title from df
airline_ontime_percentage = airline_ontime_totals.sort_values(by='percentage', ascending=False)

# transform to series
airline_ontime_percentage = pd.Series(airline_ontime_percentage['percentage'])

# Series of airport names and percentages
q7 = airline_ontime_percentage.loc[airline_ontime_percentage >= airline_ontime_percentage.iloc[11]]
print(q7)

## 8.  Determine the average length (in minutes) by airline of a delay due
##     to the national aviation system.  Give a Series of airline name (not
##     code) as index and average delay lengths as values, sorted from largest
##     to smallest average delay length.

# subset the data to extract entries of late aircraft
late_aircraft = airline_series[airline_series.str.contains('national aviation system')]
# get the total number of late aircraft delays
late_aircraft_totals = late_aircraft[0::2].str.split(':').str[-1].astype(float).reset_index(drop=True)

# create df to store totals and airline names
airline_nas = pd.concat([late_aircraft_totals, airline_names], axis=1)

# group by airline and get total delays average
airline_nas_totals = (airline_nas[0].groupby(airline_nas[1])).mean()

q8 = airline_nas_totals.sort_values(ascending=False)  # Series of airline names and average delay times
print(q8)
## 9.  For each month, determine the rates (as percentages) of flights delayed
##     by weather. Give a Series sorted by month (1, 2, ..., 12) with the
##     corresponding percentages as values.

# extract entries of the data that contain weather and get totals
weather = airline_series[airline_series.str.contains('weather')]
weather_totals = weather[0::2].str.split(':').str[-1].astype(float).reset_index(drop=True)

# extract entries of the data by month and get totals
month = airline_series[airline_series.str.contains('month')]
month_totals = month.str.split(':').str[-1].reset_index(drop=True).astype(int)

# make df of weather delays and totals
weather_delays = pd.concat([month_totals, ontime_flight_totals, weather_totals],axis=1)

# group the totals by the month and sum
weather_delays_by_month = weather_delays[[2,1]].groupby(weather_delays[0])
weather_delays_by_month = weather_delays_by_month.sum()

# create new column to hold percentages
weather_delays_by_month['percentage'] = weather_delays_by_month[2] / weather_delays_by_month[1] * 100
# transform to series
weather_delays_by_month = pd.Series(weather_delays_by_month['percentage'])

# Series of months and percentages
q9 = weather_delays_by_month.rename_axis(None, axis=0)
print(q9)

## 10. Find all airports where the average length (in minutes) of
##     security-related flight delays exceeds 35 minutes.  Give a Series with
##     airport names (not codes) as index and average delay times as values,
##     sorted from largest to smallest average delay.

# extract entries that contain security and get totals
security = airline_series[airline_series.str.contains('security')]
security_delays = security[1::2].str.split(':').str[-1].astype(float).reset_index(drop=True)
# get total delays related to security
security_totals = security[0::2].str.split(':').str[-1].astype(float).reset_index(drop=True)

# df containing delays
delayed_flights_security = pd.concat([airport_names, security_delays, security_totals], axis=1)

# group totals by airport
delayed_flights_security_groups = delayed_flights_security[[1, 2]].groupby(delayed_flights_security[0]).sum()

# get flight delay by airport
delay_by_airport = delayed_flights_security_groups[1] / delayed_flights_security_groups[2]

# Series or airport names and average delay times
q10 = delay_by_airport[delay_by_airport > 35].sort_values(ascending=False)
print(q10)

## 11. For each year, determine the airport that had the highest rate (as a
##     percentage) of delays.  Give a Series with the years (least recent at top)
##     and airport names (not code) as MultiIndex and the percentages as values.

# get total flights
flight_totals = airline_totals[0::2].str.split().str[1].reset_index(drop=True).astype(float)  

# extract the years and get totals for each year
year = airline_series[airline_series.str.contains('year')]
year_totals = year.str.split(':').str[-1].reset_index(drop=True).astype(int)

# extract entries in the data that are delayed take total
delayed = airline_series[airline_series.str.contains('delayed:')]
delayed_totals = delayed.str.split(':').str[-1].reset_index(drop=True).astype(float)

# new df to hold the totals for flights, delays, airports
delays_by_year = pd.concat([year_totals, airport_names, delayed_totals, flight_totals], axis=1)

# group the delays by year
delays_by_year_groups = delays_by_year[[2,3]].groupby([delays_by_year[0],delays_by_year[1]])

# get the totals
delays_by_year_totals = delays_by_year_groups.sum()  # sum the group9

# create new column percentages, group by month and get totals
delays_by_year_totals['percentages'] = delays_by_year_totals[2]/delays_by_year_totals[3]*100
delays_by_year_totals = delays_by_year_totals['percentages'].groupby(level=0, group_keys=False)

q11 = delays_by_year_totals.nlargest(1)  # Series of years/airport names and percentages
print(q11)

## 12. For each airline, determine the airport where that airline had its
##     greatest percentage of delayed flights.  Give a Series with airline
##     names (not code) and airport names (not code) as MultiIndex and the
##     percentage of delayed flights as values, sorted from smallest to
##     largest percentage.

# new df to hold the totals for flights, delays, airports
delays_by_airport = pd.concat([airline_names, airport_names, delayed_totals, flight_totals], axis=1)

# group the delays by airport
delays_by_airport_groups = delays_by_airport[[2,3]].groupby([delays_by_airport[0],delays_by_airport[1]])

# get the values
delays_by_airport_totals = delays_by_airport_groups.sum()

# create new column percentages, group by airline and get totals
delays_by_airport_totals['percentages'] = delays_by_airport_totals[2]/delays_by_airport_totals[3]*100
delays_by_airport_totals = delays_by_airport_totals['percentages'].groupby(level=0, group_keys=False)

q12 = delays_by_airport_totals.nlargest(1).sort_values(ascending=True)  # Series of airline/airport and percentages
print(q12)
