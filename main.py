from player import Player
from enemy import Enemy
from location import Location
from item import Item

# enemies instantiations
skeleton = Enemy("Skeleton", 20, 100)
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

# game over global flag: Set to True when the player is defeated to end the game.
game_over = False

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
    print("[2] Items")
    print("[3] Retreat")
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
    global game_over # Declare that we intend to modify the global game_over flag

    if not player1.location.enemies:
        print("There are no enemies here")
        return

    enemy_found = False
    chosen_target_enemy = None
    enemy_list = [enemy.name for enemy in player1.location.enemies]
    while not enemy_found: # handle selection of valid enemy
        print(f'Enemies in location: {enemy_list}') # TODO <- Shows items in a list for user, might want to just have its name
        target_choice = input("Which enemy would you like to attack? (type 'cancel' to stop): ").casefold()

        if target_choice == "cancel":
            return

        # Search for the chosen enemy object in the location's enemies
        for enemy_in_location in player1.location.enemies:
            if target_choice == enemy_in_location.name.casefold():
                chosen_target_enemy = enemy_in_location
                break # Found enemy, exit "enemy_in_location" loop

        if chosen_target_enemy is None:
            print(f'{target_choice.capitalize()} was not found in this location')
            continue # Restart target selection loop to prompt again
        else:
            enemy_found = True # Valid enemy found, exit target selection loop

    # Loop to handle the actual combat (player vs. chosen_target_enemy)
    # Continues until enemy is defeated, player is defeated, or player retreats/cancels combat action.
    enemy_found_and_defeated = False
    while not enemy_found_and_defeated: # handle the combat menu, attacking back and forth and checking details
        _display_combat_menu()

        # TODO: Implement robust input handling for combat_choice (e.g., try-except for non-int, 'cancel' string)
        combat_choice = int(input("What would you like to do?: "))

        if combat_choice == 1:
            player_attack_damage = player1.attack()
            enemy_attacked_and_dead = chosen_target_enemy.take_damage(player_attack_damage) # T or F if dead or not

            print("-------Battle Details-------")
            # Always print initial damage dealt by player
            print(f'{chosen_target_enemy.name} takes {player_attack_damage} damage. Enemy remaining health: {chosen_target_enemy.health}')
            if enemy_attacked_and_dead: # Scenario 1: Enemy is defeated
                print("You defeated the enemy!")
                # remove enemy from list
                updated_enemy_list = [enemy for enemy in player1.location.enemies if enemy != chosen_target_enemy]
                player1.location.enemies = updated_enemy_list
                enemy_found_and_defeated = True
            else: # Scenario 2: Enemy is NOT defeated, so they retaliate
                enemy_attack_damage = chosen_target_enemy.attack()
                player_attacked_and_dead = player1.take_damage(enemy_attack_damage)

                if player_attacked_and_dead: # Scenario 2a: Player is defeated
                    print("You are dead")
                    game_over = True
                    break # Exit combat loop immediately upon player death
                else: # Scenario 2b: Player is NOT defeated, combat continues
                    print(f'{chosen_target_enemy.name} retaliates and attacks you.')
                    print(f'{chosen_target_enemy.name} does {chosen_target_enemy.attack_power} damage to you.')
                    print(f'Your health is now {player1.health}')
            print("---------------------------")

            # TODO: Add logic for combat option 2 (Items) and 3 (Retreat)
            # These would be 'elif combat_choice == 2:' and 'elif combat_choice == 3:'
            # Remember to handle exiting the combat loop if retreat is successful/chosen
    return


def _display_location_information():
    enemy_names = [enemy.name for enemy in player1.location.enemies]
    enemy_str = ", ".join(enemy_names) if enemy_names else "No enemies here"

    item_names = [item.name for item in player1.location.items]
    item_str = ", ".join(item_names) if item_names else "No items here"

    exit_str = ", ".join(player1.location.exits.keys()) if player1.location.exits else "No exits here"

    print(f'You are now at the {player1.location.name}. {player1.location.description}')
    print(f'There\'s a {enemy_str} enemy here and a {item_str} is available')
    print(f'Your current exits are to the {exit_str}\n')

def _get_action_input():
    # TODO: Implement robust input handling for action (e.g., try-except for non-int)

    if game_over:
        return False

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

        if game_over:
            break

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

        if game_over:
            continue_game = False

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