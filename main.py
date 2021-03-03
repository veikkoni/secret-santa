"""
Secret santa arpomis sovellus
Veikko Nieminen
"""
from random import randint
import time

TIME = 0.01
DATAFILE = "data.txt"
WISHFILE = "wishes.txt"
TNIMIVAKIO = "5" #Tuotettavien tiedostojen etuliite
STRING1 = '<meta name="viewport" content="width=device-width, initial-scale=1.0; user-scalable=no"><body style="margin: 0px;"><div style="background-image: url(\'https://i.imgur.com/vZkXw9l.jpg\'); height:100%; width:100%; background-size:cover; margin-top: 0px;""><div style="width: 100%; height: 100%; padding-top: 30%; padding-left:20%;"><div style="border: 2px solid black; padding: 15px; width:45%; min-width: 200px; overflow-wrap: break-word; font-family: Arial, Helvetica, sans-serif; border-radius: 10px; background-color: #ffffff; max-width: 300px; font-size: 14px"><center>Hei <B>'
STRING2 = '</B>!<br><br>Sinulle on arvottu<br><B>'
STRING3 = '</B><br><br>Hänen toiveensa:<br>"'
STRING4 = '"<br><br>Ei toivottua:<br>"'
STRING5 = '"<br><img src="https://i.imgur.com/mhNXPHL.png" height="180vi" width="180vi"><br>Budjetti ~20€</center></div></div></div></body>'

def lue_tiedosto(data):
    """Lukee datan tiedostosta"""

    print("Aloitetaan tiedostosta lukeminen")
    try:
        file = open(DATAFILE, "r")
    except Exception:
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


def lue_toive_tiedosto(wishes):
    """Lukee toiveet tiedostosta"""

    print("Aloitetaan toiveiden lukeminen tiedostosta")
    try:
        file = open(WISHFILE, "r")
    except Exception:
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


def tallenna_tiedosto(data, arvottu):
    """Talentaa datan tiedostoon"""

    print("Aloitetaan tiedostoon tallentaminen")

    try:
        file = open(DATAFILE, "w")
    except Exception:
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

def tallenna_toive_tiedosto(wishes):
    """Tallentaa toiveet tiedostoon"""

    print("Aloitetaan toiveiden tallentaminen tiedostoon")

    try:
        file = open(WISHFILE, "w")
    except Exception:
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

def luo_tiedostot(data, wishes):
    """Luo arvoituista tiedoista henkilökohtaiset tiedostot"""

    print("Tehdaan ykisttaiset tiedostot")
    laskin = 0
    for nimi in data:
        tnimi = TNIMIVAKIO + str(randint(1000, 10000)) + "-" + nimi.lower()+".html"
        try:
            file = open(tnimi, "w")
        except Exception:
            print("Tiedoston avaaminen epaonnistui,", laskin, "nimea tallenenttu")
            return data
        toive, epatoive = wishes[data[nimi][0]].split("/")
        if toive == "Empty":
            toive = ""
        if epatoive == "Empty":
            epatoive = ""
        file.write(STRING1 + nimi + STRING2 + data[nimi][0] + STRING3 + toive + STRING4 + epatoive + STRING5)
        file.close()
        laskin += 1
    print(laskin, "tiedostoa tehty onnistuneesti")


def syota_tietoja(data, arvottu, wishes):
    """Lisää uusia henkilöitä"""

    if not arvottu:
        nimi = input("Syota henkilon nimi: ")
        wish = input("Syöta henkilon toive (Jätä tyhjäksi käyttääksesi tiedoston toivetta): ")
        if wish != "":
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

def suorita_arvonta(data):
    """Arpoo secret santat kaikille"""

   # tallenna_tiedosto(data, False)
    lista = sorted(data)
    ongelmat = 0
    for nimi in data:
        data[nimi].pop(0)
        pahatNimet = []
        for pahaNimi in data[nimi]:
            pahatNimet.append(pahaNimi)
        data[nimi].insert(0, "None")
        jatka = True
        kiellettu = False
        while jatka is True:
            if ongelmat >= 30:
        #        print("Arvonta epaonnistui")
                return data, False
            x = randint(0, len(lista)-1)
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

    #if ongelmat < 30:
   #     print("Arvonta suoritettu onnistuneesti")

    return data, True

def tarkista_tiedot(data, arvottu):
    """Tarkistaa secret santojen toimivuuden"""

#    if not arvottu:
#        print("Tietoja ei ole viela arvottu")
#        return

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

def arvonta_wrapped(data):
    rounds = 0
    while rounds <= 1000:
        users, arvottu = suorita_arvonta(data)
        if arvottu == True:
            print("Arvonta onnistui")
            return users, arvottu
        else:
            rounds += 1
    print("Arvonta ei onnistunut")        
    return data, False


def main():
    """Päävalikko"""

    data = {}
    wishes = {}
    arvottu = False
    jatka = True

    for i in range(0, 60):
        print()

    teksti = "Tervetuloa secret santa arvontaohjelmaan. Alla muutama kayttoa helpottava ohje: Jos"+\
    "sinulla on jo käytössä tiedostoja kuten toive tai data, lataa se ennen kuin lisäät lietoja, "+\
    "muuten ne ylikirjoitetaan. Nimiketietoja pystyy muokkaamaan lisämmällä samannimisen henkilön"+\
    "uudestaan oikeilla tiedoilla. Poistaminen ja laajempi muokkaus kannattaa tehdä suoraan teido"+\
    "stoa muokaten. Arvontaa ennen tapahtuu automaattinen tallennus."

    #for i in range(len(teksti)):
   #     print(teksti[i], end="", flush=True)
    #    time.sleep(TIME) #Ei toimi chromebookissa
    print()

    while jatka:
        print()
        input("Paina jatkaaksesi...")
        for i in range(0, 60):
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
        except Exception:
            print("Vaara arvo")
            continue

        for i in range(0, 60):
            print()

        if userInput == 0:
            print("Kiitos ja hei")
            jatka = False
        elif userInput == 1:
            data, arvottu, wishes = syota_tietoja(data, arvottu, wishes)
        elif userInput == 2:
            tallenna_tiedosto(data, arvottu)
        elif userInput == 3:
            data, arvottu = lue_tiedosto(data)
        elif userInput == 4:
            data, arvottu = arvonta_wrapped(data)
        elif userInput == 5:
            luo_tiedostot(data, wishes)
        elif userInput == 6:
            tarkista_tiedot(data, arvottu)
        elif userInput == 7:
            wishes = lue_toive_tiedosto(wishes)
        elif userInput == 8:
            tallenna_toive_tiedosto(wishes)
        else:
            print("Vaara arvo")

    return 0


main()
