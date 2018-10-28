# model assumes that average points scored per game and standard deviation do not change across the course of the season
# 10k simulations takes 1 minute

import pandas as pd
import numpy as np
import scipy.stats as stats
from scipy.stats import norm
import random

data = pd.read_csv("gamedata.csv");
data = data.values

teamMeans = np.empty(10)
teamStds = np.empty(10)
teamExpectedMeans = np.empty(10)

for i in range(10):
    teamMeans[i] = data[i][5:13].mean()
    teamStds[i] = data[i][5:13].std()

teamMatchups = [[ [1, 9], [6, 8], [0, 4], [5, 7], [2, 3] ],
                [ [0, 7], [9, 6], [1, 4], [2, 5], [3, 8] ],
                [ [0, 6], [9, 5], [1, 8], [2, 4], [3, 7] ],
                [ [0, 3], [8, 2], [9, 4], [1, 7], [5, 6] ],
                [ [0, 1], [9, 2], [3, 5], [4, 6], [7, 8] ],
                [ [0, 8], [9, 7], [2, 6], [4, 5], [1, 3] ]]
playoffs = np.zeros(10)
results = np.zeros(10)

for sims in range(100000):
    numberOfWins = [5, 5, 0, 3, 4.5, 4, 5, 1.5, 3, 4]
    
    for i in range(6):
        for j in range(10):
            teamExpectedMeans[j] = norm.ppf(random.random(), loc = teamMeans[j], scale = teamStds[j])
            
        for j in range(5):
            teamOne = teamMatchups[i][j][0]
            teamTwo = teamMatchups[i][j][1]
            if teamExpectedMeans[teamOne] > teamExpectedMeans[teamTwo]:
                numberOfWins[teamOne] += 1
            elif teamExpectedMeans[teamOne] < teamExpectedMeans[teamTwo]:
                numberOfWins[teamTwo] += 1
            else:
                numberOfWins[teamOne] += 0.5
                numberOfWins[teamTwo] += 0.5
    
    for i in range(10):
        results[i] += numberOfWins[i]
    
    for i in range(6):
        if i == 0:
            maxVal = max(numberOfWins[0:5])
            maxIndex = numberOfWins.index(maxVal)
            playoffs[maxIndex] += 1
            numberOfWins[maxIndex] = -1
        elif i == 1:
            maxVal = max(numberOfWins[5:10])
            maxIndex = numberOfWins.index(maxVal)
            playoffs[maxIndex] += 1
            numberOfWins[maxIndex] = -1
        else:
            maxVal = max(numberOfWins)
            maxIndex = numberOfWins.index(maxVal)
            playoffs[maxIndex] += 1
            numberOfWins[maxIndex] = -1

for i in range (10):
    results[i] /= 100000
    playoffs[i] /= 1000
    print(data[i][0] + "'s projected wins: " + str(results[i]) + ", projected playoff odds: " + str(playoffs[i]))
