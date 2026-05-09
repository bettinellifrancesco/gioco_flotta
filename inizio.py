import random
import json
FLOTTA_MASSIMA = 16
SETTIMANE_BASE = 8
CATEGORIE_RUOLI = [
    {"nome": "cuoco",      "prezzo_settimana": 15},
    {"nome": "marinaio",   "prezzo_settimana": 10},
    {"nome": "meccanico",  "prezzo_settimana": 15},
    {"nome": "medico",     "prezzo_settimana": 25},
    {"nome": "navigatore", "prezzo_settimana": 20},
]
CATEGORIE_PROVVISTE = [
    {"nome": "verdura", "unita": "kg",     "prezzo": 0.5, "consumo": 0.5},
    {"nome": "frutta",  "unita": "kg",     "prezzo": 1.0, "consumo": 1.0},
    {"nome": "carne",   "unita": "kg",     "prezzo": 2.0, "consumo": 1.0},
    {"nome": "acqua",   "unita": "barili", "prezzo": 0.5, "consumo": 0.5},
]
CATEGORIE_MERCI = [
    {"nome": "medicinali", "descrizione": "bottiglie di medicinale", "prezzo": 1.0,  "unita": "bottiglia"},
    {"nome": "armi",       "descrizione": "armi",                    "prezzo": 5.0,  "unita": "pezzo"},
    {"nome": "sale",       "descrizione": "sale",                    "prezzo": 0.5,  "unita": "sacco"},
    {"nome": "stoffa",     "descrizione": "stoffa",                  "prezzo": 2.0,  "unita": "telo"},
    {"nome": "coltelli",   "descrizione": "coltelli",                "prezzo": 0.5,  "unita": "pezzo"},
    {"nome": "diamanti",   "descrizione": "diamanti",                "prezzo": 1.0,  "unita": "pezzo"},
]
NOMI_MERCI_BARATTABILI = ["sale", "stoffa", "coltelli", "diamanti"]
TABELLA_BARATTO = {
    "sale":     {"perla": 0.5, "manufatto": 0.5, "spezia": 1.0},
    "stoffa":   {"perla": 5.0, "manufatto": 7.0, "spezia": 3.0},
    "coltelli": {"perla": 1.0, "manufatto": 3.0, "spezia": 6.0},
    "diamanti": {"perla": 2.0, "manufatto": 4.0, "spezia": 4.0},
}
VALORE_BENI_INDIGENI = {
    "perla":     2.0,
    "manufatto": 2.0,
    "spezia":    1.0,
}
OFFERTE_ASTA = [50, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 1200]
OFFERTE_INFINITE_ASTA = [50, 300, 400, 450]
# MENU PRINCIPALE
def mostra_menu_principale():
    print("-----------NUOVO MONDO-----------")
    print("1 - nuova partita")
    print("2 - carica vecchia partita")
    print("---------------------------------")
