##
## File: assignment10.py (STAT 3250)
## Topic: Assignment 10
##

##  For this assignment you will be working with Twitter data related
##  to the season opening of Game of Thrones on April 14, 2019.  You will use
##  a set of over 10,000 tweets for this purpose.  The data is in the file
##  'GoTtweets.txt'.

##  Note: On this assignment it makes sense to use loops to extract
##  information from the tweets. Go wild.

##  The Gradescope autograder will be evaluating your code on a reduced
##  version of the GoTtweets.txt data that includes only a fraction of the
##  records.  Your code needs to automatically handle all assignments
##  to the variables q1, q2, ... to accommodate the reduced data set,
##  so do not copy/paste things from the console window, and take care
##  with hard-coding values.

import json
import numpy as np
import pandas as pd
import re
# read in the tweets
tweet_list = []
#for line in open('/Users/nolan/Desktop/classes/stat3250/data/GoTtweets.txt', 'r'):  # Open the file of tweets
for line in open('GoTtweets.txt', 'r'):  # Open the file of tweets
    tweet_list.append(json.loads(line))  # Add to 'tweetlist' after converting

# print(tweetlist[0])

## 1.  The tweets were downloaded in several groups at about the same time.
##     Are there any that appear in the file more than once?  Give a Series
##     with the tweet ID for any repeated tweets as the index and the number
##     of times each ID appears in the file as values.  Sort by the index from
##     smallest to largest.

# empty array to hold tweet id numbers
tweet_ids = []

# loop through the tweets and add id of each tweet to the list
for x in range(len(tweet_list)):
    tweet_ids.append(tweet_list[x]['id'])

repeated_tweets = pd.Series(tweet_ids).value_counts()[
    pd.Series(tweet_ids).value_counts() > 1]
# count apperances of each tweet id in the array and make series of tweets that appear more than once
q1 = repeated_tweets.sort_index(ascending=True)  # Series of tweet IDs that appear > 1 time
print(q1)

## Note: For the remaining questions in this assignment, do not worry about
##       any duplicate tweets.  Just answer the questions based on the
##       existing data set.


## 2.  Determine the number of tweets that include 'Daenerys' (any combination
##     of upper and lower case; part of another work OK) in the text of the
##     tweet.  Then do the same for 'Snow'.

# Daenerys

# count of daenerys tweets
count_daenerys = 0

# turn all tweets lowercase and add to array
lowercase_tweets = []
for x in range(len(tweet_list)):
    lowercase_tweets.append(tweet_list[x]['text'].lower())

# loop through tweets and find all that contain Daenerys
for x in range(len(lowercase_tweets)):
    # if current tweet contains daenerys add 1 to count
    if 'daenerys' in lowercase_tweets[x]:
        count_daenerys += 1

# Snow

# count of snow tweets
count_snow = 0
# loop through tweets and find all that contain Daenerys
for x in range(len(lowercase_tweets)):
    # if current tweet contains snow add 1 to count
    if 'snow' in lowercase_tweets[x]:
        count_snow += 1

q2a = count_daenerys  # number of tweets including 'daenerys'
q2b = count_snow  # number of tweets including 'snow'

print(q2a)
print(q2b)

## 3.  Find the average number of hashtags included in the tweets. (You may get
##     the wrong answer if you use the text of the tweets instead of the
##     hashtag lists.)

# hold hash tags per tweet
hashtags_per_tweet = []

# loop through the tweets and count number of hashtags in the tweet, then add number to array
for tweet in tweet_list:
    hashtagsCount = len(tweet['entities']['hashtags'])
    hashtags_per_tweet.append(hashtagsCount)

# take mean of the array
q3 = np.mean(hashtags_per_tweet)  # average number of hashtags per tweet

print(q3)

## 4.  Determine the tweets that have 0 hashtags, 1 hashtag, 2 hashtags,
##     and so on.  Give your answer as a Series with the number of hashtags
##     as index (sorted smallest to largest) and the corresponding number of
##     tweets as values. Include in your Series index only number of hashtags
##     that occur for at least one tweet. (Note: See warning in #3)

