##
## File: assignment04.py (STAT 3250)
## Topic: Assignment 4
##

##  This assignment requires the data file 'airline_tweets.csv'.  This file
##  contains records of over 14000 tweets and associated information related
##  to a number of airlines.  You should be able to read this file in using
##  the usual pandas methods.

##  Gradescope will review your code using a version of airline_tweets.csv
##  that has had about 50% of the records removed.  You will need to write
##  your code in such a way that your file will automatically produce the
##  correct answers on the new set of data.

import pandas as pd  # load pandas as pd
import numpy as np  # load numpy as np

#air = pd.read_csv('/Users/nolan/Desktop/classes/stat3250/airline_tweets.csv')  # Read in the data set
air = pd.read_csv('airline_tweets.csv')  # Read in the data set
temp = air.loc[0:10, :]
## Questions 1-8: These questions should be done without the use of loops.

## 1.  Determine the number of tweets for each airline, indicated by the
##      name in the 'airline' column of the data set.  Give the airline
##      name and corresponding number of tweets as a Series with airline
##      name as the index, sorted by tweet count from most to least.
q1 = air.groupby('airline')['tweet_created'].count().sort_values(
    ascending=False)  # Series of airlines and number of tweets
## 2.  For each airline's tweets, determine the percentage that are positive,
##      based on the classification in 'airline_sentiment'.  Give the airline
##      name and corresponding percentage as a Series with airline
##      name as the index, sorted by percentage from largest to smallest

# https://pandas.pydata.org/docs/reference/api/pandas.core.groupby.GroupBy.apply.html

# group by airline and apply the function to find positive tweet percentage to each specific airline
q2 = air.groupby('airline').apply(lambda x: len(x.loc[(x['airline_sentiment'] == 'positive')]) / len(x['airline_sentiment'])).sort_values(ascending=False)

## 3.  Find all user names (in the 'name' column) with at least 25 tweets
##      along with the number of tweets for each.  Give the user names and
##      corresponding counts as a Series with user name as index, sorted
##      by count from largest to smallest

# find all users with more than 25 tweets
over25 = air.groupby('name').filter(lambda x: x['tweet_created'].count() >= 25)
# group the over 25 tweet users and return their # of tweets in a descending list
q3 = over25.groupby('name')['tweet_created'].count().sort_values(ascending=False)

## 4.  Determine the percentage of tweets from users who have more than five
##      tweets in this data set. (Note that this is not the same as the
##      percentage of users with more than five tweets.)

# find users with more than 5 tweets
over5 = air.groupby('name').filter(lambda x: x['tweet_created'].count() > 5)
# total number of tweets from users with > 5
totalover5 = len(over5['tweet_created'])
# total number of tweets in the data set
totaltweets = len(air['tweet_created'])
q4 = (totalover5 / totaltweets) * 100  # Percentage of tweets from users with more than 5 tweets

## 5.  Among the negative tweets, determine the four reasons are the most common.
##      Give the percentage among all negative tweets for each as a Series
##      with reason as index, sorted by percentage from most to least

# filter to negative tweets
negatives = air[air['airline_sentiment'] == 'negative']
#nice = negatives['negativereason'].value_counts()  # Series of reasons and percentages

# get occurrences for each negative reason / total reasons, mult by 100 to get %, return top 4
q5 = ((negatives['negativereason'].value_counts()/negatives['negativereason'].count())*100).iloc[:4]

## 6.  How many tweets include a link to a web site? (Indicated by the
##      presence of "http" anywhere in the tweet.)

q6 = len(air[air['text'].str.contains('http')])  # Number of tweets that include a link

## 7.  How many tweets include the word "air" (upper or lower case,
##      not part of another word)?

# convert all strings to lowercase, count # of strings that include air not part of other word
q7 = air['text'].str.lower().str.contains(' air ').sum()

## 8.  How many times total does the word "help" appear in a tweet, either in
##      upper or lower case and not part of another word.

# convert all strings to lowercase, count number of occurences of help in all strings not part of another word

q8 = air['text'].str.lower().str.count(' help ').sum()  # Number of times that 'help' is included

## Questions 9-13: Some of these questions can be done without the use of
##  loops, while others cannot.  It is preferable to minimize the use of
##  loops where possible, so grading will reflect this.
##
##  Some of these questions involve hashtags and @'s.  These are special
##  Twitter objects subject to special rules.  For these problems we assume
##  that a "legal" hashtag:
##
##  (a) Starts with the "#" (pound) symbol, followed by letter and/or numbers
##       until either a space or punctuation mark (other than "#") is encountered.
##
##      Example: "#It'sTheBest" produces the hashtag "#It"
##
##  (b) The "#" symbol can be immediately preceded by punctuation, which is
##       ignored. If "#" is immediately preceded by a letter or number then
##       it is not a hashtag.
##
##      Examples: "The,#dog,is brown"  produces the hashtag "#dog"
##                "The#dog,is brown" does not produce a hashtag
##                "#dog1,#dog2" produces hashtags "#dog1" and "#dog2"
##                "#dog1#dog2" produces the hashtag "#dog1#dog2"
##
##  (c) Hashtags do not care about case, so "#DOG" is the same as "#dog"
##       which is the same as "#Dog".
##
##  (d) The symbol "#" by itself is not a hashtag
##
##  The same rules apply to Twitter handles (user names) that begin with the
##   "@" symbol.

