from collections import Counter
from tukitoiminnot import sanojen_lukeminen
from tukitoiminnot import pisteiden_hallinta
import copy

# Funktio, joka muodostaa sanoja pöydällä olevan sanan ympärille
def sisaltaa_sanan(kirjaimet, sana_param):
    siistityt_sanat = sanojen_lukeminen.anna_sanat()
    # Otetaan vain sellaiset sanat, jotka sisältävät annetun sanan
    karsitut_sanat = [sana for sana in siistityt_sanat if sana_param in sana] 

    if len(karsitut_sanat)==0:
        print("---------------------")
        print('ei osumia hakuehdoilla')
        return

    # Tulosta sanat pituusjärjestyksessä
    karsitut_sanat = sorted(karsitut_sanat, reverse=True, key=lambda x: (len(x), x)) 
    print('kaikki sanat joissa:', sana_param)
    for karsittu_sana in karsitut_sanat:
        print(karsittu_sana)
    print("---------------------")
    
    tarkistettavat_sanat = [sana.replace(sana_param, '') for sana in karsitut_sanat]

    osumat = set()
    kirjain_counter = Counter(kirjaimet)
    jokerit = kirjain_counter['*']

    # Sanoista on poistettu pöydällä olevat kirjaimet. Tarkistetaan, onko kädessä olevissa kirjaimissa kaikki jäljelle jääneet kirjaimet 
    for i, sana in enumerate(tarkistettavat_sanat):
        sana_counter = Counter(sana)
        if jokerit == 0:
            if all(sana_counter[kirjain] <= kirjain_counter[kirjain] for kirjain in sana_counter):
                    osumat.add(karsitut_sanat[i])
        elif jokerit > 0:
            temp_counter = copy.copy(sana_counter)
            for kirjain in sana_counter:
                if kirjain_counter[kirjain]>0:
                    temp_counter[kirjain] -= kirjain_counter[kirjain]
                    if temp_counter[kirjain]<0:
                        temp_counter[kirjain] = 0
            
            if jokerit >= sum(temp_counter.values()):
                osumat.add(karsitut_sanat[i])


    if len(osumat) > 0:
        sorted_tulokset = sorted(osumat, key=lambda x: (len(x), x))
        longest_length = len(max(sorted_tulokset, key=len))
        print("osumat:\n")
        for osuma in sorted_tulokset:
                #tulokset.append((osuma,get_pisteet(osuma)))
                print(f"{osuma:<{longest_length+2}}", " pisteet: ", pisteiden_hallinta.get_pisteet(osuma), sep='')
    else:
        print("---------------------")
        print('ei osumia hakuehdoilla')
    print()