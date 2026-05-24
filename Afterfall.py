# AFTERFALL : SURVIVAL

import random
import json
import time


# Stores map locations using a multi-dimensional list
world_map = [
    ["Supermarket", "Police Station", "Hospital"],
    ["Apartment Building", "Gas Station", "School"]
]


# Zombie class used during combat
class Zombie:

    def __init__(self, health, damage):

        self.health = health
        self.damage = damage


# Creates typewriter text effect
def type_text(text):

    for letter in text:

        print(letter, end="", flush=True)

        time.sleep(0.1)

    print()


# Stores all player information
player = {

    "health": 100,
    "hunger": 0,
    "stamina": 100,

    "ammo": 15,
    "shotgun_ammo": 6,

    "day": 1,
    "time": 8,

    "inventory": [
        "Knife",
        "Pistol",
        "Shotgun",
        "Bandage",
        "Water Bottle"
    ]
}

alive = True


# Possible loot items
normal_loot = [

    "Food",
    "Bandage",
    "Ammo",
    "Shotgun Shells",
    "Water Bottle",
    "Nothing"
]


# Advances in-game time
def advance_time(hours):

    player["time"] += hours

    while player["time"] >= 24:

        player["time"] -= 24

        player["day"] += 1

        type_text("\nA new day begins...")

    if player["time"] >= 18:

        type_text("\nNight has fallen...")


# Displays player status
def show_status():

    if player["time"] < 12:
        period = "AM"

    else:
        period = "PM"

    display_time = player["time"]

    if display_time > 12:

        display_time -= 12

    print("\n" + "=" * 50)

    print("        AFTERFALL : SURVIVAL")

    print("=" * 50)

    print(f"Day    : {player['day']}")
    print(f"Time   : {display_time}:00 {period}")

    print(f"Health : {player['health']}")
    print(f"Hunger : {player['hunger']}")
    print(f"Stamina: {player['stamina']}")

    print(f"Pistol Ammo : {player['ammo']}")
    print(f"Shotgun Ammo: {player['shotgun_ammo']}")

    print("=" * 50)


# Shows inventory items
def show_inventory():

    print("\n========== INVENTORY ==========")

    if len(player["inventory"]) == 0:

        print("Inventory is empty.")

    else:

        for item in player["inventory"]:

            print(f"- {item}")

    print("===============================")

    input("\nPress Enter to continue...")


# Saves game data into JSON file
def save_game():

    with open("savegame.json", "w") as file:

        json.dump(player, file)

    type_text("\nGame saved successfully.")


# Loads saved game
def load_game():

    global player

    try:

        with open("savegame.json", "r") as file:

            player = json.load(file)

        type_text("\nGame loaded successfully.")

    except FileNotFoundError:

        type_text("\nNo save file found.")


# Rest system
def rest():

    type_text("\nYou rest for the night...")

    player["health"] += 20
    player["stamina"] += 40
    player["hunger"] += 10

    if player["health"] > 100:

        player["health"] = 100

    if player["stamina"] > 100:

        player["stamina"] = 100

    player["day"] += 1
    player["time"] = 8

    type_text("\nYou wake up the next morning.")


