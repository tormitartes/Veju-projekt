# KOOLI (ja tagasi) KÄIMISE KALKULAATOR
# Vastavalt meetodile arvutab välja kui palju raha ja aega kulub, et ühel päeval koolis käia
# Annab nii sulaselged numbrid kui ka graafiku, võrdlemaks erinevaid meetodeid
# Käivitamiseks vajuta vaid Start/Run program nuppu!
# PS! Lae vajalikud teegid kindlasti alla!
# Loojad: Tormi Tartes, Mattias Reimand | Tartu Ülikool 2025

# --- Teekide kasutamine ---
# UI impordid
import customtkinter as ctk

# Jooniste impordid
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# --- Üldised akna (UI) loomise asjad---
# Akende vahetamise funktsioonid
def alusta_vajutus(aken):
    aken.destroy()
    arvutusaken()

def tagasi_vajutus(aken):
    aken.destroy()
    avaaken()

# Nupuvajutusel programm sulgeb
def programm_kinni(akna_nimi):
    print("Programm lõpetamisel...")
    akna_nimi.destroy()

# Auto/bussi sisendite sisse/välja lülitamine vastavalt raadionuppude-valikule
def uuenda_sisendite_olek():
    
    aktiivne_värv = "#211d45"
    ebaaktiivne = "#2e101a"
    checkbox_värv = "#949a9f"
    
    # Hetkel aktiivse meetodi saamine
    m = valitu.get()

    if m == 0: # Ehk auto on valitud
        # lülitab sisse sobivad kastid, mittevajaliku lülitab välja. Teised samasuguse struktuuriga 
        kütush_sisend.configure(state="normal", fg_color=aktiivne_värv)
        kütusk_sisend.configure(state="normal", fg_color=aktiivne_värv)
        bussipilet_sisend.configure(state="disabled", fg_color=ebaaktiivne, border_color="gray15")
        bussiaeg_sisend.configure(state="disabled", fg_color=ebaaktiivne)

    elif m == 1:
        kütush_sisend.configure(state="disabled", fg_color=ebaaktiivne)
        kütusk_sisend.configure(state="disabled", fg_color=ebaaktiivne)
        bussipilet_sisend.configure(state="normal", fg_color=aktiivne_värv, border_color=checkbox_värv)
        bussiaeg_sisend.configure(state="normal", fg_color=aktiivne_värv)

    else:  # teiste meetodite puhul lülitab nii auto kui bussi sisendid välja
        kütush_sisend.configure(state="disabled", fg_color=ebaaktiivne)
        kütusk_sisend.configure(state="disabled", fg_color=ebaaktiivne)
        bussipilet_sisend.configure(state="disabled", fg_color=ebaaktiivne, border_color="gray15")
        bussiaeg_sisend.configure(state="disabled", fg_color=ebaaktiivne)

# Vastavalt sisenditele genereerib vastused ja graafiku
def Genereerimise_nupp():
    print("Gen-nupp vajutatud!")
    print(f"Valitud meetodi number: {valitu.get()}.")
    main() # Vastuste kuvamine tõstetud main funktsiooni sisse
    

# Akna sätted
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue") # Valikud: "blue" , "dark-blue" and "green"

# Akna nimi on katsetamise aegadest jäänud test, kuid seda mujal välja ei paista
test = ctk.CTk()
test.title("Summaator")
test.geometry("800x700")