# empty array to hold the total hashtags per tweet
hashtag_totals = []

# loop through each tweet and add total number of hashtags to array
for x in range(len(tweet_list)):  # for loop
    hashtag_totals.append(tweet_list[x]['entities']['hashtags'])

# empty array to hold total occurrences of each hashtag total
values_per_hashtag_total = []

# loop through the total hashtags in each tweet and add count to empty array
for x in range(len(hashtag_totals)):
    values_per_hashtag_total.append(len(hashtag_totals[x]))

# create series with the total occurrences of each total hashtag value
    total_counts = pd.Series(values_per_hashtag_total).value_counts().reset_index()

# change column names to access via groupby and sort values small to large
total_counts.columns = ['tag count', 'total tweets']
total_counts = total_counts.sort_index()
# create series with total hashtags as index and number of tweets with this occurrence as value
final_counts = pd.Series(total_counts['total tweets'], index=total_counts['tag count'])

q4 = final_counts.sort_index()  # Series of number of hashtags and counts

print(q4)

## 5.  Determine the number of tweets that include the hashtag '#GoT', then
##     repeat for '#GameofThrones'.  (You may get the wrong answer if you
##     use the text of the tweets instead of the hashtag lists.)
##     Note: Hashtags are not case sensitive, so any of '#GOT', '#got', 'GOt'
##     etc are all considered matches.

# GoT

# count of hashtags containing GoT
count_GoT = 0

# loop through each tweet
for tweet in tweet_list:
    # find the hashtags in each tweet
    tag_text = tweet['entities']['hashtags']
    # loop through each tag and lower since hashtags are not case sensitive
    for i in tag_text:
        # if the text in the hashtag contains got add 1 to count
        if i['text'].lower() == 'got':
            count_GoT += 1

# GameofThrones

# count of hashtags containing GameofThrones
count_GameofThrones = 0

# loop through each tweet
for tweet in tweet_list:
    # find the hashtags in each tweet
    tag_text = tweet['entities']['hashtags']
    # loop through each tag and lower since hashtags are not case sensitive
    for i in tag_text:
        # if the text in the hashtag contains got add 1 to count
        if i['text'].lower() == 'gameofthrones':
            count_GameofThrones += 1

q5a = count_GoT  # number of tweets with '#GoT' hashtag and upper/lower variants
q5b = count_GameofThrones  # number of tweets with '#GameofThrones' hashtags and upper/lower variants

print(q5a)
print(q5b)

## 6.  Some tweeters like to tweet a lot.  Find the screen name for all
##     tweeters with at least 3 tweets in this data.  Give a Series with
##     the screen name (in lower case) as index and the number of tweets as
##     value, sorting by the index in alphbetical order.

# empty array to hold screen names
screen_names = []

# loop through tweets and add the screen name of each tweet to the array
for i in range(len(tweet_list)):
    screen_names.append(tweet_list[i]['user']['screen_name'])

# create series of users who appear more than three times and their counts
active_tweeters = pd.Series(screen_names).value_counts()[pd.Series(screen_names).value_counts() >= 3]

# sort alphabetically
q6 = active_tweeters.sort_index(ascending=True)  # Series of screen name and counts

print(q6)

## 7.  Among the screen names with 3 or more tweets, find the average
##     'followers_count' for each and then give a table with the screen
##     and average number of followers.  (Note that the number of
##     followers might change from tweet to tweet.)  Give a Series with
##     screen name (in lower case) as index and the average number of followers
##     as value, sorting by the index in alphbetical order.

follower_count = []  # hold for 'followers_count'

# loop through each tweet and add the number of followers to empty array
for i in range(len(tweet_list)):
    follower_count.append(tweet_list[i]['user']['followers_count'])

# create new data frame with the screen name and number of followers
name_followers = pd.DataFrame({'Screen Name': screen_names, 'Follower Count': follower_count})

# make series of screen names that have three or more tweets
active_name_followers = name_followers['Screen Name'].value_counts()[name_followers['Screen Name'].value_counts() >= 3]

