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
def conta_membri_vivi(lista_membri):
    return len(lista_membri)
def conta_membri_per_ruolo(lista_membri, nome_ruolo):
    contatore = 0
    for membro in lista_membri:
        if membro["ruolo"] == nome_ruolo:
            contatore = contatore + 1
    return contatore
def rimuovi_membro_casuale(lista_membri):
    if len(lista_membri) == 0:
        return None
    indice = random.randrange(len(lista_membri))
    membro_rimosso = lista_membri[indice]
    lista_membri.pop(indice)
    return membro_rimosso
def rimuovi_n_membri_non_medici(lista_membri, numero_da_rimuovere):
    # Costruiamo lista degli indici dei non-medici
    indici_non_medici = []
    for i in range(len(lista_membri)):
        if lista_membri[i]["ruolo"] != "medico":
            indici_non_medici.append(i)
    rimossi = 0
    # Rimuoviamo dal fondo per non spostare gli indici
    random.shuffle(indici_non_medici)
    da_rimuovere = min(numero_da_rimuovere, len(indici_non_medici))
    # Ordiniamo in ordine decrescente per rimuovere dal fondo
    indici_non_medici_ordinati = sorted(indici_non_medici[:da_rimuovere], reverse=True)
    for i in indici_non_medici_ordinati:
        lista_membri.pop(i)
        rimossi = rimossi + 1
    return rimossi
def aggiungi_membro(lista_membri, nome_ruolo, morale_iniziale, e_pagato):
    nuovo_membro = {"ruolo": nome_ruolo, "morale": morale_iniziale, "pagato": e_pagato}
    lista_membri.append(nuovo_membro)
def frazione_a_testo(frazione):
    if abs(frazione - 0.5) < 0.001:
        return "1/2"
    if abs(frazione - 1.0 / 3.0) < 0.001:
        return "1/3"
    if abs(frazione - 0.25) < 0.001:
        return "1/4"
    if abs(frazione - 0.2) < 0.001:
        return "1/5"
    return str(frazione)
LISTA_EVENTI = [
    {"nome": "Uomo in mare",          "ripetibile": False, "limite": 1,  "peso": 1},
    {"nome": "Verdura in mare",       "ripetibile": False, "limite": 1,  "peso": 2},
    {"nome": "Frutta in mare",        "ripetibile": False, "limite": 1,  "peso": 2},
    {"nome": "Carne in mare",         "ripetibile": False, "limite": 1,  "peso": 2},
    {"nome": "Acqua in mare",         "ripetibile": False, "limite": 1,  "peso": 2},
    {"nome": "Pesca miracolosa",      "ripetibile": False, "limite": 1,  "peso": 1},
    {"nome": "Tempesta miracolosa",   "ripetibile": False, "limite": 1,  "peso": 1},
    {"nome": "Venti favorevoli",      "ripetibile": False, "limite": 1,  "peso": 3},
    {"nome": "Cattivo tempo",         "ripetibile": False, "limite": 1,  "peso": 2},
    {"nome": "Ondata",                "ripetibile": False, "limite": 1,  "peso": 1},
    {"nome": "Infestazione ratti",    "ripetibile": False, "limite": 1,  "peso": 2},
    {"nome": "Avvistamento albatro",  "ripetibile": True,  "limite": 3,  "peso": 2},
    {"nome": "Avvistamento scialuppa","ripetibile": False, "limite": 1,  "peso": 1},
    {"nome": "Epidemia",              "ripetibile": False, "limite": 1,  "peso": 1},
    {"nome": "Attacco pirata",        "ripetibile": False, "limite": 1,  "peso": 1},
    {"nome": "Danni al timone",       "ripetibile": False, "limite": 1,  "peso": 2},
    {"nome": "Raffiche di vento",     "ripetibile": False, "limite": 1,  "peso": 2},
    {"nome": "Avvistamento isola",    "ripetibile": False, "limite": 1,  "peso": 1},
    {"nome": "Nessun imprevisto",     "ripetibile": True,  "limite": 99, "peso": 3},
]
def scegli_evento(contatore_eventi):
    nomi_disponibili = []
    pesi_disponibili = []
    for evento in LISTA_EVENTI:
        nome_evento = evento["nome"]
        volte_accaduto = contatore_eventi.get(nome_evento, 0)
        if volte_accaduto < evento["limite"]:
            nomi_disponibili.append(nome_evento)
            pesi_disponibili.append(evento["peso"])
    if len(nomi_disponibili) == 0:
        return "Nessun imprevisto"
    nome_scelto = random.choices(nomi_disponibili, weights=pesi_disponibili, k=1)[0]
    return nome_scelto