# --- Avaakna asjad ---
def avaaken():
    esileht = ctk.CTkFrame(test)
    esileht.pack(fill="both", expand=True)
    # .pack käitub erinevalt kui grid, kuid siin lehel saab sellega veel hakkama

    tekst = ctk.CTkLabel(
        esileht,
        text="Kooli pendeldamise kulukalkulaator",
        font=ctk.CTkFont(size=40, weight="bold"),
        anchor="center",
        justify="center"
        )
    tekst.pack(fill="x", pady=(200, 0))

    # Nuppude loomine
    button = ctk.CTkButton(
        esileht,
        text="Alusta!",
        font=ctk.CTkFont(size=20),
        command=lambda: alusta_vajutus(esileht)
        )
    # Ja paigutamine aknasse
    button.pack(pady=(40, 20))

    sulge = ctk.CTkButton(
        esileht,
        text="Sulge programm",
        font=ctk.CTkFont(size=18),
        fg_color="red2",
        hover_color="red4",
        command=lambda: programm_kinni(test))
    sulge.pack(pady=40)

    # Jalus
    valmistajad = ctk.CTkLabel(
        esileht,
        text="© Tormi Tartes, Mattias Reimand | Proge projekt 2025",
        font=("Arial", 15))
    valmistajad.pack(side = "bottom", fill="x", pady=(60, 0))

    # Avalehel kasutamata, aga kasulik et hiljem näha kuidas seda uuesti teha
    """
    sisesta = ctk.CTkEntry(
        master=test,
        placeholder_text="Tekst tekst tekst",
        width=200,
        height=30,
        border_width=2,
        corner_radius=10
    )
    sisesta.pack(pady=10)
    """
    