# make series of screen name as index and average number of followers for screen names with >= 3 tweets
average_followers = name_followers[name_followers['Screen Name'].isin(active_name_followers.index)].groupby(
    'Screen Name').mean()

# sort the series alphabetically
average_follower_totals = average_followers.sort_index()

# convert to series
q7 = average_follower_totals.squeeze()  # Series of screen names and mean follower counts
print(q7)


## 8.  Determine the hashtags that appeared in at least 50 tweets.  Give
##     a Series with the hashtags (lower case) as index and the corresponding
##     number of tweets as values, sorted alphabetically by hashtag.

# empty array to hold hashtags
hashtags = []

# loop through each tweet and add the hashtag to array
for tweet in tweet_list:
    # find the hashtags in each tweet
    tag_text = tweet['entities']['hashtags']
    # add text to hashtag array, lower since hashtags are not case sensitive
    for i in tag_text:
        hashtags.append(i['text'].lower())

# get total appearances of each hashtag
tag_counts = pd.Series(hashtags).value_counts()

# get tags that appear over 50 times
pop_tags = tag_counts[tag_counts > 50]

# sort alphabetically
q8 = pop_tags.sort_index(ascending=True)  # Series of hashtags and counts

print(q8)

##  9.  Some of the tweets include the location of the tweeter.  Give a Series
##      of the names of countries with at least three tweets, with country
##      name as index and corresponding tweet count as values.  Sort the
##      Series alphabetically by country name.

# empty array to hold countries
countries = []

# loop through each tweet and add the hashtag to array
for tweet in tweet_list:
    # find the hashtags in each tweet
    if tweet['place'] is not None:
        country = tweet['place']
    else:
        country = ''
    # add country to array
    for i in country:
        if country['country'] is not None:
            countries.append(country['country'])


# get total appearances of each country
country_counts = pd.Series(countries).value_counts()

# get countries greater than 3
country_counts_greater = country_counts[country_counts >= 3]

q9 = country_counts.sort_index(ascending=True)  # Series of countries with at least three tweets
print(q9)

## Questions 10-11: The remaining questions should be done using regular
##                  expressions as described in the class lectures.

## 10.  Determine the percentage of tweets (if any) with a sequence of 3 or more
##      consecutive digits.  (No spaces between the digits!)  For such tweets,
##      apply 'split()' to create a list of substrings.  Among all the
##      substrings with a sequence of at least three consecutive digits,
##      determine the percentage where the substring starts with a '@' at the
##      beginning of the substring.

# find percentage of tweets with three consecutive digits

# empty array to hold tweets that have consecutive digits
tweets_with_digits = []

# loop through each tweet, if the text contains a sequence add 1 to the count
for tweet in tweet_list:
    # find the text in each tweet
    tweet_text = tweet['text']
    # if the tweet contains sequence of three numbers add 1 to count
    if re.search(r"\d{3,}", tweet_text):
        tweets_with_digits.append(tweet_text)

q10a = (len(tweets_with_digits) / len(tweet_list)) * 100  # percentage of tweets with three consecutive digits

# find percentage of tweet that start with @

# we already have a list of substrings that have consecutive digits so we just need count

# count to hold strings that start with '@'
substring_count = 0

# loop through tweets with consecutive digits
for i in tweets_with_digits:
    # if the digits start with an @ add to count
    if re.search(r"@\d{3,}", i):
        substring_count += 1

q10b = (substring_count / len(tweets_with_digits)) * 100  # percentage starting with @ among substrings with 3 consec digits

print(q10a)
print(q10b)

## 11.  Determine if there are any cases of a tweet with a 'hashtag' that is
##      actually not a hashtag because there is a character (letter or digit)
##      immediately before the "#".  An example would be 'nota#hashtag'.
##      Count the number of tweets with such an incorrect 'hashtag'.

# count to hold total improper tags
improper_tags = 0

# loop through each tweet
for tweet in tweet_list:
    # find the text in each tweet
    tag_text = tweet['text']
    # if an improper tag exists add 1 to count
    if re.search(r"[a-zA-Z0-9]#", tag_text):
        improper_tags += 1

q11 = improper_tags  # count of tweets with bad hashtag
print(q11)