def gestisci_evento(
    nome_evento,
    lista_membri,
    quantita_provviste,
    quantita_merci,
    settimane_totali,
    albatri_avvistati,
    albatro_ucciso
):
    """
    Gestisce l'evento e restituisce un dizionario con le variazioni da applicare:
    - variazione_settimane: intero (positivo = allungamento, negativo = accorciamento)
    - variazione_morale_evento: intero da aggiungere al morale di tutti i membri
    - albatri_avvistati_aggiunta: 1 se avvistato un albatro, altrimenti 0
    - albatro_ora_ucciso: True se un albatro e' stato ucciso in questo evento
    """
    print()
    print(f"  EVENTO: {nome_evento}")
    risultato = {
        "variazione_settimane": 0,
        "variazione_morale_evento": 0,
        "albatri_avvistati_aggiunta": 0,
        "albatro_ora_ucciso": False,
    }
    frazioni_possibili = [0.5, 1.0 / 3.0, 0.25, 0.2]
    if nome_evento == "Uomo in mare":
        membro_perso = rimuovi_membro_casuale(lista_membri)
        if membro_perso is None:
            print("  Non c'era nessuno a bordo.")
        else:
            print(f"  Tragico: un {membro_perso['ruolo']} e' caduto in mare.")
    elif nome_evento == "Verdura in mare":
        indice = indice_provvista("verdura")
        frazione = random.choice(frazioni_possibili)
        perdita = quantita_provviste[indice] * frazione
        quantita_provviste[indice] = quantita_provviste[indice] - perdita
        if quantita_provviste[indice] < 0:
            quantita_provviste[indice] = 0.0
        print(f"  Tempesta: persa {frazione_a_testo(frazione)} della verdura ({round(perdita, 2)} kg).")
    elif nome_evento == "Frutta in mare":
        indice = indice_provvista("frutta")
        frazione = random.choice(frazioni_possibili)
        perdita = quantita_provviste[indice] * frazione
        quantita_provviste[indice] = quantita_provviste[indice] - perdita
        if quantita_provviste[indice] < 0:
            quantita_provviste[indice] = 0.0
        print(f"  Tempesta: persa {frazione_a_testo(frazione)} della frutta ({round(perdita, 2)} kg).")
    elif nome_evento == "Carne in mare":
        indice = indice_provvista("carne")
        frazione = random.choice(frazioni_possibili)
        perdita = quantita_provviste[indice] * frazione
        quantita_provviste[indice] = quantita_provviste[indice] - perdita
        if quantita_provviste[indice] < 0:
            quantita_provviste[indice] = 0.0
        print(f"  Tempesta: persa {frazione_a_testo(frazione)} della carne ({round(perdita, 2)} kg).")
    elif nome_evento == "Acqua in mare":
        indice = indice_provvista("acqua")
        frazione = random.choice(frazioni_possibili)
        perdita = quantita_provviste[indice] * frazione
        quantita_provviste[indice] = quantita_provviste[indice] - perdita
        if quantita_provviste[indice] < 0:
            quantita_provviste[indice] = 0.0
        print(f"  Tempesta: persa {frazione_a_testo(frazione)} dell'acqua ({round(perdita, 2)} barili).")
    elif nome_evento == "Pesca miracolosa":
        kg_pescati = random.randint(11, 20)
        indice = indice_provvista("carne")
        quantita_provviste[indice] = quantita_provviste[indice] + kg_pescati
        print(f"  Pesca miracolosa: +{kg_pescati} kg di carne (pesce).")
        risultato["variazione_morale_evento"] = 5
    elif nome_evento == "Tempesta miracolosa":
        barili_raccolti = random.randint(11, 20)
        indice = indice_provvista("acqua")
        quantita_provviste[indice] = quantita_provviste[indice] + barili_raccolti
        print(f"  Tempesta miracolosa: +{barili_raccolti} barili d'acqua raccolti.")
    elif nome_evento == "Venti favorevoli":
        guadagno_morale = random.randint(5, 15)
        risultato["variazione_settimane"] = -1
        risultato["variazione_morale_evento"] = guadagno_morale
        print(f"  Venti favorevoli: viaggio accorciato di 1 settimana. Morale +{guadagno_morale}.")
    elif nome_evento == "Cattivo tempo":
        indice = indice_merce("medicinali")
        frazione = random.choice(frazioni_possibili)
        perdita = quantita_merci[indice] * frazione
        quantita_merci[indice] = quantita_merci[indice] - perdita
        if quantita_merci[indice] < 0:
            quantita_merci[indice] = 0.0
        print(f"  Cattivo tempo: persi {frazione_a_testo(frazione)} dei medicinali ({round(perdita, 2)} bottiglie).")
        risultato["variazione_morale_evento"] = -3
    elif nome_evento == "Ondata":
        indice = indice_merce("armi")
        frazione = random.choice(frazioni_possibili)
        perdita = quantita_merci[indice] * frazione
        quantita_merci[indice] = quantita_merci[indice] - perdita
        if quantita_merci[indice] < 0:
            quantita_merci[indice] = 0.0
        print(f"  Ondata: perse {frazione_a_testo(frazione)} delle armi ({round(perdita, 2)} pezzi).")
        risultato["variazione_morale_evento"] = -3
    elif nome_evento == "Infestazione ratti":
        indice = indice_merce("stoffa")
        frazione = random.choice(frazioni_possibili)
        perdita = quantita_merci[indice] * frazione
        quantita_merci[indice] = quantita_merci[indice] - perdita
        if quantita_merci[indice] < 0:
            quantita_merci[indice] = 0.0
        print(f"  Infestazione ratti: rovinate {frazione_a_testo(frazione)} delle stoffe ({round(perdita, 2)} teli).")
        risultato["variazione_morale_evento"] = -2
    elif nome_evento == "Avvistamento albatro":
        risultato["albatri_avvistati_aggiunta"] = 1
        print("  Un albatro e' stato avvistato: buon presagio!")
        indice_armi = indice_merce("armi")
        numero_armi = int(quantita_merci[indice_armi])
        numero_vivi = conta_membri_vivi(lista_membri)
        if numero_armi >= 1 and numero_vivi > 0:
            print("  Hai armi a bordo. Puoi provare a sparare all'albatro per ottenere carne.")
            print("  Attenzione: le armi usate NON potranno essere barattate.")
            risposta = input("  Vuoi sparare all'albatro? (s/n): ").strip().lower()
            while risposta != "s" and risposta != "n":
                risposta = input("  Rispondi s oppure n: ").strip().lower()
            if risposta == "s":
                numero_colpi = min(numero_armi, numero_vivi)
                print(f"  Hai {numero_colpi} colpi a disposizione.")
                quantita_merci[indice_armi] = quantita_merci[indice_armi] - numero_colpi
                successi = 0
                for _ in range(numero_colpi):
                    if random.random() < 0.5:
                        successi = successi + 1
                if successi > 0:
                    carne_guadagnata = random.randint(10, 15)
                    indice_carne = indice_provvista("carne")
                    quantita_provviste[indice_carne] = quantita_provviste[indice_carne] + carne_guadagnata
                    print(f"  Albatro abbattuto! +{carne_guadagnata} kg di carne.")
                    risultato["albatro_ora_ucciso"] = True
                else:
                    print("  Hai sparato ma l'albatro non e' stato colpito.")
            else:
                print("  Hai deciso di non sparare.")
        else:
            print("  Non hai abbastanza armi o uomini per tentare il tiro.")

    elif nome_evento == "Avvistamento scialuppa":
        print("  Scialuppa alla deriva con 4 uomini e una cassa misteriosa.")
        risposta = input("  Vuoi salvare i 4 naufraghi? (s/n): ").strip().lower()
        while risposta != "s" and risposta != "n":
            risposta = input("  Rispondi s oppure n: ").strip().lower()
        if risposta == "s":
            for _ in range(4):
                ruolo_casuale = CATEGORIE_RUOLI[random.randint(0, len(CATEGORIE_RUOLI) - 1)]["nome"]
                morale_casuale = random.randint(25, 75)
                aggiungi_membro(lista_membri, ruolo_casuale, morale_casuale, False)
            print("  Salvati 4 naufraghi (non pagati a fine viaggio).")
            # Contenuto della cassa: tutte le merci aumentano tra 10 e 20
            for i in range(len(CATEGORIE_MERCI)):
                quantita_merci[i] = quantita_merci[i] + random.randint(10, 20)
            print("  La cassa era piena di merci! Tutte le merci sono aumentate.")
        else:
            print("  Hai lasciato andare la scialuppa.")
    elif nome_evento == "Epidemia":
        print("  Epidemia a bordo!")
        numero_medici = conta_membri_per_ruolo(lista_membri, "medico")
        indice_medicinali = indice_merce("medicinali")
        medicinali_disponibili = int(quantita_merci[indice_medicinali])
        # Determina chi si ammala (ogni non-medico ha 70% di probabilita')
        numero_ammalati = 0
        for membro in lista_membri:
            if membro["ruolo"] != "medico":
                if random.random() < 0.7:
                    numero_ammalati = numero_ammalati + 1
        numero_curati = 0
        numero_morti = 0
        if numero_ammalati == 0:
            print("  Nessuno si e' ammalato gravemente.")
        else:
            if numero_medici > 0 and medicinali_disponibili > 0:
                numero_curabili = min(numero_ammalati, medicinali_disponibili)
                quantita_merci[indice_medicinali] = quantita_merci[indice_medicinali] - numero_curabili
                numero_curati = numero_curabili
                numero_morti = numero_ammalati - numero_curati
            else:
                numero_morti = numero_ammalati
            if numero_morti > 0:
                rimossi = rimuovi_n_membri_non_medici(lista_membri, numero_morti)
                numero_morti = rimossi
            print(f"  Ammalati: {numero_ammalati} | Curati: {numero_curati} | Morti: {numero_morti}")
            print(f"  Medicinali rimasti: {int(quantita_merci[indice_medicinali])}")
    elif nome_evento == "Attacco pirata":
        numero_pirati = random.randint(3, 10)
        print(f"  Attacco pirata! La banda e' composta da {numero_pirati} pirati.")
        indice_armi = indice_merce("armi")
        numero_armi = int(quantita_merci[indice_armi])
        numero_vivi = conta_membri_vivi(lista_membri)
        numero_difensori = min(numero_armi, numero_vivi)
        # Le armi usate vengono rimosse
        quantita_merci[indice_armi] = quantita_merci[indice_armi] - numero_difensori
        uomini_persi = min(numero_pirati - numero_difensori, numero_vivi)
        if uomini_persi <= 0:
            print("  Attacco respinto senza vittime!")
        else:
            print(f"  Persi {uomini_persi} membri dell'equipaggio.")
            for _ in range(uomini_persi):
                rimuovi_membro_casuale(lista_membri)
        # Perdita casuale di merci
        for i in range(len(CATEGORIE_MERCI)):
            fattore = random.choice([0.0, 0.1, 0.25])
            perdita = quantita_merci[i] * fattore
            quantita_merci[i] = quantita_merci[i] - perdita
            if quantita_merci[i] < 0:
                quantita_merci[i] = 0.0
    elif nome_evento == "Danni al timone":
        print("  Danni al timone: servono riparazioni.")
        numero_meccanici = conta_membri_per_ruolo(lista_membri, "meccanico")
        if numero_meccanici > 0:
            print("  C'e' un meccanico a bordo: riparazione rapida (+1 settimana).")
            risultato["variazione_settimane"] = 1
        else:
            settimane_extra = random.randint(2, 4)
            print(f"  Nessun meccanico: riparazione lenta (+{settimane_extra} settimane).")
            risultato["variazione_settimane"] = settimane_extra
        risultato["variazione_morale_evento"] = -3
    elif nome_evento == "Raffiche di vento":
        print("  Raffiche di vento: la nave e' fuori rotta.")
        numero_navigatori = conta_membri_per_ruolo(lista_membri, "navigatore")
        if numero_navigatori > 0:
            print("  C'e' un navigatore a bordo: rotta corretta rapidamente (+1 settimana).")
            risultato["variazione_settimane"] = 1
        else:
            settimane_extra = random.randint(2, 4)
            print(f"  Nessun navigatore: si gira a vuoto (+{settimane_extra} settimane).")
            risultato["variazione_settimane"] = settimane_extra
        risultato["variazione_morale_evento"] = -3
    elif nome_evento == "Avvistamento isola":
        print("  Isola avvistata!")
        risposta = input("  Vuoi approdare sull'isola per un'ispezione? (s/n): ").strip().lower()
        while risposta != "s" and risposta != "n":
            risposta = input("  Rispondi s oppure n: ").strip().lower()
        if risposta == "n":
            print("  Hai deciso di non approdare.")
        else:
            # Il viaggio si allunga in ogni caso
            settimane_perse = random.randint(1, 2)
            risultato["variazione_settimane"] = settimane_perse
            # 50% abitata
            if random.random() < 0.5:
                print("  L'isola non e' abitata. Tempo perso.")
            else:
                # 50% ostili
                if random.random() < 0.5:
                    print("  Gli abitanti sono ostili! L'equipaggio viene messo in fuga.")
                else:
                    print("  Gli isolani sono amichevoli e donano merci!")
                    if albatri_avvistati > 0 and not albatro_ucciso:
                        minimo_dono = 20
                        massimo_dono = 40
                    else:
                        minimo_dono = 5
                        massimo_dono = 20
                    for i in range(len(CATEGORIE_MERCI)):
                        quantita_merci[i] = quantita_merci[i] + random.randint(minimo_dono, massimo_dono)
                    risultato["variazione_morale_evento"] = 5
    elif nome_evento == "Nessun imprevisto":
        print("  Settimana tranquilla, nessun imprevisto.")
    return risultato
