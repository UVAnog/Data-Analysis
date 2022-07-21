##
## File: assignment02.py (STAT 3250)
## Topic: Assignment 2
##

## Two *very* important rules that must be followed in order for your
## assignment to be graded correctly:
##
## a) The file name must be exactly "assignment02.py" (without the quotes)
## b) The variable names followed by "= None" must not be changed and these
##    names variable names should not be used anywhere else in your file.  Do
##    not delete these variables, if you don't know how to find a value just
##    leave it as is. (If a variable is missing the autograder will not grade
##    any of your assignment.)


## Questions 1-7: For the questions in this part, use the following
##  lists as needed:

list01 = [5, -9, -1, 8, 0, -1, -2, -7, -1, 0, -1, 6, 7, -2, -1, -5]
list02 = [-2, -5, -2, 8, 7, -7, -11, 1, -1, 6, 6, -7, -9, 1, 5, -11]
list03 = [9, 0, -8, 3, 2, 9, 3, -4, 5, -9, -7, -3, -11, -6, -5, 1]
list04 = [-4, -6, 8, 8, -5, -5, -11, -3, -1, 7, 0, 2, -5, -2, 0, -5]
list05 = [-11, -3, 8, -9, 2, -8, -7, -12, 7, 3, 2, 0, 6, 4, -11, 6]
biglist = list01 + list02 + list03 + list04 + list05

## Questions 1-7: Use for loops to answer each of the following applied
##  to the lists defined above.

## 1.  Add up the squares of the entries of biglist.
total = 0  # to keep the total

## loop through the list:
##      square the item at current index and add to total

for item in biglist:
    total += item ** 2
q1 = total  # sum of squares of entries of biglist

## 2.  Create "newlist01", which has 14 entries, each the sum of the
##      corresponding entry from list01 added to the corresponding entry
##      from list02.  That is,
##
##         newlist01[i] = list01[i] + list02[i]
##
##      for each 0 <= i <= 13.

# https://www.freecodecamp.org/news/python-for-loop-for-i-in-range-example/
# add the items at each index through first 14 elements

newlist01 = [list01[i]+list02[i] for i in range(len(list01)-2)]
q2 = newlist01

## 3.  Determine the number of entries in biglist that are less than 6.

lessthansix = 0  # total entries less than 6

# if the item at the current index is less than 6 add to the total count
for item in biglist:
    if item < 6:
        lessthansix += 1
q3 = lessthansix  # number of entries in biglist less than 6

## 4.  Create a new list called "newlist02" that contains the elements of
##      biglist that are greater than 5, given in the same order as the
##      elements appear in biglist.

newlist02 = []  # empty list

# if the item at the current index is greater than 5 add it to the list
for item in biglist:
    if item > 5:
        newlist02.append(item)
q4 = newlist02

## 5.  Find the sum of the positive entries of biglist.

sumofpositives = 0  # sum of the positive numbers

# if the item at the current index is positive add it to the sum
for item in biglist:
    if item > 0:
        sumofpositives += item
q5 = sumofpositives # sum of the positive entries of biglist

## 6.  Make a list of the first 19 negative entries of biglist, given in
##      the order that the values appear in biglist.

negativeentries = []  # empty list to hold negative entries

# if the item at the current index is negative add it to the list
for item in biglist:
    if item < 0:
        negativeentries.append(item)
q6 = negativeentries[0:19]  # list of first 19 negative entries of biglist

##  7. Identify all elements of biglist that have a smaller element that
##      immediately preceeds it.  Make a list of these elements given in
##      the same order that the elements appear in biglist.

elements = []  # empty list to hold entries
index1 = 0  # starting index
index2 = 1  # starting index

# while index 2 is not at the end
# if the item at the current index2 is greater than index1
# add to the empty list
while index2 < len(biglist):
    if biglist[index1] < biglist[index2]:
        elements.append(biglist[index2])
    index1 += 1
    index2 += 1

q7 = elements  # list of elements preceded by smaller element

## Questions 8-9: These questions use simulation to estimate probabilities
##  and expected values.

##  8. Consider the following game: You flip a fair coin.  If it comes up
##      tails, then you win $1.  If it comes up heads, then you get to
##      simultaneously flip four more fair coins.  In this case you win $1
##      for each head that appears on all flips, plus you get an extra $7 if
##      all five flips are heads.
##
##      Use 100,000 simulations to estimate the average amount of money won
##      when playing this game.

import numpy as np
# generate 100,000 random 0 (heads) and 1 (tails)
# https://docs.scipy.org/doc/numpy-1.10.1/reference/generated/numpy.random.randint.html
totals = []
for i in range(100000):  # simulate 100,000 times
    for item in range(1):
        moneywon = 0
        x = np.random.randint(2, size=1)  # first coin flip
        if x == 1:  # if tails win $1
            moneywon += 1
        else:  # if heads flip 4 more times
            y = np.random.randint(2, size=4)  # generate 4 flips
            moneywon += 1
            for i in y:
                if i == 0:  # if heads win $1
                    moneywon += 1
            if all(i == 0 for i in y):
                moneywon += 7
    totals.append(moneywon)

q8 = np.mean(totals)  # mean winnings from 100,000 times playing the game

##  9.  Jay is taking a 15 question true/false quiz online.  The
##      quiz is configured to tell him whether he gets a question
##      correct before proceeding to the next question.  The
##      responses influence Jay's confidence level and hence his
##      exam performance.  In this problem we will use simulation
##      to estimate Jay's average score based on a simple model.
##      We make the following assumptions:
##
##      * At the start of the quiz there is a 81% chance that
##        Jay will answer the first question correctly.
##      * For all questions after the first one, if Jay got
##        the previous question correct, then there is a
##        90% chance that he will get the next question
##        correct.  (And a 10% chance he gets it wrong.)
##      * For all questions after the first one, if Jay got
##        the previous question wrong, then there is a
##        72% chance that he will get the next question
##        correct.  (And a 28% chance he gets it wrong.)
##      * Each correct answer is worth 5 points, incorrect = 0.
##
##      Use 100,000 simulated quizzes to estimate Jay's average
##      score.



scores = []

for i in range(100000):
    score = 0
    question = np.random.choice([0, 1], size=1, p=[0.19, 0.81])
    score += 5
    for j in range(14):
        if question == 1:
            question_correct = np.random.choice([0, 1], size=1, p=[0.1, 0.9])
            if question_correct == 1:
                score += 5
        else:
            question_incorrect = np.random.choice([0, 1], size=1, p=[0.28, 0.72])
            if question_incorrect == 1:
                score += 5
    scores.append(score)

q9 = np.mean(scores)  # mean score from 100,000 simulated quizzes