# Random story events
def story_event():

    event = random.randint(1, 4)

    # Survivor event
    if event == 1:

        type_text("\nYou find an injured survivor.")

        print("\n1. Help")
        print("2. Ignore")
        print("3. Rob")

        choice = input("\nChoose: ")

        if choice == "1":

            reward = random.choice([
                "Food",
                "Bandage",
                "Ammo"
            ])

            type_text(f"\nThe survivor gives you: {reward}")

            if reward == "Ammo":

                player["ammo"] += 5

            else:

                player["inventory"].append(reward)

        elif choice == "2":

            type_text("\nYou walk away.")

        elif choice == "3":

            damage = random.randint(5, 15)

            player["health"] -= damage

            type_text(
                f"\nThe survivor fought back. You lost {damage} health."
            )

    # House event
    elif event == 2:

        type_text("\nYou discover an abandoned house.")

        found = random.choice([
            "Food",
            "Water Bottle",
            "Bandage",
            "Medkit"
        ])

        type_text(f"\nYou found: {found}")

        player["inventory"].append(found)

    # Military crate event
    elif event == 3:

        type_text("\nYou found a military supply crate.")

        reward = random.choice([
            "Ammo",
            "Shotgun Shells",
            "Medkit"
        ])

        type_text(f"You obtained: {reward}")

        if reward == "Ammo":

            player["ammo"] += 10

        elif reward == "Shotgun Shells":

            player["shotgun_ammo"] += 4

        else:

            player["inventory"].append(reward)

    # Trap event
    else:

        type_text("\nYou triggered a trap.")

        damage = random.randint(10, 25)

        player["health"] -= damage

        type_text(f"You lost {damage} health.")


# Gives loot after zombie fights
def zombie_loot():

    loot = random.choice(normal_loot)

    type_text("\nZombie defeated.")

    if loot == "Nothing":

        type_text("The zombie dropped nothing.")

    else:

        type_text(f"You found: {loot}")

        if loot == "Ammo":

            player["ammo"] += 5

        elif loot == "Shotgun Shells":

            player["shotgun_ammo"] += 2

        else:

            player["inventory"].append(loot)


# Combat system
def combat():

    if player["time"] >= 18:

        zombie = Zombie(80, 25)

    else:

        zombie = Zombie(50, 15)

    type_text("\nA zombie appeared!")

    while zombie.health > 0 and player["health"] > 0:

        print("\n" + "=" * 40)

        print(f"Zombie Health: {zombie.health}")
        print(f"Your Health  : {player['health']}")

        print("=" * 40)

        print("1. Pistol")
        print("2. Shotgun")
        print("3. Knife")
        print("4. Run")

        choice = input("Choose: ")

        if choice not in ["1", "2", "3", "4"]:

            raise ValueError("Invalid combat choice.")

        # Pistol attack
        if choice == "1":

            if player["ammo"] > 0:

                damage = random.randint(20, 40)

                zombie.health -= damage

                player["ammo"] -= 1

                type_text(
                    f"\nYou shot the zombie for {damage} damage."
                )

            else:

                type_text("\nNo pistol ammo left!")

        # Shotgun attack
        elif choice == "2":

            if player["shotgun_ammo"] > 0:

                damage = random.randint(40, 70)

                zombie.health -= damage

                player["shotgun_ammo"] -= 1

                type_text(
                    f"\nYou blasted the zombie for {damage} damage."
                )

            else:

                type_text("\nNo shotgun shells left!")

        # Knife attack
        elif choice == "3":

            damage = random.randint(10, 25)

            zombie.health -= damage

            type_text(
                f"\nYou stabbed the zombie for {damage} damage."
            )

        # Escape attempt
        elif choice == "4":

            escape = random.randint(1, 2)

            if escape == 1:

                type_text("\nYou escaped successfully.")

                return

            else:

                type_text("\nYou failed to escape!")

        # Zombie attacks player
        if zombie.health > 0:

            player["health"] -= zombie.damage

            type_text(
                f"\nZombie attacked you for {zombie.damage} damage."
            )

    if player["health"] <= 0:

        type_text("\nYou were killed by the zombie.")

    else:

        zombie_loot()


