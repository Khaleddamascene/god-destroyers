import mysql.connector
import random
from geopy.distance import geodesic

# --- Tietokantayhteys ---
def get_connection():
    yhteys = mysql.connector.connect(
        host='127.0.0.1',
        port=3306,
        database='fuel_to_fly',
        user='Dornaraj',
        password='123',
        autocommit=True
    )
    return yhteys

# --- Komennot ---
komennot = [
    (["apua", "h", "a", "komennot"], "apua", "Näytä kaikki komennot"),
    (["ohje", "ohjeet", "o"], "ohje", "Näytä pelin ohjeet")
]

# --- Pelin alku ---
def alku():
    global kaikki_kentat, bensa
    yhteys = get_connection()
    if yhteys is None:
        print("Tietokantayhteyttä ei voitu muodostaa. Peli ei voi jatkua.")
        exit()

    cursor = yhteys.cursor()

    # Haetaan kaikki lentokentät
    cursor.execute("""
        SELECT ident, name, latitude_deg, longitude_deg 
        FROM airport 
        WHERE latitude_deg IS NOT NULL AND longitude_deg IS NOT NULL
    """)
    kaikki_kentat = cursor.fetchall()

    # Kysy pelaajan nimi
    while True:
        nimi = input("Syötä pelaajan nimi: ").strip()
        if nimi != "":
            break
        print("Nimi ei voi olla tyhjä. Yritä uudelleen.")

    # Satunnainen aloituskenttä
    aloitus = random.choice(kaikki_kentat)
    pelaaja_ident, pelaaja_nimi, lat, lon = aloitus

    bensa = 1000
    print("\n--- PELIN ALKU ---")
    print(f"Tervetuloa peliin, {nimi}!")
    print(f"Aloitat kentältä: {pelaaja_nimi} ({pelaaja_ident})")
    print(f"Polttoainetta käytössäsi: {bensa} yksikköä\n")

    cursor.close()
    yhteys.close()

    return nimi, (pelaaja_ident, pelaaja_nimi, (lat, lon)), bensa

# --- Ohjeet ---
def Ohjeet():
    print("\nOhjeet:")
    print("Sinulle annetaan kolme vaihtoehtoa eri lentokenttiin:")
    print("- Lähin kenttä (turvallisin, saa lisää bensaa)")
    print("- Keskikenttä (tasapainoinen vaihtoehto)")
    print("- Kaukaisin kenttä (suurin riski, kuluttaa paljon polttoainetta)")
    print("Jos polttoaine loppuu kesken, peli päättyy.")
    print("Kirjoita 'apua', niin näet kaikki komennot.\n")
    input("Paina ENTER jatkaaksesi...")

# --- Komentojen käsittely ---
def HaeKomento(komento):
    komento = komento.lower().strip()
    for avainsanat, toiminto, kuvaus in komennot:
        if komento in avainsanat:
            if toiminto == "apua":
                print("\nKomennot:")
                for av, _, kuvaus in komennot:
                    print(f"'{av[0]}' : {kuvaus}")
            elif toiminto == "ohje":
                Ohjeet()
            return True
    return False

def Puhe():
    while True:
        puhe = input("> ").lower().strip()
        if not HaeKomento(puhe):
            return puhe

