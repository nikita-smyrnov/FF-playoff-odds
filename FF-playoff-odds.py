# model assumes that average points scored per game and standard deviation do not change across the course of the season
# 100k simulations takes approximately 10 minutes
import pandas as pd
import numpy as np
import scipy.stats as stats
from scipy.stats import norm
import random

SIMULATIONS = 10000
TEAMS = 10
PLAYOFF_TEAMS = 6

data = pd.read_csv("gamedata.csv");
data = data.values

teamMeans = np.empty(TEAMS)
teamStds = np.empty(TEAMS)
teamExpectedMeans = np.empty(TEAMS)

for i in range(TEAMS):
    teamMeans[i] = data[i][5:len(data[i])].mean()
    teamStds[i] = data[i][5:len(data[i])].std()

teamMatchups = [[ [0, 7], [9, 6], [1, 4], [2, 5], [3, 8] ],
                [ [0, 6], [9, 5], [1, 8], [2, 4], [3, 7] ],
                [ [0, 3], [8, 2], [9, 4], [1, 7], [5, 6] ],
                [ [0, 1], [9, 2], [3, 5], [4, 6], [7, 8] ],
                [ [0, 8], [9, 7], [2, 6], [4, 5], [1, 3] ]]
playoffs = np.zeros(TEAMS)
firstRoundBye = np.zeros(TEAMS)
results = np.zeros(TEAMS)

start = datetime.datetime.now().replace(microsecond=0)

for sims in range(SIMULATIONS):
    numberOfWins = [5, 6, 0, 4, 5.5, 5, 6, 1.5, 3, 4]
    
    for i in range(len(teamMatchups)):
        for j in range(TEAMS):
            teamExpectedMeans[j] = norm.ppf(random.random(), loc = teamMeans[j], scale = teamStds[j])
            
        for j in range(int(TEAMS/2)):
            teamOne = teamMatchups[i][j][0]
            teamTwo = teamMatchups[i][j][1]
            if teamExpectedMeans[teamOne] > teamExpectedMeans[teamTwo]:
                numberOfWins[teamOne] += 1
            elif teamExpectedMeans[teamOne] < teamExpectedMeans[teamTwo]:
                numberOfWins[teamTwo] += 1
            else:
                numberOfWins[teamOne] += 0.5
                numberOfWins[teamTwo] += 0.5
    
    for i in range(TEAMS):
        results[i] += numberOfWins[i]
    
    for i in range(PLAYOFF_TEAMS):
        if i == 0:
            maxVal = max(numberOfWins[0:int(TEAMS/2)])
            maxIndex = handleTies(numberOfWins, teamExpectedMeans, maxVal, i)
            playoffs[maxIndex] += 1
            firstRoundBye[maxIndex] += 1
            numberOfWins[maxIndex] = -1
        elif i == 1:
            maxVal = max(numberOfWins[int(TEAMS/2):TEAMS])
            maxIndex = handleTies(numberOfWins, teamExpectedMeans, maxVal, i)
            playoffs[maxIndex] += 1
            firstRoundBye[maxIndex] += 1
            numberOfWins[maxIndex] = -1
        else:
            maxVal = max(numberOfWins)
            maxIndex = handleTies(numberOfWins, teamExpectedMeans, maxVal, i)
            playoffs[maxIndex] += 1
            numberOfWins[maxIndex] = -1

for i in range(TEAMS):
    results[i] /= SIMULATIONS
    playoffs[i] /= int(SIMULATIONS/TEAMS/10)
    firstRoundBye[i] /= int(SIMULATIONS/TEAMS/10)
    print(data[i][0] + "'s projected wins: " + str(results[i]) + 
          ", projected playoff odds: " + str(playoffs[i]) + 
          ", projected odds of getting a first-round bye: " + str(firstRoundBye[i]))
