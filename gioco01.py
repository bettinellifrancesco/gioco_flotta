import json
import random

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

def arrivo_nuovo_mondo(lista_membri, quantita_merci):
    print()
    print("=== ARRIVO NEL NUOVO MONDO ===")
    print("La nave si avvicina alla costa. Alcuni indigeni armati vi osservano.")
    indice_armi = indice_merce("armi")
    numero_armi = int(quantita_merci[indice_armi])
    if numero_armi >= 1:
        risposta = input("L'equipaggio chiede: vuoi aprire il fuoco sugli indigeni? (s/n): ").strip().lower()
        while risposta != "s" and risposta != "n":
            risposta = input("Rispondi s oppure n: ").strip().lower()
        if risposta == "s":
            print("Hai aperto il fuoco. Gli indigeni reagiscono e sterminano l'equipaggio. GAME OVER.")
            return False
    print("Sbarcate nel nuovo mondo. Gli indigeni vi accolgono con entusiasmo!")
    return True

def esegui_baratto(quantita_merci):
    print()
    print("=== BARATTO ===")
    print("Il capo tribu' vuole barattare sale, stoffa, coltelli e diamanti.")
    print("Non vuole ne' armi ne' medicinali.")
    numero_perle = 0.0
    numero_manufatti = 0.0
    numero_spezie = 0.0
    for nome_merce in NOMI_MERCI_BARATTABILI:
        indice = indice_merce(nome_merce)
        quantita_disponibile = quantita_merci[indice]
        if quantita_disponibile <= 0:
            print(f"  Non hai {nome_merce}: baratto saltato.")
            continue
        print()
        print(f"  Baratto di {nome_merce} ({round(quantita_disponibile, 2)} disponibili):")
        rapporto_perla    = TABELLA_BARATTO[nome_merce]["perla"]
        rapporto_manufatto = TABELLA_BARATTO[nome_merce]["manufatto"]
        rapporto_spezia   = TABELLA_BARATTO[nome_merce]["spezia"]
        offerta_perle     = quantita_disponibile / rapporto_perla
        offerta_manufatti = quantita_disponibile / rapporto_manufatto
        offerta_spezie    = quantita_disponibile / rapporto_spezia
        guadagno_perle     = offerta_perle * VALORE_BENI_INDIGENI["perla"]
        guadagno_manufatti = offerta_manufatti * VALORE_BENI_INDIGENI["manufatto"]
        guadagno_spezie    = offerta_spezie * VALORE_BENI_INDIGENI["spezia"]
        print(f"  1) {int(offerta_perle)} perle     (profitto stimato: {round(guadagno_perle, 2)} monete)")
        print(f"  2) {int(offerta_manufatti)} manufatti (profitto stimato: {round(guadagno_manufatti, 2)} monete)")
        print(f"  3) {int(offerta_spezie)} spezie    (profitto stimato: {round(guadagno_spezie, 2)} monete)")
        scelta_valida = False
        while not scelta_valida:
            try:
                scelta = int(input("  Scegli l'opzione (1/2/3): "))
                if scelta == 1:
                    numero_perle = numero_perle + offerta_perle
                    print(f"  Ottenute {int(offerta_perle)} perle.")
                    scelta_valida = True
                elif scelta == 2:
                    numero_manufatti = numero_manufatti + offerta_manufatti
                    print(f"  Ottenuti {int(offerta_manufatti)} manufatti.")
                    scelta_valida = True
                elif scelta == 3:
                    numero_spezie = numero_spezie + offerta_spezie
                    print(f"  Ottenuti {int(offerta_spezie)} spezie.")
                    scelta_valida = True
                else:
                    print("  Scegli 1, 2 o 3.")
            except ValueError:
                print("  Inserisci un numero valido.")
        quantita_merci[indice] = 0.0

    return numero_perle, numero_manufatti, numero_spezie

