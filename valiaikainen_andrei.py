import random
import mysql.connector

for i in range(10000000):
# tehän väliaikaisia muutujia koska peli ei ole vielä täysin välmiis
    lentokentia_vierailtu = random.randint(3,1500)
    matka_matkustettu = random.randint(500,100000)
    syllables = ["ka", "ra", "zu", "mi", "lo", "ne", "shi", "tor", "vek", "ari", "en", "ox", "so", "mo", "kakka", "iso", "aivo", "aivoton", "big", "ass", "dirty", "penis"]
    def random_syllable_nickname(min_syll=2, max_syll=5):
        count = random.randint(min_syll, max_syll)
        name = "".join(random.choice(syllables) for _ in range(count))
        # Capitalize first letter for readability
        return name.capitalize()

    if __name__ == "__main__":
        for _ in range(10):
            nickname = (random_syllable_nickname())

    print (lentokentia_vierailtu)
    print (matka_matkustettu)
    print (nickname)
    print("")



    # väliaikainen sql kutsu
    yhteys = mysql.connector.connect(
        host='127.0.0.1',
        port=3306,
        database='fuel_to_fly',
        user='andrei',
        password='1234',
        autocommit=True
    )

    cursor = yhteys.cursor()

    # Nämä pitäisi tulla pelistä
    nickname = nickname
    visited_count = lentokentia_vierailtu
    total_distance = matka_matkustettu

    # Tallennetaan tulos tietokantaan
    sql = "INSERT INTO results (player_name, visited_count, total_distance) VALUES (%s, %s, %s)"
    values = (nickname, visited_count, total_distance)
    cursor.execute(sql, values)

    print(f"Sinä {nickname} vieraili {visited_count} kentässä ja lensi yhteensä {total_distance:.2f} km")

    # Haetaan paras tulos
    cursor.execute("SELECT player_name, visited_count, total_distance FROM results ORDER BY visited_count DESC LIMIT 1")
    best_by_airports = cursor.fetchone()

    if best_by_airports[0] == nickname:
        print("! Congratulations New Record! Vierailin eniteen lentokentiä")
        print(f"Eniten kenttiä: {best_by_airports[0]} vieraili {best_by_airports[1]} kentässä ja lensi {best_by_airports[2]:.2f} km")
    else: 
        print(f"Eniten kenttiä: {best_by_airports[0]} vieraili {best_by_airports[1]} kentässä ja lensi {best_by_airports[2]:.2f} km")

    # Haetaan paras matkan pituuden mukaan
    cursor.execute("SELECT player_name, visited_count, total_distance FROM results ORDER BY total_distance DESC LIMIT 1")
    best_by_distance = cursor.fetchone()

    if best_by_distance[0] == nickname:
        print("! Congratulations New Record! Matkistit isoin matkaa")
        print(f"Isoin matka: {best_by_distance[0]} vieraili {best_by_distance[1]} kentässä ja lensi {best_by_distance[2]:.2f} km")
    else:
        print(f"Isoin matka: {best_by_distance[0]} vieraili {best_by_distance[1]} kentässä ja lensi {best_by_distance[2]:.2f} km")


    



'''
# Loppuosa mikä näytä tyuloksen ja tallena se tietokantaan
nickname = nimi
visited_count = lentokentia_vierailtu
total_distance = matka_matkustettu

# Tallennetaan tulos tietokantaan
sql = "INSERT INTO results (player_name, visited_count, total_distance) VALUES (%s, %s, %s)"
values = (nickname, visited_count, total_distance)
cursor.execute(sql, values)

print(f"Sinä {nickname} vieraili {visited_count} kentässä ja lensi yhteensä {total_distance:.2f} km")

# Haetaan paras tulos
cursor.execute("SELECT player_name, visited_count, total_distance FROM results ORDER BY visited_count DESC LIMIT 1")
best_by_airports = cursor.fetchone()

if best_by_airports[0] == nickname:
    print("! Congratulations New Record! Vierailin eniteen lentokentiä")
    print(f"Eniten kenttiä: {best_by_airports[0]} vieraili {best_by_airports[1]} kentässä ja lensi {best_by_airports[2]:.2f} km")
else: 
    print(f"Eniten kenttiä: {best_by_airports[0]} vieraili {best_by_airports[1]} kentässä ja lensi {best_by_airports[2]:.2f} km")

# Haetaan paras matkan pituuden mukaan
cursor.execute("SELECT player_name, visited_count, total_distance FROM results ORDER BY total_distance DESC LIMIT 1")
best_by_distance = cursor.fetchone()

if best_by_distance[0] == nickname:
    print("! Congratulations New Record! Matkistit isoin matkaa")
    print(f"Isoin matka: {best_by_distance[0]} vieraili {best_by_distance[1]} kentässä ja lensi {best_by_distance[2]:.2f} km")
else:
    print(f"Isoin matka: {best_by_distance[0]} vieraili {best_by_distance[1]} kentässä ja lensi {best_by_distance[2]:.2f} km")

'''




