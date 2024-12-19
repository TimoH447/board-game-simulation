# Simulation of the board game "Mensch Ärgere Dich Nicht"

You can find the rules of the game for example [here](https://de.wikipedia.org/wiki/Mensch_%C3%A4rgere_Dich_nicht#Anleitung).

There are different strategies to play the game. The goal of this project is, to simulate the game to find out the best strategy.
The games are simulated without visualization.

## Strategies

1. First: Always pick the piece which has moved the furthest "first" piece.

2. Last: Always pick the last piece which is closest to the starting point. This tries to walk the pieces in a group to the finish.

3. Random: Pick the piece randomly.

## Simulation results

So afterall what is the best strategy in "Mensch Ärgere Dich Nicht"? By far the best strategy is to always move the piece which is the furthest. 
This means one should always move the same piece if possible. Trying to walk all pieces together into the finish is an even worse strategy then just
picking each turn a random piece to move.

When playing as 3 on the board for 4 people, then it is best to have the position with no immidiate player behind. This leads to an around 10 percent
higher chance of winning.

Examples:
10000 Games Simulated. Strategies: (First, First, Last, First). Win percentage: (0.32, 0.35, 0.02, 0.31).
10000 Games Simulated. Strategies: (Last, Random, Last, Random). Win percentage: (0.12, 0.37, 0.12, 0.39).
10000 Games Simulated. Strategies: (First, Random, Last, Random). Win percentage: (0.57, 0.17, 0.06, 0.2).


10000 Games Simulated. Strategies: (First, First, First, Empty). Win percentage: (0.4, 0.32, 0.28).

## Refactoring

This was an old project of mine, probably from around 2019. Nowadays although still far from writing clean code, 
I see that there was alot to improve.

Some examples:

1. Variable naming:
E.g. ich, ego (for player objects of player class), w  (for the number of the dice roll), a (for the number of attempt in a turn).