def gestisci_tradimento(quantita_merci, numero_perle, albatri_avvistati, albatro_ucciso):
    indice_armi = indice_merce("armi")
    numero_armi = int(quantita_merci[indice_armi])
    if numero_armi <= 0:
        return numero_perle, True
    print()
    print("=== IL TRADIMENTO ===")
    print(f"Durante la notte un rivale del capo tribu' ti offre 30 perle per ogni arma ({numero_armi} armi = {numero_armi * 30} perle).")
    risposta = input("Accetti l'offerta? (s/n): ").strip().lower()
    while risposta != "s" and risposta != "n":
        risposta = input("Rispondi s oppure n: ").strip().lower()
    if risposta == "s":
        numero_perle = numero_perle + numero_armi * 30
        quantita_merci[indice_armi] = 0.0
        print(f"Hai consegnato le armi. Ricevute {numero_armi * 30} perle.")
        if albatri_avvistati > 0 and albatro_ucciso:
            print("Il capo tribu' scopre il tradimento (presagio di sfiga). L'equipaggio viene sterminato. GAME OVER.")
            return numero_perle, False
        elif albatri_avvistati > 0 and not albatro_ucciso:
            print("L'albatro ti porta fortuna: non vieni scoperto.")
            return numero_perle, True
        else:
            if random.random() < 0.5:
                print("Il capo tribu' scopre il tradimento. L'equipaggio viene sterminato. GAME OVER.")
                return numero_perle, False
            else:
                print("Non sei stato scoperto. Il gioco continua.")
                return numero_perle, True
    else:
        if albatri_avvistati > 0 and albatro_ucciso:
            dono = random.randint(5, 20)
        else:
            dono = random.randint(30, 50)
        numero_perle = numero_perle + dono
        print(f"Il capo tribu' ti ringrazia con {dono} perle.")
        return numero_perle, True

def epilogo_ritorno(lista_membri, quantita_provviste, albatri_avvistati, albatro_ucciso):
    print()
    print("=== EPILOGO ===")
    print("Il capo tribu' rifornisce la nave di provviste per 3 settimane di ritorno.")
    numero_membri = conta_membri_vivi(lista_membri)
    for i in range(len(CATEGORIE_PROVVISTE)):
        consumo = CATEGORIE_PROVVISTE[i]["consumo"]
        quantita_provviste[i] = consumo * numero_membri * 3
    print("Provviste caricate per 3 settimane.")
    numero_navigatori = conta_membri_per_ruolo(lista_membri, "navigatore")
    if numero_navigatori > 0:
        settimane_ritorno = 1
    else:
        settimane_ritorno = 2
    if albatri_avvistati > 0 and albatro_ucciso:
        settimane_ritorno = settimane_ritorno + 1
    print(f"L'isola piu' vicina dista {settimane_ritorno} settimana/e.")
    return settimane_ritorno

def calcola_profitti(numero_perle,numero_manufatti,numero_spezie,lista_membri_originali_ingaggiati,settimane_effettive,denari_rimasti):
    print()
    print("=== RIENTRO IN PATRIA - CALCOLO PROFITTI ===")
    fattore_mercato = random.choice([0.5, 1.0, 2.0])
    print(f"Fattore di mercato attuale: x{fattore_mercato}")
    valore_perle     = numero_perle * VALORE_BENI_INDIGENI["perla"] * fattore_mercato
    valore_manufatti = numero_manufatti * VALORE_BENI_INDIGENI["manufatto"] * fattore_mercato
    valore_spezie    = numero_spezie * VALORE_BENI_INDIGENI["spezia"] * fattore_mercato
    profitto_totale  = valore_perle + valore_manufatti + valore_spezie
    print(f"  Perle: {int(numero_perle)} x {VALORE_BENI_INDIGENI['perla'] * fattore_mercato} = {round(valore_perle, 2)} monete")
    print(f"  Manufatti: {int(numero_manufatti)} x {VALORE_BENI_INDIGENI['manufatto'] * fattore_mercato} = {round(valore_manufatti, 2)} monete")
    print(f"  Spezie: {int(numero_spezie)} x {VALORE_BENI_INDIGENI['spezia'] * fattore_mercato} = {round(valore_spezie, 2)} monete")
    print(f"  Profitto totale: {round(profitto_totale, 2)} monete")
    paga_totale = 0.0
    for membro in lista_membri_originali_ingaggiati:
        nome_ruolo = membro["ruolo"]
        for categoria in CATEGORIE_RUOLI:
            if categoria["nome"] == nome_ruolo:
                paga_totale = paga_totale + categoria["prezzo_settimana"] * settimane_effettive
    print(f"  Paga equipaggio (durata {settimane_effettive} settimane): {round(paga_totale, 2)} monete")
    totale_disponibile = denari_rimasti + profitto_totale
    print(f"  Denari rimasti + profitti: {round(totale_disponibile, 2)}")
    saldo_finale = totale_disponibile - paga_totale
    print(f"  Saldo finale: {round(saldo_finale, 2)}")
    return saldo_finale, paga_totale, totale_disponibile

