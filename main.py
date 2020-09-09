#!/usr/bin/env python3
import sys, os, json, re, time, random
assert sys.version_info >= (3,8), "This script requires at least Python 3.8"

first = True
haveGun = False
bullet = 7
hp = 5

def load(l):
    f = open(os.path.join(sys.path[0], l))
    data = f.read()
    j = json.loads(data)
    return j

def find_passage(game_desc, pid):
    for p in game_desc["passages"]:
        if p["pid"] == pid:
            return p
    return {}

def format_passage(description):
    description = re.sub(r'//([^/]*)//',r'\1',description)
    description = re.sub(r"''([^']*)''",r'\1',description)
    description = re.sub(r'~~([^~]*)~~',r'\1',description)
    description = re.sub(r'\*\*([^\*]*)\*\*',r'\1',description)
    description = re.sub(r'\*([^\*]*)\*',r'\1',description)
    description = re.sub(r'\^\^([^\^]*)\^\^',r'\1',description)
    description = re.sub(r'(\[\[[^\|]*)\|([^\]]*\]\])',r'\1->\2',description)
    description = re.sub(r'\[\[([^(->)]*)->[^\]]*\]\]',r'[ \1 ]',description)
    return description

# ------------------------------------------------------

def update(current, game_desc, choice):
    global first

    if current == "":
        return current

    if choice.isnumeric():
        if int(choice) > len(current["links"]) or int(choice) == 0:
            print("\n\n---------------------\n\nYour input number is invalid to be an index number. Please try again.")
            time.sleep(1.5)
        else:
            current = find_passage(game_desc, current["links"][int(choice) - 1]["pid"])
            if current:
                return current
    else:
        for l in current["links"]:
            if choice == l["name"].lower():
                current = find_passage(game_desc, l["pid"])
                if current:
                    return current
        if first == False:
            print("\n\n---------------------\n\nI don't understand what you are asking me to do. Please try again.")
            time.sleep(1.5)
        else:
            first = False
    return current

def render(current):
    print(format_passage(current["text"]))

def get_input(current):
    choice = input("What would you like to do? (type quit to exit) ")
    choice = choice.lower()
    if choice in ["quit","q","exit"]:
        return "quit"
    return choice

def Battle():
    global hp
    global haveGun
    global bullet

    if random.random() < 1:
        zombieHp = random.randint(2, 3)
        attackSelection = ""
        choice = ""
        print("\n\n\n\n\n\n\n")
        print("You encounter a zombie!")
        while zombieHp > 0:
            if haveGun == True and bullet > 0:
                attackSelection = "shoot"
                print("[ (1)Shoot ]\n[ (2)Try to flee ]")
            else:
                attackSelection = "punch"
                print("[ (1)Punch ]\n[ (2)Try to flee]")
            choice = input("What would you like to do next? (type quit to exit) ").lower()
            if choice == attackSelection or choice == "1":
                if attackSelection == "shoot":
                    bullet -= 1
                    if random.random() > 0.25:
                        zombieHp = 0
                        print("You hit it!")
                    else:
                        hp -= 1
                        print("You missed!\nThe zombie attack you!")
                    print("You have " + str(bullet) + " bullet left")
                elif attackSelection == "punch":
                    zombieHp -= 1
                    print("You punched the zombie right in the face!")
                    if random.random() > 0.5:
                        hp -= 1
                        print("However, the zombie attack you as well!")
            elif choice == "flee" or choice == "2":
                if random.random() > 0.2:
                    print("You didn't flee.")
                    print("The zombie attacked you!")
                    hp -= 1
                else:
                    print("You successfully fleeded!")
                    return True
            elif choice in ["quit","q","exit"]:
                return False
            else:
                print("\n\n---------------------\n\nI don't understand what you are asking me to do. Please try again.")
                time.sleep(1.5)
            print("You have " + str(hp) + " hp left")
            time.sleep(2)
            print("\n\n\n\n\n\n\n")
            if hp <= 0:
                return False
        print("The zombie is defeated!")
    else:
        return True

# ------------------------------------------------------

def main():
    game_desc = load("game.json")
    current = find_passage(game_desc, game_desc["startnode"])
    choice = ""
    random.seed()
    global haveGun
    end = False

    while choice != "quit" and current != {} and end == False:
        result = True
        current = update(current, game_desc, choice)
        if "You are in your apartment." in str(current) or "You walked out of the apartment" in str(current) or "What are you going to do now?" in str(current) or "You tried to call the police" in str(current):
            render(current)
            choice = get_input(current)
        elif "You picked up your M1911A1" in str(current):
            haveGun = True
            render(current)
            choice = get_input(current)
        elif "You finally arrived at the refuge point" in str(current):
            result = True
            choice = "quit"
            render(current)
            end = True
        else:
            result = Battle()
            if result == False:
                print("You failed to escape!")
                choice = "quit"
            else:
                render(current)
                choice = get_input(current)

        if result == False:
            print("You failed to escape!")
            choice = "quit"

            

    print("Thanks for playing!")




if __name__ == "__main__":
    main()