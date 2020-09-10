import sys
import os
import random
import pickle


weapons = {
    "Great Sword": 40
}


class Player:
    def __init__(self, name):
        self.name = name
        self.maxhealth = 100
        self.health = self.maxhealth
        self.base_attack = 10
        self.gold = 40
        self.pots = 0
        self.weap = ['Rusty Sword']
        self.curweap = ['Rusty Sword']

    @property
    def attack(self):
        attack = self.base_attack
        if self.curweap == "Rusty Sword":
            attack += 5
        if self.curweap == "Great Sword":
            attack += 15

        return attack


class Goblin:
    def __init__(self, name):
        self.name = name
        self.maxhealth = 50
        self.health = self.maxhealth
        self.attack = 5
        self.goldgain = 10


GoblinIG = Goblin("Goblin")


class Zombie:
    def __init__(self, name):
        self.name = name
        self.maxhealth = 70
        self.health = self.maxhealth
        self.attack = 7
        self.goldgain = 10


ZombieIG = Zombie("Zombie")


def start():
    os.system("clear")
    print("Please input your name : ")
    option = input("> ")

    global PlayerIG
    PlayerIG = Player(option)
    start1()


def prefight():
    global enemy
    enemyNum = random.randint(1, 2)
    if enemyNum == 1:
        enemy = GoblinIG
    else:
        enemy = ZombieIG

    fight()


def fight():
    os.system("clear")
    print("{0} vs {1}".format(PlayerIG.name, enemy.name))
    print("{0}'s health: {1}/{2} - {3}'s Health: {4}/{5}".format(
        PlayerIG.name, PlayerIG.health, PlayerIG.maxhealth,
        enemy.name, enemy.health, enemy.maxhealth
    ))
    print("Potions %i\n" % PlayerIG.pots)
    print("1. Attack\n2. Drink Potion\n3. Run")
    option = input("> ")
    if option == "1":
        attack()
    elif option == "2":
        drinkpot()
    elif option == "3":
        run()
    else:
        fight()


def attack():
    os.system("clear")
    pAttack = random.randint(int(PlayerIG.attack / 2), PlayerIG.attack)
    eAttack = random.randint(int(enemy.attack / 2), enemy.attack)

    if pAttack == PlayerIG.attack / 2:
        print("You Miss!!")
    else:
        enemy.health -= pAttack
        print("You deal: {} damage!!".format(pAttack))

    option = input(" ")
    if enemy.health <= 0:
        win()

    os.system("clear")
    if eAttack == enemy.attack / 2:
        print("The enemy missed!")
    else:
        PlayerIG.health -= eAttack
        print("The enemy deals {} damage ! ".format(eAttack))

    option = input(" ")
    if PlayerIG.health == 0:
        die()
    else:
        fight()


def drinkpot():
    os.system("clear")
    if PlayerIG.pots == 0:
        print("You don't have any potions!")

    else:
        PlayerIG.health += 50
        if PlayerIG.health > PlayerIG.maxhealth:
            PlayerIG.health = PlayerIG.maxhealth
        print("You drink a potion!")
    option = input(" ")
    fight()


def run():
    os.system("clear")
    runNum = random.randint(1, 3)
    if runNum == 1:
        print("You have successfully run away!!")
        option = input(" ")
        start1()
    else:
        print("You failed to get away!")
        option = input("> ")
        os.system("clear")

        # eAttack = random.randint(int(enemy.attack / 2), enemy.attack)
        eAttack = random.randint(int(enemy.attack / 2), enemy.attack)

        # if eAttack == enemy.attack / 2:
        if eAttack == enemy.attack / 2:
            print("The enemy missed!")
        else:
            PlayerIG.health -= eAttack
            print("The enemy deals {} damage ! ".format(eAttack))
        option = input(" ")

        if PlayerIG.health == 0:
            die()
        else:
            fight()


def win():
    os.system("clear")
    enemy.health = enemy.maxhealth
    PlayerIG.gold += enemy.goldgain
    print("You have defeated the {0}".format(enemy.name))
    print("You found %i gold" % enemy.goldgain)
    option = input(' ')
    start1()


def die():
    os.system("clear")
    print("You have died!!!")
    option = input(" ")


def store():
    os.system("clear")
    print("Welcome to the shop\n What would you like to buy?\n")
    print("1. Great Sword\n ")
    print("2. back\n")
    option = input(" ")

    if option in weapons:
        if PlayerIG.gold >= weapons[option]:
            os.system("clear")
            PlayerIG.gold -= weapons[option]
            PlayerIG.weap.append(option)
            print("You have bought {}".format(option))
            option = input(" ")
            store()

        else:
            os.system("clear")
            print("You don't have enough gold!!")
            option = input(" ")
            store()

    elif option == "back":
        start1()

    else:
        os.system("clear")
        print("That item does not exist")
        option = input(" ")
        store()


def inventory():
    os.system("clear")
    print("What do you want to do?")
    print("1. Equip Weapon\nb. Go Back")
    option = input(">>> ")
    if option is '1':
        equip()
    elif option is 'b':
        start1()


def equip():
    os.system("clear")
    print("What do you want to equip?")
    for weapon in PlayerIG.weap:
        print(weapon)
    print("b: to go back")
    option = input("> ")
    if option is PlayerIG.curweap:
        print("You already have that weapon equipped")
        option = input(" ")
        equip()

    elif option is 'b':
        inventory()

    elif option in PlayerIG.weap:
        PlayerIG.curweap = option
        print("You have equipped {}".format(option))
        option = input("> ")
        equip()
    else:
        print("You don't have {} in your inventory".format(option))


def start1():
    os.system("clear")
    print("Name %s" % PlayerIG.name)
    print("Attack: {}".format(PlayerIG.attack))
    print("Gold: {}".format(PlayerIG.gold))
    print("Current Weapons: {}".format(PlayerIG.curweap))
    print("Positions: {}".format(PlayerIG.pots))
    print("Health: {0}/{1}".format(PlayerIG.health, PlayerIG.maxhealth))
    print("1. Fight\n2. Store\n3. Save\n4. Exit\n5. Inventory")
    option = input("> ")

    if option is '1':
        prefight()
    elif option is '2':
        store()
    elif option is '3':
        os.system("clear")
        with open("saved_file", "wb") as f:
            pickle.dump(PlayerIG, f)
            print("\nGame has been saved!\n")
        option = input("> ")
        start1()

    elif option is '4':
        sys.exit()
    elif option is '5':
        inventory()
    else:
        start1()


def main():
    os.system("clear")
    print("Welcome to my game")
    print("1. Start\n2. Load\n3. Exit")
    option = input("> ")

    if option is '1':
        start()
    elif option is '2':
        if os.path.exists("saved_file") is True:
            os.system("clear")
            with open("saved_file", "rb") as f:
                global PlayerIG
                PlayerIG = pickle.load(f)
            print("Loaded Save State...")
            option = input("> ")
            start1()
        else:
            print("You have no save file for this game")
            option = input(" ")
            main()

    elif option is '3':
        sys.exit()
    else:
        main()


if __name__ == "__main__":
    main()
