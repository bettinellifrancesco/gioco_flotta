import random
import time
import json
from datetime import datetime


FLOTTA_MAX = 16

MIN_PROV = 0.0


CONSUMO_VERDURA = 0.5
CONSUMO_FRUTTA = 1.0
CONSUMO_CARNE = 1.0
CONSUMO_ACQUA = 0.5


def mostra_menu_principale():
    print("-----------NUOVO MONDO-----------")
    print("1 - nuova partita")
    print("2 - carica vecchia partita")
    print("---------------------------------")


def acquista_equipaggio():
    
    print("------FASE 1: EQUIPAGGIO------")
    print("è il momento di ingaggiare la tua flotta!!")
    ruoli = [
        {"nome": "cuoco", "prezzo": 15},
        {"nome": "marinaio", "prezzo": 10},
        {"nome": "meccanico", "prezzo": 15},
        {"nome": "medico", "prezzo": 25},
        {"nome": "navigatore", "prezzo": 20},
    ]
    
    flotta = {r["nome"]: [] for r in ruoli}
    acquistati = 0
    ruoli_rimasti = len(ruoli)

    denari = 2000
    print(f"Denari disponibili per l'ingaggio: {denari}")

    # Prima fase: almeno 1 per ruolo
    for i in range(len(ruoli)):
        valido = False
        while not valido:
            try:
                massimo = FLOTTA_MAX - acquistati - (ruoli_rimasti - 1)
                n = int(input(f"Inserisci il numero di {ruoli[i]['nome']} (1-{massimo}): "))
                if n < 1 or n > massimo:
                    print(f"Numero non valido. Inserisci un valore tra 1 e {massimo}.")
                else:
                    costo = ruoli[i]["prezzo"] * n * 8
                    if costo > denari:
                        print(f"Denari insufficienti per {n} {ruoli[i]['nome']} (costo {costo}). Denari rimasti: {denari}")
                    else:
                        denari -= costo
                        for _ in range(n):
                            flotta[ruoli[i]["nome"]].append({"morale": 100, "pagato": True})
                        acquistati += n
                        ruoli_rimasti -= 1
                        print(f"Assunti {n} {ruoli[i]['nome']}. Denari rimasti: {denari}")
                        valido = True
            except ValueError:
                print("Inserisci un numero valido.")

    # Fase opzionale: aggiungi altri membri fino al massimo
    aggiungi_altro = True
    while aggiungi_altro and acquistati < FLOTTA_MAX:
        scelta_cont = input("Vuoi aggiungere altri personaggi? (s/n): ").strip().lower()
        if scelta_cont == 'n':
            aggiungi_altro = False
        elif scelta_cont != 's':
            print("Scelta non valida.")
        else:
            for idx, r in enumerate(ruoli, start=1):
                print(f"{idx} - {r['nome']}")
            scelta_valida = False
            while not scelta_valida:
                try:
                    scelta = int(input("Scegli il numero del personaggio: "))
                    if scelta < 1 or scelta > len(ruoli):
                        print("Scelta non valida.")
                    else:
                        scelta_valida = True
                except ValueError:
                    print("Inserisci un numero valido.")
            massimo = FLOTTA_MAX - acquistati
            n_valido = False
            while not n_valido:
                try:
                    n = int(input(f"Quanti {ruoli[scelta-1]['nome']} vuoi aggiungere? (1-{massimo}): "))
                    if n < 1 or n > massimo:
                        print(f"Numero non valido. Inserisci un valore tra 1 e {massimo}.")
                    else:
                        costo = ruoli[scelta-1]["prezzo"] * n * 8
                        if costo > denari:
                            print(f"Denari insufficienti per {n} {ruoli[scelta-1]['nome']} (costo {costo}). Denari rimasti: {denari}")
                        else:
                            denari -= costo
                            for _ in range(n):
                                flotta[ruoli[scelta-1]['nome']].append({"morale": 100, "pagato": True})
                            acquistati += n
                            print(f"Assunti {n} {ruoli[scelta-1]['nome']}. Denari rimasti: {denari}")
                            n_valido = True
                except ValueError:
                    print("Inserisci un numero valido.")

    print("\nFlotta finale:")
    tot = 0
    for v in flotta.values():
        tot += len(v)
    for k, v in flotta.items():
        print(f"  {k}: {len(v)}")
    print(f"Totale membri: {tot}/{FLOTTA_MAX}")
    return flotta, denari


