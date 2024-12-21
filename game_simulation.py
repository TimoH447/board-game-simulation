import random
import time

class Piece:
    def __init__(self, position, owner):
        self.position = position
        self.owner = owner
        self.distance_moved = 0
    
    def move(self, dice_roll):
        self.distance_moved += dice_roll
        self.position += dice_roll
        self.position %= 40


class Player(object):
    def __init__(self, position,start=0, house=4, goal=0,  strategy="random"):
        self.position = position
        self.start_position = start + 10*position
        self.house = house
        self.pieces = []
        self.goal = goal
        self.goal_field = []
        self.strategy = strategy

    def wurf(self):
        augen = random.randint(1,6)
        return augen

    def bewegen(self, bewegen_figur, dice_roll): #Bewege die Figur falls die Zielposition nicht belegt ist
        if bewegen_figur < len(self.pieces):
            
            piece = self.pieces[bewegen_figur]
            piece_distance = piece.distance_moved
            new_distance_moved=piece_distance + dice_roll
        
            if new_distance_moved >= 40 and new_distance_moved < 44 and (new_distance_moved not in self.goal_field): #Figur ins Ziel bewegen
                self.goal_field.append(new_distance_moved)
                self.pieces.remove(piece)
                self.goal=self.goal +1
            else:
                piece.move(dice_roll)
        return
  
    def reset(self):
        self.house=4
        self.pieces=[]
        self.goal_field=[]
        self.goal=0

class Board:
    def __init__(self, players):
        """
        Initialize the board with a specified number of players.
        Each player will have their starting house, field, and goal areas managed.
        """
        self.num_players = len(players)
        self.players = players
        self.board = [None] * 40  # Represent the main board with 40 slots (track positions).

    def move_piece(self, player_index, piece_index, dice_roll):
        """
        Move a player's piece based on the dice roll and apply game rules.
        Handle pieces entering the goal area if they reach the end of the track.
        """
        player = self.players[player_index]

        piece = player.pieces[piece_index]

        # Check if the piece will enter the goal
        if piece.distance_moved+dice_roll >= 40:
            goal_position = piece.distance_moved+dice_roll

            # Ensure the piece fits in the goal area
            if goal_position < 44 and goal_position not in player.goal_field:
                player.goal_field.append(goal_position)
                player.pieces.remove(piece)
                player.goal += 1
                return True
            else:
                return False

        # Normal move on the main board
        current_position = piece.position
        new_position = (current_position + dice_roll)%40
        if self.board[new_position] is not None:
            self.knock_out_piece(new_position, player_index)

        # Update the board and the player's position
        self.board[current_position] = None
        self.board[new_position] = player_index
        player.pieces[piece_index].move(dice_roll)
        return True

    def knock_out_piece(self, position,player_index):
        """
        Knock out a piece at the given position, sending it back to its owner's house.
        """
        for player in self.players:
            if player.position != player_index:
                for piece in player.pieces:
                    if piece.position == position:
                        player.pieces.remove(piece)
                        player.house += 1
                        break

    def can_move(self, player_index, piece_index, roll):
        """
        Check if a piece can move based on the current board state.
        """
        player = self.players[player_index]
        piece_position = player.pieces[piece_index]
        new_position = (piece_position + roll) % 40

        # Check if the new position is blocked by the player's own pieces
        if new_position in player.pieces:
            return False
        return True

    def add_piece_to_board(self, player_index):
        """
        Add a piece from the player's house to the starting position if possible.
        """
        player = self.players[player_index]
        if player.house > 0 and self.board[player.start_position]!=player_index:
            if self.board[player.start_position] is not None:
                self.knock_out_piece(player.start_position,player_index)
            self.board[player.start_position] = player_index
            player.pieces.append(Piece(player.start_position, player_index))
            player.house -= 1

    def display_board(self):
        """
        Display the current state of the board for debugging purposes.
        """
        # Create an empty board representation
        board_representation = ['.' for _ in range(40)]
        
        # Place player pieces on the board
        for player in self.players:
            for piece in player.pieces:
                board_representation[piece.position % 40] = str(player.position)
        
        # Define the board layout
        board_layout = """
                {8} {9} {10}
                {7}   {11} 
                {6}   {12}
                {5}   {13}
        {0} {1} {2} {3} {4}   {14} {15} {16} {17} {18}
        {39}                   {19}
        {38} {37} {36} {35} {34}   {24} {23} {22} {21} {20}
                {33}   {25}
                {32}   {26}
                {31}   {27}
                {30} {29} {28}
        """
        
        # Format the board layout with the current board representation
        formatted_board = board_layout.format(*board_representation)
        
        # Print the formatted board
        print(formatted_board)