def controlla_scorte(
    lista_membri,
    quantita_provviste,
    settimane_rimanenti,
    razioni_correnti,
    delta_morale
):
    """
    razioni_correnti[i] = moltiplicatore razione per la provvista i (1.0 normale, 0.5 dimezzata, ecc.)
    delta_morale = variazione morale accumulata per settimana (viene modificata qui)
    Restituisce delta_morale aggiornato.
    """
    numero_membri = conta_membri_vivi(lista_membri)
    for i in range(len(CATEGORIE_PROVVISTE)):
        nome_provvista = CATEGORIE_PROVVISTE[i]["nome"]
        consumo_base = CATEGORIE_PROVVISTE[i]["consumo"]
        consumo_settimana = consumo_base * razioni_correnti[i] * numero_membri
        quantita_provviste[i] = quantita_provviste[i] - consumo_settimana
        if quantita_provviste[i] < 0:
            quantita_provviste[i] = 0.0
        quantita_rimasta = quantita_provviste[i]
        if quantita_rimasta <= 0 and consumo_settimana > 0:
            print(f"  ATTENZIONE: {nome_provvista} ESAURITA! Morale -10 a settimana.")
            delta_morale = delta_morale - 10
        else:
            fabbisogno_futuro = consumo_base * razioni_correnti[i] * numero_membri * settimane_rimanenti
            if quantita_rimasta < fabbisogno_futuro and razioni_correnti[i] > 0.125:
                print(f"  Le scorte di {nome_provvista} non bastano per {settimane_rimanenti} settimane restanti.")
                print(f"  Rimaste: {round(quantita_rimasta, 2)} | Fabbisogno: {round(fabbisogno_futuro, 2)}")
                risposta = input(f"  Vuoi dimezzare le razioni di {nome_provvista}? (s/n): ").strip().lower()
                while risposta != "s" and risposta != "n":
                    risposta = input("  Rispondi s oppure n: ").strip().lower()
                if risposta == "s":
                    razioni_correnti[i] = razioni_correnti[i] * 0.5
                    delta_morale = delta_morale - 5
                    print(f"  Razioni di {nome_provvista} dimezzate. Morale -5 a settimana.")
            fabbisogno_doppio = consumo_base * razioni_correnti[i] * numero_membri * settimane_rimanenti * 2
            if quantita_rimasta >= fabbisogno_doppio and razioni_correnti[i] <= 1.0:
                print(f"  Le scorte di {nome_provvista} sono abbondanti!")
                risposta = input(f"  Vuoi raddoppiare le razioni di {nome_provvista}? (s/n): ").strip().lower()
                while risposta != "s" and risposta != "n":
                    risposta = input("  Rispondi s oppure n: ").strip().lower()
                if risposta == "s":
                    razioni_correnti[i] = razioni_correnti[i] * 2.0
                    delta_morale = delta_morale + 5
                    print(f"  Razioni di {nome_provvista} raddoppiate. Morale +5 a settimana.")
    return delta_morale
