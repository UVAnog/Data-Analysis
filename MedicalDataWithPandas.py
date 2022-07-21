##
## File: assignment05.py (STAT 3250)
## Topic: Assignment 5
##

##  This assignment requires the data file 'diabetic_data.csv'.  This file
##  contains records for over 100,000 hospitalizations for people who have
##  diabetes.  The file 'diabetic_info.pdf' contains information on the
##  codes used for a few of the entries.  Missing values are indicated by
##  a '?'.  You should be able to read in this file using the usual
##  pandas methods.

##  The Gradescope autograder will be evaluating your code on a reduced
##  version of the diabetic_data.csv data that includes about 35% of the
##  records.  Your code needs to automatically handle all assignments
##  to the variables q1, q2, ... to accommodate the reduced data set,
##  so do not copy/paste things from the console window, and take care
##  with hard-coding values.

##  Note: Many of the questions on this assignment can be done without the
##  use of loops, either explicitly or implicitly (apply). Scoring will take
##  this into account.

import pandas as pd # load pandas as pd
import numpy as np
dia = pd.read_csv('diabetic_data.csv')
#dia = pd.read_csv('/Users/nolan/Desktop/classes/stat3250/diabetic_data.csv')
dia1 = dia.loc[:10,:]

## 1.  Determine the average number of procedures ('num_procedures') for
##     those classified as females and for those classified as males.

q1f = dia['num_procedures'].groupby(dia['gender']).mean().loc['Female']  # female average number of procedures
q1m = dia['num_procedures'].groupby(dia['gender']).mean().loc['Male']  # male average number of procedures

## 2.  Determine the average length of hospital stay ('time_in_hospital')
##     for each race classification.  (Omit those unknown '?' but include
##     those classified as 'Other'.)  Give your answer as a Series with
##     race for the index sorted alphabetically.

q2 = dia['time_in_hospital'].groupby(dia['race']).mean().drop('?')  # Series of average length of stay by race

## 3.  Determine the percentage of total days spent in the hospital due to
##     stays ("time_in_hospital") of at least 7 days. (Do not include the %
##     symbol in your answer.)

# find stays of at least 7 days
daysover7 = np.sum(dia.loc[dia['time_in_hospital'] >= 7, 'time_in_hospital'])
q3 = (daysover7/np.sum(dia['time_in_hospital'])) * 100  # percentage of days from stays of at least 7 days

## 4.  Among the patients in this data set, what percentage had at least
##     three recorded hospital visits?  Each distinct record can be assumed
##     to be for a separate hospital visit. Do not include the % symbol in
##     your answer.

# find distinct patients
totalpatients = len(np.unique(dia['patient_nbr']))

# find patients with at least 3 stays
patientsover3 = np.sum(dia['patient_nbr'].value_counts() >= 3)
q4 = (patientsover3/totalpatients) * 100   # percentage patients with at least three visits

## 5.  List the top-15 most common diagnoses, based on the codes listed
##     collectively in the columns 'diag_1', 'diag_2', and 'diag_3'.
##     Give your response as a Series with the diagnosis code as the
##     index and the number of occurances as the values, sorted by
##     values from largest to smallest.  If more than one value could
##     go in the 15th position, include all that could go in that
##     position.  (This is the usual "include ties" policy.)

# make a collection of the diagnoses
diagnoses = pd.concat(([dia['diag_1'], dia['diag_2'], dia['diag_3']]))

topdiagnoses = diagnoses.value_counts()[0:15].sort_values(ascending=False)  # top-15 diagnoses plus any ties

q5 = topdiagnoses.loc[topdiagnoses >= topdiagnoses.iloc[14]]
print(q5)

# 6.  The 'age' in each record is given as a 10-year range of ages.  Assume
##     that the age for a person is the middle of the range.  (For instance,
##     those with 'age' [40,50) are assumed to be 45.)  Determine the average
##     age for each classification in the column 'acarbose'.  Give your
##     answer as a Series with the classification as index and averages as
##     values, sorted from largest to smallest average.
diaCopy = dia


# defining and using a function to find the middle of each age range

def findmiddle(x):
    # ages are given as [x-y)
    # split the range and find each number individually
    # https://stackoverflow.com/questions/6903557/splitting-on-first-occurrence
    y = x.split(')')[0].split('[')[1].split('-')
    # find the middle value of each range
    return (float(y[0]) + float(y[1])) / 2


# make a new column in df that applies function to find middle to each range in age column
# i.e row containing [70, 80) will contain 75 under middle column
diaCopy['middle'] = diaCopy['age'].apply(findmiddle)

q6 = diaCopy['middle'].groupby(dia['acarbose']).mean().sort_values(ascending=False)  # Series of classifications and averages

