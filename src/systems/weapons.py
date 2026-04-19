class Weapon:
    def __init__(
        self,
        name,
        weapon_type,
        damage,
        range,
        cooldown,
        image=None,
        weapon_distance=10,
        hand_offset_x=0,
        hand_offset_y=0,
        rotation_offset=0
    ):
        self.name = name
        self.weapon_type = weapon_type
        self.damage = damage
        self.range = range
        self.cooldown = cooldown
        self.image = image

        self.weapon_distance = weapon_distance
        self.hand_offset_x = hand_offset_x
        self.hand_offset_y = hand_offset_y
        self.rotation_offset = rotation_offset