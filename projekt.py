#Autosõidu kulu arvutamine
def autokulu(distants, kütusekulu, kütusehind):
    rahakulu = round((distants/100) * kütusehind * kütusekulu, 2)
    return rahakulu

def autoaeg(distants):
    kesk_linnas = 35
    kesk_maanteel = 90
    #Keskmine kiirus linnas autoga on 35km/h
    #Maanteel liikudes 80km/h
    #Arvestame, et linna raadius on 10km, seega selles vahemikus on linnakiirus, pikema distantsi puhul lisatakse maanteekiirus
    kokku = None
    if distants <= 10:
        kokku = distants / kesk_linnas
    elif distants > 10:
        distants -= 10
        linnas = 10 / kesk_linnas
        maanteeaeg = distants / kesk_maanteel
        
        kokku = linnas + maanteeaeg
    minutites = round(kokku * 60)
    return minutites

#Bussikulude arvutamine
def bussikulu(soodustus):
    pilet = None
    if soodustus == True:
        pilet = 1
    else:
        pilet = 1.5
    return pilet

#Hetkel teeb kasutajalt küsimisega
#def bussiaeg(distants)

#ratta, tõukerattaga liigeldes kulud
def kergliikleja_aeg(distants, jalgsi):
    if jalgsi == True:
        jalakiirus = 5
        aeg = distants / jalakiirus
    else:
        #(elektri)Ratta ja elektritõukeratta keskmine kiirus
        kesk_kiirus = 15
        aeg = distants / kesk_kiirus
    minutites = round(aeg * 60)
        
    return minutites

#andmed vajavad verifitseerimist
def rendi_kergliikleja_kulud(distants):
    aeg = kergliikleja_aeg(distants, False)
    #Boltist võetud hinnad
    avamistasu = 0.2
    ajahind = 0.24
    
    kokku = round(avamistasu + (aeg * ajahind), 2)
    return kokku, aeg

#takso kulud
def takso_hind(distants):
    aeg = autoaeg(distants)
    stardihind = 2
    #Väga üldistatud hinnad, hiljem täpsustab
    distantsihind = 0.9
    ajahind = 0.2
    
    kokku = round(stardihind + (distants * distantsihind) + (aeg * ajahind), 2)
    return kokku


def main():
    #Tõenäoliselt läheb see ümber tegemisele kui hakata teostama kasutajaliidest
    while True:
        try:
            distants = float(input("Sisesta läbitav distants: "))
            print("Liikumisvariandid:\n 1 = Auto\n 2 = Buss\n 3 = Jalgsi\n 4 = Rendi(tõuke)ratas\n 5 = Takso\n 6 = Oma (elektri)(tõuke)ratas")
            meetod = int(input("Sisesta liikumisvariant: "))
            break
        except:
            print("Vigane sisend!")
            continue
    
    if meetod == 1:
        liitrit_sajale = float(input("Sisesta kütusekulu (l/100km): "))
        kütusehind = 1.5 #Hiljem automatiseerib selle väärtuse saamist
        raha = autokulu(distants, liitrit_sajale, kütusehind)
        aeg = autoaeg(distants)
        print(f"Autoga liikudes kulub ühe päevaga {2 * raha}€ ja {2 * aeg} minutit.")
        
    elif meetod == 2:
        soodustus = False
        kas_soodustus = input("Kas sa oled Tartusse sisse kirjutada (y/n): ")
        if kas_soodustus == "y":
            soodustus = True
        ajakulu = int(input("Mitu minutit kestab sinu bussisõit?: "))
        hind = bussikulu(soodustus)
        print(f"Bussiga liikudes kulub ühe päevaga {2 * hind}€ ja {2 * ajakulu} minutit.")
        
    elif meetod == 3:
        aeg = kergliikleja_aeg(distants, True)
        print(f"Jalgsi käies kulub päevas 0€(!) ja {2 * aeg} minutit.")
        
    elif meetod == 4:
        raha, aeg = rendi_kergliikleja_kulud(distants)
        print(f"Rentides elektri(tõuke)ratast kulub päevas {2 * raha}€ ja {2 * aeg} minutit.")

    elif meetod == 5:
        aeg = autoaeg(distants)
        raha = takso_hind(distants)
        print(f"Taksoga liigeldes kulub päevas {2 * raha}€ ja {2 * aeg} minutit.")
        
    elif meetod == 6:
        aeg = kergliikleja_aeg(distants, False)
        print(f"Oma (tõuke)rattaga käies kulub päevas 0€(!) ja {2 * aeg} minutit.")
        
if __name__ == "__main__":
    main()