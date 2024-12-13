from game_simulation import simulation

game_setup = {
    #the game can be played by 2-4 players
    "number_of_players": 4, 
    #list with a position number for each player, position 0 is the player to start, position 1 is the next corner and so on.
    "player_positions": [0,1,2,3], 
    #list of strategies for each player, ("random","first","last")
    "strategies": ["first","last","last","first"]
}

number_of_games_to_simulate = 1000

statistics = simulation(number_of_games_to_simulate=number_of_games_to_simulate,
                        **game_setup)