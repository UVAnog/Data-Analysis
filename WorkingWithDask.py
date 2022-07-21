##
## File: assignment13.py (STAT 3250)
## Topic: Assignment 13
##


##  These questions are similar to reviewed lecture material, but
##  provide some experience with Dask.

import dask.dataframe as dd #import libraries
import numpy as np
import pandas as pd
dtypes = {
 'Date First Observed': str, 'Days Parking In Effect    ': str,
 'Double Parking Violation': str, 'Feet From Curb': np.float32,
 'From Hours In Effect': str, 'House Number': str,
 'Hydrant Violation': str, 'Intersecting Street': str,
 'Issue Date': str, 'Issuer Code': np.float32,
 'Issuer Command': str, 'Issuer Precinct': np.float32,
 'Issuer Squad': str, 'Issuing Agency': str,
 'Law Section': np.float32, 'Meter Number': str,
 'No Standing or Stopping Violation': str,
 'Plate ID': str, 'Plate Type': str,
 'Registration State': str, 'Street Code1': np.uint32,
 'Street Code2': np.uint32, 'Street Code3': np.uint32,
 'Street Name': str, 'Sub Division': str,
 'Summons Number': np.uint32, 'Time First Observed': str,
 'To Hours In Effect': str, 'Unregistered Vehicle?': str,
 'Vehicle Body Type': str, 'Vehicle Color': str,
 'Vehicle Expiration Date': str, 'Vehicle Make': str,
 'Vehicle Year': np.float32, 'Violation Code': np.uint16,
 'Violation County': str, 'Violation Description': str,
 'Violation In Front Of Or Opposite': str, 'Violation Legal Code': str,
 'Violation Location': str, 'Violation Post Code': str,
 'Violation Precinct': np.float32, 'Violation Time': str
}

nyc = dd.read_csv('nyc-parking-tickets2015.csv', dtype=dtypes, usecols=dtypes.keys())
#nyc = dd.read_csv('/Users/nolan/Desktop/classes/stat3250/data/nyc-parking-tickets2015.csv', dtype=dtypes, usecols=dtypes.keys())


## 1.  There are several missing values in the 'Vehicle Body Type' column. Impute
##     missing values of 'Vehicle Body Type' with the mode. What is the mode?

# get the mode
vehicle_body_type_mode = nyc['Vehicle Body Type'].mode().compute()[0]
# replace missing values with mode
nyc['Vehicle Body Type'] = nyc['Vehicle Body Type'].fillna(vehicle_body_type_mode)

q1 = vehicle_body_type_mode  # Report the mode, the most common Vehicle Body Type.
print(q1)

## 2.  How many missing data points are there in the 'Intersecting Street' column?

missing_intersecting_street = nyc['Intersecting Street'].isnull().sum().compute()

q2 = missing_intersecting_street  # Number of missing data points
print(q2)

## 3.  What percentage of vehicle makes are Jeeps during the months of March -
##     September (inclusive) of 2015?

# convert dates to datetime objects
nyc['Issue Date'] = nyc['Issue Date'].astype('datetime64[ns]')

# subset data to get 2015
nyc_2015 = nyc[(nyc['Issue Date'].dt.year == 2015)]

# subset data to get march - september
nyc_march_sep_2015 = nyc_2015[(nyc['Issue Date'] >= '03-01-2015') & (nyc['Issue Date'] <= '06-30-2015')]

# count occurences of jeeps
car_counts = nyc_march_sep_2015['Vehicle Make'].value_counts().compute()
len_makes = len(nyc_march_sep_2015)

num_jeeps = car_counts.loc['JEEP']
q3 = (num_jeeps / len_makes) * 100   # Percentage of Jeeps
print(q3)

## 4.  What's the most common color of a car in 2015? Maintain the color in all caps.

# value count the cars
car_counts = nyc_2015['Vehicle Color'].value_counts().compute()

# sort
most_common_color = car_counts.sort_values(ascending=False).index[0]

# get the highest
q4 = most_common_color  # Most common car color
print(q4)

## 5.  Find all the cars in any year that are the same color as q4. What percentage of
##     those care are sedans?

# get cars in 2015 data set that are grey
grey_cars = nyc_2015[(nyc_2015['Vehicle Color'] == q4)]

# get total that are sedans
grey_types = grey_cars['Vehicle Body Type'].value_counts().compute()
num_sedans = grey_types.loc['SDN']

# get total of all grey cars
len_grey_cars = len(grey_cars)
# sedans / total grey * 100
q5 = (num_sedans / len_grey_cars) * 100  # Percentage of sedans
print(q5)

## 6.  Make a table of the top 5 registration states, sorted greatest to least.

# get counts of registrations in each state (groupby state, count reg?)
total_registrations = nyc['Registration State'].value_counts().compute()
# sort from top to bottom
total_registrations_sorted = total_registrations.sort_values(ascending=False)
# get top 5 including ties
top5_registrations = total_registrations_sorted.loc[total_registrations_sorted >= total_registrations_sorted.iloc[4]]
q6 = top5_registrations  # Series of top 5 registration states
print(q6)

## 7.  Perhaps someone bought a new vehicle and kept the same license plate. How many license
##     plates have more than one 'Vehicle Make' associated with the respective plate?
# get counts of license plates
license_counts = nyc.groupby('Plate ID').apply(lambda x: x['Vehicle Make'].nunique(), meta='x').compute()

# get those greater than 2
plates_over2 = license_counts[license_counts >= 2]
q7 = len(plates_over2)  # Number of license plates
print(q7)

## 8.  Determine the top three hours that result in the most parking violations.
##     "0011A" would be 12:11 AM and "0318P" would be 3:18 PM. Report the solution
##     with the index in the format of "01A" and the count.
# slice first two to get the hour
nyc['Violation Hour'] = nyc['Violation Time'].str[:2]

# slice last character to get am/pm
nyc['AM / PM'] = nyc['Violation Time'].str[-1]

# combine slices to new column
nyc['Violation Time Sliced'] = nyc['Violation Hour'] + nyc['AM / PM']

# get top hours
violations_per_hour = nyc['Violation Time Sliced'].value_counts().compute()

# sort
top_hours = violations_per_hour.sort_values(ascending=False)

top3_hours = top_hours.loc[top_hours >= top_hours.iloc[2]]

q8 = top3_hours  # Series with top three hours
print(q8)

## 9.  Among the tickets issued by Precinct 99, what is the average distance from the
##     curb in feet?

# subset to tickets issued by precint 99
precint_99 = nyc[(nyc['Violation Precinct'] == 99)]

# get average of distance
average_distance = precint_99['Feet From Curb'].mean()

q9 = average_distance.compute()  # Average distance from the curb
print(q9)