# --- Arvutusakna asjad ---
def arvutusaken():
    # Siin .grid süsteem kasutusel. 
    # Mõned muutujad peavad olema globaalsed, et neid väljastpoolt saaks muuta/näha
    global distants_sisend
    global valitu
    global arvutus
    global kütusk_sisend
    global kütush_sisend
    global pilet_olek
    # Kastide sisse/välja lülitamisel vaja need ka globaalseks teha
    global bussipilet_sisend
    global bussiaeg_sisend
    
    # Sisendite värvid vastavalt olekule
    aktiivne_värv = "#211d45"
    ebaaktiivne = "#2e101a"
    checkbox_värv = "#949a9f"
    
    # Akna konfigureerimine grid süsteemis, et saaks alamraame luua
    test.grid_rowconfigure(5, weight=1)
    test.grid_columnconfigure(5, weight=1)
    
    # Arvutusakna peamine raam
    arvutus = ctk.CTkFrame(test, fg_color="transparent")
    arvutus.grid(row=5, column=5, sticky="nsew")
    arvutus.grid_columnconfigure(0, weight=1)
    arvutus.grid_rowconfigure(7, weight=1) # Alumine tekst võtab ülejäänud vaba ruumi enda alla
    # Püha jumal need grid-id ja frame-id on segased asjad

    # Navigeerimisnuppude kood
    kontrollriba = ctk.CTkFrame(
        arvutus,
        fg_color="transparent"
        )
    kontrollriba.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
    kontrollriba.grid_columnconfigure(0, weight=1)
        
    tagasi_nupp = ctk.CTkButton(
        kontrollriba,
        text="Tagasi avalehele",
        font=ctk.CTkFont(size=20),
        command=lambda: tagasi_vajutus(arvutus)
        )
    tagasi_nupp.grid(row=0, column=0, sticky="w")

    sulge_nupp = ctk.CTkButton(
        kontrollriba,
        text="Sulge programm",
        font=ctk.CTkFont(size=20),
        fg_color="red2",
        hover_color="red4",
        command= lambda: programm_kinni(test))
    sulge_nupp.grid(row=0, column=1, sticky="e")


    # Elemendi ülesseadmine 
    Vali_meetod = ctk.CTkLabel(
        arvutus,
        text="Vali transpordimeetod: ",
        font=("Arial", 24),
        fg_color="transparent"
        )
    # Sellesama elemendi paigaldamine aknasse, samasugune struktuur mujal
    Vali_meetod.grid(row=1, column=0, padx=20, pady=10)
    #Kuna ta on ainus element siin reas, siis talle ei tee eraldi raami


    # Raadionupud
    valikud = ctk.CTkFrame(
        arvutus,
        fg_color="gray13"
        )
    valikud.grid(row=3, column=0, pady=10, sticky="ew", padx=20)

    # Valitud meetodi väärtus, vaikimisi 0 (auto)
    valitu = ctk.IntVar(value=0)
    
    # Valikute nuppude loomine ja asetamine
    meetodid = ["Auto", "Buss", "Jalgsi", "Renditõuks", "Takso", "Oma ratas"]
    for i, meetod in enumerate(meetodid): # i on järjekorranumber
        ctk.CTkRadioButton(
            valikud,
            text=meetod,
            font=ctk.CTkFont(size=18),
            variable=valitu,
            value=i,
            command=uuenda_sisendite_olek
            ).grid(row=0, column=i, padx=10, pady=10)
        # Et need asuks keskel, võrdsel kaugusel teineteisest
        valikud.grid_columnconfigure(i, weight=1)


    # Sisendite raam, jaotus
    sisendid = ctk.CTkFrame(
        arvutus,
        fg_color="gray12"
        )
    sisendid.grid(row=4, column=0, sticky="ew", padx=20, pady=10)
    sisendid.grid_rowconfigure((0, 4), weight=1)
    sisendid.grid_columnconfigure((0, 1), weight=1)

    # Distantsi asjad
    seletus1 = ctk.CTkLabel(
        sisendid,
        text="Igal juhul vaja:",
        font=ctk.CTkFont(size=20, weight="bold")
        )
    seletus1.grid(row=0, column=0, padx=5, pady=5)

    distants_tekst = ctk.CTkLabel(
        sisendid,
        text="Distants (km)",
        font=ctk.CTkFont(size=18)
        )
    distants_tekst.grid(row=1, column=0, padx=5, pady=5)

    distants_sisend = ctk.CTkEntry(
        sisendid,
        placeholder_text="Sisesta distants (km)",
        fg_color=aktiivne_värv
        )
    distants_sisend.grid(row=1, column=1, padx=5, pady=5)

    # Kütuse hinna asjad
    seletus2 = ctk.CTkLabel(
        sisendid,
        text="Auto puhul vaja:",
        font=ctk.CTkFont(size=20, weight="bold")
        )
    seletus2.grid(row=2, column=0, padx=5, pady=5)

    kütush_tekst = ctk.CTkLabel(
        sisendid,
        text="Kütuse hind (€/l) (vaikimisi 1.5€)",
        font=ctk.CTkFont(size=18)
        )
    kütush_tekst.grid(row=3, column=0, padx=5, pady=5)

    global kütusväärtus # Mõned global väärtused pole üles tõstetud et vajadusel saaks kergelt neid vahetada, leida seotud element
    kütusväärtus = ctk.DoubleVar(value=1.5)
    kütush_sisend = ctk.CTkEntry(
        sisendid,
        placeholder_text="Kütuse hind",
        textvariable=kütusväärtus
        )
    kütush_sisend.grid(row=3, column=1, padx=5, pady=5)

    # Kütuse kulu asjad
    kütusk_tekst = ctk.CTkLabel(
        sisendid,
        text="Kütusekulu (l/100km)",
        font=ctk.CTkFont(size=18)
        )
    kütusk_tekst.grid(row=4, column=0, padx=5, pady=5)
    
    kütusk_sisend = ctk.CTkEntry(
        sisendid,
        placeholder_text="Kütusekulu",
        )
    kütusk_sisend.grid(row=4, column=1, padx=5, pady=5)

    #Bussi asjad
    seletus3 = ctk.CTkLabel(
        sisendid,
        text="Bussi puhul vaja:",
        font=ctk.CTkFont(size=20, weight="bold")
        )
    seletus3.grid(row=5, column=0, padx=5, pady=5)

    bussipilet_tekst = ctk.CTkLabel(
        sisendid,
        text="Bussi puhul sooduspilet",
        font=ctk.CTkFont(size=18)
        )
    bussipilet_tekst.grid(row=6, column=0, padx=5, pady=5)
    
    pilet_olek=ctk.BooleanVar() # Annab kas False või True
    bussipilet_sisend = ctk.CTkCheckBox(
        sisendid,
        text="Olemas?",
        variable=pilet_olek
        )
    bussipilet_sisend.grid(row=6, column=1, padx=5, pady=5)

    bussiaeg_tekst = ctk.CTkLabel(
        sisendid,
        text="Kui kaua bussisõit kestab (min)",
        font=ctk.CTkFont(size=18)
        )
    bussiaeg_tekst.grid(row=7, column=0, padx=5, pady=5)
    
    global bussisisend
    bussisisend = ctk.IntVar()
    bussiaeg_sisend = ctk.CTkEntry(
        sisendid,
        placeholder_text="Bussisõidu aeg (min)",
        textvariable=bussisisend
        )
    bussiaeg_sisend.grid(row=7, column=1, padx=5, pady=5)
    
    # kastide deaktiveerimise osa, programmi käivitades vaja korra jooksutada
    uuenda_sisendite_olek()


    # Tulemuste genereerimise nupp
    gen_nupp = ctk.CTkButton(
        arvutus,
        text="Genereeri tulemused ja graafik",
        font=ctk.CTkFont(size=20),
        command= lambda: Genereerimise_nupp()  
        )
    gen_nupp.grid(row=5, column=0, padx=20, pady=(20, 10))
    

    # --- Tulemuste kuvamine ---
    tulemused = ctk.CTkFrame(
        arvutus,
        fg_color="transparent"
        )
    tulemused.grid(row=6, column=0, padx=20, pady=10, sticky="nsew")
    tulemused.grid_rowconfigure((0, 1), weight=1)
    tulemused.grid_columnconfigure((0, 1), weight=1)

    # Raha asjad
    rahaline_kulu = ctk.CTkLabel(
        tulemused,
        text="Rahaline kulu:",
        font=ctk.CTkFont(size=18)
        )
    rahaline_kulu.grid(row=0, column=0, padx=5, pady=5, sticky="e")

    global rahaline_summa
    rahaline_summa = ctk.CTkLabel(
        tulemused,
        text="",
        font=ctk.CTkFont(size=18),
        )
    rahaline_summa.grid(row=0,column=1, padx=5, pady=5, sticky="w")
        
    # Aja asjad
    ajaline_kulu= ctk.CTkLabel(
        tulemused,
        text="Ajaline kulu:",
        font=ctk.CTkFont(size=18),
        )
    ajaline_kulu.grid(row=1, column=0, padx=5, pady=5, sticky="e")

    global ajaline_summa
    ajaline_summa = ctk.CTkLabel(
        tulemused,
        text="",
        font=ctk.CTkFont(size=18),
        )
    ajaline_summa.grid(row=1, column=1, padx=10, pady=10, sticky="w")
    
    # Programmi katsetamisel kasutatud element, nüüd kasutatud hoiatusena
    debug = ctk.CTkFrame(
        arvutus,
        fg_color="gray9",
        )
    debug.grid(row=7, column=0, padx=5, sticky="nesw")
    debug.grid_columnconfigure(0, weight=1)
    debug.grid_rowconfigure(0, weight=1) #See rida vist ei tee midagi
    
    global bugtext
    bugtext = ctk.CTkLabel(
        debug,
        text="""Tähelepanu! Tulemusi arvutatakse edasi-tagasi käiku arvestades.
Programmi algoritmid ei pruugi olla täpsed, kasuta omal vastutusel.
Loojad ei hüvita ebatäpsetest summadest tulenevaid kulutusi.""",
        font=ctk.CTkFont(size=12)
        )
    bugtext.grid(row=0, column=0)
    
    # Kui vaja bugtexti kasutada oma päris eesmärgil, siis siit saab pärast uuesti
    # muidu kasutuses oleva teksti kätte
    """Tähelepanu! Tulemusi arvutatakse edasi-tagasi käiku arvestades.
Programmi algoritmid ei pruugi olla täpsed, kasuta omal vastutusel.
Loojad ei hüvita ebatäpsetest summadest tulenevaid kulutusi."""

