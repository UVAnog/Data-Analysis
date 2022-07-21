##
## File: assignment12.py (STAT 3250)
## Topic: Assignment 12
##


##  In this assignment we revisit past NCAA men's basketball tournaments
##  (including the glorious 2019 edition) using data from the file
##
##      'ncaa.csv':  NCAA Men's Tournament Scores, 1985-2019
##
##  The organization of the file is fairly clear.  Each record has information
##  about one game, including the year, the teams, the final score, and each
##  team's tournament seed.

##  Two important points:
##    1) Each team is assigned a "seed" at the start of the tournament.  The
##       teams thought to be better are assigned smaller number seeds.  (So
##       the best teams are assigned 1 and the worst assigned 16.)  In this
##       assignment a "lower seed" refers to a worse team and hence larger
##       seed number, with the opposite meaning for "higher seed".
##    2) All questions refer only to the data in this in 'ncaa.csv' so you
##       don't need to worry about tournaments prior to 1985.

##  Note: The data set is from Data.World, with the addition of the 2019
##  tournament provided by your dedicated instructor. (There was no 2020
##  tournament and the 2021 tournament didn't turn out to your instructor's
##  liking so that data is omitted.)

##  Submission Instructions: Submit your code in Gradescope under
##  'Assignment 12 Code'.  The autograder will evaluate your answers to
##  Questions 1-8.  You will also generate a separate PDF for the graphs
##  in Questions 9-11, to be submitted in Gradescope under 'Assignment 12 Graphs'.


# read in data
import pandas as pd  # load pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('ncaa.csv')
#data = pd.read_csv('/Users/nolan/Desktop/classes/stat3250/data/ncaa.csv')
## 1.  Find all schools that have won the championship. Report your results in
##     a Series that has the schools as index and number of championships for
##     values, sorted alphabetically by school.

# print Team when the score is larger than school 1, print team.1 if it is smaller
data['Winner'] = np.where(data['Score'] > data['Score.1'], data['Team'], data['Team.1'])
# find all the wins that came from the championship game
Championships = data.loc[(data['Region Name'] == 'Championship')]
# get the total number of championship wins for each team
q1 = Championships['Winner'].value_counts()  # Series of champions and counts
print(q1)
print(type(q1))

## 2.  Determine all schools that have been in the tournament at least 25 times.
##     Report your results as a Series with schools as index and number of times
##     in the tournament as values, sorted alphabetically by school.

# find the first round of the tournament to ensure the team was a part of the 64 included
tournament_teams = data[data['Round'] == 1]

# concatenate the teams in the tournament by row
round1_teams = pd.concat([tournament_teams['Team'], tournament_teams['Team.1']], axis=0)

# get the total appearances for each team ( same as how many times they appeared in round 1 of a tournament)
total_appearances = round1_teams.value_counts().sort_index()

# find teams > 25
q2 = total_appearances[total_appearances >= 25]  # Series of schools and tournament appearance counts
print(q2)
print(type(q2))

## 3.  Find all years when the school that won the tournament was seeded
##     3 or lower. (Remember that "lower" seed means a bigger number!) Give
##     a DataFrame with years as index and corresponding school and seed
##     as columns (from left to right).  Sort by year from least to most recent.

# get the winning seed of each game
# if the score > score.1 print seed, if score.1 is higher print seed.1
data['Winning Seed'] = np.where(data['Score'] > data['Score.1'], data['Seed'], data['Seed.1'])

# subset the data to only championship games similar to problem 1
Championship_Seeds = data.loc[(data['Region Name'] == 'Championship')]

# subset champions to those whose seed is 3 or greater
Champion_Seed_3orMore = Championship_Seeds[Championship_Seeds['Winning Seed'] >= 3]

# get the years, winner, and seed
q3 = Champion_Seed_3orMore[['Winner', 'Winning Seed']].set_index(
    Champion_Seed_3orMore['Year'])  # DataFrame of years, schools, seeds

print(q3)
print(type(q3))

## 4.  Determine the average tournament seed for each school.  Make a Series
##     of all schools that have an average seed of 5.0 or higher (that is,
##     the average seed number is <= 5.0).  The Series should have schools
##     as index and average seeds as values, sorted alphabetically by
##     school

