kirjainpisteet = {
    'a': 1, 'i': 1, 'n': 1, 's': 1, 't': 1, 'e': 1,'k': 2, 'l': 2, 'o': 2, 'ä': 2,'u': 3, 'm': 3,'h': 4, 'j': 4, 'p': 4, 'r': 4, 'y': 4, 'v': 4,'f':8,'d': 7, 'ö': 7, 'g':8,'b':8,'c': 10,'w': 0, 'q': 0,'x':0,'*': 0, 'à':0,'z':0,'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0,'š':0, 'é':0
}

def get_pisteet(sana):
    summa = 0
    for char in sana:
        if char in kirjainpisteet:
            summa += kirjainpisteet[char]
    return summa