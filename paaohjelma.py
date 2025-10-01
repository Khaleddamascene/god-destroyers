# --- DATABASE ---
import mysql.connector
import random
from geopy.distance import geodesic

def get_connection():
    yhteys = mysql.connector.connect(
        host='127.0.0.1',
        port=3307,
        database='fuel_to_fly',
        user='khaled',
        password='1234',
        autocommit=True
    )
    return yhteys

#####  """Khaled"""
def alku():
    yhteys = get_connection()
    cursor = yhteys.cursor()

    # 1. Kysy pelaajan nimi (pakollinen)
    while True:
        nimi = input("Syötä pelaajan nimi: ").strip()
        if nimi != "":
            break
        print("Nimi ei voi olla tyhjä. Yritä uudelleen.")

    # 2. Satunnainen lähtökenttä
    cursor.execute("""
        SELECT ident, name, latitude_deg, longitude_deg 
        FROM airport 
        WHERE latitude_deg IS NOT NULL AND longitude_deg IS NOT NULL
    """)
    kaikki_kentat = cursor.fetchall()
    aloitus = random.choice(kaikki_kentat)
    pelaaja_ident, pelaaja_nimi, lat, lon = aloitus

    # 3. Polttoaine alussa
    bensa = 1000

    # Tulostetaan tiedot
    print("\n--- PELIN ALKU ---")
    print(f"Tervetuloa peliin {nimi}!")
    print(f"Aloitat kentältä: {pelaaja_nimi} ({pelaaja_ident})")
    print(f"Polttoainetta käytössäsi: {bensa} yksikköä\n")

    cursor.close()
    yhteys.close()

    return nimi, (pelaaja_ident, pelaaja_nimi, (lat, lon)), bensa


#######

# Globaali polttoaine
bensa = 0
maa = "Ei maata"
maanosa = "Ei maanosaa"

komennot = [
    (["apua", "h", "a", "komennot"], "apua", "Nämä komennot"),
    (["ohje", "ohjeet", "o"], "ohje", "Pelin ohjeet"),
    (["tilanne", "t"], "tilanne", "Pelin tilanne")
]

def Tilanne():
    global bensa, maa, maanosa
    print("----Tilanteesi----")
    print("Bensaa:", bensa)
    print("Maa:", maa)
    print("Maanosa:", maanosa)

def Ohjeet():
    print("Ohjeet:")
    print("Sinulle annetaan vaihtoehtoja eri lentokenttiin.")
    print("Sinun täytyy valita kenttä, johon sinulla riittää bensaa.")
    print("Jos kenttä on liian kaukana niin häviät.")
    print("Oikeasta vastauksesta matkustat sille kentälle.")
    print("Kentällä saat lisää bensaa ja uuden valinnan.")
    print("Yritä päästä mahdollisimman pitkälle")
    print("Kirjoita 'apua', niin saat apua.")
    print("Onnea!")
    input("Jep!")

def HaeKomento(komento):
    komento = str(komento).lower().strip()
    for avainsanat, toiminto, kuvaus in komennot:
        if komento in avainsanat:
            if toiminto == "apua":
                print("Komennot:")
                for av, _, kuvaus in komennot:
                    print(f"'{av[0]}' : {kuvaus}")
            elif toiminto == "ohje":
                Ohjeet()
            elif toiminto == "tilanne":
                Tilanne()
            return True
    return False

def Puhe():
    while True:
        puhe = input("> ").lower().strip()
        if not HaeKomento(puhe):
            return puhe

# --- VARSINAINEN PELI ---
def pelaa_peli(pelaaja_nimi, pelaaja_kentta, aloitus_bensa):
    global bensa
    bensa = aloitus_bensa

    yhteys = get_connection()
    cursor = yhteys.cursor()

    pelaaja_ident, pelaaja_kentta_nimi, pelaaja_sijainti = pelaaja_kentta
    print(f"Pelaajan kenttä: {pelaaja_kentta_nimi} ({pelaaja_ident})\n")

    # Hae kentät paitsi nykyinen
    cursor.execute("""
        SELECT ident, name, latitude_deg, longitude_deg 
        FROM airport 
        WHERE ident != %s
    """, (pelaaja_ident,))
    kaikki_kentat = cursor.fetchall()
    kolme_kenttaa = random.sample(kaikki_kentat, 3)

    kentta_etaisyydet = []
    for ident, name, lat, lon in kolme_kenttaa:
        kentta_sijainti = (lat, lon)
        matka = geodesic(pelaaja_sijainti, kentta_sijainti).km
        kentta_etaisyydet.append((ident, name, matka, kentta_sijainti))

    kentta_etaisyydet.sort(key=lambda x: x[2])

    print("Kolme vaihtoehtoista lentokenttää:")
    for i, kentta in enumerate(kentta_etaisyydet):
        print(f"{i+1}. {kentta[1]} ({kentta[0]}) - {kentta[2]:.1f} km")

    valinta = int(input("\nValitse kenttä (1-3): "))
    valittu = kentta_etaisyydet[valinta-1]

    if valittu == kentta_etaisyydet[0]:
        print(f"Turvallinen valinta! Saat lisää polttoainetta (+200).")
        bensa += 200
    elif valittu == kentta_etaisyydet[1]:
        print(f"Matka onnistui, mutta kulutit paljon polttoainetta.")
        bensa -= int(valittu[2])  # vähennetään matkan verran
    else:
        print(f"Liian kaukana! Polttoaine ei riitä, peli loppuu.")
        bensa = 0

    print(f"\nTilanne: Polttoainetta jäljellä {bensa} yksikköä.")

    cursor.close()
    yhteys.close()

# --- MAIN ---
if __name__ == "__main__":
    print("Fuel to Fly\n")
    input("Press ENTER to start!\n")
    print("Kirjoita 'ohje', niin saat pelin ohjeet.\n")
    Puhe()
    print("Peli alkaa!\n")

    # Käynnistetään alku ja peli
    nimi, kentta, aloitus_bensa = alku()
    pelaa_peli(nimi, kentta, aloitus_bensa)
