import random
import time

class Spieler(object):
    def __init__(self, position,start=0, wurfanzahl=0,entscheidungen=0, haus=4, ziel=0, feld=[], zielfeld=[], taktik="random"):
        self.Position = position
        self.Start = start + 10*position
        self.Wurfanzahl = wurfanzahl
        self.Entscheidungen = entscheidungen
        self.Haus = haus
        self.Ziel = ziel
        self.Feld = feld.copy()
        self.Zielfeld = zielfeld.copy()
        self.Taktik = taktik

    def wurf(self):
        augen = random.randint(1,6)
        return augen

    def bewegen(self, bewegen_figur, bewegen_distanz): #Bewege die Figur falls die Zielposition nicht belegt ist
        if bewegen_figur < len(self.Feld):
            
            aktuelle_position = self.Feld[bewegen_figur]
            zielposition=aktuelle_position + bewegen_distanz
        
            if zielposition >= self.Start +40:
                if zielposition<self.Start + 44:
                    if not zielposition in self.Zielfeld:
                        self.Zielfeld.append(zielposition)
                        self.Feld.remove(aktuelle_position)
                        self.Ziel=self.Ziel +1
            else:
                self.Feld[bewegen_figur] = zielposition
        return
  
    def reset(self):
        self.Haus=4
        self.Feld=[]
        self.Zielfeld=[]
        self.Ziel=0
        self.Wurfanzahl=0
        self.Entscheidungen=0

class Game:
    def __init__(self, number_of_players, players, max_turns = 500):
        self.number_of_players = number_of_players
        self.players = players
        self.active_player =0# index of the current player
        self.max_turns = max_turns
        self.turn_counter = 0

        self.winner = None

    def reset_game(self):
        # reset all players for the next game
        for beendetes_spiel in range(self.number_of_players):
            self.players[beendetes_spiel].reset()
        self.winner=None
        self.turn_counter=0
        self.active_player=0
        

    def start_game(self):
        self.reset_game()

        # Game stops after each player made 500 turns or there is a winner
        while self.turn_counter<500 and self.winner is None:
            self.play_turn(0)
            if self.players[self.active_player].Ziel == 4:
                #decisions[aktiver_spieler]=decisions[aktiver_spieler]+ spielerliste[aktiver_spieler].Entscheidungen
                #number_of_wins[aktiver_spieler] = number_of_wins[aktiver_spieler]+1
                #würfe[aktiver_spieler]=würfe[aktiver_spieler]+spielerliste[aktiver_spieler].Wurfanzahl
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
        player.Wurfanzahl = player.Wurfanzahl +1
        #Wurde eine 6 gewürfelt?
        if dice_roll==6:
            #Ist noch eine Figur im Haus?
            if player.Haus != 0:
                if not player.Start in player.Feld:
                    schlagen(player.Start,self.players)
                    player.Feld.append(player.Start)
                    player.Haus=player.Haus-1
                    self.play_turn(attempt)
                else:
                    ausgewählte_figur = self.select_piece_to_move(dice_roll)
                    if ausgewählte_figur<len(player.Feld):
                        schlagen(player.Feld[ausgewählte_figur]+dice_roll,self.players)
                        player.bewegen(ausgewählte_figur, dice_roll)
                    self.play_turn(attempt)
            else:
                ausgewählte_figur = self.select_piece_to_move(dice_roll)
                if ausgewählte_figur<len(player.Feld):
                    schlagen(player.Feld[ausgewählte_figur]+dice_roll,self.players)
                    player.bewegen(ausgewählte_figur, dice_roll)
                self.play_turn(attempt)

                
        elif len(player.Feld)>0:   #die erste Figur auf dem Feld weiterbewegen (es wurde keine 6 gewürfelt) 
            ausgewählte_figur = self.select_piece_to_move(dice_roll)
            if ausgewählte_figur<len(player.Feld):
                schlagen(player.Feld[ausgewählte_figur]+dice_roll,self.players)
                player.bewegen(ausgewählte_figur, dice_roll)
            return
        elif player.Haus + player.Ziel==4:  #3 Freiversuche falls alle im Haus sind, abgesehen von denen die im Ziel  sind
            self.play_turn(attempt+1)
        else:
            return

    def select_piece_to_move(self, dice_roll):
        player=self.players[self.active_player]
        möglichkeiten=list(range(len(player.Feld)))
        
        #figuren aus der die nicht bewegt werden können aus der Liste streichen
        for fiterator in möglichkeiten:
            if player.Feld[fiterator]+dice_roll in player.Feld:
                möglichkeiten.remove(fiterator)
            if player.Feld[fiterator]+dice_roll in player.Zielfeld:
                möglichkeiten.remove(fiterator)
            if player.Feld[fiterator]+dice_roll > player.Start +43:
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
                if player.Feld[fiterator2]==player.Start:
                    return fiterator2
            #Figur die Schlagen kann bewegen
            for fiterator3 in möglichkeiten:
                if player.Feld[fiterator3]+dice_roll<player.Start+40:
                    for fui in self.players:
                        skaliertes_Feld=fui.Feld.copy()
                        skaliertes_Feld= [k%40 for k in skaliertes_Feld]
                        if (player.Feld[fiterator3]+dice_roll)%40 in skaliertes_Feld:
                            return fiterator3
            player.Entscheidungen=player.Entscheidungen +1
            #taktik mit der weitesten Figur laufen
            if player.Taktik=="first":
                firsttemp=möglichkeiten[0] 
                firstvalue=player.Feld[möglichkeiten[0]]
                for fiterator4 in möglichkeiten: #alle möglichkeiten durchgehen
                    if player.Feld[fiterator4]>firstvalue:
                        firstvalue=player.Feld[fiterator4]
                        firsttemp=fiterator4
                return firsttemp
            #taktik mit der langsamsten Figur laufen
            if player.Taktik=="last":
                firsttemp=möglichkeiten[0] 
                firstvalue=player.Feld[möglichkeiten[0]]
                for fiterator4 in möglichkeiten: #alle möglichkeiten durchgehen
                    if player.Feld[fiterator4]<firstvalue:
                        firstvalue=player.Feld[fiterator4]
                        firsttemp=fiterator4
                return firsttemp 
        
            #Zufällige Figurauswahl falls keine Taktik ausgewählt wurde
            return möglichkeiten[random.randint(0,len(möglichkeiten)-1)]

def schlagen(schlagen_position, schlagen_spielerliste):
    for schlagen_spieler in schlagen_spielerliste:
        if schlagen_position in schlagen_spieler.Feld:
            schlagen_spieler.Feld.remove(schlagen_position)
            schlagen_spieler.Haus=schlagen_spieler.Haus +1
        if schlagen_position+40 in schlagen_spieler.Feld:
            schlagen_spieler.Feld.remove(schlagen_position+40)
            schlagen_spieler.Haus=schlagen_spieler.Haus +1
        if schlagen_position-40 in schlagen_spieler.Feld:
            schlagen_spieler.Feld.remove(schlagen_position-40)
            schlagen_spieler.Haus=schlagen_spieler.Haus +1
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
        players.append(Spieler(position=player_positions[i],taktik=strategies[i]))
    players=sorted(players, key= lambda x: x.Position)

    game = Game(number_of_players, players)

    würfe=[0]*number_of_players
    number_of_wins=[0]*number_of_players
    decisions=[0]*number_of_players

    gesamtzeit=time.time()
    for stichprobe in range(number_of_games_to_simulate):
        game.start_game()
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