def esegui_asta():
    print()
    print("=== ASTA DELLA NAVE ===")
    risposta = input("Vuoi mettere all'asta la nave per pagare l'equipaggio? (s/n): ").strip().lower()
    while risposta != "s" and risposta != "n":
        risposta = input("Rispondi s oppure n: ").strip().lower()
    if risposta == "n":
        print("Hai rifiutato l'asta.")
        return 0.0
    offerte_da_fare = list(OFFERTE_ASTA)
    random.shuffle(offerte_da_fare)
    offerte_gia_proposte_una_volta = []
    ricavo = 0.0
    venduto = False

    while not venduto:
        if len(offerte_da_fare) == 0:
            offerte_da_fare = list(OFFERTE_INFINITE_ASTA)
            random.shuffle(offerte_da_fare)
        offerta_corrente = offerte_da_fare[0]
        offerte_da_fare.pop(0)
        if offerta_corrente not in OFFERTE_INFINITE_ASTA:
            if offerta_corrente in offerte_gia_proposte_una_volta:
                continue
            offerte_gia_proposte_una_volta.append(offerta_corrente)
        print(f"Offerta: {offerta_corrente} monete.")
        risposta = input("Accetti? (s/n): ").strip().lower()
        while risposta != "s" and risposta != "n":
            risposta = input("Rispondi s oppure n: ").strip().lower()
        if risposta == "s":
            ricavo = offerta_corrente
            venduto = True
    print(f"Nave venduta per {ricavo} monete.")
    return ricavo

def mostra_esito_finale(saldo_finale):
    print()
    print("=== FINE DEL GIOCO ===")
    if saldo_finale > 0:
        print(f"Esito POSITIVO: riesci a pagare tutti e ti avanzano {round(saldo_finale, 2)} monete. Complimenti!")
    elif saldo_finale == 0:
        print("Esito NULLO: riesci a pagare tutti ma non ti avanza nulla. Tanta fatica per niente.")
    else:
        print(f"Esito NEGATIVO: non riesci a pagare l'equipaggio. Debito di {round(abs(saldo_finale), 2)} monete.")

