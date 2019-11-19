from random import randint
import time

DATAFILE = "data.txt"
WISHFILE = "wishes.txt"
TNIMIVAKIO = "4" #Tuotettavien tiedostojen etuliite

def lueTiedosto(data):
    print("Aloitetaan tiedostosta lukeminen")
    try:
        file = open(DATAFILE, "r")
    except:
        print("Tiedoston lukeminen epaonnistui")
        return data, False
    next(file)
    laskuri = 0
    for rivi in file:
        laskuri += 1
        rivi = rivi[:-1]
        sanat = rivi.split(";")
        key = str(sanat[0])
        data[key] = []
        sanat.pop(0)
        for i in range(len(sanat)):
            data[key].append(sanat[i])

    print(laskuri, "nimiketietoa haettu tiedostosta")
    file.close()
    
    arvottu = True
    
    for nimi in data:
        if data[nimi][0] == "None":
            arvottu = False
    
    return data, arvottu


def lueToiveTiedosto(wishes):
    print("Aloitetaan toiveiden lukeminen tiedostosta")
    try:
        file = open(WISHFILE, "r")
    except:
        print("Tiedoston lukeminen epaonnistui")
        return wishes
    next(file)
    laskuri = 0
    for rivi in file:
        laskuri += 1
        rivi = rivi[:-1]
        sanat = rivi.split(";")
        wishes[str(sanat[0])] = str(sanat[1])

    print(laskuri, "toivetta haettu tiedostosta")
    file.close()
    
    return wishes
    
    
def tallennaTiedosto(data, arvottu):
    
    print("Aloitetaan tiedostoon tallentaminen")

    try:
        file = open(DATAFILE, "w")
    except:
        print("Tiedoston lukeminen epaonnistui")
        return data
    
    file.write("Tama on secret santan datatiedosto. ")
    file.write("Data on muotoa nimi;kohde;kiellot\n")
    laskuri = 0
    for nimi in sorted(data):
        laskuri += 1
        teksti = nimi
        for i in range(len(data[nimi])):
            teksti += ";" + str(data[nimi][i])
        teksti += "\n"
        file.write(teksti)

    file.close()    
    print(laskuri, "nimiketietoa tallennettu tiedostoon")
    
    return data

def tallennaToiveTiedosto(wishes):
    
    print("Aloitetaan toiveiden tallentaminen tiedostoon")

    try:
        file = open(WISHFILE, "w")
    except:
        print("Tiedoston lukeminen epaonnistui")
        return
    
    file.write("Tama on secret santan toivetiedosto. ")
    file.write("Data on muotoa nimi;toive\n")
    laskuri = 0
    for nimi in sorted(wishes):
        laskuri += 1
        teksti = nimi + ";" + wishes[nimi] + "\n"
        file.write(teksti)

    file.close()    
    print(laskuri, "toivetta tallennettu tiedostoon")
    
    return

def luoTiedostot(data):
    
    print("Tehdaan ykisttaiset tiedostot")
    laskin = 0
    for nimi in data:
        tnimi = TNIMIVAKIO + str(randint(1000, 10000)) + "-" + nimi.lower()
        try:
            file = open(tnimi, "w")
        except:
            print("Tiedoston avaaminen epaonnistui,", laskin, "nimea tallenenttu")
            return data
        file.write(nimi + "\nSinulle on arvottu\n" + data[nimi][0]) 
        file.close()
        laskin += 1
    print(laskin, "tiedostoa tehty onnistuneesti")
        
def syotaTietoja(data, arvottu, wishes):
    
    if not arvottu:
        nimi = input("Syota henkilon nimi: ")
        wish = input("Syöta henkilon toive (Jätä tyhjäksi käyttääksesi tiedoston toivetta): ")
        if (wish != ""):
            wishes[nimi] = wish
        data[nimi] = [None]
        syote = " "
        while syote != "":
            syote = input("Syota henkilon kielletyt henkilot (Paina enter kun valmis): ")
            if syote != "":
                data[nimi].append(syote)
    else:
        print("Homma on jo arvottu, kannattaako lisata?")
        print("0 Ei")
        print("1 Kylla")
        if int(input("Syote: ")) == 1:
            nimi = input("Syota henkilon nimi: ")
            data[nimi] = []
            
    arvottu = False
    return data, arvottu, wishes

