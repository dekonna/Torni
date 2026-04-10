class Weapon:
    def __init__(self, name, weapon_type, damage, range, cooldown):
        self.name = name
        self.weapon_type = weapon_type or "ranged"
        self.damage = damage
        self.range = range
        self.cooldown = cooldown