def nuova_partita():
    denari = 2000
    lista_membri = acquista_equipaggio()
    denari, quantita_provviste = acquista_provviste(denari)
    denari, quantita_merci = acquista_merci(denari)
    print(f"\nPerfetto! Denari rimasti: {round(denari, 2)}")
    lista_membri_ingaggiati_originali = []
    for membro in lista_membri:
        copia = {"ruolo": membro["ruolo"], "pagato": membro["pagato"]}
        lista_membri_ingaggiati_originali.append(copia)
    # Stato viaggio
    settimane_totali = SETTIMANE_BASE
    settimana_di_partenza = 1
    contatore_eventi = {}
    albatri_avvistati = 0
    albatro_ucciso = False
    razioni_correnti = [1.0, 1.0, 1.0, 1.0]
    delta_morale = 0
    viaggio_completato, lista_membri, quantita_provviste, quantita_merci, settimane_totali, albatri_avvistati, albatro_ucciso, denari = viaggio(
        lista_membri, quantita_provviste, quantita_merci, denari,
        settimane_totali, settimana_di_partenza, contatore_eventi,
        albatri_avvistati, albatro_ucciso, razioni_correnti, delta_morale
    )
    if not viaggio_completato:
        print("Il viaggio e' terminato prematuramente. GAME OVER.")
        return
    # Arrivo nel nuovo mondo
    atterrato = arrivo_nuovo_mondo(lista_membri, quantita_merci)
    if not atterrato:
        return
    # Baratto
    numero_perle, numero_manufatti, numero_spezie = esegui_baratto(quantita_merci)
    # Tradimento
    numero_perle, sopravvissuto = gestisci_tradimento(
        quantita_merci, numero_perle, albatri_avvistati, albatro_ucciso
    )
    if not sopravvissuto:
        return
    # Epilogo e ritorno
    settimane_ritorno = epilogo_ritorno(lista_membri, quantita_provviste, albatri_avvistati, albatro_ucciso)
    settimane_totali = settimane_totali + settimane_ritorno
    # Calcolo profitti
    saldo_finale, paga_totale, totale_disponibile = calcola_profitti(
        numero_perle, numero_manufatti, numero_spezie,
        lista_membri_ingaggiati_originali,
        settimane_totali,
        denari
    )
    if saldo_finale < 0:
        ricavo_asta = esegui_asta()
        saldo_finale = saldo_finale + ricavo_asta
    mostra_esito_finale(saldo_finale)

def partita_da_salvataggio():
    stato = carica_partita()
    if stato is None:
        print("Nessun salvataggio trovato. Avvio nuova partita.")
        nuova_partita()
        return
    lista_membri = stato["lista_membri"]
    quantita_provviste = stato["quantita_provviste"]
    quantita_merci = stato["quantita_merci"]
    settimane_totali = stato["settimane_totali"]
    settimana_corrente = stato["settimana_corrente"] + 1
    contatore_eventi = stato["contatore_eventi"]
    albatri_avvistati = stato["albatri_avvistati"]
    albatro_ucciso = stato["albatro_ucciso"]
    razioni_correnti = stato["razioni_correnti"]
    delta_morale = stato["delta_morale"]
    denari = stato["denari_rimasti"]
    lista_membri_ingaggiati_originali = []
    for membro in lista_membri:
        if membro["pagato"]:
            copia = {"ruolo": membro["ruolo"], "pagato": True}
            lista_membri_ingaggiati_originali.append(copia)
    viaggio_completato, lista_membri, quantita_provviste, quantita_merci, settimane_totali, albatri_avvistati, albatro_ucciso, denari = viaggio(
        lista_membri, quantita_provviste, quantita_merci, denari,
        settimane_totali, settimana_corrente, contatore_eventi,
        albatri_avvistati, albatro_ucciso, razioni_correnti, delta_morale
    )
    if not viaggio_completato:
        print("Il viaggio e' terminato prematuramente. GAME OVER.")
        return
    atterrato = arrivo_nuovo_mondo(lista_membri, quantita_merci)
    if not atterrato:
        return
    numero_perle, numero_manufatti, numero_spezie = esegui_baratto(quantita_merci)
    numero_perle, sopravvissuto = gestisci_tradimento(
        quantita_merci, numero_perle, albatri_avvistati, albatro_ucciso
    )
    if not sopravvissuto:
        return

    settimane_ritorno = epilogo_ritorno(lista_membri, quantita_provviste, albatri_avvistati, albatro_ucciso)
    settimane_totali = settimane_totali + settimane_ritorno
    saldo_finale, paga_totale, totale_disponibile = calcola_profitti(
        numero_perle, numero_manufatti, numero_spezie,
        lista_membri_ingaggiati_originali,
        settimane_totali,
        denari
    )
    if saldo_finale < 0:
        ricavo_asta = esegui_asta()
        saldo_finale = saldo_finale + ricavo_asta
    mostra_esito_finale(saldo_finale)
