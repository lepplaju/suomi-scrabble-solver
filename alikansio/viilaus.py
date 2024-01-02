import re
import copy
from collections import Counter
from alikansio.kirjainpaikat import kerro_kirjaimet, get_pisteet

kirjainpisteet = {
    'a': 1, 'i': 1, 'n': 1, 's': 1, 't': 1, 'e': 1,'k': 2, 'l': 2, 'o': 2, 'ä': 2,'u': 3, 'm': 3,'h': 4, 'j': 4, 'p': 4, 'r': 4, 'y': 4, 'v': 4,'f':7,'d': 7, 'ö': 7, 'g':8,'b':8,'c': 10,'w': 0, 'q': 0,'x':0,'*': 0, '-': 0, 'à':0,'z':0,'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0,'š':0, 'é':0
}

def get_alkuosa(tilaa_edessa, sana_alku, sanalista, kirjaimet):
    reg_patt = f".{{0,{tilaa_edessa}}}{sana_alku}"
    #print('reg_patt',reg_patt)
    reg = re.compile(reg_patt)
    #print(reg)
    karsitut_sanat = [word for word in sanalista if reg.fullmatch(word)]  
    kirjaimet_poydalla = sana_alku.replace('.', '')
    if len(karsitut_sanat)==0:
        #print('ei karsittuja sanoja')
        return
    tarkistettavat_sanat = [kerro_kirjaimet(sana, kirjaimet_poydalla) for sana in karsitut_sanat]
    #print('tarkistettavat sanat', tarkistettavat_sanat)

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
    #print('reg_patt',reg_patt)
    reg = re.compile(reg_patt)
    #print(reg)
    karsitut_sanat = [word for word in sanalista if reg.fullmatch(word)]  
    kirjaimet_poydalla = sana_loppu.replace('.', '')
    if len(karsitut_sanat)==0:
        #print('ei karsittuja sanoja')
        return
    tarkistettavat_sanat = [kerro_kirjaimet(sana, kirjaimet_poydalla) for sana in karsitut_sanat]
    #print('tarkistettavat sanat', tarkistettavat_sanat)

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

def get_kokonaisuus(sanalista, kirjaimet, poyta):
    tilaa_edessa = int(poyta[0])
    tilaa_lopussa = int(poyta[-1])
    jaljelle_jaava = poyta[1:-1]
    #print('jaljelle_jaava', jaljelle_jaava)
    #print('tilaa edessa', tilaa_edessa, tilaa_lopussa)
    reg_patt = f".{{0,{tilaa_edessa}}}{jaljelle_jaava}.{{0,{tilaa_lopussa}}}"
    #print('reg_patt',reg_patt)
    reg = re.compile(reg_patt)

    karsitut_sanat = [word for word in sanalista if reg.fullmatch(word)]  
    kirjaimet_poydalla = jaljelle_jaava.replace('.', '')
    if len(karsitut_sanat)==0:
        print('ei karsittuja sanoja')
        return
    tarkistettavat_sanat = [kerro_kirjaimet(sana, kirjaimet_poydalla) for sana in karsitut_sanat]
    print('kasitut', karsitut_sanat, '\n')
    #print('tarkistettavat sanat', tarkistettavat_sanat)

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



def kolme_osaa(siistityt_sanat, kirjaimet, poyta):
    ilman_loppuosaa = poyta.rsplit('.', 1)[0]
    ilman_alkuosaa = poyta.split('.',1)[-1]  
    #osat = list(filter(None, poyta.split('.')))
    #print('osat', osat)

    tilaa_edessa = int(ilman_loppuosaa[0])
    alkuosa = ilman_loppuosaa[1:]
    loppuosa = ilman_alkuosaa[:-1]
    tilaa_takana = int(ilman_alkuosaa[-1])   
    #print('alkuosa',ilman_loppuosaa)
    #print('alkuosa', alkuosa)
    #print('tilaa edessa', tilaa_edessa)

    #print('loppuosa',ilman_alkuosaa)
    #print('loppuosa', loppuosa)
    #print('tilaa takana', tilaa_takana)

    tasmaavat_alkusanat = get_alkuosa(tilaa_edessa, alkuosa, siistityt_sanat, kirjaimet)
    #print('tasmaavat_alkusanat', tasmaavat_alkusanat)
    tasmaavat_loppusanat = get_loppuosa(tilaa_takana, loppuosa, siistityt_sanat, kirjaimet)
    #print('tasmaavat_loppusanat', tasmaavat_loppusanat)
    tasmaavat_koko = get_kokonaisuus(siistityt_sanat, kirjaimet, poyta)
    #print('tasmaavat_koko', tasmaavat_koko)

    kaikki_tasmaavat = list(tasmaavat_alkusanat.union(tasmaavat_loppusanat).union(tasmaavat_koko))
    sorted_osumat = sorted(kaikki_tasmaavat, key=lambda x: (len(x), x))
    #print('kaikki tasmaavat', sorted_osumat)
    if len(sorted_osumat) > 0 :
            print(sorted_osumat)
            longest_sana = len(max(sorted_osumat, key=len))
            for osuma in sorted_osumat:
                print(f"{osuma:<{longest_sana+2}}", " pisteet: ", get_pisteet(osuma), sep='')
    else:
        print('ei osumia hakuehdoilla')
        
    print('---------------------')