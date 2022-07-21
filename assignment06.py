##
## File: assignment06.py (STAT 3250)
## Topic: Assignment 6
##

##  The questions this assignment are based on "timing_log.txt".
##  The file "timing_log.txt" contains the set of all WeBWorK
##  log entries on April 1, 2011.  The entries are organized by
##  one log entry per line, with each line including the following:
##
##  --the date and time of the entry
##  --a number that is related to the user (but is not unique)
##  --something that appears to be the epoch time stamp
##  --a hyphen
##  --the "WeBWorK element" that was accessed
##  --the "runTime" required to process the problem
##
##  Note: Some or all of the questions on this assignment can be done without the
##  use of loops, either explicitly or implicitly (apply). As usual, scoring
##  will take this into account.

##  The Gradescope autograder will be evaluating your code on a reduced
##  version of the timing_log.txt data that includes only a fraction of the
##  records.  Your code needs to automatically handle all assignments
##  to the variables q1, q2, ... to accommodate the reduced data set,
##  so do not copy/paste things from the console window, and take care
##  with hard-coding values.


## Load pandas and read in the data set
import pandas as pd  # load pandas as pd
import numpy as np
loglines = open('timing_log.txt').read().splitlines()
#loglines = open('/Users/nolan/Desktop/classes/stat3250/timing_log.txt').read().splitlines()

## 1.  How many log entries were for requests for a PDF version of an
##     assignment?  Those are indicated by "hardcopy" appearing in the
##     WeBWorK element.

logs = pd.Series(loglines)
q1 = np.sum(logs.str.contains('hardcopy'))  # number of log entries requesting a PDF

print(q1)
## 2.  What percentage of log entries involved a Spring '12 section of MATH 1320?
count = logs.str.contains('MATH1320').sum()
q2 = (count/len(logs)) * 100  # percentage of log entries, Spring '12 MATH 1320
print(q2)
## 3. How many different classes use the system? Treat each different name
##    as a different class, even if there is more than one section of a course.

# each class is  [/webwork2/class/.../]
# separate at the / to separate classes
webwork = logs.str.split().str[8]

# remove / and ]
webwork = webwork.str[2:].str[:-1]

# check if the class ends with / and remove it
webwork[webwork.str[-1] == '/'] = webwork.str[:-1].replace('-','')

# make a series where each index is a class using the system in format of  [webwork2, class, ... ]
users = webwork.str.split('/')

q3 = len(np.unique(users[users.str.len() > 1].str[1]))  # number of different classes using the system
print(q3)

## 4.  Find the percentage of log entries that came from an initial
##     log in.  For those, the WeBWorK element has the form
##
##          [/webwork2/ClassName] or [/webwork2/ClassName/]
##
##     where "ClassName" is the name of a class.

# can use series i made in q3

q4 = (np.sum(users.str.len() == 2)/len(loglines)) * 100  # percentage of log entries from initial log in
print(q4)

## 5.  Determine the percentage of log entries for each section of MATH 1310
##     from Spring 2012, among the total number of log entries for MATH 1310,
##     Spring 2012.  Give the percentages as a Series with class name as
##     index and percentages as values, sorted by percentage largest to smallest.
##     (The class name should be of the form 'Spring12-MATH1310-InstructorName')

# get indexes where there are two elements
entries = users[users.str.len() > 1]

# get indexes that have both math 1310 and spring 2012
matches = entries[(entries.str[1].str.contains('MATH1310')) & (entries.str[1].str.contains('Spring12'))].str[1]

q5 = (matches.value_counts()/len(matches)) * 100  # Series of MATH 1310 sections and percentage within MATH 1310
print(q5)

## 6.  How many log entries were from instructors performing administrative
##     tasks?  Those are indicated by "instructor" alone in the 3rd position of
##     the WeBWorK element.

# get indexes containing an instructor (3 elements)
entries2 = users[users.str.len() > 2]

q6 = np.sum(entries2.str[2] == 'instructor')  # number of instructor administrative log entries
print(q6)

## 7.  Find the number of log entries for each hour of the day. Give the
##     counts for the top-5 (plus ties as usual) as a Series, with hour of day
##     as index and the count as values, sorted by count from largest to
##     smallest.

# split each line and get the hour
hours = logs.str.split().str[3].str.split(":").str[0]

# get series of hours most to least occuring
tophours = hours.value_counts().sort_values(ascending=False)

q7 = tophours.loc[tophours >= tophours.iloc[4]]  # Series of entry count by hour, top 5
print(q7)

## 8.  Find the number of log entries for each minute of each hour of the day.
##     Give the counts for the top-8 (plus ties as usual) as a Series, with
##     hour:minute pairs as index and the count as values, sorted by count
##     from largest to smallest.  (An example of a possible index entry
##     is 15:47)

# split each line and get hours:minutes
times = logs.str.split().str[3].str[0:5]

# get series of hours:mins most to least occuring
toptimes = times.value_counts().sort_values(ascending=False)

q8 = toptimes.loc[toptimes >= toptimes.iloc[7]]  # Series of counts by hour:minute, top-8 plus ties
print(q8)

## 9. Determine which 5 classes had the largest average "runTime".  Give a
##    Series of the classes and their average runTime, with class as index
##    and average runTime as value, sorted by value from largest to smallest.

# get the runtimes at 12 element and convert to float
runtimes = logs.str.split().str[11].astype(float)

# get classes
classes = entries[entries.str.len() > 1]

q9 = runtimes.groupby(classes.str[1]).mean().sort_values(ascending=False)[0:5]  # Series of classes and average runTimes
print(q9)

## 10. Determine the percentage of log entries that were accessing a problem.
##     For those, the WeBWorK element has the form
##
##           [/webwork2/ClassName/AssignmentName/Digit]
##     or
##           [/webwork2/ClassName/AssignmentName/Digit/]
##
##     where "ClassName" is the name of the class, "AssignmentName" the
##     name of the assignment, and "Digit" is a positive digit.

# indexes where there are 4 elements to fit the form
entries2 = entries[entries.str.len() == 4]

q10 = 100*np.sum(entries2.str[3].str.isdigit())/len(loglines)  # percentage of log entries accessing a problem

print(q10)
## 11. Find the top-10 (plus tied) WeBWorK problems that had the most log entries,
##     and the number of entries for each (plus ties as usual).  Sort the
##     table from largest to smallest.
##     (Note: The same problem number from different assignments and/or
##     different classes represent different WeBWorK problems.)
##     Give your answer as a Series with index entries of the form
##
##          ClassName/AssignmentName/Digit
##
##     and counts for values, sorted by counts from largest to smallest.

# get indexes where there are at least 4 components
entries3 = entries[entries.str.len() > 3]

# get subset and make the last component a digit in order to count
entries4 = entries3[entries3.str[3].str.isdigit()]

# form each possible combination in order to group them and count
probs = entries3.str[1] + '/' + entries4.str[2] + '/' + entries4.str[3]

topprobs = probs.value_counts()[0:10]

q11 = topprobs.loc[topprobs >= topprobs.iloc[9]]  # Series of problems and counts
print(q11)
