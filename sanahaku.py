from alikansio import kirjainpaikat, viilaus
import re
import csv
import copy
from collections import Counter

# Ladattu tiedosto omassa hakemistossa
tiedostonnimi = 'aineisto/nykysuomensanalista2022.csv'

kaikki_sanat = []
pituusjarjestys = True
max_pituus_global = 15

kirjainpisteet = {
    'a': 1, 'i': 1, 'n': 1, 's': 1, 't': 1, 'e': 1,'k': 2, 'l': 2, 'o': 2, 'ä': 2,'u': 3, 'm': 3,'h': 4, 'j': 4, 'p': 4, 'r': 4, 'y': 4, 'v': 4,'f':8,'d': 7, 'ö': 7, 'g':8,'b':8,'c': 10,'w': 0, 'q': 0,'x':0,'*': 0, '-': 0, 'à':0,'z':0,'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0,'š':0, 'é':0
}

with open(tiedostonnimi, encoding='utf-8') as tiedosto:
    csv_tiedosto = csv.reader(tiedosto)
    for rivi in csv_tiedosto:
        kaikki_sanat.extend(rivi)

siistityt_sanat = []
erottaja = '\\t'

for sana in kaikki_sanat[1:]:
    temp = (re.split(erottaja, sana, maxsplit=1)[0])

    if len(temp) <= max_pituus_global and len(temp)>1:
        siistityt_sanat.append(temp.lower())

#---------------------------------------------------------------
def sisaltaa_sanan(sana_param, kirjaimet):
    karsitut_sanat = [sana for sana in siistityt_sanat if sana_param in sana]
    karsitut_sanat = sorted(karsitut_sanat, reverse=True, key=lambda x: (len(x), x))
    print('kaikki sanat joissa:', sana_param)
    for karsittu_sana in karsitut_sanat:
        print(karsittu_sana)
    if len(karsitut_sanat)==0:
        print("---------------------")
        print('ei osumia hakuehdoilla')
        return
    tarkistettavat_sanat = [sana.replace(sana_param, '') for sana in karsitut_sanat]

    osumat = set()
    kirjain_counter = Counter(kirjaimet)
    jokerit = kirjain_counter['*']

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
    
    if len(osumat) <1 :
        print("---------------------")
        print('ei osumia hakuehdoilla')
        print()
        return
    print('---------------------')
    if len(osumat) > 0:
        sorted_tulokset = sorted(osumat, key=lambda x: (len(x), x))
        longest_length = len(max(sorted_tulokset, key=len))
        for osuma in sorted_tulokset:
                #tulokset.append((osuma,get_pisteet(osuma)))
                print(f"{osuma:<{longest_length+2}}", " pisteet: ", get_pisteet(osuma), sep='')
    else:
        print("---------------------")
        print('ei osumia hakuehdoilla')
    print()
    


#---------------------------------------------------------------