# Graafiku-, põhiprogramm järgmisena
#Mõned asjad muudetud, et töötaks kasutajaliidesega

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
TAKSO_KM = 0.90       # väga üldistatud hinnad
TAKSO_MINUT = 0.20 

# ----- GRAAFIKU KONSTANDID (varieeruvus) -----

AUTO_KÜTUSEKULU_VAIKIMISI = 8.0
BUSSIPILET_KESKMINE = 1.25
BUSSI_KIIRUS = 25  # km/h (kui buss pole valitud, arvutab aja distantsi järgi)

# ----- ABIFUNKTSIOONID (sisendi küsimine) -----

# While True funktsioonidest eemaldatud, ei läinud UI-ga kokku
def küsi_float(küsimus, miinimum=0.0):  # kasutatakse distantsi ja kütusekulu küsimisel
    """Küsib ujukomaarvu. Lubab koma või punkti. Kontrollib miinimumi."""
    try:
        s = küsimus.replace(",", ".").strip()
        x = float(s)
        if x < miinimum:
            print(f"Palun sisesta arv suurem kui {miinimum}.")
        else:
            return x
    except ValueError:
        rahaline_summa.configure(text=f"Vigane sisend!")
        ajaline_summa.configure(text=f"Vigane sisend!")


def küsi_int_vahemikus(küsimus, min_v, max_v):  # kasutatakse transpordivaliku ja bussi aja küsimusel
    """Küsib täisarvu ja kontrollib, et see oleks vahemikus."""
    try:
        x = int(küsimus.strip())
        if min_v <= x <= max_v:
            return x
        print(f"Palun sisesta arv vahemikus {min_v}-{max_v}.")
    except ValueError:
        rahaline_summa.configure(text=f"Vigane sisend!")
        ajaline_summa.configure(text=f"Vigane sisend!")


