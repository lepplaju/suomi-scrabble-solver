import re
import copy
from tukitoiminnot import sanojen_lukeminen
from tukitoiminnot import pisteiden_hallinta
from collections import Counter

kaikki_sanat = sanojen_lukeminen.anna_sanat()
# Syöte tulisi olla muodossa "tilaa edessä" , kirjaimet, esim "i.a.u" ja tilaa lopussa => "2i.a.u2"
def edistynyt_haku(kirjaimet, poyta): 
    #siistityt_sanat = sanojen_lukeminen.anna_sanat()
    taydellisesti_tasmaavat = taydellinen_tasmays(kirjaimet, poyta)
    sorted_tulokset = sorted(taydellisesti_tasmaavat, key=lambda x: (len(x), x))
    if len(sorted_tulokset) > 0:
        longest_length = len(max(sorted_tulokset, key=len))
        for osuma in sorted_tulokset:
            print(f"{osuma:<{longest_length+2}}", " pisteet: ", pisteiden_hallinta.get_pisteet(osuma), sep='')
    else:
        print("Ei osmia")
        return
    #print('täydellisesti tasmaavat', taydellisesti_tasmaavat)
    if poyta.count('.') > 1:
            osat = list(filter(None, poyta.split('.')))
            # Haetaan myös lyhyempiä sanoja kolmen tai kahden osan syötteillä
            osa_osumat = set()
            if len(osat) == 2:
                osa_osumat = kaksi_osaa(kirjaimet, poyta)
                return
            elif len(osat) == 3:
                osa_osumat = kolme_osaa(kirjaimet, poyta)
                return
    kaikki_osumat = list(taydellisesti_tasmaavat.union(osa_osumat))
    if len(kaikki_osumat) == 0:
        print('ei osumia!')
        return
    sorted_osumat = sorted(kaikki_osumat, key=lambda x: (len(x), x))
    print(sorted_osumat)
    longest_sana = len(max(sorted_osumat, key=len))
    for osuma in sorted_osumat:
        print(f"{osuma:<{longest_sana+2}}", " pisteet: ", pisteiden_hallinta.get_pisteet(osuma), sep='')


def kaksi_osaa(kirjaimet, poyta):
    tilaa_edessa = int(poyta[0])
    tilaa_takana = int(poyta[-1]) 

    # poistetaan pöydän syötteestä niin, että pöydälle voidaan muodostaa myös lyhyempiä sanoja
    sana_alku = ''
    sana_loppu = ''
    if tilaa_edessa > 0:
        sana_alku = poyta[1:-3]  
    if tilaa_takana > 0:
        sana_loppu = poyta[3:-1]

    print('alku:', sana_alku)
    print('loppu:', sana_loppu)
    if sana_alku != "":
        tasmaavat_alkusanat = get_alkuosa(tilaa_edessa, sana_alku, kirjaimet)

    if sana_loppu != "":
        tasmaavat_loppusanat = get_loppuosa(tilaa_takana, sana_loppu, kirjaimet)

    kaikki_tasmaavat = tasmaavat_alkusanat.union(tasmaavat_loppusanat)

    return kaikki_tasmaavat

def kolme_osaa(kirjaimet, poyta):
    ilman_loppuosaa = poyta.rsplit('.', 1)[0]
    ilman_alkuosaa = poyta.split('.',1)[-1]  

    tilaa_edessa = int(ilman_loppuosaa[0])
    alkuosa = ilman_loppuosaa[1:]
    loppuosa = ilman_alkuosaa[:-1]
    tilaa_takana = int(ilman_alkuosaa[-1])   

    tasmaavat_alkusanat = get_alkuosa(tilaa_edessa, alkuosa, kirjaimet)
    tasmaavat_loppusanat = get_loppuosa(tilaa_takana, loppuosa, kirjaimet)

    lyhyet_tasmaavat = tasmaavat_alkusanat.union(tasmaavat_loppusanat)
    return lyhyet_tasmaavat




# Palauttaa vain ja ainoastaan sellaiset sanat, jotka pitävät sisällään kaikki pöydän kirjaimet
def taydellinen_tasmays(kirjaimet, poyta):
    tilaa_edessa = int(poyta[0])
    tilaa_lopussa = int(poyta[-1])
    jaljelle_jaava = poyta[1:-1]
    reg_patt = f".{{0,{tilaa_edessa}}}{jaljelle_jaava}.{{0,{tilaa_lopussa}}}"
    reg = re.compile(reg_patt)

    karsitut_sanat = [sana for sana in kaikki_sanat if reg.fullmatch(sana)]  
    if len(karsitut_sanat)==0:
        print('ei karsittuja sanoja')
        return
    print('kasitut', karsitut_sanat, '\n')

    kirjaimet_poydalla = jaljelle_jaava.replace('.', '')
    poydan_counter = Counter(kirjaimet_poydalla)
    # tarkistettavat_sanat = [anna_jaljelle_jaavat(sana, kirjaimet_poydalla) for sana in karsitut_sanat]
    kaden_counter = Counter(kirjaimet)

    # yhdistetään pöydän kirjaimet ja kädessä olevat kirjaimet samaan "laskimeen"
    kirjain_counter = poydan_counter + kaden_counter

    jokerit = kirjain_counter['*']
   
    osumat = set()
    for i, sana in enumerate(karsitut_sanat):
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
    return osumat    


def get_alkuosa(tilaa_edessa, sana_alku, kirjaimet):
    sanalista = kaikki_sanat
    reg_patt = f".{{0,{tilaa_edessa}}}{sana_alku}"
    reg = re.compile(reg_patt)
    karsitut_sanat = [word for word in sanalista if reg.fullmatch(word)]
    kirjaimet_poydalla = sana_alku.replace('.', '')
    if len(karsitut_sanat)==0:
        print('ei karsittuja sanoja')
        return
    
    poydan_counter = Counter(kirjaimet_poydalla)
    kaden_counter = Counter(kirjaimet)
    kirjain_counter = poydan_counter + kaden_counter 
    jokerit = kirjain_counter['*']
   
    osumat = set()
    for i, sana in enumerate(karsitut_sanat):
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
    return osumat


def get_loppuosa(tilaa_lopussa, sana_loppu, kirjaimet):
    sanalista = kaikki_sanat
    reg_patt = f"{sana_loppu}.{{0,{tilaa_lopussa}}}"
    reg = re.compile(reg_patt)
    karsitut_sanat = [word for word in sanalista if reg.fullmatch(word)]

    kirjaimet_poydalla = sana_loppu.replace('.', '')
    if len(karsitut_sanat)==0:
        print('ei karsittuja sanoja')
        return
    poydan_counter = Counter(kirjaimet_poydalla)
    kaden_counter = Counter(kirjaimet)
    kirjain_counter = poydan_counter + kaden_counter
    jokerit = kirjain_counter['*']
   
    osumat = set()
    for i, sana in enumerate(karsitut_sanat):
        sana_counter = Counter(sana)
        if jokerit == 0:
            if all(sana_counter[kirjain] <= kirjain_counter[kirjain] for kirjain in sana_counter):
                osumat.add(karsitut_sanat[i])
        elif jokerit > 0:
            temp_counter = copy.copy(sana_counter)
            for kirjain in sana_counter:
                if kirjain_counter[kirjain]>0:
                    temp_counter[kirjain] -= kirjain_counter[kirjain]
        
            if jokerit >= sum(temp_counter.values()):
                osumat.add(karsitut_sanat[i])

    return osumat