## 7.  Determine all medical specialties that have an average hospital stay
##     (based on time_in_hospital) of at least 7 days.  Give a Series with
##     specialty as index and average hospital stay as values, sorted from
##     largest to smallest average stay.

# group time in hospital by medical specialty
specialties = dia['time_in_hospital'].groupby(dia['medical_specialty'])

q7 = dia['time_in_hospital'].groupby(dia['medical_specialty']).mean()[specialties.mean() >= 7].sort_values(ascending=False)  # Series of specialities and average stays

##  8. Three medications for type 2 diabetes are 'glipizide', 'glimepiride',
##     and 'glyburide'.  There are columns in the data for each of these.
##     Determine the number of records for which at least two of these
##     are listed as 'Steady'.

# make true false series for each medication
med1 = (dia['glipizide'] == 'Steady')
med2 = (dia['glimepiride'] == 'Steady')
med3 = (dia['glyburide'] == 'Steady')

# count total of true pairs
q8 = np.sum((med1 & med2) | (med1 & med3) | (med2 & med3))  # number of records with at least two 'Steady'


##  9. Find the percentage of "time_in_hospital" accounted for by the top-100
##     patients in terms of number of times in file.  (Include all patients
##     that tie the 100th patient.)

# group data by patient number, count number of times each patient appears
patients = dia['patient_nbr'].groupby(dia['patient_nbr']).count().sort_values(ascending=False)
# take top 100 patients
toppatients = patients.iloc[100]
# get set of patients above cutoff
# https://stackoverflow.com/questions/52169051/pandas-dataframe-row-selection-combined-condition-index-and-column-values
patientstop100 = patients.index[patients >= toppatients]
# Percentage of time from top-100 patients
q9 = (np.sum(dia.loc[dia['patient_nbr'].isin(patientstop100), 'time_in_hospital'])/np.sum(dia['time_in_hospital'])) * 100

## 10. What percentage of reasons for admission ('admission_source_id')
##     correspond to some form of transfer from another care source?

# getting the ids that are transfers from the pdf
transfernumbers = [4, 5, 6, 10, 18, 22, 25, 26]

# https://numpy.org/doc/stable/reference/generated/numpy.intersect1d.html
# "Return the sorted, unique values that are in both of the input arrays."
# using this to get the admissions that align with transfer numbers
transfers = np.intersect1d(np.unique(dia['admission_source_id']), transfernumbers)

q10 = (dia['admission_source_id'].value_counts()[transfers].sum()/len(dia)) * 100  # Percentage of admission by transfer

## 11. The column 'discharge_disposition_id' gives codes for discharges.
##     Determine the 5 codes that resulted in the greatest percentage of
##     readmissions.  Give your answer as a Series with discharge code
##     as index and readmission percentage as value, sorted by percentage
##     from largest to smallest.

# make a new column with all 0's
dia['readmission'] = 0

# check if patient was readmitted, if they were make value in readmissions column 1
dia.loc[dia['readmitted'] == '<30', 'readmission'] = 1
dia.loc[dia['readmitted'] == '>30', 'readmission'] = 1

# count the total discharges
totaldischarges = dia['readmission'].groupby(dia['discharge_disposition_id']).count()

# total the readmissions
totalreadmissions = dia['readmission'].groupby(dia['discharge_disposition_id']).sum()

# Series of discharge codes and readmission percentages
q11 = ((totalreadmissions/totaldischarges) * 100).sort_values(ascending=False).iloc[:5]

## 12. The columns from 'metformin' to 'citoglipton' are all medications,
##     with "Up", "Down", and "Steady" indicating the patient is taking that
##     medication.  For each of these medications, determine the average
##     number of medications from this group that patients are taking.
##     Give a Series of all medications with an average of at least 1.5,
##     with the medications as index and averages as values, sorted
##     largest to smallest average.
##     (Hint: df.columns gives the column names of the data frame df.)


# make subset df of just the medication columns
meds = dia.loc[:, 'metformin':'citoglipton']

# convert to series with medication as index, values are all 0
medseries = pd.Series(0, index=meds.columns)  # series with meds as index


# function to indicate use of medication 0 = no 1 = yes
def meduse(x):
    if (x == 'Up') or (x == 'Down') or (x == 'Steady'):
        return 1
    else:
        return 0


# loop through sub df, if medication is used mark as 1, not used is 0
for med in meds.columns:
    meds[med] = meds[med].apply(meduse)

# make a new column to indicate medicine use, specifying axis = 1 to indicate where sum is occurring
meds['medicated'] = np.sum(meds, axis=1)

# loop through each column, find count of medication, replace value in series with the calculated average
for i in medseries.index:
    count = meds.loc[meds[i] == 1, 'medicated']
    medseries.loc[i] = np.mean(count)

# sort values and return those with average >= 1.5
q12 = medseries.sort_values(ascending=False).where(medseries >= 1.5).dropna()  # Series of medications and averages