def acquista_equipaggio():
    print("------FASE 1: EQUIPAGGIO------")
    print("e' il momento di ingaggiare la tua flotta!!")
    print("devi ingaggiare almeno 1 persona per ogni ruolo.")

    for indice in range(len(CATEGORIE_RUOLI)):
        ruolo = CATEGORIE_RUOLI[indice]
        print(f"{indice + 1} - {ruolo['nome']} : {ruolo['prezzo_settimana']} monete a settimana")
    quantita_per_ruolo = [0, 0, 0, 0, 0]

    totale_acquistati = 0

    ruoli_ancora_da_comprare = len(CATEGORIE_RUOLI)

    #almeno 1 per ruolo

    for indice in range(len(CATEGORIE_RUOLI)):
        nome_ruolo = CATEGORIE_RUOLI[indice]["nome"]
        corretto = False
        while not corretto:

            try:
                massimo_acquistabile = FLOTTA_MASSIMA - totale_acquistati - (ruoli_ancora_da_comprare - 1)
                numero = int(input(f"Quanti {nome_ruolo} vuoi ingaggiare? (1-{massimo_acquistabile}): "))
                if numero < 1 or numero > massimo_acquistabile:
                    print(f"Inserisci un numero tra 1 e {massimo_acquistabile}.")
                else:

                    quantita_per_ruolo[indice] = numero
                    totale_acquistati = totale_acquistati + numero
                    ruoli_ancora_da_comprare = ruoli_ancora_da_comprare - 1
                    print(f"Ingaggiati {numero} {nome_ruolo}.")
                    corretto = True

            except ValueError:

                print("Inserisci un numero valido.")

    # Acquisto opzionale
    risposta = ""
    while risposta != "n" and totale_acquistati < FLOTTA_MASSIMA:
        risposta = input("Vuoi aggiungere altri personaggi? (s/n): ").strip().lower()
        if risposta == "s":
            print("Quale ruolo vuoi aggiungere?")

            for indice in range(len(CATEGORIE_RUOLI)):
                print(f"{indice + 1} - {CATEGORIE_RUOLI[indice]['nome']}")

            scelta_valida = False

            while not scelta_valida:

                try:
                    scelta = int(input("Scegli il numero del ruolo: "))
                    if scelta < 1 or scelta > len(CATEGORIE_RUOLI):
                        print("Scelta non valida.")

                    else:

                        massimo_acquistabile = FLOTTA_MASSIMA - totale_acquistati
                        numero_valido = False

                        while not numero_valido:
                            try:
                                numero = int(input(f"Quanti {CATEGORIE_RUOLI[scelta - 1]['nome']} vuoi aggiungere? (1-{massimo_acquistabile}): "))

                                if numero < 1 or numero > massimo_acquistabile:
                                    print(f"Inserisci un numero tra 1 e {massimo_acquistabile}.")

                                else:
                                    quantita_per_ruolo[scelta - 1] = quantita_per_ruolo[scelta - 1] + numero
                                    totale_acquistati = totale_acquistati + numero
                                    print(f"Aggiunti {numero} {CATEGORIE_RUOLI[scelta - 1]['nome']}.")
                                    numero_valido = True
                                    scelta_valida = True

                            except ValueError:
                                print("Inserisci un numero valido.")
                except ValueError:
                    print("Inserisci un numero valido.")
        elif risposta != "n":
            print("Rispondi s oppure n.")
    print()
    print(f"Flotta finale ({totale_acquistati}/{FLOTTA_MASSIMA}):")
    for indice in range(len(CATEGORIE_RUOLI)):
        print(f"  {CATEGORIE_RUOLI[indice]['nome']}: {quantita_per_ruolo[indice]}")
    lista_membri = []
    for indice in range(len(CATEGORIE_RUOLI)):
        nome_ruolo = CATEGORIE_RUOLI[indice]["nome"]
        for i in range(quantita_per_ruolo[indice]):

            membro = {"ruolo": nome_ruolo, "morale": 100, "pagato": True}
            lista_membri.append(membro)
    return lista_membri
# FASE 2: PROVVISTE

def acquista_provviste(denari):
    print("------FASE 2: PROVVISTE------")
    print("benvenuto nello shop delle provviste!!")
    print(f"denari disponibili: {denari}")

    for indice in range(len(CATEGORIE_PROVVISTE)):
        provvista = CATEGORIE_PROVVISTE[indice]
        print(f"{indice + 1} - {provvista['nome']} : {provvista['prezzo']} monete al {provvista['unita']}")

    quantita_provviste = [0.0, 0.0, 0.0, 0.0]
    acquistando = True
    while acquistando:

        risposta = input("Vuoi acquistare provviste? (s/n): ").strip().lower()
        if risposta == "n":
            acquistando = False
        elif risposta == "s":
            corretto = False
            while not corretto:
                try:

                    numero = int(input("Inserisci il numero della provvista: "))
                    quantita = float(input("Quanta quantita' vuoi (minimo 1): "))
                    if numero < 1 or numero > len(CATEGORIE_PROVVISTE) or quantita < 1:
                        print("Numero o quantita' non valida.")
                    else:
                        costo = CATEGORIE_PROVVISTE[numero - 1]["prezzo"] * quantita
                        if costo > denari:
                            print("Denari insufficienti.")
                        else:
                            denari = denari - costo
                            quantita_provviste[numero - 1] = quantita_provviste[numero - 1] + quantita
                            nome = CATEGORIE_PROVVISTE[numero - 1]["nome"]
                            print(f"Acquistati {quantita} {CATEGORIE_PROVVISTE[numero - 1]['unita']} di {nome}. Denari rimasti: {round(denari, 2)}")
                            corretto = True

                except ValueError:
                    print("Inserisci un numero valido.")

        else:
            print("Rispondi s oppure n.")

    return denari, quantita_provviste

