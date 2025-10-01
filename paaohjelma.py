# --- DATABASE ---
import random

import mysql.connector
from geopy.distance import geodesic

#import sqlite3

def get_connection():
    yhteys = mysql.connector.connect(
        host='127.0.0.1',
        port=3306,
        database='fuel_to_fly',
        user='elmo',
        password='kikkeli123',
        autocommit=True
    )
    return yhteys



nimi = "No Name Set"
bensa = 0

ika = 0
pankkiTunnus = ""

# Lista kentistä, missä on käynyt (että tietää olla menemättä uudelleen/sieltä ei enää saa bensaa yms):
kaydytKentat = {"EFYL", "Ylivieska Airfield"} 
maa = "Ei maata" 
maanosa = "Ei maanosaa" 

komennot = [
    (["apua", "h", "a", "komennot"], "apua", "Nämä komennot"),
    (["ohje", "ohjeet", "o"], "ohje", "Pelin ohjeet"),
    (["tilanne", "t"], "tilanne", "Pelin tilanne")
]

def Tilanne():
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
def pelaa_peli():
    ika = int(input)
    if ika < 18:
        print("Liian nuori, häivy!")
        return
    yhteys = get_connection()
    cursor = yhteys.cursor()

    cursor.execute("SELECT name, latitude_deg, longitude_deg FROM airport WHERE ident='EFHK';")
    pelaaja_kentta = cursor.fetchone()
    pelaaja_sijainti = (pelaaja_kentta[1], pelaaja_kentta[2])

    print(f"Pelaajan kenttä: {pelaaja_kentta[0]} ({pelaaja_sijainti})")

    cursor.execute("""
        SELECT name, latitude_deg, longitude_deg 
        FROM airport 
        WHERE ident != 'EFHK'
    """)
    kaikki_kentat = cursor.fetchall()   
    kolme_kenttaa = random.sample(kaikki_kentat, 3)

    kentta_etaisyydet = []
    for kentta in kolme_kenttaa:
        kentta_sijainti = (kentta[1], kentta[2])
        matka = geodesic(pelaaja_sijainti, kentta_sijainti).km
        kentta_etaisyydet.append((kentta[0], matka, kentta_sijainti))

    kentta_etaisyydet.sort(key=lambda x: x[1])

    print("\nKolme vaihtoehtoista lentokenttää:")
    for i, kentta in enumerate(kentta_etaisyydet):
        print(f"{i+1}. {kentta[0]} - {kentta[1]:.1f} km")

    valinta = int(input("\nValitse kenttä (1-3): "))
    valittu = kentta_etaisyydet[valinta-1]

    if valittu == kentta_etaisyydet[0]:
        print("Turvallinen valinta! Saat lisää polttoainetta (+200).")
    elif valittu == kentta_etaisyydet[1]:
        print("Matka onnistui, mutta kulutit paljon polttoainetta.")
    else:
        print("Liian kaukana! Polttoaine ei riitä, peli loppuu.")

    cursor.close()
    yhteys.close()

# --- MAIN ---
if __name__ == "__main__":
    print("Fuel to Fly\n")
    print("Kirjoita 'ohje', niin saat pelin ohjeet.\n")
    input("Press ENTER to start!\n")
    pelaa_peli()
