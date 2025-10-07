# --- DATABASE ---
import random
import mysql.connector
from geopy.distance import geodesic


def get_connection():
    yhteys = mysql.connector.connect(
        host='127.0.0.1',
        port=3306,
        database='fuel_to_fly',
        user='aaro',
        password='2005',
        autocommit=True
    )
    return yhteys

yhteys = get_connection()
cursor = yhteys.cursor()

#####  """Khaled"""
def alku():
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
    bensa = 10000

    # Tulostetaan tiedot
    print("\n--- PELIN ALKU ---")
    print(f"Tervetuloa peliin {nimi}!")
    print(f"Aloitat kentältä: {pelaaja_nimi} ({pelaaja_ident})")
    print(f"Polttoainetta käytössäsi: {bensa} litraa\n")

    return nimi, (pelaaja_ident, pelaaja_nimi, (lat, lon)), bensa


#######

# Globaali polttoaine
bensa = 0
maa = "Ei maata"
maanosa = "Ei maanosaa"
peliKaynnissa = True

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
    print("Sinulle annetaan kolme vaihtoehtoista lentokenttää.")
    print("Kaikki kentät kuluttavat bensaa 1 litra / km.")
    print("Lähin kenttä → turvallinen valinta, saat +3000 polttoainetta.")
    print("Jos polttoaine loppuu, peli päättyy.")
    print("Kirjoita 'apua', niin saat apua.")
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
    global bensa, peliKaynnissa
    bensa = aloitus_bensa

    pelaaja_ident, pelaaja_kentta_nimi, pelaaja_sijainti = pelaaja_kentta
    print(f"\nOlet kentällä: {pelaaja_kentta_nimi} ({pelaaja_ident})")
    print(f"Polttoainetta jäljellä: {bensa:.0f}\n")

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

    print("Kolme vaihtoehtoista lentokenttää (1 km = 1 litra):")
    for i, kentta in enumerate(kentta_etaisyydet):
        tyyppi = " (Lähin +3000)" if i == 0 else ""
        print(f"{i+1}. {kentta[1]} ({kentta[0]}) - {kentta[2]:.1f} km{tyyppi}")

    while True:
        try:
            valinta = int(input("\nValitse kenttä (1-3): "))
            if 1 <= valinta <= 3:
                break
            else:
                print("Valitse numero 1-3.")
        except ValueError:
            print("Anna numero 1-3.")

    valittu = kentta_etaisyydet[valinta-1]
    matka = int(valittu[2])

    print(f"\nLennät kentälle {valittu[1]} ({valittu[0]}) - {matka} km")

    bensa -= matka

    if valittu == kentta_etaisyydet[0]:
        print("Turvallinen valinta! Saat +3000 polttoainetta.")
        bensa += 3000


    if bensa <= 0:
        print("\nPolttoaine loppui!")
        print("Peli päättyi. Kiitos pelaamisesta!")
        peliKaynnissa = False
    else:
        print(f"Matka kulutti {matka} litraa polttoainetta.")
        print(f"Polttoainetta jäljellä: {bensa:.0f} litraa.\n")

    return (valittu[0], valittu[1], valittu[3]), bensa


# --- MAIN ---
if __name__ == "__main__":
    print("Fuel to Fly\n")
    input("Press ENTER to start!\n")
    print("Kirjoita 'ohje', niin saat pelin ohjeet.\n")
    Puhe()
    print("Peli alkaa!\n")

    # Käynnistetään alku ja peli
    nimi, kentta, aloitus_bensa = alku()

while peliKaynnissa:
    kentta, aloitus_bensa = pelaa_peli(nimi, kentta, aloitus_bensa)

# Lopuksi nämä voi sulkea (ei tarvitse koko ajan avata ja sulkea)
cursor.close()
yhteys.close()
