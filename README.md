# Fantasy football playoff odds calculator
Based on the concept of using Monte Carlo simulations to simulate a season a large number of times. Uses the external libraries NumPy, SciPy, and pandas (made in Python).

Purpose: simulates the season a user-specified number of times in order to compute:
- Predicted wins (ties as counted as 0.5 wins)
- Odds of making the playoffs
- Odds of securing a first-round bye (defined as winning the division)

NOTE: This is still a work-in-progress, so repeated/redundant code may be seen. Feel free to fork the repo and submit a pull request if you wish to aid the project.

TUTORIAL:
In order to use this (whether you run it as a Windows distribution, a macOS distribution, or the actual script), some steps need to be taken:
- First, look at the example "gamedata.csv" and "matchups.csv" spreadsheets. Replace the data in each spreadsheet with your own (would recommend Excel or Google Sheets). Each template spreadsheet should be self-explanatory to fill out, with two exceptions:

Division ("gamedata.csv"): Place a number depending on which division the player is in. For example, if there are 4 divisions, each player should have a number from 1 through 4. The players do not have to be placed in order of division.

Week X Matchups ("matchups.csv"): For each week, write down the matchups down the column of the week. As an example, let's say team 2 plays team 4, and team 1 plays team 3. The column should be written as follows:
team 2
team 4
team 1
team 3

You can switch around the order of matchups, as well as the teams in each matchups. For example, the following column would also be equivalent:
team 3
team 1
team 4
team 2

- Second, add both of these spreadsheet files inside the "FF-playoff-odds" folder that comes with the distribution. You will see a few files/folders in there that are necessary for running the program; just ignore them and drop the spreadsheets in there. Make sure they are named exactly as the example ones are, otherwise the program will not run.

- Third, run the program through the shortcut outside the "FF-playoff-odds" folder. The program should prompt you for some information (number of simulations, number of playoff spots, and number of first-round byes awarded).

Depending on how many simulations were run, there may be a decent wait. Here are some benchmarks (may vary depending on your computer):
	- 5-7 seconds for 1,000 simulations
	- 45-55 seconds for 10,000 simulations (recommended, not too long of a wait and gives relatively good accuracy)
	- 8-10 minutes for 100,000 simulations

Note that entering any number of simulations less than 100 has been disabled (program breaks, and results would be too inaccurate for use anyway).
Also note that decimal rounding to a specific number of places has not been implemented, so as a result, any number entered in other than the 3 listed above may lead to ugly looking results (will fix this soon).

TO-DO:
- Add decimal rounding to make results appear cleaner
- Add option to export results to a file
- Add compatibility for other fantasy leagues (should work for basketball, but not sure)
- Generate odds of making it to championship (as well as odds of winning it)