denari = 2000
flotta = [
    {"nome": "cuoco", "prezzo": 15},
    {"nome": "marinaio", "prezzo": 10},
    {"nome": "meccanico", "prezzo": 15},
    {"nome": "medico", "prezzo": 25},
    {"nome": "navigatore", "prezzo": 20},
]


def mostra_menu_principale():
    print("-----------NUOVO MONDO-----------")
    print("1 - nuova partita")
    print("2 - carica vecchia partita")
    print("---------------------------------")


def acquista_equipaggio(flotta):
    print("------FASE 1: EQUIPAGGIO------")
    print("è il momento di ingaggiare la tua flotta!!")
    print("di seguito troverai tutti i personaggi disponibili")
    print("seleziona almeno 1 personaggio per tipologia!!")
    for i, membro in enumerate(flotta):
        print(f"{i+1} - {membro['nome']} : {membro['prezzo']} oro")
    conta = [
        {"nome": "cuochi", "q": 0},
        {"nome": "marinai", "q": 0},
        {"nome": "meccanici", "q": 0},
        {"nome": "medici", "q": 0},
        {"nome": "navigatori", "q": 0},
    ]
    FLOTTA_MAX = 16
    acquistati = 0
    ruoli_rimasti = len(conta)

    # acquisto obbligatorio di almeno 1 personaggio per ogni ruolo
    for i in range(len(conta)):
        corretto = False
        while not corretto:
            try:
                massimo = FLOTTA_MAX - acquistati - (ruoli_rimasti - 1)
                n = int(input(f"Inserisci il numero di {conta[i]['nome']} (1-{massimo}): "))
                if n <= 0 or n > massimo:
                    print(f"Numero non valido. Inserisci un valore tra 1 e {massimo}!!")
                else:
                    conta[i]["q"] += n
                    acquistati += n
                    ruoli_rimasti -= 1
                    corretto = True
            except ValueError:
                print("Inserisci un numero valido.")

    #acquisto opzionale di altri membri
    continua = ""
    while continua != "n" and acquistati < FLOTTA_MAX:
        continua = input("Vuoi aggiungere altri personaggi? (s/n): ").lower()
        if continua == "s":
            print("Quale personaggio vuoi aggiungere?")
            for i, membro in enumerate(conta):
                print(f"{i+1} - {membro['nome']}")

            scelta_valida = False
            while not scelta_valida:
                try:
                    scelta = int(input("Scegli il numero del personaggio: "))
                    if scelta < 1 or scelta > len(conta):
                        print("Scelta non valida.")
                    else:
                        massimo = FLOTTA_MAX - acquistati
                        n_valido = False
                        while not n_valido:
                            try:
                                n = int(input(f"Quanti {conta[scelta-1]['nome']} vuoi aggiungere? (1-{massimo}): "))
                                if n <= 0 or n > massimo:
                                    print(f"Numero non valido. Inserisci un valore tra 1 e {massimo}.")
                                else:
                                    conta[scelta - 1]["q"] += n
                                    acquistati += n
                                    scelta_valida = True
                                    n_valido = True
                            except ValueError:
                                print("Inserisci un numero valido.")
                except ValueError:
                    print("Inserisci un numero valido.")

 
    print(f"\nFlotta ({acquistati}/{FLOTTA_MAX}):")
    for membro in conta:
        print(f"  {membro['nome'].capitalize()}: {membro['q']}")


