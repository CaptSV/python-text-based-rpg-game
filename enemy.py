class Enemy:
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.attack_power = attack_power

    def attack(self, target):
        return target # use getter/setters to ask the target to take damage and pass on attack_power that way

    def take_damage(self, amount):
        self.health -= amount
        return self.health