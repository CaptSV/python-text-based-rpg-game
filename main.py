from player import Player
from enemy import Enemy
from location import Location
from item import Item

# enemies instantiations
skeleton = Enemy("Skeleton", 20, 5)
goblin = Enemy("Goblin", 30, 10)

# items instantiations
potion = Item("Health Potion", "Heal 20 Health")
sword = Item("Sword", "Steel Sword, rusty but can do the job. 15 Damage")

# locations instantiations
home = Location("Home", "Your home, a safe haven to rest", [], [], {})
forest = Location("Forest", "A serene forest, but one can't be too careful out here", [skeleton], [potion], {})
cave = Location("Cave", "Dark and damp. Scary but peaceful", [skeleton, goblin], [sword, potion], {})
dungeon = Location("Dungeon", "An abandoned dungeon, used for slavery and torture", [goblin], [potion], {})

# locations - updating exits
home.exits["North"] = forest # <- update home to have all locations
dungeon.exits["South"] = home
forest.exits["East"] = cave
cave.exits["West"] = dungeon

# player instantiation
player1 = Player("Tim", 100, 25, [], home)

def display_main_menu():
    print("-----Main Menu-----")
    print("[1] Start Game")
    print("[2] Quit")
    print("-------------------")


# main game logic
def start_game():
    print("Game Started")

    #insert main game code here
    player_name = input("Character Name: ")
    player1.name = player_name
    print("---------------------------")
    print(f'Hello {player1.name}, welcome to the world of Shystra')
    print("---------------------------")
    print("Your current state is as follows:")
    player1.player_status()
    print()

    # navigation check and update <- might put into its own function since you need to call it several times
    exits_str = ", ".join(player1.location.exits.keys()) if player1.location.exits else "No Exits"
    navigation_check = True
    while navigation_check:
        print(f'You are currently at {player1.location.name} and your exits are at the {exits_str}')
        direction = input("Where would you like to go? (North, South, East or West): ").capitalize()
        next_location = player1.navigate(direction)
        if not next_location:
            print("You can't go that way!")
            print("---------------------------\n")
        else:
            print(f'You are heading to the {direction}\n')
            navigation_check = False

    # display location info
    enemy_names = [enemy.name for enemy in player1.location.enemies]
    enemy_str = ", ".join(enemy_names) if enemy_names else "No enemies here"

    item_names = [item.name for item in player1.location.items]
    item_str = ", ".join(item_names) if item_names else "No items here"

    print(f'You are now at the {player1.location.name}. {player1.location.description}')
    print(f'There\'s a {enemy_str} enemy here and a {item_str} is available')


# main menu
if __name__ == "__main__":
    continue_game = True
    while continue_game:
        display_main_menu()
        try:
            menu_option = int(input("Choice: "))
            if menu_option == 1:
                start_game()
                continue_game = False
            elif menu_option == 2:
                print("Exiting Game")
                continue_game = False
            else:
                print("Please choose a correct option (1 or 2)")
        except ValueError:
            print("Please choose a correct option (1 or 2)")