def acquista_provviste(denari):
    print("------FASE 2: PROVVISTE------")
    provviste = [
        {"nome": "verdura", "um": "kg", "prezzo": 0.5},
        {"nome": "frutta", "um": "kg", "prezzo": 1},
        {"nome": "carne", "um": "kg", "prezzo": 2},
        {"nome": "acqua", "um": "barili", "prezzo": 0.5},
    ]

    for i, provvista in enumerate(provviste):
        print(f"{i+1} - {provvista['nome']} : {provvista['prezzo']} monete al {provvista['um']}")
    print("benvenuto nello shop delle provviste!!")
    print(f"denari disponibili: {denari}")

    acquisto = input("se vuoi acquistare provviste premi s altrimenti per continuare premi n: ").lower()
    while acquisto != "s" and acquisto != "n":
        print("scelta non valida!!")
        acquisto = input("se vuoi acquistare provviste premi s altrimenti per continuare premi n: ").lower()

    corretto = False
    while not corretto and acquisto == "s":
        try:
            numero_provvista = int(input("inserisci il numero della provvista che vuoi acquistare: "))
            quantità = float(input("quanti kg/barili vuoi (minimo 1): "))
            if numero_provvista > len(provviste) or numero_provvista < 1 or quantità < 1:
                print("hai inserito un numero errato!!")
            else:
                costo = provviste[numero_provvista - 1]["prezzo"] * quantità
                if costo > denari:
                    print("denari insufficienti!!")
                else:
                    denari -= costo 
                    print(f"denari rimasti: {denari}")
                    continuo = input("vuoi acquistare altre provviste s/n: ").lower()
                    while continuo != "s" and continuo != "n":
                        print("inserisci una scelta valida!!")
                        continuo = input("vuoi acquistare altre provviste s/n: ").lower()

                    if continuo == "s":
                        corretto = False
                    elif continuo == "n":
                        corretto = True
        except ValueError:
            print("inserisci un numero valido!!")

    return denari 


def acquista_merci(denari):
    print("------FASE 3: MERCI------")
    print("benvenuto nello shop delle merci!!")
    merci = [
        {"tipo": "bottiglie di medicinale", "prezzo": 1, "um": "a bottiglia"},
        {"tipo": "armi", "prezzo": 5, "um": "ad arma"},
        {"tipo": "sale", "prezzo": 0.5, "um": "al sacco"},
        {"tipo": "stoffa", "prezzo": 2, "um": "al telo"},
        {"tipo": "coltelli", "prezzo": 0.5, "um": "al pezzo"},
        {"tipo": "diamanti", "prezzo": 1, "um": "al pezzo"},
    ]

    for i, merce in enumerate(merci):
        print(f"{i+1} - {merce['tipo']} : {merce['prezzo']} moneta/e {merce['um']}")
    print(f"denari disponibili: {denari}")

    acquisto = input("se vuoi acquistare merci premi s altrimenti per continuare premi n: ").lower()
    while acquisto != "s" and acquisto != "n":
        print("scelta non valida!!")
        acquisto = input("se vuoi acquistare merci premi s altrimenti per continuare premi n: ").lower()

    corretto = False
    while not corretto and acquisto == "s":
        try:
            numero_merce = int(input("inserisci il numero della merce che vuoi acquistare: "))
            quantità = float(input("inserisci la quantità (minimo 1): "))
            if numero_merce > len(merci) or numero_merce < 1 or quantità < 1:
                print("hai inserito un numero errato!!")
            else:
                costo = merci[numero_merce - 1]["prezzo"] * quantità
                if costo > denari:
                    print("denari insufficienti!!")
                else:
                    denari -= costo  
                    print(f"denari rimasti: {denari}")
                    continuo = input("vuoi acquistare altre provviste s/n: ").lower()
                    while continuo != "s" and continuo != "n":
                        print("inserisci una scelta valida!!")
                        continuo = input("vuoi acquistare altre provviste s/n: ").lower()

                    if continuo == "s":
                        corretto = False
                    elif continuo == "n":
                        corretto = True
        except ValueError:
            print("inserisci un numero valido!!")

    return denari  


def shop():
    print("------BENVENUTO NELLO SHOP------")
    print("devi completare 3 fasi prima di partire!")
    print("--------------------------------")

    acquista_equipaggio(flotta)                          # fase 1
    denari_aggiornati = acquista_provviste(denari)       # fase 2 — salva il ritorno
    denari_aggiornati = acquista_merci(denari_aggiornati) # fase 3 — passa i denari aggiornati

    print(f"Perfetto, ora sei pronto per il viaggio!! Denari rimasti: {denari_aggiornati}")


def nuova_partita():
    shop()


def carica_partita():
    print("caricamento partita...")


def main():
    mostra_menu_principale()
    corretto = False
    while not corretto:
        scelta = input("Benvenuto in NUOVO MONDO!! Scegli: ")
        if scelta == "1":
            corretto = True
            nuova_partita()
        elif scelta == "2":
            carica_partita()
            corretto = True
        else:
            print("Errore d'inserimento")


main()