def tarkista_poytasyote(kirjaimet, poyta, min_pituus, max_pituus):

    aloituslukko = False
    kuvitussyote = copy.deepcopy(poyta)
    if len(kuvitussyote.replace('.', '')) > 1:

        if kuvitussyote[0].isdigit():
            if kuvitussyote.count('.') > 1:
                osat = list(filter(None, kuvitussyote.split('.')))
                if len(osat) > 2:
                    viilaus.kolme_osaa(siistityt_sanat,kirjaimet, poyta)
                    return
                kirjainpaikat.edistynyt_parsija(siistityt_sanat, kirjaimet, poyta)
                return
            parsijan_sanat = list(kirjainpaikat.parsija(siistityt_sanat, kirjaimet, poyta))
            sorted_tulokset = sorted(parsijan_sanat, key=lambda x: (len(x), x))
            if len(sorted_tulokset) > 0:
                longest_length = len(max(sorted_tulokset, key=len))
                for osuma in sorted_tulokset:
                    print(f"{osuma:<{longest_length+2}}", " pisteet: ", get_pisteet(osuma), sep='')
                return
            else:
                print("Ei osmia")
                return
        
        sana_poydalla = poyta.replace('.', '')
        sisaltaa_sanan(sana_poydalla, kirjaimet)
        return
    karsitut_sanat = []
    if kuvitussyote[0].isalpha():
        aloituslukko = True
        aloituskirjain = kuvitussyote[0].lower()
    elif kuvitussyote[-1].isalpha():
        lopetuslukko = True
        lopetuskirjain = kuvitussyote[-1].lower()

    if aloituslukko==True:
        karsitut_sanat = [sana[1:] for sana in siistityt_sanat if sana[0]==aloituskirjain and len(sana) >= min_pituus and len(sana) <= max_pituus]
    elif lopetuslukko == True:
        karsitut_sanat = [sana[:-1] for sana in siistityt_sanat if sana[-1]==lopetuskirjain and len(sana) >= min_pituus and len(sana) <= max_pituus]
    else:
        print('virheellinen syöte')

    if len(karsitut_sanat) == 0:
        print("---------------------")
        print('ei osumia hakuehdoilla')
        return
    
    print('karsitut sanat', len(karsitut_sanat))
    print('listattuna:', karsitut_sanat)
    print("---------------------")
    

    osumat = set()

    kirjain_counter = Counter(kirjaimet)
    jokerit = kirjain_counter['*']

    
    for sana in karsitut_sanat:
        sana_counter = Counter(sana)
        if jokerit == 0:
            if all(sana_counter[kirjain] <= kirjain_counter[kirjain] for kirjain in sana_counter):
                if aloituslukko == True:
                    osumat.add(aloituskirjain+sana)
                elif lopetuslukko == True:
                    osumat.add(sana+lopetuskirjain)
        elif jokerit > 0:
            temp_counter = copy.copy(sana_counter)
            for kirjain in sana_counter:
                if kirjain_counter[kirjain]>0:
                    temp_counter[kirjain] = temp_counter[kirjain]-1
            
            if jokerit >= sum(temp_counter.values()):
                if aloituslukko == True:
                    osumat.add(aloituskirjain+sana)
                elif lopetuslukko == True:
                    osumat.add(sana+lopetuskirjain)

    tulokset = []
    sorted_tulokset = None
    if len(osumat) > 0:
        if pituusjarjestys == True:
            sorted_tulokset = sorted(osumat, key=lambda x: (len(x), x))
            longest_length = len(max(sorted_tulokset, key=len))
            for i, osuma in enumerate(sorted_tulokset):
                print(f"{osuma:<{longest_length+2}}", " : ", get_pisteet(osuma), sep='')
        else:
            for i, osuma in enumerate(osumat):
                tulokset.append((osuma,get_pisteet(osuma)))
                sorted_tulokset = sorted(tulokset, key=lambda x: x[1])
                longest_length = len(max(sorted_tulokset, key=lambda x: len(x[0]))[0])

            if sorted_tulokset is not None:
                for ind, pari in enumerate(sorted_tulokset):
                    print(f"{pari[0]:<{longest_length+2}}", " - pisteet: ", pari[1], sep='')    
            else:
                #print("---------------------")
                print('ei osumia hakuehdoilla!')
        print()

    else:
        #print("---------------------")
        print('ei osumia hakuehdoilla!')

    

    

        



def get_pisteet(sana):
    summa = 0
    for char in sana:
        if char in kirjainpisteet:
            summa += kirjainpisteet[char]
    return summa