# get rows of seeds
Seeds = pd.concat([tournament_teams['Seed'], tournament_teams['Seed.1']], axis=0)

# get seeds of teams in the tournament
Tournament_Seeds = pd.concat([round1_teams, Seeds], axis=1)

# group seed with school
SeedTeam = Tournament_Seeds[1].groupby(Tournament_Seeds[0])

# get average seed, sort alphabetically
Seed_Means = SeedTeam.mean().sort_index()

q4 = Seed_Means[Seed_Means <= 5]  # Series of schools and average seed
print(q4)
print(type(q4))

## 5.  For each tournament round, determine the percentage of wins by the
##     higher seeded team. (Ignore games of teams with the same seed.)
##     Give a Series with round number as index and percentage of wins
##     by higher seed as values sorted by round in order 1, 2, ..., 6.
##     (Remember, a higher seed means a lower seed number.)

# if the seed is smaller (higher) than seed.1, add the team, if not, add team.1
data['Higher Seed'] = np.where(data['Seed'] < data['Seed.1'], data['Team'], data['Team.1'])

# if the winner is higher seed =  true, if not = false
data['Higher Seed Winner'] = np.where(data['Higher Seed'] == data['Winner'], True, False)

# group higher seed by each round
High_Seeds = data['Higher Seed Winner'].groupby(data['Round'])

q5 = High_Seeds.mean() * 100  # Series of round number and percentage higher seed wins
print(q5)
print(type(q5))

## 6.  For each seed 1, 2, 3, ..., 16, determine the average number of games
##     won per tournament by a team with that seed.  Give a Series with seed
##     number as index and average number of wins as values, sorted by seed
##     number 1, 2, 3, ..., 16. (Hint: There are 35 tournaments in the data set
##     and each tournamentstarts with 4 teams of each seed.  We are not
##     including "play-in" games which are not part of the data set.)
print("##################################")

# create new column for margin
data['Margin'] = abs(data['Score'] - data['Score.1'])

# get different years in the data and make into a list
years = data['Year'].unique()
years = years.tolist()

# empty data frame to hold win percentages
win_percentages = pd.DataFrame([])

for year in years:
    for seed in range(1, 16):
        # get the seeds for that year
        year_seed = data.loc[(data['Year'] == year) & ((data['Seed'] == seed) | (data['Seed.1'] == seed))]
        # get the wins
        year_seed_score = year_seed.loc[((year_seed['Seed'] == seed) & (year_seed['Margin'] > 0)) |
                                   ((year_seed['Seed.1'] == seed) & (year_seed['Margin'] < 0))]
        # append to empty df
        win_percentages = win_percentages.append(pd.DataFrame({seed:year_seed_score.shape[0]/4}, index=[seed]),
                                                 ignore_index=True)

# drop all nulls
win_percentages = win_percentages.apply(lambda x: pd.Series(x.dropna().values))
# permutate frame to work with
win_percentages = win_percentages.transpose()
# get average wins
win_percentages = win_percentages.mean(axis=1)
q6 = win_percentages  # Series of seed and average number of wins
print(q6)
print(type(q6))
print("##################################")
## 7.  For each year's champion, determine their average margin of victory
##     across all of their games in that year's tournament. Find the champions
##     that have an average margin of victory of at least 15. Give a DataFrame
##     with year as index and champion and average margin of victory as columns
##     (from left to right), sorted by from highest to lowest average victory
##     margin.

# subset the data frame to get team / margin / year
team_margins = data[['Team', 'Margin', 'Year']]

# subset the data frame to get team.1 / margin / year
team_1_margins = data[['Team.1', 'Margin', 'Year']]

# rename team column for merge
team_1_margins.rename({1: 'Team'}, axis='index')

# merge columns together to get total margins
total_team_margins = pd.concat([team_margins, team_1_margins], ignore_index=True)

# group margin with team/year, find mean
total_margins = total_team_margins['Margin'].groupby([total_team_margins['Team'], total_team_margins['Year']]).mean()

# reset index
total_margins = total_margins.reset_index()