# ----- ARVUTUSFUNKTSIOONID -----

def auto_kulu(distants_km, kütusekulu_l_100km):  
    try:
        #bugtext.configure(text=f"{kütusväärtus.get()}")
        kütuse_hind = kütusväärtus.get()
    except:
        kütuse_hind = KÜTUSEHIND # KÜTUSEHIND = 1.5

    return (distants_km / 100) * kütuse_hind * kütusekulu_l_100km


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
    #bugtext.configure(text=f"{pilet_olek.get()}")
    return BUSSIPILET_SOODUS if soodustus else BUSSIPILET_TAVALINE

# arvutab bussi aja kui on valitud teine transpordimeetod
def buss_aeg_min(distants_km):
    """Tagastab bussisõidu aja minutites (lihtsustatud: distants / BUSSI_KIIRUS)."""
    if BUSSI_KIIRUS <= 0:
        return 0.0
    return (distants_km / BUSSI_KIIRUS) * 60


def kergliikleja_aeg_min(distants_km, jalgsi):
    """Tagastab jalgsi/rattaga/tõuksiga liikumise aja minutites (EI ümarda siin)."""
    kiirus = JALA_KIIRUS if jalgsi else RATTA_KIIRUS
    if kiirus <= 0:
        return 0.0
    return (float(distants_km) / kiirus) * 60


def rendi_kergliikleja_kulu_ja_aeg(distants_km):
    """Tagastab renditõuksi/rendijalgratta kulu ja aja (aeg ei ole ümardatud)."""
    aeg_minutites = kergliikleja_aeg_min(distants_km, jalgsi=False)
    kulu = BOLT_AVAMINE + (aeg_minutites * BOLT_MINUT)  # ei ümarda
    return kulu, aeg_minutites


def takso_kulu(distants_km):
    """Tagastab takso rahalise kulu (ei ümarda)."""
    aeg_minutites = auto_aeg_min(distants_km)
    return TAKSO_START + (distants_km * TAKSO_KM) + (aeg_minutites * TAKSO_MINUT)


# ---------------------------
# --- GRAAFIKU OSA (funktsioon) ---
# ---------------------------