class Game:
    def __init__(self, number_of_players, players, max_turns = 500):
        self.number_of_players = number_of_players
        self.players = players
        self.active_player =0# index of the current player
        self.max_turns = max_turns
        self.turn_counter = 0
        self.board = Board(players)

        self.winner = None

    def reset_game(self):
        # reset all players for the next game
        for beendetes_spiel in range(self.number_of_players):
            self.players[beendetes_spiel].reset()
        self.winner=None
        self.turn_counter=0
        self.active_player=0
        self.board = Board(self.players)
        

    def start_game(self):
        self.reset_game()

        # Game stops after each player made 500 turns or there is a winner
        while self.turn_counter<500 and self.winner is None:
            self.play_turn(0)
            if self.players[self.active_player].goal == 4:
                
                self.winner = self.active_player
            self.active_player = (self.active_player + 1) % self.number_of_players
            if self.active_player == 0:
                self.turn_counter += 1

    def debug_game(self):
        self.reset_game()
        while self.turn_counter<500 and self.winner is None:
            input("Press Enter to continue...")
            self.play_turn(0)
            #output the board
            print("Active player:", self.active_player)
            print("Turn:", self.turn_counter)
            for player in self.players:
                print(f"Player {player.position} - Home: {player.house}, Goal: {player.goal}")
                print("Pieces:", [piece.position for piece in player.pieces])

            self.board.display_board()
            

            if self.players[self.active_player].goal == 4:
                self.winner = self.active_player
            self.active_player = (self.active_player + 1) % self.number_of_players
            if self.active_player == 0:
                self.turn_counter += 1

    
    def get_winner(self):
        return self.winner

    def play_turn(self,attempt):
        """
        Executes a single turn (spielzug) for a player in the game.

        This function simulates a player's turn, rolling a dice and determining 
        the next move based on the result. If a player rolls a 6, special rules apply, 
        such as placing a new piece on the board. The function handles multiple attempts 
        (up to 3) in case the player cannot make a move.

        Args:
            spielzug_spielerliste (list): A list of all players (Spieler objects).
            spielzug_spieler (int): Index of the active player in spielzug_spielerliste.
            a (int): The number of attempts already made in this turn (used to limit retries).

        Returns:
            None: The function updates the game state in-place.
        """
        #Nach dem dritten Versuch ist Schluss
        if attempt>2:
            return
        #Variablen
        player=self.players[self.active_player]
        #Die gewüfelte Zahl
        dice_roll = player.wurf()
        #Wurde eine 6 gewürfelt?
        if dice_roll==6:
            #Ist noch eine Figur im Haus?
            if player.house != 0:
                #Ist das Startfeld frei?
                if not any(piece.position == player.start_position for piece in player.pieces):
                    self.board.add_piece_to_board(self.active_player)
                    self.play_turn(attempt)
                else: #Figur auf dem Startfeld bewegen
                    ausgewählte_figur = self.select_piece_to_move(dice_roll)
                    if ausgewählte_figur<len(player.pieces):
                        self.board.move_piece(self.active_player, ausgewählte_figur, dice_roll)
                    self.play_turn(attempt)
            else: #Figur auf dem Feld 6 Felder weiterbewegen
                ausgewählte_figur = self.select_piece_to_move(dice_roll)
                if ausgewählte_figur<len(player.pieces):
                    self.board.move_piece(self.active_player, ausgewählte_figur, dice_roll)
                self.play_turn(attempt)

        # no 6 was rolled 
        elif len(player.pieces)>0:   
            ausgewählte_figur = self.select_piece_to_move(dice_roll)
            if ausgewählte_figur<len(player.pieces):
                self.board.move_piece(self.active_player, ausgewählte_figur, dice_roll)
            return
        elif player.house + player.goal==4:  #3 Freiversuche falls alle im Haus sind, abgesehen von denen die im Ziel  sind
            self.play_turn(attempt+1)
        else:
            return

    def select_piece_to_move(self, dice_roll):
        player=self.players[self.active_player]
        möglichkeiten=list(range(len(player.pieces)))
        
        #figuren aus der die nicht bewegt werden können aus der Liste streichen
        for fiterator in möglichkeiten:
            if (player.pieces[fiterator].position+dice_roll)%40 in [piece.position for piece in player.pieces]:
                möglichkeiten.remove(fiterator)
            elif player.pieces[fiterator].distance_moved+dice_roll in player.goal_field:
                möglichkeiten.remove(fiterator)
            elif player.pieces[fiterator].distance_moved +dice_roll > 43:
                möglichkeiten.remove(fiterator)
        #kann keine Figur bewegt werden wird der Wert 9 zurückgegeben
        if len(möglichkeiten)==0:
            return 9
        #wenn nur eine Figur 
        elif len(möglichkeiten)==1:
            return möglichkeiten[0]
        else:
            #Figur auf Startfeld bewegen
            for fiterator2 in möglichkeiten:
                if player.pieces[fiterator2].position==player.start_position:
                    return fiterator2
            #Figur die Schlagen kann bewegen
            for fiterator3 in möglichkeiten:
                if player.pieces[fiterator3].distance_moved +dice_roll<player.start_position+40:
                    for fui in self.players:
                        if ((player.pieces[fiterator3].position+dice_roll)%40 in [piece.position for piece in fui.pieces]):
                            return fiterator3

            #player.Entscheidungen=player.Entscheidungen +1
            #taktik mit der weitesten Figur laufen
            if player.strategy=="first":
                firsttemp=möglichkeiten[0] 
                firstvalue=player.pieces[möglichkeiten[0]].distance_moved
                for fiterator4 in möglichkeiten: #alle möglichkeiten durchgehen
                    if player.pieces[fiterator4].distance_moved>firstvalue:
                        firstvalue=player.pieces[fiterator4].distance_moved
                        firsttemp=fiterator4
                return firsttemp
            #taktik mit der langsamsten Figur laufen
            if player.strategy=="last":
                firsttemp=möglichkeiten[0] 
                firstvalue=player.pieces[möglichkeiten[0]].distance_moved
                for fiterator4 in möglichkeiten: #alle möglichkeiten durchgehen
                    if player.pieces[fiterator4].distance_moved<firstvalue:
                        firstvalue=player.pieces[fiterator4].distance_moved
                        firsttemp=fiterator4
                return firsttemp 
        
            #Zufällige Figurauswahl falls keine Taktik ausgewählt wurde
            return möglichkeiten[random.randint(0,len(möglichkeiten)-1)]