def suoritaArvonta(data):
    tallennaTiedosto(data, False)
    lista = sorted(data)
    for nimi in data:
        data[nimi].pop(0)
        pahatNimet = []
        for pahaNimi in data[nimi]:
            pahatNimet.append(pahaNimi)
        data[nimi].insert(0, "None")        
        ongelmat = 0
        jatka = True
        kiellettu = False
        while jatka is True:
            if ongelmat >= 30:
                print("Arvonta epaonnistui")
                return data, False
            x = randint(0,len(lista)-1)
            arvottuNimi = lista[x]
            if arvottuNimi != nimi:
                for kielletty in pahatNimet:
                    if arvottuNimi == kielletty:
                        kiellettu = True
                        
                if not kiellettu:
                    lista.pop(x)
                    data[nimi].pop(0)
                    data[nimi].insert(0, arvottuNimi)
                    jatka = False
            ongelmat += 1

    if ongelmat < 30:
        print("Arvonta suoritettu onnistuneesti")
                    
    return data, True

def tarkistaTiedot(data, arvottu):
    
    
    if not arvottu:
        print("Tietoja ei ole viela arvottu")
        return
    
    ongelmia = 0
    lista = sorted(data)
    
    for nimi in sorted(data):
        for nimi2 in data[nimi]:
            if nimi2 not in lista:
                ongelmia += 1
                print(nimi, "henkilon kielto", nimi2, "ei loytynyt osallistujista")

    if ongelmia > 0:
        print("Yhteensa", ongelmia, "kielloista on turhia")

    
    for nimi in sorted(data):
        kielletty = data[nimi][0]
        lista = data[nimi].copy()
        lista.pop(0)
        for nimi2 in lista:
            if nimi2 == kielletty:
                ongelmia += 1
                print("ONGELMA:", nimi, "sai kielletyn henkilon")

    lista = sorted(data).copy()
    lista2 = []
    for nimi in data:
        lista2.append(data[nimi][0])
    lista2 = sorted(lista2)
    if len(lista) == len(lista2):
        for nimi in lista:
            if nimi in lista2:
                lista.remove(nimi)
                lista2.remove(nimi)
    else:
        ongelmia += 1
        print("ONGELMA: Arvotut ei sama kuin osallistuja")
        
    if len(lista) != len(lista2):
        ongelmia += 1
        print("ONGELMA: Arvotut ei tasmaa osallistujia")

    print("Kohdattiin", ongelmia, "ongelmaa")
    return        

def main():
    data = {}
    wishes = {}
    arvottu = False
    for i in range(0,60):
        print()
    teksti = "Tervetuloa secret santa arvontaohjelmaan. Alla muutama kayttoa helpottava ohje: Jos sinulla on jo käytössä tiedostoja kuten toive tai data, lataa se ennen kuin lisäät lietoja, muuten ne ylikirjoitetaan. Nimiketietoja pystyy muokkaamaan lisämmällä samannimisen henkilön uudestaan oikeilla tiedoilla. Poistaminen ja laajempi muokkaus kannattaa tehdä suoraan teidostoa muokaten. Arvontaa ennen tapahtuu automaattinen tallennus."
    for i in teksti:
        print(i, end="")
        #time.sleep(0.1) #Ei toimi chromebookissa

    while True:
        print()
        input("Paina jatkaaksesi...")
        for i in range(0,60):
            print()
        print("0 Lopeta ohjelma")
        print("1 Syota tietoja")
        print("2 Tallenna tiedostoon")
        print("3 Lue tiedostosta")
        print("4 Arvo parit")
        print("5 Luo nimelliset tiedostot")
        print("6 Tarkista arvot")
        print("7 Lue toiveet tiedostosta")
        print("8 Tallenna toiveet tiedostoon")
        print()
        print("Ladattuna", len(data), "nimiketietoa")
        if arvottu:
            print("Parit on jo arvottu")
        else:
            print("Pareja ei ole viela arvottu")

        print("Ladattuna", len(wishes), "toivetta")
        print()
    
        try:
            userInput = int(input("Mita haluat tehda: "))
        except:
            print("Vaara arvo")
            continue

        for i in range(0,60):
            print()

        if userInput == 0:
            print("Kiitos ja hei")
            return 0
        elif userInput == 1:
            data, arvottu, wishes = syotaTietoja(data, arvottu, wishes)
        elif userInput == 2:
            tallennaTiedosto(data, arvottu)
        elif userInput == 3:
            data, arvottu = lueTiedosto(data)
        elif userInput == 4:
            data, arvottu = suoritaArvonta(data)
        elif userInput == 5:
            luoTiedostot(data)
        elif userInput == 6:
            tarkistaTiedot(data, arvottu)
        elif userInput == 7:
            wishes = lueToiveTiedosto(wishes)
        elif userInput == 8:
            tallennaToiveTiedosto(wishes)
        else:
            print("Vaara arvo")
    





main()
