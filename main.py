from random import randint

def lueTiedosto(data):
    print("Aloitetaan tiedostosta lukeminen")
    try:
        file = open("data.txt", "r")
    except:
        print("Tiedoston lukeminen epaonnistui")
        return data
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
                
    
    
def tallennaTiedosto(data, arvottu):
    
    print("Aloitetaan tiedostoon tallentaminen")

    try:
        file = open("data.txt", "w")
    except:
        print("Tiedoston lukeminen epaonnistui")
        return data
    
    file.write("Tama on secret santan datatiedosto. ")
    file.write("Data on muotoa Nimi, kohde, kiellot\n")
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

def luoTiedostot(data):
    
    print("Tehdaan ykisttaiset tiedostot")
    laskin = 0
    for nimi in data:
        tnimi = "5"+ str(randint(1000, 10000)) + "-" + nimi.lower()
        try:
            file = open(tnimi, "w")
        except:
            print("Tiedoston avaaminen epaonnistui,", laskin, "nimea tallenenttu")
            return data
        file.write(nimi + "\nSinulle on arvottu\n" + data[nimi][0]) 
        file.close()
        laskin += 1
    print(laskin, "tiedostoa tehty onnistuneesti")
        
def syotaTietoja(data, arvottu):
    
    if not arvottu:
        nimi = input("Syota henkilon nimi: ")
        data[nimi] = [None]
        syote = " "
        while syote != "":
            syote = input("Syota henkilon kielletyt henkilot: ")
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
    return data, arvottu

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
    arvottu = False
    
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
        print("Ladattuna", len(data), "nimiketietoa")
        if arvottu:
            print("Parit on jo arvottu")
        else:
            print("Pareja ei ole viela arvottu")
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
            data, arvottu = syotaTietoja(data, arvottu)
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
        else:
            print("Vaara arvo")
    





main()