def schlagen(schlagen_position, schlagen_spielerliste):
    for schlagen_spieler in schlagen_spielerliste:
        for piece in schlagen_spieler.pieces[:]:
            if piece.position == schlagen_position:
                schlagen_spieler.pieces.remove(piece)
                schlagen_spieler.house += 1
    return

def summerize_results(number_of_games_to_simulate, number_of_players, player_positions, strategies, results):
    """
    Prints a summary of the simulation to the console.

    Args:
        number_of_games_to_simulate (int): Number of games to simulate.
        number_of_players (int): Number of players in the game.
        player_positions (list): Starting positions for players.
        strategies (list): List of strategies for each player.
        result (dictionary): Results and statistics from the simulation.

    Returns:
        None
    """

    print("//////////// SIMULATION OVERVIEW /////////////////////////////////////////////////\n")
    print("Number of players:", number_of_players, "Number of games simulated:", number_of_games_to_simulate, "\n")
    for i in range(number_of_players):
        print(f"Player {i} - Board position: {player_positions[i]}, Strategy: {strategies[i]}")
    print("\n//////////// SIMULATION RESULTS //////////////////////////////////////////////////\n")

    print(f"Duration of simulation in seconds: {results["overall_simulation_time"]}\n")
    for i in range(number_of_players):
        print(f"Player {i} - Number of wins: {results["number_of_wins"][i]}, Win percentage: {results["number_of_wins"][i]/number_of_games_to_simulate}")
    print("\n//////////////////////////////////////////////////////////////////////////////////")


def simulation(number_of_games_to_simulate, number_of_players, player_positions, strategies):
    """
    Simulates multiple games of a board game.

    Args:
        number_of_games_to_simulate (int): Number of games to simulate.
        number_of_players (int): Number of players in the game.
        player_positions (list): Starting positions for players.
        strategies (list): List of strategies for each player.

    Returns:
        None
    """

    players=[]
    for i in range(number_of_players):
        players.append(Player(position=player_positions[i],strategy=strategies[i]))
    players=sorted(players, key= lambda x: x.position)

    game = Game(number_of_players, players)

    würfe=[0]*number_of_players
    number_of_wins=[0]*number_of_players
    decisions=[0]*number_of_players

    gesamtzeit=time.time()
    for stichprobe in range(number_of_games_to_simulate):
        game.debug_game()
        winner = game.get_winner()
        if winner is not None:
            number_of_wins[winner]+=1
            würfe[winner]=würfe[winner]+game.turn_counter

        
    overall_simulation_time = time.time()-gesamtzeit

    results = {
        "overall_simulation_time": overall_simulation_time,
        "number_of_dice_rolls": würfe,
        "number_of_decisions": decisions,
        "number_of_wins": number_of_wins,
    }
    summerize_results(number_of_games_to_simulate, number_of_players, player_positions, strategies, results)