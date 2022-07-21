##
## File: assignment08.py (STAT 3250)
## Topic: Assignment 8
##

##  This assignment requires data from three files:
##
##      'movies.txt':  A file of nearly 3900 movies
##      'reviewers.txt':  A file of over 6000 reviewers who provided ratings
##      'ratings.txt':  A file of over 1,000,000 movie ratings
##
##  The file 'readme.txt' has more information about these files.
##  You will need to consult the readme.txt file to answer some of the questions.

##  Note: Some or all of the questions on this assignment can be done without the
##  use of loops, either explicitly or implicitly (apply). As usual, scoring
##  will take this into account.

##  The Gradescope autograder will be evaluating your code on a reduced
##  version of the movies.txt data that includes only a fraction of the
##  records.  Your code needs to automatically handle all assignments
##  to the variables q1, q2, ... to accommodate the reduced data set,
##  so do not copy/paste things from the console window, and take care
##  with hard-coding values.


## It is recommended that you read in the data sets in the manner shown below.
movietext = open('movies.txt', encoding='utf8').read().splitlines()
reviewertext = open('reviewers.txt', encoding='utf8').read().splitlines()
ratingtext = open('ratings.txt', encoding='utf8').read().splitlines()

# reading in for local use
#movietext = open('/Users/nolan/Desktop/classes/stat3250/data/movies.txt', encoding='utf8').read().splitlines()
#reviewertext = open('/Users/nolan/Desktop/classes/stat3250/data/reviewers.txt', encoding='utf8').read().splitlines()
#ratingtext = open('/Users/nolan/Desktop/classes/stat3250/data/ratings.txt', encoding='utf8').read().splitlines()

# imports
import pandas as pd
import numpy as np

# create series for each text file
movies = pd.Series(movietext)
reviewers = pd.Series(reviewertext)
ratings = pd.Series(ratingtext)

review_df = pd.DataFrame(
    {'ReviewerID': reviewers.str.split('::').str[0].astype('int').tolist(),
     'Gender': reviewers.str.split('::').str[1].tolist(),
     'Age': reviewers.str.split('::').str[2].astype('int').tolist(),
     'Occupation': reviewers.str.split('::').str[3].astype('int').tolist(),
     'Zip': reviewers.str.split('::').str[4].tolist(),
     'State': reviewers.str.split('::').str[5].tolist()
     })

ratings_df = pd.DataFrame(
    {'ReviewerID': ratings.str.split('::').str[0].astype('int').tolist(),
     'MovieID': ratings.str.split('::').str[1].astype('int').tolist(),
     'Ratings': ratings.str.split('::').str[2].astype('int').tolist()
    })
movies_df = pd.DataFrame(
    {'MovieID': movies.str.split('::').str[0].astype('int').tolist(),
     'Title': movies.str.split('::').str[1].tolist(),
     'Genres': movies.str.split('::').str[2].tolist(),
    })



## 1.  Based on the data in 'reviewers.txt': Determine the percentage of all
##     reviewers that are female.  Determine the percentage of all reviewers in
##     the 35-44 age group.  Among the 18-24 age group, find the percentage
##     of reviewers that are male.


q1a = np.sum(reviewers.str.split('::').str[1].str.contains('F')) / len(reviewers) * 100  # percentage of female reviewers
q1b = np.sum(reviewers.str.split('::').str[2].str.contains('35')) / len(reviewers) * 100  # percentage age 35-44
# get the 18 age group
agegroup18 = reviewers[reviewers.str.split('::').str[2].str.contains('18')]  # get
q1c = np.sum(agegroup18.str.split('::').str[1].str.contains('M')) / len(agegroup18) * 100 # percentage of males reviewers in 18-24 age group

print(q1a)
print(q1b)
print(q1c)

## 2.  Give a year-by-year Series of counts for the number of ratings, with
##     the rating year as index and the counts as values, sorted by rating
##     year in ascending order.

# making timestamp
ratings_df["Timestamp"] = pd.to_numeric(ratings.str.split('::').str[3])
timestamps = pd.Series(ratings_df["Timestamp"])

# getting the years
years = pd.to_datetime(timestamps, unit='s').dt.year

ratings_df["Years"] = years

q2 = ratings_df.groupby("Years").count().iloc[:,0]  # Series of rating counts by year rated

print(q2)

## 3.  Determine the average rating from female reviewers and the average
##     rating from male reviewers.

# get all of the female reviewers
females = review_df[review_df['Gender'] == 'F']
q3a = females.merge(ratings_df, on='ReviewerID')['Ratings'].mean()  # average rating for female reviewers
print(q3a)
# get all of the make reviewers
males = review_df[review_df['Gender'] == 'M']
q3b = males.merge(ratings_df, on='ReviewerID')['Ratings'].mean()  # average rating for male reviewers
print(q3b)

## 4.  Determine the number of movies that received an average rating of
##     less than 1.75.  (Movies and remakes should be considered as
##     different.)

