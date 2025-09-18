import Minecraft

print(Minecraft.kala)
print(Minecraft.kissa)

game_name = "Minecraft"

print(game_name)
print("Start / Quit")
inp = ""
while True:
    inp = input()
    if inp == "Start":
        break
    elif inp == "Quit":
        #Quit the game
        break
    

print("What is your name?")
name = input()

print("What continent will you start in?")
continent = input()

print("What country in " + continent + "?")
country = input()

print("What difficulty? (Easy/Medium/Hard)")
difficulty = input()