# --- Pelin pääosa ---
def pelaa_peli(pelaaja_kentta):
    global bensa, kaikki_kentat
    pelaaja_ident, pelaaja_kentta_nimi, pelaaja_sijainti = pelaaja_kentta

    print(f"\nNykyinen kenttä: {pelaaja_kentta_nimi} ({pelaaja_ident})\n")

    # Lasketaan etäisyydet kaikille muille kentille
    kentta_etaisyydet = []
    for ident, name, lat, lon in kaikki_kentat:
        if ident == pelaaja_ident:
            continue
        matka = geodesic(pelaaja_sijainti, (lat, lon)).km
        kentta_etaisyydet.append((ident, name, matka, (lat, lon)))

    # Järjestetään etäisyyden mukaan
    kentta_etaisyydet.sort(key=lambda x: x[2])

    # Valitaan lähin, keskimmäinen ja kaukaisin
    if len(kentta_etaisyydet) >= 3:
        lahin = kentta_etaisyydet[0]
        keskimmainen = kentta_etaisyydet[len(kentta_etaisyydet)//2]
        kaukaisin = kentta_etaisyydet[-1]
        vaihtoehdot = [lahin, keskimmainen, kaukaisin]
    else:
        vaihtoehdot = kentta_etaisyydet

    random.shuffle(vaihtoehdot)

    print("Vaihtoehtoiset lentokentät:")
    for i, (ident, name, _, _) in enumerate(vaihtoehdot, start=1):
        print(f"{i}. {name:40} ({ident})")  # ei näytetä etäisyyksiä

    # Käyttäjän valinta
    while True:
        s = input("\nValitse kenttä (1-{}): ".format(len(vaihtoehdot))).strip()
        if s == "":
            print("Anna valinta 1-{} tai komento (esim. 'apua').".format(len(vaihtoehdot)))
            continue
        if HaeKomento(s):
            continue
        try:
            valinta = int(s)
            if 1 <= valinta <= len(vaihtoehdot):
                break
            else:
                print(f"Valitse numero 1–{len(vaihtoehdot)}.")
        except ValueError:
            print("Anna numero tai kirjoita 'apua' nähdäksesi komennot.")

    valittu = vaihtoehdot[valinta - 1]
    matka = valittu[2]

    # Tarkistetaan riittääkö bensa
    if bensa < matka:
        print(f"Polttoaine ei riitä lennolle ({matka:.1f} km). Peli päättyy.")
        bensa = 0
        return pelaaja_kentta, matka

    # Lentomatkan kulutus
    kulutus = int(matka)
    bensa -= kulutus

    # Polttoaineen lisäys / viesti
    if valittu == vaihtoehdot[0]:
        print("Turvallinen valinta! Saat lisää polttoainetta (+200).")
        bensa += 200
    elif len(vaihtoehdot) >= 2 and valittu == vaihtoehdot[1]:
        print("Hyvä valinta! Keskipitkä lento onnistui.")
    else:
        print("Kaukaisin kenttä! Lento onnistui, mutta kulutit paljon polttoainetta.")

    print(f"Lensit {matka:.1f} km (kulutus {kulutus}). Polttoainetta jäljellä {bensa}.\n")

    # Päivitetään uusi sijainti
    uusi_kentta = (valittu[0], valittu[1], valittu[3])
    return uusi_kentta, matka

# --- MAIN ---
if __name__ == "__main__":
    print("=== Fuel to Fly ===\n")
    input("Paina ENTER aloittaaksesi!\n")
    print("Kirjoita 'ohje', jos haluat pelin ohjeet.\n")

    # Näytetään ohjeet, jos pelaaja haluaa
    Puhe()

    # Pelin aloitus
    nimi, kentta, aloitus_bensa = alku()
    bensa = aloitus_bensa

    # Seurataan käytyjä kenttiä ja kokonaismatkaa
    kayty_kentat = [kentta]
    kokonaismatka = 0

    # Pääpelisilmukka
    while bensa > 0:
        kentta, matka = pelaa_peli(kentta)
        if kentta not in kayty_kentat:
            kokonaismatka += matka
            kayty_kentat.append(kentta)

    # Tallennetaan tulokset tietokantaan
    yhteys = get_connection()
    cursor = yhteys.cursor()

    nickname = nimi
    visited_count = len(kayty_kentat)
    total_distance = kokonaismatka

    sql = "INSERT INTO results (player_name, visited_count, total_distance) VALUES (%s, %s, %s)"
    values = (nickname, visited_count, total_distance)
    cursor.execute(sql, values)
    yhteys.commit()

    print(f"Sinä {nickname} vierailit {visited_count} kentässä ja lensit yhteensä {total_distance:.2f} km\n")

    # Paras tulos kenttien mukaan
    cursor.execute("SELECT player_name, visited_count, total_distance FROM results ORDER BY visited_count DESC, total_distance DESC LIMIT 1")
    best_by_airports = cursor.fetchone()
    if best_by_airports[0] == nickname:
        print("! Congratulations New Record! Vierailit eniten lentokenttiä")
    print(f"Eniten kenttiä: {best_by_airports[0]} vieraili {best_by_airports[1]} kentässä ja lensi {best_by_airports[2]:.2f} km\n")

    # Paras matkan pituuden mukaan
    cursor.execute("SELECT player_name, visited_count, total_distance FROM results ORDER BY total_distance DESC, visited_count DESC LIMIT 1")
    best_by_distance = cursor.fetchone()
    if best_by_distance[0] == nickname:
        print("! Congratulations New Record! Lensit pisimmän matkan")
    print(f"Isoin matka: {best_by_distance[0]} vieraili {best_by_distance[1]} kentässä ja lensi {best_by_distance[2]:.2f} km\n")

    cursor.close()
    yhteys.close()