def acquista_provviste(denari):
    print("------FASE 2: PROVVISTE------")
    provviste_list = [
        {"nome": "verdura", "um": "kg", "prezzo": 0.5},
        {"nome": "frutta", "um": "kg", "prezzo": 1},
        {"nome": "carne", "um": "kg", "prezzo": 2},
        {"nome": "acqua", "um": "barili", "prezzo": 0.5},
    ]
    provviste = {p["nome"]: 0.0 for p in provviste_list}
    print(f"Denari disponibili: {denari}")
    acquistando = True
    while acquistando:
        scelta = input("Vuoi acquistare provviste? (s/n): ").strip().lower()
        if scelta == 'n':
            acquistando = False
        elif scelta != 's':
            print("Scelta non valida.")
        else:
            for i, p in enumerate(provviste_list, start=1):
                print(f"{i} - {p['nome']} : {p['prezzo']} per {p['um']}")
            valido_merce = False
            while not valido_merce:
                try:
                    num = int(input("Inserisci il numero della provvista: "))
                    qty = float(input("Quanti (minimo 1): "))
                    if num < 1 or num > len(provviste_list) or qty < 1:
                        print("Hai inserito un numero o una quantità non valida.")
                    else:
                        costo = provviste_list[num-1]["prezzo"] * qty
                        if costo > denari:
                            print("Denari insufficienti.")
                        else:
                            denari -= costo
                            provviste[provviste_list[num-1]["nome"]] += qty
                            print(f"Acquistati {qty} {provviste_list[num-1]['um']} di {provviste_list[num-1]['nome']}. Denari rimasti: {denari}")
                            continua_acquisto = input("Vuoi acquistare altre provviste s/n: ").strip().lower()
                            while continua_acquisto != 's' and continua_acquisto != 'n':
                                print("Inserisci una scelta valida!!")
                                continua_acquisto = input("Vuoi acquistare altre provviste s/n: ").strip().lower()
                            if continua_acquisto == 'n':
                                valido_merce = True
                                acquistando = False
                            else:
                                valido_merce = True
                except ValueError:
                    print("Inserisci un numero valido.")
    return denari, provviste


def acquista_merci(denari):
    print("------FASE 3: MERCI------")
    merci_list = [
        {"key": "medicinali", "descr": "bottiglie di medicinale", "prezzo": 1, "um": "bottiglia"},
        {"key": "armi", "descr": "armi", "prezzo": 5, "um": "pezzo"},
        {"key": "sale", "descr": "sale", "prezzo": 0.5, "um": "sacco"},
        {"key": "stoffa", "descr": "stoffa", "prezzo": 2, "um": "telo"},
        {"key": "coltelli", "descr": "coltelli", "prezzo": 0.5, "um": "pezzo"},
        {"key": "diamanti", "descr": "diamanti", "prezzo": 1, "um": "pezzo"},
    ]
    merci = {}
    for m in merci_list:
        merci[m["key"]] = 0.0
    print(f"Denari disponibili: {denari}")
    acquistando = True
    while acquistando:
        scelta = input("Vuoi acquistare merci? (s/n): ").strip().lower()
        if scelta == 'n':
            acquistando = False
        elif scelta != 's':
            print("Scelta non valida.")
        else:
            for i, m in enumerate(merci_list, start=1):
                print(f"{i} - {m['descr']} : {m['prezzo']} per {m['um']}")
            valido_merce = False
            while not valido_merce:
                try:
                    num = int(input("Inserisci il numero della merce: "))
                    qty = float(input("Inserisci la quantità (minimo 1): "))
                    if num < 1 or num > len(merci_list) or qty < 1:
                        print("Hai inserito un numero o una quantità non valida.")
                    else:
                        costo = merci_list[num-1]["prezzo"] * qty
                        if costo > denari:
                            print("Denari insufficienti.")
                        else:
                            denari -= costo
                            merci[merci_list[num-1]["key"]] += qty
                            print(f"Acquistati {qty} {merci_list[num-1]['um']} di {merci_list[num-1]['descr']}. Denari rimasti: {denari}")
                            continua_acq = input("Vuoi acquistare altre merci s/n: ").strip().lower()
                            while continua_acq != 's' and continua_acq != 'n':
                                print("Inserisci una scelta valida!!")
                                continua_acq = input("Vuoi acquistare altre merci s/n: ").strip().lower()
                            if continua_acq == 'n':
                                valido_merce = True
                                acquistando = False
                            else:
                                valido_merce = True
                except ValueError:
                    print("Inserisci un numero valido.")
    return denari, merci


