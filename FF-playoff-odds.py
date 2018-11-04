# model assumes that average points scored per game and standard deviation do not change across the course of the season
# 100k simulations takes around 8-10 minutes
import pandas as pd
import numpy as np
import scipy.stats as stats
from scipy.stats import norm
import random

SIMULATIONS = int(input("How many simulations would you like to run: "))
PLAYOFF_TEAMS = int(input("How many playoff spots are there: "))

def handleTies(wins, means, maxVal, division):
    ties = []
    if division == 0:
        for i in range(int(TEAMS/2)):
            if wins[i] == maxVal:
                ties.append(i)
    elif division == 1:
         for i in range(int(TEAMS/2), TEAMS):
            if wins[i] == maxVal:
                ties.append(i)
    else:
        for i in range(TEAMS):
            if wins[i] == maxVal:
                ties.append(i)
    
    maxMean = -1
    maxIndex = ties[0]
    for i in ties:
        if maxMean < means[i]:
            maxMean = means[i]
            maxIndex = i
        
    return maxIndex

data = pd.read_csv("gamedata.csv");
data = data.values
TEAMS = len(data)

teamMeans = np.empty(TEAMS)
teamStds = np.empty(TEAMS)
teamExpectedMeans = np.empty(TEAMS)

for i in range(TEAMS):
    teamMeans[i] = data[i][5:len(data[i])].mean()
    teamStds[i] = data[i][5:len(data[i])].std()

teamMatchups = pd.read_csv("matchups.csv")
teamMatchups = teamMatchups.values
teamMatchups = teamMatchups.transpose()

for i in range(len(teamMatchups)):
    for j in range(TEAMS):
        teamMatchups[i][j] = data[:,0].tolist().index(teamMatchups[i][j]);

numberOfWins = np.zeros(TEAMS)
playoffs = np.zeros(TEAMS)
firstRoundBye = np.zeros(TEAMS)
results = np.zeros(TEAMS)

for sims in range(SIMULATIONS):
    for i in range(TEAMS):
        numberOfWins[i] = data[i][1] + 0.5*data[i][3]
    
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
    playoffs[i] /= int(SIMULATIONS/100)
    firstRoundBye[i] /= int(SIMULATIONS/100)
    print(data[i][0] + "'s projected wins: " + str(results[i]) + 
          ", projected playoff odds: " + str(playoffs[i]) + 
          ", projected odds of getting a first-round bye: " + str(firstRoundBye[i]))

input("Press enter to exit. ")