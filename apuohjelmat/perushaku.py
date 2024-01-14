from collections import Counter
from tukitoiminnot import sanojen_lukeminen
from tukitoiminnot import pisteiden_hallinta
import copy

# Perushaun sisäänkäynti
def perushaku(kirjaimet):
    max_pituus = 15
    pituusjarjestys = True
    siistityt_sanat = sanojen_lukeminen.anna_sanat()

    osumat = set()
    kirjain_counter = Counter(kirjaimet)
    jokerit = kirjain_counter['*']
    
    for sana in siistityt_sanat:
        sana_counter = Counter(sana)

        if jokerit == 0: # Jos annetuissa kirjaimissa ei ole jokereita
            if all(sana_counter[kirjain] <= kirjain_counter[kirjain] for kirjain in sana_counter):
                osumat.add(sana)

        else: # Jos annetuissa kirjaimissa on jokereita
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

    if pituusjarjestys: # tuloksien pituusjärjestys
        longest_length = len(max(osumat, key=len))
        sorted_tulokset = sorted(osumat, key=lambda x: (len(x), x))
        for i, osuma in enumerate(sorted_tulokset):
            print(f"{i+1:<3}: {osuma:<{longest_length+2}}", " : ", pisteiden_hallinta.get_pisteet(osuma), sep='')    

    else: # tai tuloksien pistejärjestys 
        for i, osuma in enumerate(osumat):
            tulokset.append((osuma,pisteiden_hallinta.get_pisteet(osuma)))
        
        sorted_tulokset = sorted(tulokset, key=lambda x: x[1])
        longest_length = len(max(sorted_tulokset, key=lambda x: len(x[0]))[0])

        for ind, pari in enumerate(sorted_tulokset):
            print(f"{pari[0]:<{longest_length+2}}", " - pisteet: ", pari[1], sep='')    
        print()