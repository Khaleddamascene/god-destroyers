bensa = 1000
maa = "Ei maata"
komennot = {
            ["apua", "h" , "a" , "komennot"]:"Nämä komennot", 
            ["ohje" , "ohjeet" , "o"]:"Pelin ohjeet",
            ["tilanne", "t"]:"Pelin tilanne"
            }

def Tilanne():
    print("----Tilanteesi----")
    print("Bensaa: ", bensa)

def HaeKomento(komento):
    komento = str(komento).lower()
    if komento == "h" or komento == "apua" or komento == "a" or komento == "komennot":
        for k in komennot:
            print("'" + k[0] + "' : " + k)
    if komento == "ohje" or "ohjeet" or komento == "o":
        Ohjeet
    if komento in komennot[1]:
        return
    
def Ohjeet():
    print("Ohjeet:")
    print("Sinulle annetaan vaihtoehtoja eri lentokenttiin.")
    print("Sinun täytyy valita kenttä, johon sinulla riittää bensaa.")
    print("Jos kenttä on liian kaukana niin häviät.")
    print("Oikeasta vastauksesta matkustat sille kentälle.")
    print("Kentällä saat lisää bensaa ja uuden valinnan.")
    print("Yritä päästä mahdollisimman pitkälle")
    print("Kirjoita 'Apua', niin saat apua.")
    print("Onnea!")
    input("Jep!")
        
def Puhe():
    while True:
        # Jos on komento, niin se antaa laittaa inputin uudestaan
        puhe = input.lower()
        
        if puhe in komennot:
            HaeKomento(puhe)
        else:
            break
    

print("Fuel to Fly")
print("")
input("Press ENTER to start!")
print("")
print("Kirjoita 'ohje', niin saat pelin ohjeet.")
Puhe

print("Peli alkaa")