def joonista_vordlus_graafik(distants_km, valik, auto_kütusekulu_l_100km=None, buss_soodustus=None, buss_aeg_üks_ots=None):
    """Joonistab tabeli + graafiku (kõik täpid).
       Valitud meetod joonistatakse tärniga ja nimi on 'Teie valik (meetod)'."""

    EDASI_TAGASI = 2

    nimed = {
        1: "Auto",
        2: "Buss",
        3: "Jalgsi",
        4: "Rendi(tõuke)ratas",
        5: "Takso",
        6: "Oma ratas",
    }
    valitud_nimi = nimed[valik]
    valiku_silt = f"Teie valik ({valitud_nimi})"

    # --- GRAAFIKU OSA: arvuta kõigi meetodite täpid (edasi-tagasi) ---
    # Auto: kui pole valitud, kasuta vaikimisi 8 l/100km või mis iganes on sätestatud vaikimisi
    if valik == 1 and auto_kütusekulu_l_100km is not None:
        auto_kulu_l_100km = auto_kütusekulu_l_100km
    else:
        auto_kulu_l_100km = AUTO_KÜTUSEKULU_VAIKIMISI

    auto_aeg = round(EDASI_TAGASI * auto_aeg_min(distants_km))
    auto_kulu_eur = EDASI_TAGASI * auto_kulu(distants_km, auto_kulu_l_100km)

    # Buss: kui pole valitud, kulu = keskmine 1.25 (üks ots), aeg distantsist
    if valik == 2 and buss_soodustus is not None:
        buss_pilet = bussi_kulu(buss_soodustus)
    else:
        buss_pilet = BUSSIPILET_KESKMINE

    if valik == 2 and buss_aeg_üks_ots is not None:
        buss_aeg = EDASI_TAGASI * buss_aeg_üks_ots  # kasutaja sisestatud aeg (üks ots)
    else:
        buss_aeg = round(EDASI_TAGASI * buss_aeg_min(distants_km))

    buss_kulu = EDASI_TAGASI * buss_pilet

    # Jalgsi
    jalgsi_aeg = round(EDASI_TAGASI * kergliikleja_aeg_min(distants_km, jalgsi=True))
    jalgsi_kulu = 0.0

    # Rendi(tõuke)ratas
    rendi_kulu_ots, rendi_aeg_ots = rendi_kergliikleja_kulu_ja_aeg(distants_km)
    rendi_aeg = round(EDASI_TAGASI * rendi_aeg_ots)
    rendi_kulu = EDASI_TAGASI * rendi_kulu_ots

    # Takso
    takso_aeg = round(EDASI_TAGASI * auto_aeg_min(distants_km))
    takso_kulu_päevas = EDASI_TAGASI * takso_kulu(distants_km)

    # Oma ratas
    oma_ratas_aeg = round(EDASI_TAGASI * kergliikleja_aeg_min(distants_km, jalgsi=False))
    oma_ratas_kulu = 0.0

    punktid = [
        ("Auto", auto_aeg, auto_kulu_eur),
        ("Buss", buss_aeg, buss_kulu),
        ("Jalgsi", jalgsi_aeg, jalgsi_kulu),
        ("Rendi(tõuke)ratas", rendi_aeg, rendi_kulu),
        ("Takso", takso_aeg, takso_kulu_päevas),
        ("Oma ratas", oma_ratas_aeg, oma_ratas_kulu),
    ]

    # --- GRAAFIKU OSA: Figure + tabel ülal, graafik all ---
    fig = plt.figure(figsize=(10, 6))
    gs = fig.add_gridspec(nrows=2, ncols=1, height_ratios=[1, 4])

    ax_table = fig.add_subplot(gs[0])
    ax = fig.add_subplot(gs[1])

    # --- GRAAFIKU OSA: tabel (kõik täpid, valitud rea nimi asendub) ---
    col_labels = ["Liikumisviis", "Aeg (min, edasi-tagasi)", "Kulu (€ , edasi-tagasi)"]
    cell_text = []
    for nimi, aeg, kulu in punktid:
        nimi_tabelis = valiku_silt if nimi == valitud_nimi else nimi
        cell_text.append([nimi_tabelis, f"{aeg:d}", f"{kulu:.2f}"])

    ax_table.axis("off")
    table = ax_table.table(
        cellText=cell_text,
        colLabels=col_labels,
        cellLoc="center",
        loc="center"
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.2)

    # --- GRAAFIKU OSA: graafiku alus ---
    ax.set_title("Transpordiviiside võrdlus (umbkaudsed arvutused)")
    ax.set_xlabel("Aeg (min)")
    ax.set_ylabel("Kulu (€)")
    ax.grid(True, linestyle="--", alpha=0.4)

    # telgede ulatus
    max_aeg = max(a for _, a, _ in punktid)
    max_kulu = max(k for _, _, k in punktid)
    x_max = max(10, max_aeg * 1.15)
    y_max = max(5,  max_kulu * 1.25)
    ax.set_xlim(0, x_max)
    ax.set_ylim(0, y_max)

    # --- GRAAFIKU OSA: joonista punktid (valitud meetod on tärn) ---
    # väiksed nihked tekstile, et kattumist vähendada
    dx = x_max * 0.01
    dy = y_max * 0.01

    for nimi, aeg, kulu in punktid:
        if nimi == valitud_nimi:
            ax.scatter([aeg], [kulu], marker="*", s=350, label=valiku_silt)
            ax.text(aeg + dx, kulu + dy, valiku_silt, ha="left", va="bottom")
        else:
            ax.scatter([aeg], [kulu], s=70)
            ax.text(aeg + dx, kulu + dy, nimi, ha="left", va="bottom")

    ax.legend()

    plt.tight_layout()
    plt.show()