# Exploration system
def explore():

    print("\n========== MAP ==========")

    for row in world_map:

        print(row)

    print("=========================")

    print("\n1. Supermarket")
    print("2. Police Station")
    print("3. Hospital")
    print("4. Apartment Building")
    print("5. Gas Station")
    print("0. Cancel")

    location_choice = input("\nWhere do you want to go? ")

    locations = {

        "1": "Supermarket",
        "2": "Police Station",
        "3": "Hospital",
        "4": "Apartment Building",
        "5": "Gas Station"
    }

    if location_choice == "0":

        return

    if location_choice not in locations:

        type_text("\nInvalid location.")

        return

    location = locations[location_choice]

    type_text(f"\nYou travel to the {location}...")

    advance_time(4)

    player["stamina"] -= random.randint(5, 15)

    player["hunger"] += random.randint(5, 10)

    event = random.randint(1, 100)

    # Story event
    if event <= 30:

        story_event()

    # Zombie event
    elif event <= 70:

        combat()

    # Loot event
    elif event <= 90:

        loot = random.choice(normal_loot)

        type_text(f"\nYou found: {loot}")

        if loot == "Ammo":

            player["ammo"] += 5

        elif loot == "Shotgun Shells":

            player["shotgun_ammo"] += 2

        elif loot != "Nothing":

            player["inventory"].append(loot)

    # Quiet event
    else:

        type_text("\nThe area was quiet.")


# Allows player to use items
def use_item():

    usable_items = []

    for item in player["inventory"]:

        if item in [
            "Food",
            "Bandage",
            "Water Bottle",
            "Medkit"
        ]:

            usable_items.append(item)

    if len(usable_items) == 0:

        type_text("\nYou have no usable items.")

        input("\nPress Enter to continue...")

        return

    print("\n========== USE ITEM ==========")

    for index, item in enumerate(usable_items):

        print(f"{index + 1}. {item}")

    print("0. Exit")

    try:

        choice = int(input("\nSelect item: "))

        if choice == 0:

            return

        item = usable_items[choice - 1]

        # Bandage
        if item == "Bandage":

            player["health"] += 20

            if player["health"] > 100:

                player["health"] = 100

            type_text("\nYou used a Bandage.")

        # Food
        elif item == "Food":

            player["hunger"] -= 20

            if player["hunger"] < 0:

                player["hunger"] = 0

            type_text("\nYou ate some food.")

        # Water bottle
        elif item == "Water Bottle":

            player["stamina"] += 15

            if player["stamina"] > 100:

                player["stamina"] = 100

            type_text("\nYou drank water.")

        # Medkit
        elif item == "Medkit":

            player["health"] = 100

            type_text("\nYou used a Medkit.")

        player["inventory"].remove(item)

        advance_time(1)

        input("\nPress Enter to continue...")

    except:

        type_text("\nInvalid input.")


# Checks if player is alive
def check_player_status():

    global alive

    if player["hunger"] >= 100:

        type_text("\nYou died from starvation.")

        alive = False

    if player["health"] <= 0:

        type_text("\nYou died.")

        alive = False


# Game title screen
print("=" * 50)

print("      WELCOME TO AFTERFALL")

print("=" * 50)

type_text("""
INSTRUCTIONS:
- Explore for loot
- Fight zombies
- Manage health and hunger
- Survive for 15 days
- Zombies are stronger at night
""")


# Load save file option
load = input("\nLoad save? (y/n): ")

if load.lower() == "y":

    load_game()


# Main game loop
while alive:

    check_player_status()

    if not alive:

        break

    if player["day"] > 15:

        print("\n" + "=" * 50)

        print("CONGRATULATIONS!")

        print("You survived 15 days.")

        print("=" * 50)

        break

    show_status()

    print("1. Explore")
    print("2. Rest")
    print("3. Inventory")
    print("4. Use Item")
    print("5. Save Game")
    print("6. Quit")

    choice = input("\nChoose: ")

    if choice == "1":

        explore()

    elif choice == "2":

        rest()

    elif choice == "3":

        show_inventory()

    elif choice == "4":

        use_item()

    elif choice == "5":

        save_game()

    elif choice == "6":

        type_text("\nThanks for playing.")

        break

    else:

        type_text("\nInvalid choice.")


# Final game over screen
print("\n" + "=" * 50)

print("GAME OVER")

print(f"You survived until Day {player['day']}.")

print("=" * 50)
