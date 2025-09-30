bensa = 1000
# Lista kentistä, missä on käynyt (että tietää olla menemättä uudelleen/sieltä ei enää saa bensaa yms):
kaydytKentat = {"EFYL", "Ylivieska Airfield"} # ident, name (Tämä on vain esimerkki miten tämän voi tehdä)

# Ei ole pakko tehdä (koska country-taulussa)
maa = "Ei maata" # country taulu
maanosa = "Ei maanosaa" # country taulu


# Lista komennoista: (avainsanat, toiminto, kuvaus)
komennot = [
    (["apua", "h", "a", "komennot"], "apua", "Nämä komennot"),
    (["ohje", "ohjeet", "o"], "ohje", "Pelin ohjeet"),
    (["tilanne", "t"], "tilanne", "Pelin tilanne")
]

def Tilanne():
    print("----Tilanteesi----")
    print("Bensaa:", bensa)
    print(":", )
    print("Maanosa:", )
    print(":", )

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
            # Jos avainsana on listassa, niin tässä tarkistetaan sen toiminto osuus:
            if toiminto == "apua":
                print("Komennot:")
                for av, _, kuvaus in komennot:
                    print(f"'{av[0]}' : {kuvaus}")
            elif toiminto == "ohje":
                Ohjeet()
            elif toiminto == "tilanne":
                Tilanne()
            return True
    return False  # ei ollut komento

def Puhe():
    while True:
        puhe = input("> ").lower().strip()
        if not HaeKomento(puhe):
            return puhe  # ei ollut komento > palautetaan peliin

# -------------------------
print("Fuel to Fly\n")
input("Press ENTER to start!\n")
print("Kirjoita 'ohje', niin saat pelin ohjeet.")

Puhe()
print("Peli alkaa")
peliKaynnissa = True

while peliKaynnissa:
    Tilanne()
    



# Listataan kuinka monessa paikassa on käynyt
print("Olet käynyt:",
      " lentokentällä",
      " maassa",
      " maanosassa",
      "\nKäytit: ",   " bensaa.")

print("Viime ennätykset:",
      " lentokentällä",
      " maassa",
      " maanosassa"
      "\nKäytit: ",   " bensaa.")