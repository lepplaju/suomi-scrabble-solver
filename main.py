from apuohjelmat import alku_tai_lopetushaku, perushaku, sisaltaa_sanan_haku, edistynyt_haku
from tukitoiminnot import sanojen_lukeminen

# Ohjelman pyörii loputtomassa silmukassa tässä. Ohjelman voi lopettaa syöttämällä kirjainten käsittelyn metodiksi "0"
while True:
    print('\nValitse kirjainten käsittelyn metodi: \n1) Perushaku, 2) aloitus- tai lopetuskirjain erikseen, 3) sisältää sanan, 4) Edistynyt haku, 0) Lopeta ohjelma')
    metodi = input()
    if metodi == '0':
        break

    if metodi == '1':
        print("\nAnna kädessä olevat kirjaimet:")
        kirjaimet = input()
        perushaku.perushaku(kirjaimet)
        continue
    elif metodi == '2':
        print("Anna kädessä olevat kirjaimet ja välilyönnillä erotettuna sanan aloitus- tai lopetusehto (esim \"..n\"):")
        syote = input()
        alku_tai_lopetushaku.alku_tai_lopetushaku(syote)
        continue
    elif metodi == '3':
        print("Anna kädessä olevat kirjaimet ja välilyönnillä erotettuna sana, jonka täytyy olla tuloksissa:")
        syote = input()
        kirjaimet, poyta = syote.split(' ')
        sisaltaa_sanan_haku.sisaltaa_sanan(kirjaimet, poyta)
        continue
    elif metodi == '4':
        print("Anna kädessä olevat kirjaimet ja edistynyt hakuehto:")
        syote = input()
        kirjaimet, poyta = syote.split(' ')
        edistynyt_haku.edistynyt_haku(kirjaimet, poyta)
        continue
    elif metodi == '0':
        print('Ohjelma lopetetaan')
        break
    else: 
        print('Virheellinen syöte!')
        continue