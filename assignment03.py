##
## File: assignment03.py (STAT 3250)
## Topic: Assignment 3
##

##  The questions in this assignment refer to the data in the
##  file 'absent.csv'.  The data contains 740 records from an
##  employer, with 21 columns of data for each record.  (There
##  are a few missing values indicated by zeros where zeros
##  are clearly not appropriate.)  The file 'absent.pdf' has
##  a summary of the meanings for the variables.
##
##  All of these questions can be completed without loops.  You
##  should try to do them this way, "code efficiency" will take
##  this into account.

import numpy as np  # load numpy as np
import pandas as pd  # load pandas as pd

absent = pd.read_csv('absent.csv')  # import the data set as a pandas dataframe
#absent = pd.read_csv('/Users/nolan/Desktop/classes/stat3250/absent.csv')

## 1.  Find the mean absent time among all records.

q1 = np.mean(absent)['Absenteeism time in hours']  # mean of "Absenteeism" hours

## 2.  Determine the number of records corresponding to
##     being absent on a Thursday.


q2 = len(absent.loc[(absent['Day of the week'] == 5)])

## 3.  Find the number of unique employees IDs represented in
##     this data.

q3 = len(absent['ID'].unique())  # number of unique employee IDs

## 4.  Find the average transportation expense for the employee
##     with ID = 34.

# get transportation column of employees with id 34, find transportation expense column, take mean

q4 = np.mean(absent.loc[(absent['ID'] == 34)]['Transportation expense'])  # Average transportation expense, ID = 34

## 5.  Find the total number of hours absent for the records
##     for employee ID = 11.

# get id 11, find hours absent, take total

q5 = np.sum(absent.loc[(absent['ID'] == 11)]['Absenteeism time in hours'])   # total hours absent, ID = 11

## 6.  Find (a) the mean number of hours absent for the records of those who
##     have no pets, then (b) do the same for those who have more than one pet.

# find employees with no pet, find hours absent column, take mean
q6a = np.mean(absent.loc[(absent['Pet'] == 0)]['Absenteeism time in hours'])  # mean hours absent, no pet

# find employees with > 1 pet, find hours absent column, take mean
q6b = np.mean(absent.loc[(absent['Pet'] > 1)]['Absenteeism time in hours'])  # mean hours absent, more than one pet

## 7.  Among the records for absences that exceeded 8 hours, find (a) the
##     proportion that involved smokers.  Then (b) do the same for absences
##     of no more then 4 hours.

smokers_over8 = len(absent.loc[((absent['Absenteeism time in hours'] > 8) & (absent['Social smoker'] == 1))])
total_over8 = len(absent.loc[(absent['Absenteeism time in hours'] > 8)])
# find absences > 8, find total of smokers
q7a = smokers_over8 / total_over8  # proportion of smokers, absence greater than 8 hours

# find absences <= 4, find total of smokers
smokers_under4 = len(absent.loc[((absent['Absenteeism time in hours'] <= 4) & (absent['Social smoker'] == 1))])
total_under4 = len(absent.loc[(absent['Absenteeism time in hours'] <= 4)])

q7b = smokers_under4 / total_under4  # proportion of smokers, absence no more than 4 hours

## 8.  Repeat Question 7, this time for social drinkers in place of smokers.

# same as above, find absences > 8, total drinkers
drinkers_over8 = len(absent.loc[((absent['Absenteeism time in hours'] > 8) & (absent['Social drinker'] == 1))])
totaldrinkers_over8 = len(absent.loc[(absent['Absenteeism time in hours'] > 8)])

q8a = drinkers_over8 / totaldrinkers_over8 # proportion of social drinkers, absence greater than 8 hours

# same as above, find absences <= 4, total drinkers
drinkers_under4 = len(absent.loc[((absent['Absenteeism time in hours'] <= 4) & (absent['Social drinker'] == 1))])
totaldrinkers_under4 = len(absent.loc[(absent['Absenteeism time in hours'] <= 4)])

q8b = drinkers_under4 / totaldrinkers_under4 # proportion of social drinkers, absence no more than 4 hours

## 9.  Find the top-5 employee IDs in terms of total hours absent.  Give
##     the IDs and corresponding total hours absent as a Series with ID
##     for the index, sorted by the total hours absent from most to least.

# group by ids, find hours absent hours for each id, total them, sort
q9 = absent.groupby('ID')['Absenteeism time in hours'].sum().sort_values(ascending=False).iloc[:5]

## 10. Find the average hours absent per record for each day of the week.
##     Give the day number and average as a Series with the day number
##     as the index, sorted by day number from smallest to largest.

# group by day of the week, total hours for each day, take average
q10 = absent.groupby('Day of the week')['Absenteeism time in hours'].mean()  # Series of average hours absent by day of week.

## 11. Repeat Question 10 replacing day of the week with month.
##     Give the month number and average as a Series with the month number
##     as the index, sorted by month number from smallest to largest.

# group by month, total the hours for each month, take average, take 1-13 because 0 is not a month and has no values
q11 = absent.groupby('Month of absence')['Absenteeism time in hours'].mean().iloc[1:13] # Series of average hours absent by day of week.

## 12. Find the top 3 most common reasons for absence for the social smokers.
##      Give the reason code and number of occurances as a Series with the
##      reason code as the index, sorted by number of occurances from
##      largest to smallest.  (If there is a tie for 3rd place,
##      include all that tied for that position.)

# take subset of dataframe by selecting only smokers
socialSmokers = absent.loc[(absent['Social smoker'] == 1)]

# group the subset by reason for absense and total the hours for each reason, sort
q12 = socialSmokers.groupby('Reason for absence')['Absenteeism time in hours'].sum().sort_values(ascending=False).iloc[:3]