def salva_partita_su_file(stato, filename="salvataggio.json"):
    try:
        with open(filename, 'w') as f:
            json.dump(stato, f, indent=2)
        print(f"Partita salvata su '{filename}'.")
    except Exception as e:
        print(f"Errore durante il salvataggio: {e}")


def carica_partita_da_file(filename="salvataggio.json"):
    try:
        with open(filename, 'r') as f:
            stato = json.load(f)
        print(f"Caricamento da '{filename}' riuscito.")
        return stato
    except FileNotFoundError:
        print("Nessun salvataggio trovato.")
        return {}
    except Exception as e:
        print(f"Errore durante il caricamento: {e}")
        return {}


def shop():
    denari = 2000
    flotta, denari = acquista_equipaggio()
    denari, provviste = acquista_provviste(denari)
    denari, merci = acquista_merci(denari)
    print(f"Perfetto, ora sei pronto per il viaggio!! Denari rimasti: {denari}")
    return flotta, provviste, merci, denari


def viaggio(flotta, provviste, merci, settimane_totali=8, stato=None, interattivo=True):
    eventi = [
        {"nome": "Uomo in mare", "ripetibile": False, "peso": 1},
        {"nome": "Verdura in mare", "ripetibile": False, "peso": 2},
        {"nome": "Frutta in mare", "ripetibile": False, "peso": 2},
        {"nome": "Carne in mare", "ripetibile": False, "peso": 2},
        {"nome": "Acqua in mare", "ripetibile": False, "peso": 2},
        {"nome": "Pesca miracolosa", "ripetibile": False, "peso": 1},
        {"nome": "Tempesta miracolosa", "ripetibile": False, "peso": 1},
        {"nome": "Venti favorevoli", "ripetibile": True, "peso": 3},
        {"nome": "Cattivo tempo", "ripetibile": False, "peso": 2},
        {"nome": "Ondata", "ripetibile": False, "peso": 1},
        {"nome": "Infestazione ratti", "ripetibile": False, "peso": 2},
        {"nome": "Avvistamento albatro", "ripetibile": True, "limite": 3, "peso": 2},
        {"nome": "Avvistamento scialuppa", "ripetibile": False, "peso": 1},
        {"nome": "Epidemia", "ripetibile": False, "peso": 1},
        {"nome": "Attacco pirata", "ripetibile": False, "peso": 1},
        {"nome": "Danni al timone", "ripetibile": False, "peso": 2},
        {"nome": "Raffiche di vento", "ripetibile": False, "peso": 2},
        {"nome": "Avvistamento isola", "ripetibile": False, "peso": 1},
        {"nome": "Nessun imprevisto", "ripetibile": True, "peso": 3},
    ]

    # inizializza stato: usa lo stato caricato se presente
    if stato and isinstance(stato, dict):
        settimana_corrente = stato.get("settimana_corrente", 1)
        conta_eventi = stato.get("conta_eventi", {})
        storia_eventi = stato.get("storia_eventi", [])
    else:
        settimana_corrente = 1
        conta_eventi = {}
        storia_eventi = []
    stima_iniziale = settimane_totali

    # Stato extra
    razioni = {"verdura": 1.0, "frutta": 1.0, "carne": 1.0, "acqua": 1.0}
    albatro_avvistamenti = 0
    albatro_ucciso = False

    print("-------BENVENUTI-------")
    print("SI DA IL VIA AL VIAGGIO")
    print("-----BUONA FORTUNA-----")
    print(f"Durata stimata: {settimane_totali} settimane")

    # Assicuriamoci che le provviste siano presenti
    for key in ("verdura", "frutta", "carne", "acqua"):
        if key not in provviste:
            provviste[key] = 0.0

    def frazione_a_testo(frazione):
        d = frazione - 0.5
        if d < 0:
            d = -d
        if d < 1e-9:
            return "1/2"
        d = frazione - (1/3)
        if d < 0:
            d = -d
        if d < 1e-9:
            return "1/3"
        d = frazione - 0.25
        if d < 0:
            d = -d
        if d < 1e-9:
            return "1/4"
        d = frazione - 0.2
        if d < 0:
            d = -d
        if d < 1e-9:
            return "1/5"
        return f"{int(frazione * 100)}%"

    def conta_membri_vivi():
        totale = 0
        for lista in flotta.values():
            totale += len(lista)
        return totale

    def scegli_evento():
        disponibili = []
        pesi = []
        for e in eventi:
            nome = e["nome"]
            occorrenze = conta_eventi.get(nome, 0)
            aggiungi = True
            if not e.get("ripetibile", False) and occorrenze > 0:
                aggiungi = False
            if e.get("limite") is not None and occorrenze >= e["limite"]:
                aggiungi = False
            if aggiungi:
                disponibili.append(e)
                pesi.append(e.get("peso", 1))
        if not disponibili:
            return random.choice(eventi)
        return random.choices(disponibili, weights=pesi, k=1)[0]

    def rimuovi_membro_casuale():
        ruoli_disponibili = []
        for r, lst in flotta.items():
            if len(lst) > 0:
                ruoli_disponibili.append(r)
        if len(ruoli_disponibili) == 0:
            return "", {}
        ruolo = random.choice(ruoli_disponibili)
        idx = random.randrange(len(flotta[ruolo]))
        membro = flotta[ruolo].pop(idx)
        return ruolo, membro

    def aggiungi_membro(ruolo, morale, pagato):
        if ruolo not in flotta:
            flotta[ruolo] = []
        flotta[ruolo].append({"morale": morale, "pagato": pagato})

    def rimuovi_n_membri_non_medici(n):
        rimossi = []
        while n > 0:
            candidati = []
            for r in flotta.keys():
                if r != "medico" and len(flotta[r]) > 0:
                    candidati.append(r)
            if len(candidati) == 0:
                n = 0
            else:
                ruolo = random.choice(candidati)
                idx = random.randrange(len(flotta[ruolo]))
                flotta[ruolo].pop(idx)
                rimossi.append(ruolo)
                n -= 1
        return rimossi

    def gestisci_evento(evt):
        nome = evt["nome"]
        conta_eventi[nome] = conta_eventi.get(nome, 0) + 1
        storia_eventi.append(nome)
        data_e_ora = str(datetime.now())
        print(f"[" + data_e_ora + "] Settimana " + {settimana_corrente} + ": " + nome)
        risultato = {}

        # mappa per gli eventi che causano perdite in mare
        in_mare_map = {
            "Verdura in mare": "verdura",
            "Frutta in mare": "frutta",
            "Carne in mare": "carne",
            "Acqua in mare": "acqua",
        }

        if nome == "Uomo in mare":
            ruolo, membro = rimuovi_membro_casuale()
            if ruolo == "":
                print("Non c'era nessuno a bordo da perdere.")
            else:
                print("Tragico: un " + ruolo + " è finito in mare e non ce l'ha fatta.")
                risultato["morto"] = ruolo
            return risultato

        if nome in in_mare_map:
            fraz = random.choice([0.5, 1/3, 0.25, 0.2])
            tipo = in_mare_map[nome]
            quantita = provviste.get(tipo, 0)
            perdita = quantita * fraz
            nuovo_val = quantita - perdita
            if nuovo_val < 0:
                nuovo_val = 0.0
            provviste[tipo] = nuovo_val
            print(f"Perdita di " + frazione_a_testo(fraz) + " della scorta (" + tipo + "): -" + {round(perdita, 2)} + " " + tipo + ".")
            risultato["perdita_tipo"] = tipo
            risultato["perdita_frac"] = fraz
            risultato["perdita_qty"] = perdita
            return risultato

        if nome == "Pesca miracolosa":
            kg = random.randint(11, 20)
            provviste["carne"] = provviste.get("carne", 0) + kg
            print(f"Pesca miracolosa: raccolti circa " + {kg} + " kg di pesce (aggiunti a 'carne').")
            risultato["pesca_kg"] = kg
            risultato["morale_variazione"] = 5
            return risultato

        if nome == "Tempesta miracolosa":
            aggiunta = random.randint(11, 20)
            provviste["acqua"] = provviste.get("acqua", 0) + aggiunta
            print(f"Tempesta miracolosa: alcuni membri hanno raccolto acqua! +" +{aggiunta} + " barili.")
            risultato["acqua_aggiunta"] = aggiunta
            return risultato

        if nome == "Venti favorevoli":
            morale_gain = random.randint(5, 15)
            if settimane_totali - settimana_corrente >= 1:
                print(f"Venti favorevoli: il viaggio procede più velocemente (-1 settimana). Morale +" +{morale_gain} + ".")
                risultato["accorcia_settimane"] = 1
                risultato["morale_variazione"] = morale_gain
            else:
                print(f"Venti favorevoli, ma il beneficio è minimo. Morale +" +{morale_gain} + ".")
                risultato["morale_variazione"] = morale_gain
            return risultato

        if nome == "Cattivo tempo":
            fraz = random.choice([0.5, 1/3, 0.25, 0.2])
            perdita = merci.get("medicinali", 0) * fraz
            nuovo_med = merci.get("medicinali", 0) - perdita
            if nuovo_med < 0:
                nuovo_med = 0
            merci["medicinali"] = nuovo_med
            print(f"Cattivo tempo: parte delle bottiglie di medicinale si rovescia (-" + frazione_a_testo(fraz) + "). Perduta: " + {round(perdita, 2)} + ".")
            risultato["perdita_medicinali"] = perdita
            risultato["morale_variazione"] = -3
            return risultato
        if nome == "Ondata":
            fraz = random.choice([0.5, 1/3, 0.25, 0.2])
            perdita = merci.get("armi", 0) * fraz
            nuovo_armi = merci.get("armi", 0) - perdita
            if nuovo_armi < 0:
                nuovo_armi = 0
            merci["armi"] = nuovo_armi
            print(f"Ondata: parte delle armi è finita in mare (-" + frazione_a_testo(fraz) + "). Perduta: " + {round(perdita, 2)} + ".")
            risultato["onde_perdita_frac"] = fraz
            risultato["onde_perdita_tipo"] = "armi"
            risultato["morale_variazione"] = -3
            return risultato

        if nome == "Infestazione ratti":
            fraz = random.choice([0.5, 1/3, 0.25, 0.2])
            perdita = merci.get("stoffa", 0) * fraz
            if perdita > 0:
                nuovo_stoffa = merci.get("stoffa", 0) - perdita
                if nuovo_stoffa < 0:
                    nuovo_stoffa = 0
                merci["stoffa"] = nuovo_stoffa
            print("Infestazione di ratti: alcune stoffe sono state rovinate.")
            risultato["ratti"] = [("stoffa", perdita)] if perdita > 0 else []
            risultato["morale_variazione"] = -2
            return risultato

        if nome == "Avvistamento albatro":
            # non modifichiamo direttamente albatro_avvistamenti: restituiamo l'incremento
            risultato["albatro_inc"] = 1
            print("Albatro avvistato: buon auspicio per l'equipaggio.")
            risultato["albatro_avvistato"] = True
            num_armi = merci.get("armi", 0)
            membri_vivi = conta_membri_vivi()
            if num_armi >= 1 and membri_vivi > 0:
                print("Hai armi a bordo. Puoi provare a sparare all'albatro per ottenere carne.")
                print("Attenzione: le armi usate non potranno essere barattate e saranno rimosse dalle merci.")
                scelta = input("Vuoi provare a sparare all'albatro? (s/n): ").strip().lower()
                if scelta == 's':
                    if num_armi < membri_vivi:
                        tentativi = int(num_armi)
                    else:
                        tentativi = int(membri_vivi)
                    print(f"Hai a disposizione " + {tentativi} + " colpi (min(numero armi, membri vivi)).")
                    colpi = tentativi
                    successi = 0
                    for _ in range(colpi):
                        if random.random() < 0.5:
                            successi += 1
                    nuovo_armi = merci.get("armi", 0) - colpi
                    if nuovo_armi < 0:
                        nuovo_armi = 0
                    merci["armi"] = nuovo_armi
                    risultato["armi_usate"] = colpi
                    if successi > 0:
                        aggiunta_carne = random.randint(10, 15)
                        provviste["carne"] = provviste.get("carne", 0) + aggiunta_carne
                        print(f"Albatro abbattuto! +" + {aggiunta_carne} + " kg di carne.")
                        risultato["albatro_ucciso"] = True
                    else:
                        print("Hai sparato ma l'albatro non è stato abbattuto.")
                        risultato["albatro_ucciso"] = False
                else:
                    print("Hai deciso di non sparare all'albatro.")
            else:
                print("Non ci sono armi o non ci sono abbastanza persone per provare a sparare.")
            return risultato

        if nome == "Avvistamento scialuppa":
            print("Scialuppa alla deriva con 4 uomini e una cassa: vuoi salvare i naufraghi?")
            scelta = input("Salvare i 4 uomini? (s/n): ").strip().lower()
            if scelta == 's':
                ruoli_possibili = list(flotta.keys())
                for _ in range(4):
                    ruolo = random.choice(ruoli_possibili)
                    morale_nuovo = random.randint(25, 75)
                    aggiungi_membro(ruolo, morale_nuovo, False)
                for k in merci:
                    if k in ("medicinali", "armi", "sale", "stoffa", "coltelli", "diamanti"):
                        aggiunta = random.randint(10, 20)
                        merci[k] = merci.get(k, 0) + aggiunta
                print("Hai salvato 4 uomini; sono stati aggiunti alla flotta (non pagati). Cassa svuotata nelle merci.")
                risultato["scialuppa_salvata"] = 4
            else:
                print("Hai lasciato la scialuppa al largo. Niente saldo.")
            return risultato

        if nome == "Epidemia":
            lista_malati = []
            for ruolo in flotta:
                if ruolo != "medico":
                    membri = flotta[ruolo]
                    for _ in range(len(membri)):
                        if random.random() < 0.7:
                            lista_malati.append(ruolo)
            if not lista_malati:
                print("Epidemia: nessuno si è ammalato in modo fatale.")
                risultato["ammalati"] = 0
                return risultato
            medici = 0
            if flotta.get("medico"):
                medici = len(flotta["medico"])
            medicinali_disponibili = merci.get("medicinali", 0)
            ammalati = len(lista_malati)
            curati = 0
            morti = []
            if medici > 0 and medicinali_disponibili > 0:
                if ammalati < medicinali_disponibili:
                    curabili = ammalati
                else:
                    curabili = int(medicinali_disponibili)
                nuovo_med = merci.get("medicinali", 0) - curabili
                if nuovo_med < 0:
                    nuovo_med = 0
                merci["medicinali"] = nuovo_med
                curati = curabili
                da_odiare = ammalati - curati
                if da_odiare > 0:
                    morti = rimuovi_n_membri_non_medici(da_odiare)
            else:
                morti = rimuovi_n_membri_non_medici(ammalati)
            print(f"Epidemia: ammalati " + {ammalati} + ", curati " + {curati} + ", morti " + {len(morti)} + ". Medicinali rimanenti: " + {medicinali_disponibili})
            risultato["ammalati"] = ammalati
            risultato["curati"] = curati
            risultato["morti"] = morti
            return risultato

        if nome == "Attacco pirata":
            numero_pirati = random.randint(3, 10)
            membri_vivi = conta_membri_vivi()
            num_armi = merci.get("armi", 0)
            if num_armi < membri_vivi:
                numero_difensori = int(num_armi)
            else:
                numero_difensori = membri_vivi
            nuovo_armi = merci.get("armi", 0) - numero_difensori
            if nuovo_armi < 0:
                nuovo_armi = 0
            merci["armi"] = nuovo_armi
            perdite = []
            uomini_persi_calc = numero_pirati - numero_difensori
            if uomini_persi_calc > 0:
                if uomini_persi_calc < membri_vivi:
                    uomini_persi = uomini_persi_calc
                else:
                    uomini_persi = membri_vivi
                for _ in range(uomini_persi):
                    ruolo, membro = rimuovi_membro_casuale()
                    if ruolo:
                        perdite.append(ruolo)
                print(f"Attacco pirata! Persi " + {len(perdite)} + " membri.")
            else:
                print("Attacco pirata respinto senza vittime!")
            perdite_merci = []
            for k in merci:
                perdita = merci[k] * random.choice([0.0, 0.1, 0.25])
                if perdita > 0:
                    nuovo_k = merci[k] - perdita
                    if nuovo_k < 0:
                        nuovo_k = 0
                    merci[k] = nuovo_k
                    perdite_merci.append((k, perdita))
            risultato["pirati_morti"] = perdite
            risultato["pirati_perdite_merci"] = perdite_merci
            risultato["armi_usate"] = numero_difensori
            return risultato

        if nome == "Danni al timone":
            print("Danni al timone: servono riparazioni.")
            if flotta.get("meccanico"):
                print("C'è un meccanico a bordo: riparazione più veloce (+1 settimana).")
                risultato["aggiungi_settimane"] = 1
            else:
                aggiungi = random.randint(2, 4)
                print(f"Nessun meccanico: riparazione lunga (+" + {aggiungi} + " settimane).")
                risultato["aggiungi_settimane"] = aggiungi
            risultato["morale_variazione"] = -3
            return risultato

        if nome == "Raffiche di vento":
            print("Raffiche di vento: rotta allungata e difficoltà.")
            if flotta.get("navigatore"):
                print("C'è un navigatore: impatto ridotto (+1 settimana).")
                risultato["aggiungi_settimane"] = 1
            else:
                aggiungi = random.randint(2, 4)
                print(f"Nessun navigatore: devi allungare la rotta (+" + {aggiungi} + " settimane).")
                risultato["aggiungi_settimane"] = aggiungi
            risultato["morale_variazione"] = -3
            return risultato

        if nome == "Avvistamento isola":
            print("Isola avvistata: vuoi approdare per ispezionare?")
            scelta = input("Approdi sull'isola? (s/n): ").strip().lower()
            if scelta != 's':
                print("Decidi di non approdare.")
                return risultato
            if random.random() < 0.5:
                print("L'isola non è abitata. Nulla di fatto, ma tempo perso.")
                risultato["aggiungi_settimane"] = 1
                return risultato
            if random.random() < 0.5:
                print("Gli abitanti sono ostili e mettono in fuga l'equipaggio.")
                risultato["aggiungi_settimane"] = 1
                return risultato
            print("Isola amichevole: gli isolani donano merci.")
            bonus_min = 5
            bonus_max = 20
            if albatro_avvistamenti > 0 and not albatro_ucciso:
                bonus_min = 20
                bonus_max = 40
            for k in merci:
                if k in ("medicinali", "armi", "sale", "stoffa", "coltelli", "diamanti"):
                    aggiunta = random.randint(bonus_min, bonus_max)
                    merci[k] = merci.get(k, 0) + aggiunta
            risultato["aggiungi_settimane"] = random.randint(1, 2)
            risultato["isola_donazioni"] = True
            risultato["morale_variazione"] = 5
            return risultato

        if nome == "Nessun imprevisto":
            print("Settimana tranquilla: nessun imprevisto.")
            return risultato

        print("Evento non gestito.")
        return risultato

    def anima_nave():
        pista = 20
        passi = pista + 1
        durata_settimana = 2.0  # secondi per settimana (ridotto per test più veloci)
        ritardo = durata_settimana / passi
        meta = passi // 2
        for posizione in range(passi):
            onde = "~" * posizione
            print(onde + "⛵")
            if posizione == meta:
                risposta_valida = False
                while not risposta_valida:
                    risposta = input("Vuoi saltare questa settimana? (y/n): ").strip().lower()
                    if risposta == 'y':
                        return True
                    elif risposta == 'n':
                        risposta_valida = True
                    else:
                        print("Rispondi 'y' per sì oppure 'n' per no.")
                time.sleep(ritardo)
            else:
                time.sleep(ritardo)
        return False

    risultati = []
    while settimana_corrente <= settimane_totali:
        print(f"--- SETTIMANA " + {settimana_corrente} + " di " + {settimane_totali} + " ---")
        evento_scelto = scegli_evento()
        risultato = gestisci_evento(evento_scelto)
        # applica aggiornamenti di stato restituiti dall'evento
        if risultato.get("albatro_inc"):
            albatro_avvistamenti = albatro_avvistamenti + risultato.get("albatro_inc", 0)
        if "albatro_ucciso" in risultato:
            albatro_ucciso = bool(risultato.get("albatro_ucciso"))
        risultati.append({"settimana": settimana_corrente, "evento": evento_scelto["nome"], "risultato": risultato})

        # Se tutta la flotta è stata annientata, termina la partita
        totale_membri = 0
        for lista in flotta.values():
            totale_membri += len(lista)
        if totale_membri <= 0:
            print("Tutti i membri della flotta sono morti. Il viaggio è fallito. GAME OVER")
            return {"settimane": settimane_totali, "risultati": risultati, "conteggi": conta_eventi, "storia": storia_eventi, "morto": True}

        # applica modifiche temporali
        if "aggiungi_settimane" in risultato:
            aggiungi = risultato["aggiungi_settimane"]
            settimane_totali += aggiungi
            print(f"Il viaggio si allunga di {aggiungi} settimana/e. Nuova durata stimata: {settimane_totali} settimane.")
        if "accorcia_settimane" in risultato:
            acc = risultato["accorcia_settimane"]
            nuovo_val = settimane_totali - acc
            if nuovo_val < settimana_corrente:
                settimane_totali = settimana_corrente
            else:
                settimane_totali = nuovo_val
            print(f"Il viaggio si accorcia di {acc} settimana/e. Nuova durata stimata: {settimane_totali} settimane.")

        # applica variazione di morale a tutti i membri, se presente
        if "morale_variazione" in risultato:
            varia = risultato["morale_variazione"]
            if varia != 0:
                for lista in flotta.values():
                    for membro in lista:
                        membro_morale = membro.get("morale", 0)
                        nuovo = membro_morale + varia
                        if nuovo > 100:
                            nuovo = 100
                        if nuovo < 0:
                            nuovo = 0
                        membro["morale"] = nuovo
                print(f"Morale modificato di {varia} per tutti i membri.")

        if interattivo:
            saltata = anima_nave()
            if saltata:
                print("Settimana saltata dall'utente.")
        else:
            print("(modalità non interattiva: salto animazione)")

        # Alla fine della settimana (esclusa l'ultima) offrire salvataggio
        if interattivo and settimana_corrente < settimane_totali:
            scelta_salvataggio_valida = False
            while not scelta_salvataggio_valida:
                scelta_salva = input("Vuoi salvare la partita? (s/n): ").strip().lower()
                if scelta_salva == 's':
                    stato_da_salvare = {
                        'flotta': flotta,
                        'provviste': provviste,
                        'merci': merci,
                        'settimane_totali': settimane_totali,
                        'settimana_corrente': settimana_corrente,
                        'conta_eventi': conta_eventi,
                        'storia_eventi': storia_eventi,
                        'albatro_avvistamenti': albatro_avvistamenti,
                        'albatro_ucciso': albatro_ucciso,
                    }
                    salva_partita_su_file(stato_da_salvare)
                    scelta_salvataggio_valida = True
                elif scelta_salva == 'n':
                    scelta_salvataggio_valida = True
                else:
                    print("Scelta non valida. Rispondi 's' o 'n'.")

        settimana_corrente += 1

    print("RIEPILOGO DEL VIAGGIO")
    if conta_eventi:
        print("- Eventi registrati:")
        for nome in conta_eventi:
            print(f" - " + {nome} + ": " + {conta_eventi[nome]} + " volta/e")
    else:
        print("Nessun evento registrato.")
    print("Stato finale flotta:")
    for ruolo in flotta:
        print(f"  " +{ruolo} + ": " + {len(flotta[ruolo])} + " membri")
    print("Stato finale provviste:")
    for k in provviste:
        print(f"  " + {k} + ": " + {round(provviste[k], 2)})
    print("Stato finale merci:")
    for k in merci:
        print(f"  " + {k} + ": " + {round(merci[k], 2)})
    print("Simulazione completata.")
    return {"settimane": settimane_totali, "risultati": risultati, "conteggi": conta_eventi, "storia": storia_eventi}


def main():
    mostra_menu_principale()
    scelta_corretta = False
    while not scelta_corretta:
        scelta = input("Benvenuto in NUOVO MONDO!! Scegli: ").strip()
        if scelta == "1":
            scelta_corretta = True
            flotta, provviste, merci, denari = shop()
            viaggio(flotta, provviste, merci, settimane_totali=8, interattivo=True)
        elif scelta == "2":
            scelta_corretta = True
            stato = carica_partita_da_file()
            if not stato:
                print("Nessun salvataggio trovato. Avvio nuova partita.")
                flotta, provviste, merci, denari = shop()
                viaggio(flotta, provviste, merci, settimane_totali=8, interattivo=True)
            else:
                loaded_flotta = stato.get('flotta', {})
                loaded_provviste = stato.get('provviste', {})
                loaded_merci = stato.get('merci', {})
                settimane_totali = stato.get('settimane_totali', 8)
                viaggio(loaded_flotta, loaded_provviste, loaded_merci, settimane_totali=settimane_totali, stato=stato, interattivo=True)
        else:
            print("Errore d'inserimento")


main()















   