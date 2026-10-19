
class Stand: #creo l'oggetto stand
    def __init__(self, codice_stand,dimensione_stand,padiglione,prezzo_stand):
        self.codice_stand = codice_stand
        self.dimensione_stand = int(dimensione_stand)
        self.padiglione = int(padiglione)
        self.prezzo_stand = float(prezzo_stand)
        self.disponibile = True
        self.espositore = None

    def __str__(self): #serve per la stampa degli stand ordinati per prezzo
        return f"{self.codice_stand} : {self.dimensione_stand}mq - Padiglione {self.padiglione} - Prezzo {self.prezzo_stand} - Disponibile {self.disponibile}"

class StandClassico(Stand): # creo la sottoclasse di stand
    def __init__(self,codice_stand,dimensione_stand,padiglione,prezzo,numero_prese):
        super().__init__(codice_stand,dimensione_stand,padiglione,prezzo)
        self.numero_prese = int(numero_prese)

    def __str__(self): #stampa della sottoclasse
        return super().__str__()+ f" - Numero Prese {self.numero_prese}"

class StandPremium(Stand): #creo la seconda sottoclasse di stand
    def __init__(self,codice_stand,dimensione_stand,padiglione,prezzo_stand,posizione ):
        super().__init__(codice_stand,dimensione_stand,padiglione,prezzo_stand)
        self.posizione = posizione

    def __str__(self):
        return super().__str__()+ f" - Posizione {self.posizione}"

class Espositore: #creo l'oggetto espositore
    def __init__(self,codice_espositore,nome,cognome):
        self.codice_espositore = codice_espositore
        self.nome = nome
        self.cognome = cognome
        self.stand = None


class LingottoFiere: #oggetto lingotto fiere
    def __init__(self, nome_fiera):
        """Inizializza gli attributi e le strutture dati"""
        self.nome_fiera = nome_fiera
        self.lista_stand = []
        self.lista_espositori = []


        # TODO

    """Aggiungere setter e getter se necessari"""
    # TODO

    def carica_file_dati(self, file_path):
        """Carica i dati (stand ed espositori) dal file"""
        try:
            file_csv = open(file_path, "r")
            for riga in file_csv:
                riga = riga.strip()#prendo la riga e tolgo gli spazi al fondo
                pezzo = riga.split(",")#divido la riga in pezzetti
                #Caso per lo Stand:
                if pezzo[0].startswith("ST"):#guardo se il primo pezzo contenente il codice inizia con ST ed è quindi uno stand
                    posizione = ""
                    if len(pezzo) > 4:#guardo se ho piu di 4 pezzi, se si vuol dire che ho un campo in più alla posisione [4] che è la posizione
                        posizione = pezzo[4].strip()

                    if posizione == "" or posizione == "<unset>": # se la cella della posizione è vuota allora carico solo i 4 pezzi
                        stand = Stand(pezzo[0], pezzo[1], pezzo[2], pezzo[3])
                    else:
                        try:
                            # guardo se posizione un numero , se si lo carico nello standClassico perchè ho indica le prese aggiuntive
                            n_prese = int(posizione)
                            stand = StandClassico(pezzo[0], pezzo[1], pezzo[2], pezzo[3], n_prese)
                        except ValueError:
                            # Se posizione è testo allora ho una posizione e lo carico nello StandPremium
                            stand = StandPremium(pezzo[0], pezzo[1], pezzo[2], pezzo[3], posizione)


                    self.lista_stand.append(stand) #aggiungo lo stand alla lista

                #Caso per l'estintore
                elif pezzo[0].startswith("ES"): #controllo se inizia con ES il primo pezzetto
                    espositore = Espositore(pezzo[0], pezzo[1], pezzo[2])
                    self.lista_espositori.append(espositore)

            file_csv.close()
            print("Caricamento completato con successo!")

        except FileNotFoundError:
            raise FileNotFoundError("File non trovato.")

        # TODO

    def assegna_stand_a_espositore(self, codice_stand, codice_espositore):
        """Associa uno stand a un espositore"""
        # Cerco lo stand
        stand_trovato = None
        for stand in self.lista_stand:
            if stand.codice_stand == codice_stand:
                stand_trovato = stand
                break #se trova il codice nella lista si ferma di scorrerla
        if stand_trovato is None:#se non lo trova
            raise Exception("Stand non trovato")

        # Cerco l'espositore
        espositore_trovato = None
        for espositore in self.lista_espositori:
            if espositore.codice_espositore == codice_espositore:
                espositore_trovato = espositore
                break #se trova il codice nella lista si ferma di scorrerla
        if espositore_trovato is None:
            raise Exception("Espositore non trovato")

        #Metto dei controlli per vedere se lo stand e l'espositore sono liberi
        if not stand_trovato.disponibile:
            raise Exception("Stand non disponibile")

        if espositore_trovato.stand is not None:
            raise Exception("Espositore già associato a uno stand")

        # Nel caso lo se lo stand e l'espositore sono liberi allora posso assegnare una nuova occupazioone
        stand_trovato.espositore = espositore_trovato
        espositore_trovato.stand = stand_trovato
        stand_trovato.disponibile = False


    def elenca_espositori(self):
        """Stampa l'elenco degli espositori con lo stand assegnato"""
        for espositore in self.lista_espositori:
            if espositore.stand is None:
                print(f"{espositore.codice_espositore} - {espositore.nome} {espositore.cognome}: nessuno stand")
            else:
                print(
                    f"{espositore.codice_espositore} - {espositore.nome} {espositore.cognome}: stand {espositore.stand.codice_stand}")

    def stand_ordinati_per_prezzo(self):
        """Restituisce la lista ordinata degli stand in base al prezzo"""
        from operator import attrgetter
        stand_ordinati = sorted(self.lista_stand, key=attrgetter("prezzo_stand"))
        return stand_ordinati

