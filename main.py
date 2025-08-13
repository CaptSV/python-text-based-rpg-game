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

def _display_main_menu():
    print("-----Main Menu-----")
    print("[1] Start Game")
    print("[2] Quit")
    print("-------------------")

def _display_action_menu():
    print("-------Action Menu-------")
    print("[1] Move to a Location")
    print("[2] Attack Enemy")
    print("[3] Pick Up Item")
    print("[4] Quit to Main Menu")
    print("-------------------------")


def _get_valid_navigation_input():
    navigation_check = True
    while navigation_check:
        exits_str = ", ".join(player1.location.exits.keys()) if player1.location.exits else "No exits here"
        print(f'You are currently at {player1.location.name} and your exits are at the {exits_str}')
        direction = input("Where would you like to go? (North, South, East or West): ").capitalize() # <- Error handling when NOT one of the options eg: 123, Home, Top, Lol
        next_location = player1.navigate(direction)
        if not next_location:
            print("You can't go that way!\n")
        else:
            navigation_check = False

def _handle_item_input():

    if not player1.location.items:
        print("There are no items in this location\n")
        return

    item_found_and_taken = False
    while not item_found_and_taken:
        print(f'\nLocation items: {[i.name for i in player1.location.items]}')
        item_choice = input("What item would you like to take? (type 'cancel' to stop): ").casefold()

        if item_choice == "cancel":
            print("Cancelled item pickup.\n")
            return

        found_item = None
        for item_in_location in player1.location.items:
            if item_choice == item_in_location.name.casefold():
                found_item = item_in_location
                break

        if found_item:
            player1.inventory.append(found_item)
            player1.location.items.remove(found_item)
            print(f'\nYou picked up the {found_item.name} and added it into your inventory.')
            item_found_and_taken = True
        else:
            print(f'There\'s no \'{item_choice}\' here. Try again or \'cancel\'.\n')

        print(f'Your inventory: {[i.name for i in player1.inventory]}')


def _display_location_information():
    enemy_names = [enemy.name for enemy in player1.location.enemies]
    enemy_str = ", ".join(enemy_names) if enemy_names else "No enemies here"

    item_names = [item.name for item in player1.location.items]
    item_str = ", ".join(item_names) if item_names else "No items here"

    exit_str = ", ".join(player1.location.exits.keys()) if player1.location.exits else "No exits here"

    print(f'\nYou are now at the {player1.location.name}. {player1.location.description}')
    print(f'There\'s a {enemy_str} enemy here and a {item_str} is available')
    print(f'Your current exits are to the {exit_str}\n')

def _get_action_input():
    action = int(input("What would you like to do?: "))
    match action:
        case 1:
            print("Move")
        case 2:
            print("Attack")
        case 3: # <- Needs to handle choosing which item to pick up if multiple items found. Right now just takes them all.
            _handle_item_input()
        case 4:
            print("Quit")
        case _:
            print("None")

# main game logic
def start_game():
    print("Game Started")

    # insert main game code here
    player_name = input("Character Name: ")
    player1.name = player_name
    print("---------------------------")
    print(f'Hello {player1.name}, welcome to the world of Shystra')
    print("---------------------------")
    print("Your current state is as follows:")
    player1.player_status()
    print()

    # navigation check and update <- move to its own function to call multiple times
    _get_valid_navigation_input()

    # display location info <- move to its own function to call multiple times
    _display_location_information()

    # create an action menu for move, fight, pick up item
    _display_action_menu()

    # put valid_navigation_input into move choice menu
    _get_action_input()

# main menu
if __name__ == "__main__":
    continue_game = True
    while continue_game:
        _display_main_menu()
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