def aggiorna_morale(lista_membri, delta_morale, variazione_evento):
    """
    Applica delta_morale (accumulato) + variazione_evento (una tantum) a tutti i membri.
    Rimuove i membri con morale <= 0.
    Restituisce il numero di morti per morale.
    """
    variazione_totale = delta_morale + variazione_evento
    morti_per_morale = 0
    # Iteriamo al contrario per poter rimuovere senza problemi di indici
    i = len(lista_membri) - 1
    while i >= 0:
        lista_membri[i]["morale"] = lista_membri[i]["morale"] + variazione_totale
        if lista_membri[i]["morale"] > 100:
            lista_membri[i]["morale"] = 100
        if lista_membri[i]["morale"] <= 0:
            lista_membri.pop(i)
            morti_per_morale = morti_per_morale + 1
        i = i - 1
    return morti_per_morale
def mostra_riepilogo(lista_membri, quantita_provviste, quantita_merci):
    print()
    print("  --- RIEPILOGO FINE SETTIMANA ---")
    print(f"  Membri vivi: {conta_membri_vivi(lista_membri)}")
    for membro in lista_membri:
        print(f"    {membro['ruolo']} - morale: {membro['morale']}")
    print("  Provviste:")
    for i in range(len(CATEGORIE_PROVVISTE)):
        print(f"    {CATEGORIE_PROVVISTE[i]['nome']}: {round(quantita_provviste[i], 2)} {CATEGORIE_PROVVISTE[i]['unita']}")
    print("  Merci:")
    for i in range(len(CATEGORIE_MERCI)):
        print(f"    {CATEGORIE_MERCI[i]['descrizione']}: {round(quantita_merci[i], 2)}")