# ----- PÕHIPROGRAMM -----

def main():
    try:
        auto_kütusekulu_l_100km = None
        buss_soodustus = None
        buss_aeg_üks_ots = None
        
        
        distants_km = float(distants_sisend.get())

        valik = valitu.get() + 1 # Kuna valitu algab 0, aga meetodid algavad 1

        raha_päevas = 0.0
        aeg_päevas = 0
        täpne_nimi = "Teie valik (täpne)"

        if valik == 1:  # Auto
            kütusekulu_l_100km = küsi_float(kütusk_sisend.get(), miinimum=0.0)
            
            auto_kütusekulu_l_100km = kütusekulu_l_100km  # Salvestus graafiku jaoks
             
            kulu_üks_ots = auto_kulu(distants_km, kütusekulu_l_100km)
            aeg_üks_ots = auto_aeg_min(distants_km)

            raha_päevas = 2 * kulu_üks_ots
            aeg_päevas = round(2 * aeg_üks_ots)
            print("Autoga koolis käimine (edasi-tagasi):")

        elif valik == 2:  # Buss
            vastus = pilet_olek.get()
            soodustus = (vastus == True)

            buss_soodustus = soodustus  # Salvestus graafiku jaoks

            bussi_aeg_min_sisend = bussisisend.get()
            
            buss_aeg_üks_ots = bussi_aeg_min_sisend  # Salvestus graafiku jaoks
            
            kulu_üks_ots = bussi_kulu(soodustus)
            raha_päevas = 2 * kulu_üks_ots
            aeg_päevas = 2 * bussi_aeg_min_sisend
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
        
        rahaline_summa.configure(text=f"{raha_päevas:.2f}€")
        ajaline_summa.configure(text=f"{aeg_päevas} minutit")
        

        # --- GRAAFIKU OSA: joonista võrdlusgraafik distantsi põhjal ---

        joonista_vordlus_graafik(
            distants_km,
            valik,
            auto_kütusekulu_l_100km=auto_kütusekulu_l_100km,
            buss_soodustus=buss_soodustus,
            buss_aeg_üks_ots=buss_aeg_üks_ots
        )
        
        return (round(raha_päevas, 2), aeg_päevas)
    except:
        rahaline_summa.configure(text=f"Vigane sisend!")
        ajaline_summa.configure(text=f"Vigane sisend!")
        
avaaken()
test.mainloop()