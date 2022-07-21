##
## File: assignment07.py (STAT 3250)
## Topic: Assignment 7
##

##  This assignment requires the data file 'movies.txt'.  This file
##  contains records for nearly 3900 movies, including a movie ID number,
##  the title (with year of release, which is not part of the title), and a
##  list of movie genre classifications (such as Romance, Comedy, etc).  Note
##  that a given movie can be classified into more than one genre -- for
##  instance Toy Story is classified as "Animation", "Children's", and
##  "Comedy".

##  Note: Some or all of the questions on this assignment can be done without the
##  use of loops, either explicitly or implicitly (apply). As usual, scoring
##  will take this into account.

##  The Gradescope autograder will be evaluating your code on a reduced
##  version of the movies.txt data that includes only a fraction of the
##  records.  Your code needs to automatically handle all assignments
##  to the variables q1, q2, ... to accommodate the reduced data set,
##  so do not copy/paste things from the console window, and take care
##  with hard-coding values.

import numpy as np  # load numpy as np
import pandas as pd  # load pandas as pd

# Read in the movie data as text; leave in encoding = 'utf8'
movielines = open('movies.txt', encoding='utf8').read().splitlines()
#movielines = open('/Users/nolan/Desktop/classes/stat3250/movies.txt', encoding='utf8').read().splitlines()

## 1.  Determine the number of movies included in genre "Animation", the number
##     in genre "Horror", and the number in both "Comedy" and "Crime".

# change movielines to series
movielines = pd.Series(movielines)

# get all the genres
moviegenres = movielines.str.split("::").str[2]

q1a = np.sum(moviegenres.str.contains('Animation'))  # Genre includes Animation
q1b = np.sum(moviegenres.str.contains('Horror'))  # Genre includes Horror
q1c = np.sum(moviegenres.str.contains('Comedy') & moviegenres.str.contains('Crime'))  # Genre includes both Comedy and Crime

print(q1a)
print(q1b)
print(q1c)
## 2.  Among the movies in the genre "Horror", what percentage have the word
##     "massacre" in the title?  What percentage have 'Texas'? (Upper or lower
##     cases are allowed here.)

# get the titles and their years
movietitlesandyears = movielines.str.split("::").str[1]

# since the titles will all end in the same place we can get the individual titles
movietitles = movietitlesandyears.str[:-7]

# get all the movie titles in the Horror genre
horrormovies = movietitles[moviegenres.str.contains('Horror')]

q2a = (np.sum(horrormovies.str.lower().str.contains('massacre'))/len(horrormovies)) * 100  # percentage in Horror that includes 'massacre'
q2b = (np.sum(horrormovies.str.lower().str.contains('texas'))/len(horrormovies)) * 100  # percentage in Horror that includes 'texas'

print(q2a)
print(q2b)

## 3.  Among the movies with exactly one genre, determine the genres that
##     have at least 50 movies classified with that genre.  Give a Series
##     with genre as index and counts as values, sorted largest to smallest
##     by count.

# make a list of genres for each movie
moviegenreslist = moviegenres.str.split('|')

# extract movies with at least 1 genre and get counts of each
onegenre = moviegenreslist[moviegenreslist.str.len() == 1].str[0].value_counts()

q3 = onegenre[onegenre > 50]  # Series of genres for at least 50 movies and counts

print(q3)
## 4.  Determine the number of movies that have 1 genre, 2 genres, 3 genres,
##     and so on.  Give your results in a Series, with the number of genres
##     as the index and the counts as values, sorted by index values from
##     smallest to largest.

q4 = moviegenreslist.str.len().value_counts()  # Series of number of genres and counts
print(q4)
## 5.  How many remakes are in the data? We say a movie is a remake if the title is
##     exactly the same as the title of an older movie. For instance, if 'Hamlet'
##     is in the data set 4 times, then 3 of those should be counted as remakes.
##     (Note that a sequel is not the same as a remake -- "Jaws 2" is completely
##     different from "Jaws".)

q5 = len(movietitles[movietitles.duplicated()])  # number of remakes in data set
print(q5)

## 6.  Determine for each genre the percentage of movies in the data set that
##     are classified as that genre.  Give a Series of all with 8% or more,
##     with genre as index and percentage as values, sorted from highest to
##     lowest percentage.

percentages = pd.Series(sum(moviegenreslist, [])).value_counts()/len(movietitles) * 100
q6 = percentages[percentages >= 8]  # Series of genres and percentages
print(q6)

## 7.  It is thought that musicals have become less popular over time.  We
##     judge that assertion here as follows: Compute the median release year
##     for all movies that have genre "Musical", and then do the same for all
##     other movies.

# get all of the years as integer to perform operations
movieyears = movietitlesandyears.str[-5:-1].astype(int)

# get all rows that contain 'Musical'
q7a = movieyears[moviegenres.str.contains('Musical')].median()  # median release year for Musical

# https://blog.finxter.com/tilde-python-pandas-dataframe/ get all rows that do not contain 'Musical'
q7b = movieyears[~moviegenres.str.contains('Musical')].median()  # median release year for non-Musical

print(q7a)
print(q7b)

##  8. Determine how many movies came from each decade in the data set.
##     An example of a decade: The years 1980-1989, which we would label as
##     1980.  (Use this convention for all decades in the data set.)
##     Give your answer as a Series with decade as index and counts as values,
##     sorted by decade 2000, 1990, 1980, ....


# get the decades by getting the remainder of the year when divided by 10
# https://towardsdatascience.com/how-to-group-yearly-data-by-periods-5199a1dba5db
decades = (movieyears - movieyears % 10)

q8 = decades.value_counts().sort_index(ascending=False)  # Series of decades and counts

print(q8)

##  9. For each decade in the data set, determine the percentage of titles
##     that have exactly one word.  (Note: "Jaws" is one word, "Jaws 2" is not)
##     Give your answer as a Series with decade as index and percentages as values,
##     sorted by decade 2000, 1990, 1980, ....

# get decades, get titles with only one word, get unique values and sort
q9 = decades[movietitles.str.split().str.len() == 1].value_counts().sort_index(ascending=False)  # Series of percentage 1-word titles by decade

print(q9)

## 10. For each genre, determine the percentage of movies classified in
##     that genre also classified in at least one other genre.  Give your
##     answer as a Series with genre as index and percentages as values,
##     sorted largest to smallest percentage.

# group into genres -> moviegenreslist from earlier
# find movies in each genre that have more than 1 genre listed
# divide by total movies in that genre
allgenres = moviegenreslist.explode().value_counts()
q10 = (((allgenres - onegenre) / allgenres) * 100).sort_values(ascending=False)
print(q10)