def calcola_ammutinamento(
    lista_membri,
    razioni_correnti,
    albatri_avvistati,
    albatro_ucciso,
    settimane_totali
):
    punteggio = 0
    cause = []
    razione_ridotta = False
    for i in range(len(CATEGORIE_PROVVISTE)):
        if razioni_correnti[i] < 1.0:
            razione_ridotta = True
    if razione_ridotta:
        punteggio = punteggio + 30
        cause.append("Razioni cibo ridotte (+30)")
    numero_cuochi = conta_membri_per_ruolo(lista_membri, "cuoco")
    if numero_cuochi == 0:
        punteggio = punteggio + 30
        cause.append("Nessun cuoco a bordo (+30)")
    if albatri_avvistati > 0 and albatro_ucciso:
        punteggio = punteggio + 30
        cause.append("Presagio di sfiga: albatro ucciso (+30)")
    if albatri_avvistati > 0 and not albatro_ucciso:
        punteggio = punteggio - 20
        cause.append("Ottimismo: albatro avvistato e rispettato (-20)")
    numero_vivi = conta_membri_vivi(lista_membri)
    if numero_vivi > 12:
        punteggio = punteggio + 30
        cause.append("La nave e' troppo affollata (+30)")

    # Settimane extra rispetto alle 8 base
    settimane_extra = settimane_totali - SETTIMANE_BASE
    if settimane_extra > 0:
        punteggio = punteggio + settimane_extra * 10
        cause.append(f"Viaggio troppo lungo: +{settimane_extra} settimane (+{settimane_extra * 10})")
    elif settimane_extra < 0:
        punteggio = punteggio + settimane_extra * 10  # sottrae
        cause.append(f"Viaggio accorciato: {settimane_extra} settimane ({settimane_extra * 10})")

    return punteggio, cause