def hae_kaikki_sanat(annetut_kirjaimet):
    pituus = None
    if pituus is not None and int(pituus) > 2:
        max_pituus = int(pituus)
    else:
        max_pituus = max_pituus_global

    min_pituus = 2
    
    poyta = ''
    if ' ' in annetut_kirjaimet:
        temp = annetut_kirjaimet.split(' ')
        kirjaimet = temp[0]
        poyta = temp[1]
        tarkista_poytasyote(kirjaimet, poyta, min_pituus, max_pituus)
        return
    else:
        kirjaimet = annetut_kirjaimet
    
        
    print('kirjaimet\n', kirjaimet, sep='')

    

    osumat = set()
    if min_pituus is not None and max_pituus is not None:
        karsitut_sanat = [sana for sana in siistityt_sanat if len(sana) >= min_pituus and len(sana) <= max_pituus]
        kirjain_counter = Counter(kirjaimet)
        jokerit = kirjain_counter['*']
        print('jokerit:', jokerit)

        
        for sana in karsitut_sanat:
            sana_counter = Counter(sana)

            if jokerit == 0:
                if all(sana_counter[kirjain] <= kirjain_counter[kirjain] for kirjain in sana_counter):
                    osumat.add(sana)
            else:
                temp_counter = copy.copy(sana_counter)
                for kirjain in sana_counter:            
                    if kirjain_counter[kirjain]>0:
                        temp_counter[kirjain] -= kirjain_counter[kirjain]
                        if temp_counter[kirjain]<0:
                            temp_counter[kirjain] = 0
                if jokerit >= sum(temp_counter.values()):
                    osumat.add(sana)
            
    
    print('hakuehdon täyttävien määrä:', len(osumat))
    
    
    tulokset = []

    if pituusjarjestys == True:
        longest_length = len(max(osumat, key=len))
        sorted_tulokset = sorted(osumat, key=lambda x: (len(x), x))
        for i, osuma in enumerate(sorted_tulokset):
            print(f"{i+1:<3}: {osuma:<{longest_length+2}}", " : ", get_pisteet(osuma), sep='')    
    else:
        for i, osuma in enumerate(osumat):
            tulokset.append((osuma,get_pisteet(osuma)))
        
        sorted_tulokset = sorted(tulokset, key=lambda x: x[1])
        longest_length = len(max(sorted_tulokset, key=lambda x: len(x[0]))[0])

        for ind, pari in enumerate(sorted_tulokset):
            print(f"{pari[0]:<{longest_length+2}}", " - pisteet: ", pari[1], sep='')    
        print()



# Ohjelman varsinainen ajo tapahtuu tässä
while True:
    print('\nAnna kirjaimet: ')
    kirjaimet = input()
    if kirjaimet == 'q':
        break
    hae_kaikki_sanat(kirjaimet)



#---------------------------------------------------------------
def hae_sanat(annetut_kirjaimet, annettu_pituus):
    min_pituus = None
    max_pituus = None 
    if '-' in annettu_pituus:
        min_pituus, max_pituus = annettu_pituus.split('-')
        min_pituus = int(min_pituus)
        max_pituus = int(max_pituus)
    else:
        pituus = int(annettu_pituus)
    
    if len(annetut_kirjaimet) > 0 and len(annetut_kirjaimet) < 10:
        kirjaimet = annetut_kirjaimet
    else:
        kirjaimet = ''

    hakuehto =''
    for kirjain in kirjaimet:
        hakuehto += r'(?=.*' + re.escape(kirjain) + r')'
    osumat = []
    if min_pituus is not None and max_pituus is not None:
        karsitut_sanat = [sana for sana in siistityt_sanat if len(sana) >= min_pituus and len(sana) <= max_pituus]
        for sana in karsitut_sanat:
            if re.search(hakuehto, sana):
                osumat.append(sana)
    elif pituus > 0:
        karsitut_sanat = [sana for sana in siistityt_sanat if len(sana) == pituus]
        for sana in karsitut_sanat:
            if re.search(hakuehto, sana):
                osumat.append(sana)
        
    elif pituus == 0:
        for sana in siistityt_sanat:
            if re.search(hakuehto, sana):
                osumat.append(sana)

    print('hakuehdon täyttävien määrä:', len(osumat))
    for i, osuma in enumerate(osumat):
        print(i, ": ", osuma, sep='')   
    
    #---------------------------------------------------------------