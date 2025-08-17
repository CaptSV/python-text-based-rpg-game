from player import Player
from enemy import Enemy
from location import Location
from item import Item

# enemies instantiations
skeleton = Enemy("Skeleton", 20, 5)
goblin = Enemy("Goblin", 30, 10)

# items instantiations - currently have no functionality yet, when doing that create the items in the item.py
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
player1 = Player("Tim", 100, 10, [], home)

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
    print("[4] Show Player Status")
    print("[5] Quit to Main Menu")
    print("-------------------------")

def _display_combat_menu():
    print("-------Combat Menu-------")
    print("[1] Attack")
    # print("[2] Items") <-- implement later
    # print("[3] Retreat") <-- implement later
    print("-------------------------")

def _handle_navigation_input():
    navigation_check = True
    while navigation_check:
        exits_str = ", ".join(player1.location.exits.keys()) if player1.location.exits else "No exits here"
        print(f'You are currently at {player1.location.name} and your exits are at the {exits_str}')
        direction = input("Where would you like to go? North, South, East or West. (type 'cancel' to stop): ").capitalize()

        if direction == "Cancel":
            print("Cancelled moving location\n")
            return

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
        print(f'\nLocation items: {[i.name for i in player1.location.items]}') # <- Shows items in a list for user, might want to just have its name
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

def _handle_attack_input():

    if not player1.location.enemies:
        print("There are no enemies here")
        return

    enemy_found_and_defeated = False
    while not enemy_found_and_defeated:
        print(f'Enemies in location: {[enemy.name for enemy in player1.location.enemies]}') # <- Shows items in a list for user, might want to just have its name
        target_choice = input("Which enemy would you like to attack? (type 'cancel' to stop): ").casefold()

        if target_choice == "cancel":
            print("Cancelled attack.\n")
            return

        # might need to introduce another loop for the attacking and item using
        enemy_defeated = False
        while not enemy_defeated:
            _display_combat_menu()
            combat_action = int(input("What would you like to do?: "))
            if combat_action == 1:
                for enemy_in_location in player1.location.enemies:
                    if target_choice == enemy_in_location.name.casefold():
                        player_attack_damage = player1.attack()
                        enemy_dead = enemy_in_location.take_damage(player_attack_damage)

                        print("-------Battle Details-------")
                        print(f'{enemy_in_location.name} takes {player_attack_damage} damage. Enemy remaining health: {enemy_in_location.health}')
                        print(f'{enemy_in_location.name} retaliates and attacks you.')
                        enemy_attack_damage = enemy_in_location.attack()
                        player1.take_damage(enemy_attack_damage)
                        print(f'{enemy_in_location.name} does {enemy_in_location.attack_power} damage to you.')
                        print(f'Your health is now {player1.health}')
                        print("---------------------------")

                        if enemy_dead:
                            print(f'You defeated the {enemy_in_location.name}')

                            updated_enemy_list = player1.location.enemies.copy()
                            print(f'Updated enemy list >> {[enemy.name for enemy in updated_enemy_list]}')
                            enemy_remaining = updated_enemy_list.remove(enemy_in_location)
                            player1.location.enemies = enemy_remaining
                            if player1.location.enemies:
                                print(f'Location enemies updated >> {[enemy.name for enemy in player1.location.enemies]}')
                            else:
                                print("NO MORE ENEMIES")

                            # TODO: Fix bug - list.remove() returns None, causing player1.location.enemies to become None
                            # The current logic will break the enemy list after the first defeat.
                            # Need to correctly remove the enemy object from player1.location.enemies list
                            # without assigning None.


def _display_location_information():
    enemy_names = [enemy.name for enemy in player1.location.enemies]
    enemy_str = ", ".join(enemy_names) if enemy_names else "No enemies here"

    item_names = [item.name for item in player1.location.items]
    item_str = ", ".join(item_names) if item_names else "No items here"

    exit_str = ", ".join(player1.location.exits.keys()) if player1.location.exits else "No exits here"

    print(f'You are now at the {player1.location.name}. {player1.location.description}')
    print(f'There\'s a {enemy_str} enemy here and a {item_str} is available')
    print(f'Your current exits are to the {exit_str}\n')

def _get_action_input(): # <- Currently doesn't handle character input, will break out of action loop and into main_menu loop if character
    action = int(input("What would you like to do?: "))
    match action:
        case 1:
            _handle_navigation_input()
            return True
        case 2:
            _handle_attack_input()
            return True
        case 3:
            _handle_item_input()
            return True
        case 4:
            player1.player_status()
            return True
        case 5:
            print("Exiting Game")
            return False
        case _:
            print("Not a valid option")
            return True

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

    # action input loop
    action_loop = True
    while action_loop:
        _display_location_information()
        _display_action_menu()
        action_loop = _get_action_input()
        if not action_loop:
            break


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