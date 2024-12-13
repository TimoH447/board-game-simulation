import random
import time

class Spieler(object):
    def __init__(self, spieler,start=0, wurfanzahl=0,entscheidungen=0, haus=4, ziel=0, feld=[], zielfeld=[], taktik="random"):
        self.Spieler = spieler
        self.Start = start + 10*spieler
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


print('Start')
#######################
#    Spieler 0 = Schwarz
#    Spieler 1 = Gelb
#    Spieler 2 = Grün
#    Spieler 3 = Rot
######################
n = 4#int(input("Wie viele spielen mit?"))

x={"schwarz": Spieler(0, taktik="first"), "gelb": Spieler(1), "grün": Spieler(2,taktik="first"), "rot": Spieler(3)}
spielerliste=[x["schwarz"], x["gelb"],x["grün"],x["rot"]]

"""for global_i in range(n):
    print("Welche Farben möchte Spieler", global_i+1,"?")
    spielerliste.append(x[input()])"""
würfe=[0]*n
analyse=[0]*n
decisions=[0]*n
spieldurchläufe=100

gesamtzeit=time.time()
for stichprobe in range(spieldurchläufe):
    ende=0
    #zeit=time.time()
    #Ein Spieldurchgang (bricht nachdem jeder Spieler 500 Züge hatte automatisch ab)
    while ende<500:
        
        #jeder Spieler macht einen zug
        for aktiver_spieler in range(n):
            spielzug(spielerliste, aktiver_spieler,0)
            if spielerliste[aktiver_spieler].Ziel == 4:
                decisions[aktiver_spieler]=decisions[aktiver_spieler]+ spielerliste[aktiver_spieler].Entscheidungen
                analyse[aktiver_spieler] = analyse[aktiver_spieler]+1
                würfe[aktiver_spieler]=würfe[aktiver_spieler]+spielerliste[aktiver_spieler].Wurfanzahl
                break
        else:
            ende=ende+1
            continue
        break
    for beendetes_spiel in range(n):
        spielerliste[beendetes_spiel].reset()

print("Spieler:", n, "Spiele:", spieldurchläufe)
print('Dauer der Simulation in Sekunden: ', time.time()-gesamtzeit)

for i in range(len(analyse)):
    decisions[i]=decisions[i]/analyse[i]
    würfe[i]=würfe[i]/analyse[i]
    analyse[i]=analyse[i]/spieldurchläufe
    
print(analyse)
print(würfe)
print(decisions)

def simulation(game_setup,number_of_games_to_simulate):
    pass