def gestisci_ammutinamento(
    lista_membri,
    razioni_correnti,
    albatri_avvistati,
    albatro_ucciso,
    settimane_totali
):
    """
    Restituisce True se c'e' ammutinamento (gioco finisce), False altrimenti.
    """
    punteggio, cause = calcola_ammutinamento(
        lista_membri, razioni_correnti, albatri_avvistati, albatro_ucciso, settimane_totali
    )
    if punteggio >= 100:
        print()
        print("  !!! AMMUTINAMENTO !!! L'equipaggio abbandona la nave.")
        print("  Cause:")
        for causa in cause:
            print(f"    - {causa}")
        return True
    elif punteggio >= 1:
        print()
        print(f"  ATTENZIONE: rischio ammutinamento (punteggio: {punteggio}).")
        print("  Cause:")
        for causa in cause:
            print(f"    - {causa}")
    return False
def ricalcola_settimane_per_morale(lista_membri, settimane_totali):
    numero_vivi = conta_membri_vivi(lista_membri)
    if numero_vivi == 0:
        return settimane_totali
    numero_morale_basso = 0
    for membro in lista_membri:
        if membro["morale"] <= 30:
            numero_morale_basso = numero_morale_basso + 1
    if numero_morale_basso > numero_vivi / 2:
        print("  Piu' della meta' dell'equipaggio e' demoralizzata: viaggio +1 settimana.")
        settimane_totali = settimane_totali + 1
    return settimane_totali
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
def viaggio(
    lista_membri,
    quantita_provviste,
    quantita_merci,
    denari_rimasti,
    settimane_totali,
    settimana_di_partenza,
    contatore_eventi,
    albatri_avvistati,
    albatro_ucciso,
    razioni_correnti,
    delta_morale
):
    print()
    print("-------BENVENUTI-------")
    print("SI DA IL VIA AL VIAGGIO")
    print("-----BUONA FORTUNA-----")
    print(f"Durata stimata: {settimane_totali} settimane")
    settimana_corrente = settimana_di_partenza
    while settimana_corrente <= settimane_totali:
        print()
        print(f"=== SETTIMANA {settimana_corrente} di {settimane_totali} ===")
        nome_evento = scegli_evento(contatore_eventi)
        contatore_eventi[nome_evento] = contatore_eventi.get(nome_evento, 0) + 1
        risultato_evento = gestisci_evento(
            nome_evento,
            lista_membri,
            quantita_provviste,
            quantita_merci,
            settimane_totali,
            albatri_avvistati,
            albatro_ucciso
        )
        albatri_avvistati = albatri_avvistati + risultato_evento["albatri_avvistati_aggiunta"]
        if risultato_evento["albatro_ora_ucciso"]:
            albatro_ucciso = True
        variazione_settimane = risultato_evento["variazione_settimane"]
        if variazione_settimane != 0:
            settimane_totali = settimane_totali + variazione_settimane
            if settimane_totali < settimana_corrente:
                settimane_totali = settimana_corrente
            if variazione_settimane > 0:
                print(f"  Il viaggio si allunga di {variazione_settimane} settimana/e. Nuova durata: {settimane_totali}.")
            else:
                print(f"  Il viaggio si accorcia di {abs(variazione_settimane)} settimana/e. Nuova durata: {settimane_totali}.")
        if conta_membri_vivi(lista_membri) <= 0:
            print("Tutti i membri dell'equipaggio sono morti. GAME OVER.")
            return False, lista_membri, quantita_provviste, quantita_merci, settimane_totali, albatri_avvistati, albatro_ucciso, denari_rimasti
        settimane_rimanenti = settimane_totali - settimana_corrente
        delta_morale = controlla_scorte(
            lista_membri, quantita_provviste, settimane_rimanenti, razioni_correnti, delta_morale
        )
        variazione_evento = risultato_evento["variazione_morale_evento"]
        morti_morale = aggiorna_morale(lista_membri, delta_morale, variazione_evento)
        if morti_morale > 0:
            print(f"  {morti_morale} membre/i morto/i per morale a zero.")
        if conta_membri_vivi(lista_membri) <= 0:
            print("Tutti i membri dell'equipaggio sono morti. GAME OVER.")
            return False, lista_membri, quantita_provviste, quantita_merci, settimane_totali, albatri_avvistati, albatro_ucciso, denari_rimasti
        mostra_riepilogo(lista_membri, quantita_provviste, quantita_merci)
        ammutinamento = gestisci_ammutinamento(
            lista_membri, razioni_correnti, albatri_avvistati, albatro_ucciso, settimane_totali
        )
        if ammutinamento:
            return False, lista_membri, quantita_provviste, quantita_merci, settimane_totali, albatri_avvistati, albatro_ucciso, denari_rimasti
        settimane_totali = ricalcola_settimane_per_morale(lista_membri, settimane_totali)
        if settimana_corrente < settimane_totali:
            risposta = input("Vuoi salvare la partita? (s/n): ").strip().lower()
            while risposta != "s" and risposta != "n":
                risposta = input("Rispondi s oppure n: ").strip().lower()
            if risposta == "s":
                salva_partita(
                    lista_membri, quantita_provviste, quantita_merci,
                    settimane_totali, settimana_corrente,
                    contatore_eventi, albatri_avvistati, albatro_ucciso,
                    razioni_correnti, delta_morale, denari_rimasti
                )
        settimana_corrente = settimana_corrente + 1
    return True, lista_membri, quantita_provviste, quantita_merci, settimane_totali, albatri_avvistati, albatro_ucciso, denari_rimasti
