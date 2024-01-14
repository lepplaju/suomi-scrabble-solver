import re
import csv



def lue_tiedosto():
    max_pituus_global = 15 # Asetetaan maksimipituus sanalle (scrabble laudan koko)
    # Ladattu tiedosto omassa hakemistossa
    tiedostonnimi = 'aineisto/nykysuomensanalista2022unedited.csv'
    kaikki_sanat = []

    # Avataan tiedosto ja luetaan sanat listaan
    with open(tiedostonnimi, encoding='utf-8') as tiedosto:
        csv_tiedosto = csv.reader(tiedosto)
        for rivi in csv_tiedosto:
            rivi_ilman_pilkkuja = [s.replace(',', '') for s in rivi]
            kaikki_sanat.extend(rivi_ilman_pilkkuja) # Tiedosto sisältää pilkkuja, jotka aiheuttavat ongelmia myöhemmin. Poistetaan pilkut

    siistityt_sanat = []
    # Rivit sisältävät tabulaattoreita, joten sitä käytetään erottimena
    erottaja = '\\t'

    # Ensimmäinen rivi sisältää sarakkeiden otsikot, joten se ohitetaan
    for sana in kaikki_sanat[1:]:
        temp = (re.split(erottaja, sana, maxsplit=1)[0])

        if len(temp) <= max_pituus_global and len(temp)>1:
            siistityt_sanat.append(temp.lower())
            
    return siistityt_sanat

_siistityt_sanat = lue_tiedosto()

def anna_sanat():    
    return _siistityt_sanat