movies_and_ratings = movies_df.merge(ratings_df, on='MovieID')
average_ratings = movies_and_ratings.groupby('MovieID')['Ratings'].mean()  #groupby movies and get mean
q4 = average_ratings[average_ratings < 1.75].count()  # count of number with average rating less than 1.75
print(q4)

## 5.  Determine the number of movies listed in 'movies.txt' for which there
##     is no rating in 'ratings.txt'.

q5 = len(movies_df) - len(np.unique(movies_df.merge(ratings_df, on='MovieID')['MovieID']))  # number of movies that were not rated
print(q5)

## 6.  Among the ratings from male reviewers, determine the average
##     rating for each occupation classification (including 'other or not
##     specified'), and give the results in a Series sorted from highest to
##     lowest average with the occupation title (not the code) as index.


def getoccupation(x):
    if x == 0:
        return "other/not specified"
    elif x == 1:
        return "academic/educator"
    elif x == 2:
        return "artist"
    elif x == 3:
        return "clerical/admin"
    elif x == 4:
        return "college/grad student"
    elif x == 5:
        return "customer service"
    elif x == 6:
        return "doctor/health care"
    elif x == 7:
        return "executive/managerial"
    elif x == 8:
        return "farmer"
    elif x == 9:
        return "homemaker"
    elif x == 10:
        return "K-12 student"
    elif x == 11:
        return "lawyer"
    elif x == 12:
        return "programmer"
    elif x == 13:
        return "retired"
    elif x == 14:
        return "sales/marketing"
    elif x == 15:
        return "scientist"
    elif x == 16:
        return "self-employed"
    elif x == 17:
        return "technician/engineer"
    elif x == 18:
        return "tradesman/craftsman"
    elif x == 19:
        return "unemployed"
    elif x == 20:
        return "writer"


review_df['OccupationTitle'] = review_df['Occupation'].apply(getoccupation)

get_males = review_df[review_df['Gender'] == 'M']

temp1 = pd.DataFrame(get_males.merge(ratings_df, on='ReviewerID').groupby('OccupationTitle')['Ratings'].mean())

q6 = temp1.iloc[:, 0].sort_values(ascending=False)


print(q6)

## 7.  Determine the average rating for each genre, and give the results in
##     a Series with genre as index and average rating as values, sorted
##     alphabetically by genre.

genre_ratings = []

# make a list of genres for each movie
moviegenreslist = movies_df['Genres'].str.split('|')
onegenre = moviegenreslist[moviegenreslist.str.len() == 1].str[0]

temp = movies_df.merge(ratings_df, on='MovieID')

for i in onegenre:
    genre_ratings.append(temp[temp['Genres'].str.contains(i)]['Ratings'].mean())

q7 = pd.Series(genre_ratings, index=onegenre).sort_values(ascending=False).drop_duplicates()   # Series of average rating by genre

print(q7)

## 8.  For the reviewer age category, assume that the reviewer has age at the
##     midpoint of the given range.  (For instance '35-44' has age (35+44)/2 = 39.5)
##     For 'under 18' assume an age of 16, and for '56+' assume an age of 60.
##     For each possible rating (1-5) determine the average age of the reviewers
##     giving that rating.  Give your answer as a Series with rating as index
##     and average age as values, sorted by rating from 1 to 5.

# merging dfs
reviewers_and_ratings = review_df.merge(ratings_df, on='ReviewerID')

# changing the ages to the midpoints
reviewers_and_ratings["Age"].replace(
    {1: 16, 18: 21, 25: 29.5, 35: 39.5, 45: 47, 50: 52.5, 56: 60},
    inplace=True)

q8 = reviewers_and_ratings.groupby('Ratings')['Age'].mean().sort_index()   # Series of average age by rating
print(q8)

## 9.  Find the top-5 "states" in terms of average rating.  Give as a Series
##     with the state as index and average rating as values, sorted from
##     highest to lowest average rating. (Include any ties as usual)
##     Note: "states" includes US territories and military bases. See the
##     readme.txt file for more information on what constitutes a "state"
##     for this assignment.


q9 = reviewers_and_ratings.groupby('State')['Ratings'].mean().sort_values(ascending=False).nlargest(5)  # top-5 states by average rating
print(q9)

## 10. For each age group, determine the occupation that gave the lowest
##     average rating.  Give a Series that includes the age group code and
##     occupation title as a multiindex, and average rating as values.  Sort
##     the Series by age group code from youngest to oldest.

rate_and_review = review_df.merge(ratings_df, on='ReviewerID')

rating_by_occupation = rate_and_review['Ratings'].groupby(
    [
        rate_and_review['Age'],
        rate_and_review['OccupationTitle']
    ]).mean()
q10 = rating_by_occupation.groupby('Age', group_keys=False).nsmallest(1)   # Series of average ratings by age code and occupation title

print(q10)


