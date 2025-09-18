
import mysql.connector

yhteys = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='',
         password='',
         autocommit=True
         )



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
