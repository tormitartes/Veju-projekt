# ----- KONSTANDID (hinnad ja kiirused) -----

KÜTUSEHIND = 1.5
AUTO_KIIRUS_LINN = 35
AUTO_KIIRUS_MAANTEE = 90
LINNA_RAADIUS = 10

BUSSIPILET_TAVALINE = 1.50
BUSSIPILET_SOODUS = 1.00

JALA_KIIRUS = 5
RATTA_KIIRUS = 15

BOLT_AVAMINE = 0.20
BOLT_MINUT = 0.24     # hinnad Boltist võetud

TAKSO_START = 2.00
TAKSO_KM = 0.90       # väga üldistatud hinnad, vajavad verifitseerimist
TAKSO_MINUT = 0.20


# ----- ABIFUNKTSIOONID (sisendi küsimine) -----

def küsi_float(küsimus, miinimum=0.0):  # kasutatakse distantsi ja kütusekulu küsimisel
    """Küsib ujukomaarvu. Lubab koma või punkti. Kontrollib miinimumi."""
    while True:
        try:
            s = input(küsimus).replace(",", ".").strip()
            x = float(s)
            if x < miinimum:
                print(f"Palun sisesta arv suurem kui {miinimum}.")
            else:
                return x
        except ValueError:
            print("Vigane sisend! Palun sisesta number.")


def küsi_int_vahemikus(küsimus, min_v, max_v):  # kasutatakse transpordivaliku ja bussi aja küsimusel
    """Küsib täisarvu ja kontrollib, et see oleks vahemikus."""
    while True:
        try:
            x = int(input(küsimus).strip())
            if min_v <= x <= max_v:
                return x
            print(f"Palun sisesta arv vahemikus {min_v}-{max_v}.")
        except ValueError:
            print("Vigane sisend! Palun sisesta täisarv.")


# ----- ARVUTUSFUNKTSIOONID -----

def auto_kulu(distants_km, kütusekulu_l_100km):
    """Tagastab autosõidu rahalise kulu (ei ümarda)."""
    return (distants_km / 100) * KÜTUSEHIND * kütusekulu_l_100km


def auto_aeg_min(distants_km):
    """Tagastab autosõidu aja minutites (EI ümarda siin)."""
    if distants_km <= LINNA_RAADIUS:
        aeg_tundides = distants_km / AUTO_KIIRUS_LINN
    else:
        maantee_distants = distants_km - LINNA_RAADIUS
        linna_aeg = LINNA_RAADIUS / AUTO_KIIRUS_LINN
        maantee_aeg = maantee_distants / AUTO_KIIRUS_MAANTEE
        aeg_tundides = linna_aeg + maantee_aeg

    return aeg_tundides * 60


def bussi_kulu(soodustus):
    """Tagastab bussi pileti hinna."""
    if soodustus:
        return BUSSIPILET_SOODUS
    else:
        return BUSSIPILET_TAVALINE


def kergliikleja_aeg_min(distants_km, jalgsi):
    """Tagastab jalgsi/rattaga/tõuksiga liikumise aja minutites (EI ümarda siin)."""
    if jalgsi:
        kiirus = JALA_KIIRUS
    else:
        kiirus = RATTA_KIIRUS

    aeg_tundides = distants_km / kiirus
    return aeg_tundides * 60


def rendi_kergliikleja_kulu_ja_aeg(distants_km):
    """Tagastab renditõuksi/rendijalgratta kulu ja aja (aeg ei ole ümardatud)."""
    aeg_minutites = kergliikleja_aeg_min(distants_km, jalgsi=False)
    kulu = BOLT_AVAMINE + (aeg_minutites * BOLT_MINUT)  # ei ümarda
    return kulu, aeg_minutites


def takso_kulu(distants_km):
    """Tagastab takso rahalise kulu (ei ümarda)."""
    aeg_minutites = auto_aeg_min(distants_km)  # nüüd on see täpne (float) minutites
    return TAKSO_START + (distants_km * TAKSO_KM) + (aeg_minutites * TAKSO_MINUT)

# ----- PÕHIPROGRAMM -----

def main():
    distants_km = küsi_float("Sisesta läbitav distants (km): ", miinimum=0.0)

    print("\nLiikumisvariandid:")
    print(" 1 = Auto")
    print(" 2 = Buss")
    print(" 3 = Jalgsi")
    print(" 4 = Rendi(tõuke)ratas")
    print(" 5 = Takso")
    print(" 6 = Oma (elektri)(tõuke)ratas")

    valik = küsi_int_vahemikus("Sisesta liikumisvariandi number: ", 1, 6)

    raha_päevas = 0.0
    aeg_päevas = 0

    if valik == 1:  # Auto
        kütusekulu_l_100km = küsi_float("Sisesta auto kütusekulu (l/100km): ", miinimum=0.0)
        kulu_üks_ots = auto_kulu(distants_km, kütusekulu_l_100km)
        aeg_üks_ots = auto_aeg_min(distants_km)

        raha_päevas = 2 * kulu_üks_ots
        aeg_päevas = round(2 * aeg_üks_ots)
        print("Autoga koolis käimine (edasi-tagasi):")

    elif valik == 2:  # Buss
        while True:
            vastus = input("Kas oled Tartusse sisse kirjutatud? (y/n): ").strip().lower()
            if vastus in ("y", "n"):
                soodustus = (vastus == "y")
                break
            print("Palun vasta y või n.")

        bussi_aeg_min = küsi_int_vahemikus("Mitu minutit kestab sinu bussisõit?: ", 0, 100000)

        kulu_üks_ots = bussi_kulu(soodustus)
        raha_päevas = 2 * kulu_üks_ots
        aeg_päevas = 2 * bussi_aeg_min  # bussiaeg on täisarv, pole vaja ümardada
        print("Bussiga koolis käimine (edasi-tagasi):")

    elif valik == 3:  # Jalgsi
        aeg_üks_ots = kergliikleja_aeg_min(distants_km, jalgsi=True)
        raha_päevas = 0.0
        aeg_päevas = round(2 * aeg_üks_ots)
        print("Jalgsi koolis käimine (edasi-tagasi):")

    elif valik == 4:  # Rendiratas / renditõuks
        kulu_üks_ots, aeg_üks_ots = rendi_kergliikleja_kulu_ja_aeg(distants_km)
        raha_päevas = 2 * kulu_üks_ots
        aeg_päevas = round(2 * aeg_üks_ots)
        print("Renditõuksiga koolis käimine (edasi-tagasi):")

    elif valik == 5:  # Takso
        kulu_üks_ots = takso_kulu(distants_km)
        aeg_üks_ots = auto_aeg_min(distants_km)

        raha_päevas = 2 * kulu_üks_ots
        aeg_päevas = round(2 * aeg_üks_ots)
        print("Taksoga koolis käimine (edasi-tagasi):")

    elif valik == 6:  # Oma ratas
        aeg_üks_ots = kergliikleja_aeg_min(distants_km, jalgsi=False)
        raha_päevas = 0.0
        aeg_päevas = round(2 * aeg_üks_ots)
        print("Oma rattaga koolis käimine (edasi-tagasi):")

    print(f"Rahaline kulu: {raha_päevas:.2f}€")
    print(f"Ajaline kulu:  {aeg_päevas} minutit")


if __name__ == "__main__":
    main()

