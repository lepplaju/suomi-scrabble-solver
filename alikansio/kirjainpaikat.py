import re
import copy
from collections import Counter

kirjainpisteet = {
    'a': 1, 'i': 1, 'n': 1, 's': 1, 't': 1, 'e': 1,'k': 2, 'l': 2, 'o': 2, 'ä': 2,'u': 3, 'm': 3,'h': 4, 'j': 4, 'p': 4, 'r': 4, 'y': 4, 'v': 4,'f':7,'d': 7, 'ö': 7, 'g':8,'b':8,'c': 10,'w': 0, 'q': 0,'x':0,'*': 0, '-': 0, 'à':0,'z':0,'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0,'š':0, 'é':0
}

def kerro_kirjaimet(sanan_kirjaimet, kirjaimet_poydalla):
    kirjainsetti = set(kirjaimet_poydalla)
    jaljelle_jaavat = []
    for letter in sanan_kirjaimet:
        if letter in kirjainsetti:
            kirjainsetti.remove(letter)
        else:
            jaljelle_jaavat.append(letter)
    return ''.join(jaljelle_jaavat)

def get_alkuosa(tilaa_edessa, sana_alku, sanalista, kirjaimet):
    reg_patt = f".{{0,{tilaa_edessa}}}{sana_alku}"
    print('reg_patt',reg_patt)
    reg = re.compile(reg_patt)
    print(reg)
    karsitut_sanat = [word for word in sanalista if reg.fullmatch(word)]
    kirjaimet_poydalla = sana_alku.replace('.', '')
    if len(karsitut_sanat)==0:
        print('ei karsittuja sanoja')
        return
    tarkistettavat_sanat = [kerro_kirjaimet(sana, kirjaimet_poydalla) for sana in karsitut_sanat]


    kirjain_counter = Counter(kirjaimet)
    jokerit = kirjain_counter['*']
   
    osumat = set()
    for i, sana in enumerate(tarkistettavat_sanat):
        sana_counter = Counter(sana)
        if jokerit == 0:
            if all(sana_counter[kirjain] <= kirjain_counter[kirjain] for kirjain in sana_counter):
                osumat.add(karsitut_sanat[i])
        elif jokerit > 0:
            temp_counter = copy.copy(sana_counter)
            for kirjain in sana_counter:
                if kirjain_counter[kirjain]>0:
                    temp_counter[kirjain] = temp_counter[kirjain]-1
        
            if jokerit >= sum(temp_counter.values()):
                osumat.add(karsitut_sanat[i])

    return osumat

def get_loppuosa(tilaa_lopussa, sana_loppu, sanalista, kirjaimet):
    reg_patt = f"{sana_loppu}.{{0,{tilaa_lopussa}}}"
    print('reg_patt',reg_patt)
    reg = re.compile(reg_patt)
    print(reg)
    karsitut_sanat = [word for word in sanalista if reg.fullmatch(word)]

    kirjaimet_poydalla = sana_loppu.replace('.', '')
    if len(karsitut_sanat)==0:
        print('ei karsittuja sanoja')
        return
    tarkistettavat_sanat = [kerro_kirjaimet(sana, kirjaimet_poydalla) for sana in karsitut_sanat]

    kirjain_counter = Counter(kirjaimet)
    jokerit = kirjain_counter['*']
   
    osumat = set()
    for i, sana in enumerate(tarkistettavat_sanat):
        sana_counter = Counter(sana)
        if jokerit == 0:
            if all(sana_counter[kirjain] <= kirjain_counter[kirjain] for kirjain in sana_counter):
                osumat.add(karsitut_sanat[i])
        elif jokerit > 0:
            temp_counter = copy.copy(sana_counter)
            for kirjain in sana_counter:
                if kirjain_counter[kirjain]>0:
                    temp_counter[kirjain] = temp_counter[kirjain]-1
        
            if jokerit >= sum(temp_counter.values()):
                osumat.add(karsitut_sanat[i])

    return osumat


def get_osat(sanalista, kirjaimet, syote):
    tilaa_edessa = int(syote[0])
    tilaa_takana = int(syote[-1])   
    sana_alku = syote[1:-3]
    sana_loppu = syote[3:-1]

    print('alku:', sana_alku)
    print('loppu:', sana_loppu)
    tasmaavat_alkusanat = get_alkuosa(tilaa_edessa, sana_alku, sanalista, kirjaimet)

    tasmaavat_loppusanat = get_loppuosa(tilaa_takana, sana_loppu, sanalista, kirjaimet)

    kaikki_tasmaavat = tasmaavat_alkusanat.union(tasmaavat_loppusanat)

    return kaikki_tasmaavat

    

def get_pisteet(sana):
    summa = 0
    for char in sana:
        if char in kirjainpisteet:
            summa += kirjainpisteet[char]
    return summa


# miten erotellaan kun 2a.i.u2 vs 2a...u2 
def edistynyt_parsija(sanalista,kirjaimet, syote): 
    if ".." in syote: 
        osa_osumat = get_osat(sanalista, kirjaimet, syote)
        taydet_osumat = parsija(sanalista,kirjaimet, syote)

        kaikki_osumat = list(osa_osumat.union(taydet_osumat))
        sorted_osumat = sorted(kaikki_osumat, key=lambda x: (len(x), x))
        if len(sorted_osumat) >0 :
            longest_sana = len(max(sorted_osumat, key=len))
            for osuma in sorted_osumat:
                print(f"{osuma:<{longest_sana+2}}", " pisteet: ", get_pisteet(osuma), sep='')
        else:
            print('ei osumia hakuehdoilla')
        
        print('---------------------')


def parsija(sanalista,kirjaimet, syote):
    palautettavat = set()
    jaljelle_jaavat = copy.copy(syote)
    tilaa_ennen = int(syote[0])
    tilaa_jalkeen = int(syote[-1])
    jaljelle_jaavat = jaljelle_jaavat.replace(str(tilaa_ennen),'').replace(str(tilaa_jalkeen),'')


    regex_pattern = f".{{0,{tilaa_ennen}}}{jaljelle_jaavat}.{{0,{tilaa_jalkeen}}}"
    regex = re.compile(regex_pattern)

    karsitut_sanat = [word for word in sanalista if regex.fullmatch(word)]
    print('Karsitut sanat: ',karsitut_sanat)


    kirjaimet_poydalla = jaljelle_jaavat.replace('.', '')

    if len(karsitut_sanat)==0:
        print('ei karsittuja sanoja')
        return palautettavat
    tarkistettavat_sanat = [kerro_kirjaimet(sana, kirjaimet_poydalla) for sana in karsitut_sanat]
    kirjain_counter = Counter(kirjaimet)
    jokerit = kirjain_counter['*']

    for i, sana in enumerate(tarkistettavat_sanat):
        sana_counter = Counter(sana)
        if jokerit == 0:
            if all(sana_counter[kirjain] <= kirjain_counter[kirjain] for kirjain in sana_counter):
                    palautettavat.add(karsitut_sanat[i])
        elif jokerit > 0:
            temp_counter = copy.copy(sana_counter)
            for kirjain in sana_counter:
                if kirjain_counter[kirjain]>0:
                    temp_counter[kirjain] = temp_counter[kirjain]-1
            
            if jokerit >= sum(temp_counter.values()):
                palautettavat.add(karsitut_sanat[i])

    return palautettavat

    
