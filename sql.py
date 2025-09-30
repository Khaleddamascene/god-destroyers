import mysql.connector
from geopy.distance import geodesic # etäisyys laskemista varteen
import PelinKulku
import Minecraft

# yhteys = mysql.connector.connect(
#          host='127.0.0.1',
#          port= 3306,
#          database='flight_game',
#          user='',
#          password='',
#          autocommit=True
#          )

import mysql.connector

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


def hae_maa(koodi):
    sql = "SELECT name, municipality FROM airport WHERE ident = %s"
    kursori = yhteys.cursor()
    kursori.execute(sql, (koodi,))
    tulos = kursori.fetchall()
    if kursori.rowcount > 0:
        for rivi in tulos:
            print(f'{koodi} => {rivi}') 
    else:
        print("Ei löytynyt.")
    return

koodi = input("Anna koodi: ")
hae_maa(koodi)


def hae_koordinaatit(icao):
    sql = f"SELECT name, latitude_deg, longitude_deg FROM airport WHERE ident = '{icao}'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchone()  # haetaan vain yksi rivi

    if tulos:
        nimi = tulos[0]
        koordinaatit = (tulos[1], tulos[2])  # tuple (lat, lon)
        return nimi, koordinaatit
    else:
        print(f"Lentokenttää {icao} ei löytynyt.")
        return None, None


# Pääohjelma
yhteys = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='flight_game',
    user='andrei',
    password='1234',
    autocommit=True
)

icao1 = input("Anna ensimmäisen lentokentän ICAO-koodi (esim. EFHK): ")
icao2 = input("Anna toisen lentokentän ICAO-koodi (esim. EGLL): ")

nimi1, koord1 = hae_koordinaatit(icao1)
nimi2, koord2 = hae_koordinaatit(icao2)

if koord1 and koord2:
    etaisyys_km = geodesic(koord1, koord2).km
    print(f"Etäisyys {nimi1} ja {nimi2} välillä on {etaisyys_km:.2f} km")
