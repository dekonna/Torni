import pygame
from src.systems.weapons import Weapon


class WeaponFactory:

    @staticmethod
    def create(name):

        if name == "Bat":
            bat_image = pygame.image.load(
                "assets/sprites/melee_weapons/Baseballbat.png"
            ).convert_alpha()

            bat_image = pygame.transform.scale(bat_image, (24, 24))

            return Weapon(
                "Bat",
                "melee",
                15,
                50,
                400,
                bat_image,

                weapon_distance=5,
                hand_offset_x=4,
                hand_offset_y=5,
                rotation_offset=0
            )

        elif name == "Pistol":
            return Weapon(
                name="Pistol",
                weapon_type="ranged",
                damage=20,
                range=500,
                cooldown=200,
                image=None,  # lisää kuva myöhemmin
                weapon_distance=20
            )

        raise ValueError(f"Unknown weapon: {name}")