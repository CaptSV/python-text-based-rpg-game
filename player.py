class Player:
    def __init__(self, name, health, attack_power, inventory, location):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.inventory = inventory
        self.location = location

    def player_status(self):
        print(f'Name: {self.name}')
        print(f'Health: {self.health}')
        print(f'Attack Power: {self.attack_power}')
        print(f'Inventory: {self.inventory}')
        print(f'Location: {self.location.name} - {self.location.description}, heading out your door sets you North.')

    def attack(self, target):
        return target  # use getter/setters to ask the target to take damage and pass on attack_power that way

    def take_damage(self, amount):
        return amount

    def navigate(self, direction):
        next_location = self.location.exits.get(direction)
        if next_location:
            self.location = next_location
            return True
        else:
            return False