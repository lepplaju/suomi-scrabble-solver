import copy
from collections import Counter
from tukitoiminnot import sanojen_lukeminen
from tukitoiminnot import pisteiden_hallinta
# syötteen tulisi olla muodossa "kirjaim ..i" tai "kirjaim i.." aloitus- tai lopetuskirjain välilyönnillä erotettuna ja pisteet siihen suuntaan mihin on tilaa rakentaa sanaa
def alku_tai_lopetushaku(syote):
    pituusjarjestys = True
    if ' ' in syote:
        apu = syote.split(' ')
        kirjaimet = apu[0]
        aloitus_tai_lopetusehto = apu[1]
    else: 
        print('virheellinen syöte')
        return
        
    aloituslukko = False
    siistityt_sanat = sanojen_lukeminen.anna_sanat()
    karsitut_sanat = []
    if aloitus_tai_lopetusehto[0].isalpha():
        aloituslukko = True
        aloituskirjain = aloitus_tai_lopetusehto[0].lower()
    elif aloitus_tai_lopetusehto[-1].isalpha():
        lopetuslukko = True
        lopetuskirjain = aloitus_tai_lopetusehto[-1].lower()

    if aloituslukko==True: # Lisätään sanat listaan ilman pöydällä olevaa kirjainta
        karsitut_sanat = [sana[1:] for sana in siistityt_sanat if sana[0]==aloituskirjain]
    elif lopetuslukko == True:
        karsitut_sanat = [sana[:-1] for sana in siistityt_sanat if sana[-1]==lopetuskirjain]
    else:
        print('Ei löytynyt aloitus- tai lopetuskirjainta')
        return

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
                    temp_counter[kirjain] -= kirjain_counter[kirjain]
                    if temp_counter[kirjain]<0:
                        temp_counter[kirjain] = 0
            
            if jokerit >= sum(temp_counter.values()):
                if aloituslukko == True:
                    osumat.add(aloituskirjain+sana)
                elif lopetuslukko == True:
                    osumat.add(sana+lopetuskirjain)

    tulokset = []
    sorted_tulokset = None

    # Tulostetaan tulokset pituus- tai pistejärjestyksessä
    if len(osumat) > 0:
        if pituusjarjestys:
            sorted_tulokset = sorted(osumat, key=lambda x: (len(x), x))
            longest_length = len(max(sorted_tulokset, key=len))
            for i, osuma in enumerate(sorted_tulokset):
                print(f"{osuma:<{longest_length+2}}", " : ", pisteiden_hallinta.get_pisteet(osuma), sep='')
        else:
            for i, osuma in enumerate(osumat):
                tulokset.append((osuma,pisteiden_hallinta.get_pisteet(osuma)))
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