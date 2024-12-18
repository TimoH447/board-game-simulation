import random
import time

class Game:
    def __init__(self, number_of_players, players, max_turns = 500):
        self.number_of_players = number_of_players
        self.players = players
        self.current_turn =0# index of the current player
        self.max_turns = max_turns
        self.turn_counter = 0

        self.winner = None

    def reset_game(self):
        # reset all players for the next game
        for beendetes_spiel in range(self.number_of_players):
            self.players[beendetes_spiel].reset()
        self.winner=None
        self.turn_counter=0
        self.current_turn=0
        

    def start_game(self):
        self.reset_game()

        #Ein Spieldurchgang (bricht nachdem jeder Spieler 500 Züge hatte automatisch ab)
        while self.turn_counter<500:
            
            #jeder Spieler macht einen zug
            for aktiver_spieler in range(self.number_of_players):
                spielzug(self.players, aktiver_spieler,0)

                # Check if player has won 
                if self.players[aktiver_spieler].Ziel == 4:
                    #decisions[aktiver_spieler]=decisions[aktiver_spieler]+ spielerliste[aktiver_spieler].Entscheidungen
                    #number_of_wins[aktiver_spieler] = number_of_wins[aktiver_spieler]+1
                    #würfe[aktiver_spieler]=würfe[aktiver_spieler]+spielerliste[aktiver_spieler].Wurfanzahl
                    self.winner = aktiver_spieler
                    break
            else: # never saw an else statement after foor loop
                # The else clause executes after the loop completes normally. 
                # This means that the loop did not encounter a break statement.
                self.turn_counter += 1
                continue # jump to start of the while loop 
            break
    
    def get_winner(self):
        return self.winner

    def play_turn(self):
        pass
    def check_winner(self):
        pass
    def end_game(self):
        pass

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
        #print(augen)
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

def figurauswahl(f_spielerliste, f_spieler, f_distanz):
    ego = f_spielerliste[f_spieler]
    möglichkeiten=list(range(len(ego.Feld)))
    
    #figuren aus der die nicht bewegt werden können aus der Liste streichen
    for fiterator in möglichkeiten:
        if ego.Feld[fiterator]+f_distanz in ego.Feld:
            möglichkeiten.remove(fiterator)
        if ego.Feld[fiterator]+f_distanz in ego.Zielfeld:
            möglichkeiten.remove(fiterator)
        if ego.Feld[fiterator]+f_distanz > ego.Start +43:
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
            if ego.Feld[fiterator2]==ego.Start:
                return fiterator2
        #Figur die Schlagen kann bewegen
        for fiterator3 in möglichkeiten:
            if ego.Feld[fiterator3]+f_distanz<ego.Start+40:
                for fui in f_spielerliste:
                    skaliertes_Feld=fui.Feld.copy()
                    skaliertes_Feld= [k%40 for k in skaliertes_Feld]
                    if (ego.Feld[fiterator3]+f_distanz)%40 in skaliertes_Feld:
                        return fiterator3
        ego.Entscheidungen=ego.Entscheidungen +1
        #taktik mit der weitesten Figur laufen
        if ego.Taktik=="first":
            firsttemp=möglichkeiten[0] 
            firstvalue=ego.Feld[möglichkeiten[0]]
            for fiterator4 in möglichkeiten: #alle möglichkeiten durchgehen
                if ego.Feld[fiterator4]>firstvalue:
                    firstvalue=ego.Feld[fiterator4]
                    firsttemp=fiterator4
            return firsttemp
        #taktik mit der langsamsten Figur laufen
        if ego.Taktik=="last":
            firsttemp=möglichkeiten[0] 
            firstvalue=ego.Feld[möglichkeiten[0]]
            for fiterator4 in möglichkeiten: #alle möglichkeiten durchgehen
                if ego.Feld[fiterator4]<firstvalue:
                    firstvalue=ego.Feld[fiterator4]
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

def spielzug(spielzug_spielerliste, spielzug_spieler, a):
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
    if a>2:
        return
    #Variablen
    ich=spielzug_spielerliste[spielzug_spieler]
    #Die gewüfelte Zahl
    w =ich.wurf()
    ich.Wurfanzahl = ich.Wurfanzahl +1
    #Wurde eine 6 gewürfelt?
    if w==6:
        #Ist noch eine Figur im Haus?
        if ich.Haus != 0:
            if not ich.Start in ich.Feld:
                schlagen(ich.Start,spielzug_spielerliste)
                ich.Feld.append(ich.Start)
                ich.Haus=ich.Haus-1
                spielzug(spielzug_spielerliste, spielzug_spieler, a)
            else:
                ausgewählte_figur = figurauswahl(spielzug_spielerliste, spielzug_spieler, w)
                if ausgewählte_figur<len(ich.Feld):
                    schlagen(ich.Feld[ausgewählte_figur]+w,spielzug_spielerliste)
                    ich.bewegen(ausgewählte_figur, w)
                spielzug(spielzug_spielerliste, spielzug_spieler, a)
        else:
            ausgewählte_figur = figurauswahl(spielzug_spielerliste, spielzug_spieler, w)
            if ausgewählte_figur<len(ich.Feld):
                schlagen(ich.Feld[ausgewählte_figur]+w,spielzug_spielerliste)
                ich.bewegen(ausgewählte_figur, w)
            spielzug(spielzug_spielerliste, spielzug_spieler, a)
            
    elif len(ich.Feld)>0:   #die erste Figur auf dem Feld weiterbewegen (es wurde keine 6 gewürfelt) 
        ausgewählte_figur = figurauswahl(spielzug_spielerliste, spielzug_spieler, w)
        if ausgewählte_figur<len(ich.Feld):
            schlagen(ich.Feld[ausgewählte_figur]+w,spielzug_spielerliste)
            ich.bewegen(ausgewählte_figur, w)
        return
    elif ich.Haus + ich.Ziel==4:  #3 Freiversuche falls alle im Haus sind
        spielzug(spielzug_spielerliste, spielzug_spieler, a+1)
    else:
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