# FASE 3: MERCI
def acquista_merci(denari):
    print("------FASE 3: MERCI------")
    print("benvenuto nello shop delle merci!!")
    print(f"denari disponibili: {denari}")
    for indice in range(len(CATEGORIE_MERCI)):

        merce = CATEGORIE_MERCI[indice]
        print(f"{indice + 1} - {merce['descrizione']} : {merce['prezzo']} monete a {merce['unita']}")

    quantita_merci = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    acquistando = True
    while acquistando:
        risposta = input("Vuoi acquistare merci? (s/n): ").strip().lower()
        if risposta == "n":
            acquistando = False
        elif risposta == "s":
            corretto = False
            while not corretto:

                try:
                    numero = int(input("Inserisci il numero della merce: "))
                    quantita = float(input("Inserisci la quantita' (minimo 1): "))
                    if numero < 1 or numero > len(CATEGORIE_MERCI) or quantita < 1:
                        print("Numero o quantita' non valida.")
                    else:
                        costo = CATEGORIE_MERCI[numero - 1]["prezzo"] * quantita
                        if costo > denari:
                            print("Denari insufficienti.")
                        else:
                            denari = denari - costo
                            quantita_merci[numero - 1] = quantita_merci[numero - 1] + quantita
                            nome = CATEGORIE_MERCI[numero - 1]["descrizione"]
                            print(f"Acquistati {quantita} {CATEGORIE_MERCI[numero - 1]['unita']} di {nome}. Denari rimasti: {round(denari, 2)}")
                            corretto = True

                except ValueError:
                    print("Inserisci un numero valido.")
        else:
            print("Rispondi s oppure n.")
    return denari, quantita_merci


def salva_partita(
    lista_membri,
    quantita_provviste,
    quantita_merci,
    settimane_totali,
    settimana_corrente,
    contatore_eventi,
    albatri_avvistati,
    albatro_ucciso,
    razioni_correnti,
    delta_morale,
    denari_rimasti

):

    stato = {
        "lista_membri": lista_membri,
        "quantita_provviste": quantita_provviste,
        "quantita_merci": quantita_merci,
        "settimane_totali": settimane_totali,
        "settimana_corrente": settimana_corrente,
        "contatore_eventi": contatore_eventi,
        "albatri_avvistati": albatri_avvistati,
        "albatro_ucciso": albatro_ucciso,
        "razioni_correnti": razioni_correnti,
        "delta_morale": delta_morale,
        "denari_rimasti": denari_rimasti,
    }
    try:
        with open("salvataggio.json", "w") as file:
            json.dump(stato, file, indent=2)
        print("  Partita salvata.")
    except Exception:
        print("  Errore durante il salvataggio.")

def carica_partita():
    try:
        with open("salvataggio.json", "r") as file:
            stato = json.load(file)
        print("Partita caricata correttamente.")
        return stato
    except FileNotFoundError:
        print("Nessun salvataggio trovato.")
        return None
    except Exception:
        print("Errore durante il caricamento.")
        return None
def indice_provvista(nome):
    for i in range(len(CATEGORIE_PROVVISTE)):
        if CATEGORIE_PROVVISTE[i]["nome"] == nome:
            return i
    return -1

def indice_merce(nome):
    for i in range(len(CATEGORIE_MERCI)):
        if CATEGORIE_MERCI[i]["nome"] == nome:
            return i
    return -1