# subset championship winner and year
championship_margins = Championships[['Winner', 'Year']]

# merge total margins for each game and the championship games
total_championship_margins = pd.merge(total_margins, championship_margins, how='left')

# find the winner in average margin
winning_margins = total_championship_margins.loc[(
        total_championship_margins['Winner'] == total_championship_margins['Team'])]

# sort by margin, reset index
sorted_margins = winning_margins.sort_values(by='Margin')
sorted_margins = sorted_margins.reset_index()

# top 10 average margin of victory in all games played by that team.
tops = sorted_margins[['Winner', 'Margin']].set_index(sorted_margins['Year'])

q7 = tops  # DataFrame of years, schools, average margin of victory
print(q7)
print(type(q7))

## 8.  Determine the 2019 champion.  Use code to extract the correct school,
##     not your knowledge of college backetball history.
champ =  Championships[['Winner', 'Year']].loc[(Championships['Year'] == 2019)]
q8 = str(champ['Winner'])# 2019 champion!
print(q8)

##  Questions 9-11: These require the creation of several graphs. In addition to
##  the code in your Python file, you will also upload a PDF document (not Word!)
##  containing your graphs (be sure they are labeled clearly).  Include the
##  required code in this file and put your graphs in a PDF document for separate
##  submission.  All graphs should have an appropriate title and labels for
##  the axes.  For these questions the only output required are the graphs.
##  When your PDF is ready submit it under 'Assignment 12 Graphs' in Gradescope.

# imports for plots

## 9.  For each year of the tournament, determine the average margin of
##     victory for each round.  Then make a histogram of these averages,
##     using 16 bins and a range of [0,32].
import matplotlib.pyplot as plt

# group data by year
x = data.groupby(['Year'])

# empty list to hold values for df
years = []

# loop through the groups
# https://stackoverflow.com/questions/14734533/how-to-access-pandas-groupby-dataframe-by-key
for k, gp in x:
    # append value for year, round, and margin
    years.append(gp[['Year', 'Round', 'Margin']])

# concat the list to make new df
appended_data = pd.concat(years)

# group by round and get average
# group the result by year and round and get the average margin for each
# https://jamesrledoux.com/code/group-by-aggregate-pandas
data_means = appended_data.groupby(['Year', 'Round']).agg({'Margin': ['mean']})

# making the plot
plt.hist(data_means, bins=16, range=(0,32))
plt.title("average margin of victory for each round")
plt.xlabel("average margin of victory")
plt.ylabel("frequency")
plt.show()
## 10. Produce side-by-side box-and-whisker plots, one using the Round 1
##     margin of victory for games where the higher seed wins, and one
##     using the Round 1 margin of victory for games where the lower
##     seed wins.  (Remember that higher seed = lower seed number.)
##     Orient the boxes vertically with the higher seed win data on the
##     left.

# get all the round 1 data
round_one = data.loc[(data['Round'] == 1)]

# get higher seed wins
round_one_high = round_one.loc[(round_one['Higher Seed Winner']) == True]

# get lower seed wins
round_one_low = round_one.loc[(round_one['Higher Seed Winner']) == False]

# higher seed margins
round_one_high_margins = round_one_high['Margin']

# lower seed margins
round_one_low_margins = round_one_low['Margin']
print("#########################")

# plots
boxplot_data = [round_one_high_margins, round_one_low_margins]
plt.boxplot(boxplot_data)
plt.title("round 1 margins of victory")
plt.xlabel("higher seed wins (left) vs. lower seed wins (right)")
plt.ylabel("margin of victory")
plt.show()
## 11. Produce a bar chart for the number of Round 2 victories by seed.
##     The bars should proceed left to right by seed number 1, 2, 3, ...

# get round 2 data
round_two = data.loc[(data['Round'] == 2)]

# get victories by seed
round_two_seed_wins = round_two['Winning Seed'].value_counts().sort_index()

print(type(round_two_seed_wins))
print(round_two_seed_wins)
# plot
round_two_seed_wins.plot(kind="bar")
plt.title("round 2 victories by seed")
plt.xlabel("seed of team")
plt.ylabel("total victories")
plt.show()
