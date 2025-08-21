class Player:
    def __init__(self, name, health, attack_power, inventory, location):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.inventory = inventory
        self.location = location

    def player_status(self):
        item_names = [item.name for item in self.inventory]
        item_str = ", ".join(item_names) if item_names else "No items in inventory"

        print("-------Player Status-------")
        print(f'Name: {self.name}')
        print(f'Health: {self.health}')
        print(f'Attack Power: {self.attack_power}')
        print(f'Inventory: {item_str}')
        print(f'Location: {self.location.name}\n')

    def attack(self):
        return self.attack_power

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            return True
        else:
            return False

    def navigate(self, direction):
        next_location = self.location.exits.get(direction)
        if next_location:
            self.location = next_location
            return True
        else:
            return False

    def use_item(self):
        return "Used Item"