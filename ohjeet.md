Scrabble sanojen hakeminen sanakirjasta:

    Vaihtoehto 1. (perushaku)
    - Anna kädessä olevat kirjaimet, esim 'sanapel'
        -> ohjelma palauttaa sanat, jotka annetuilla kirjaimilla on mahdollista rakentaa.
            -> [lapa, pala, salpa..]
    - Tätä vaihtoehtoa kannattaa käyttää, kun laudalla on sellaisia kirjaimia, joiden molemmilla puolilla on tilaa.
            -> Laudalla olevan kirjaimen (esim "i") voi lisätä samaan syötteeseen = 'sanapeli'
                -> [penaali, paneli, lapsi, lipas...]
    

    Vaihtoehto 2. (pöydällä olevan lopetus- tai aloituskirjaimen hyödyntäminen)
    - Anna kädessä olevat kirjaimet ja välilyönnillä eroteltuna pöydällä oleva kirjain ja kaksi pistettä sanan suunnan määrittelemiseksi:
        -> esim syöte 'sikalas a..' etsii kirjaimista muodostettavat "a"-alkuiset sanat: 
            -> palauttaa: [asiakas, aski, alas...]

        -> tai syöte 'sikalas ..a' etsii kirjaimista muodostettavat a-loppuiset sanat: 
            -> palauttaa: [kaisla, skaala, sikala...]

    - Tätä vaihtoehtoa kannattaa käyttää kun laudalla on sellaisia kirjaimia, jossa vain yhdellä puolella on tilaa.


    Vaihtoehto 3. (olemassa olevan sanaan lisääminen)
    - Anna kädessä olevat kirjaimet ja välilyönnillä eroteltuna pöydällä oleva sana, jota haluat jatkaa:
        -> esim syöte 'urstovi alas' etsii sanoja, jotka pitävät sisällään sanan "alas"
            -> palauttaa: [turvalasi, valaistus, alasti, valas...]



    Vaihtoehto 4. (edistynyt haku / usean pöydällä olevan kirjaimen käyttö)
    - Anna kädessä olevat kirjaimet, välilyönti ja seuraavat asiat:
        - maksimi tila ennen pöydällä olevaa ensimmäistä kirjainta (esim "3")
        - pöydällä olevat kirjaimet, pisteillä eroteltuna (esim "k.i", "k..i" tai "k.i.i") pisteet kuvaavat tilaa kirjaimien välillä
        - maksimi tila toisen pöydällä olevan kirjaimen jälkeen (esim "2")
            - esim syöte 'arskuti 3k.i2' etsii sellaisia sanoja:
            -> joissa k ja i on yhdellä eroteltuna,
            -> ennen k-kirjainta on enintään 3 kirjainta
            -> i-kirjaimen jälkeen on enintään 2 kirjainta 
                -> 'arskuti 3k.i2' palauttaa: [kirkaisu, tuikkia, asukki...]


Muuta tietoa:
    - Tyhjän laatan voi lisätä muiden kirjaimien joukkoon merkkinä "*"
        -> esim syöte 'karsvt* ..i'
            -> palauttaa: [rovasti, kaveri, faksi...] 

    - Sanat saa järjestettyä piste- tai pituusjärjestykseen muokkamalla pituusjärjestys-attribuutin arvoa.