## 9.  How many of the tweets have at least two Twitter handles?

# find tweets with handles
ats = air['text'].str.lower().str.replace(r'[^\w\s@]+', ' ')
# total the number of tweets that contain at least 2 handles
q9 = np.count_nonzero(np.where(ats.str.count(' @') - ats.str.count(' @ ') >= 2))
print(q9)
## 10. Suppose that a score of 3 is assigned to each positive tweet, 1 to
##      each neutral tweet, and -2 to each negative tweet.  Determine the
##      mean score for each airline and give the results as a Series with
##      airline name as the index, sorted by mean score from highest to lowest.

# make copy of air
air2 = air
# make sure / change airline sentiment column has string values
air2['airline_sentiment'] = air2['airline_sentiment'].astype(str)
# replace the strings with numerical equivalents
air2['airline_sentiment'].replace({'positive': 3, 'neutral': 1, 'negative': -2}, inplace=True)
# group by airline, find sum of the sentiments and divide by length for each
q10 = air2.groupby('airline').apply(lambda x: x['airline_sentiment'].sum() / len(x['airline_sentiment'])).sort_values(ascending=False)  # Series of airlines and mean scores

## 11. What is the total number of hashtags in tweets associated with each
##      airline?  Give a Series with the airline name as index and the
##      corresponding totals for each, sorted from most to least.

# make copy of air
air3 = air
# find all the tags
tweets = (" " + air3['text'].str.lower() + " ").str.replace(r'[^\w\s#]+', ' ')
# total hashtags
hashtags = tweets.str.count(' #') - tweets.str.count(' # ')
# add column of total tags
air3['ht_count'] = hashtags
# group by airline and get totals for each
q11 = air3.groupby('airline')['ht_count'].sum().sort_values(ascending=False)

## 12. Among the tweets that "@" a user besides the indicated airline,
##      find the percentage that include an "@" directed at the other
##      airlines in this file.

# make copy of df
ats2 = air
# make lowercase and add spaces
ats2 = (" " + ats2['text'].str.lower() + " ").str.replace(r'[^\w\s@]+', ' ')
# sum of tweets with more than one legal handle
atsCount = np.sum((ats2.str.count(' @') - ats2.str.count(' @ ')) > 1)
# make series of airline handles to check against
handles = pd.Series(['@virginamerica', '@united', '@southwestair',
                     '@jetblue', '@usairways', '@americanair'])
# make a count for each tweet to store
# using np.nonzero produced index error so using np.zeros here
# via https://numpy.org/doc/stable/reference/generated/numpy.nonzero.html
count = np.zeros(len(air))
# loop through each airline and check if the tweet contains any of the handles in the series
for i in handles:
    # mult by 1 to make contains return 1/0
    tweet = 1 * ats2.str.contains(" " + i + " ")
    # add 1/0 to the count
    count += tweet
# take the sum of tweets containing another @ over the total tweets containing > 1 @
q12 = np.sum(count > 1)/atsCount * 100  # Percentage of tweets

## 13. Suppose the same user has two or more tweets in a row, based on how they
##      appear in the file. For such tweet sequences, determine the percentage
##      for which the most recent tweet (which comes nearest the top of the
##      file) is a positive tweet.

# reread air
air = pd.read_csv('airline_tweets.csv')  # Read in the data set

# count for holding number of consecutive tweets & count for positive tweets
seqCount = 0
positives = 0

# check the first two entries and if there is a consecutive tweet add 1 to count
if air.loc[0, 'name'] == air.loc[1, 'name']:
    seqCount += 1
    # if there is a positive sentiment in the sequence add 1 to count
    if air.loc[0, 'airline_sentiment'] == 'positive':
        positives += 1
# go through the rest of the entries
for i in range(1, len(air)-1):
    # if current / next index match and previous / current index match add 1 to sequence
    if (air.loc[i, 'name'] == air.loc[i+1, 'name']) & (air.loc[i-1, 'name'] != air.loc[i, 'name']):
        seqCount += 1
        # if there is a positive sentiment in the sequence add 1 to count
        if air.loc[i, 'airline_sentiment'] == 'positive':
            positives += 1
q13 = (positives / seqCount) * 100  # Percentage of tweets
