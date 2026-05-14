import pygame
from src.systems.weapons import (
    Weapon, WeaponCategory,
    UnarmedBehavior, MeleeBehavior, RangedBehavior
)


class WeaponFactory:
    """
    Luo kaikki pelissä esiintyvät aseet.
    Uuden aseen lisääminen = uusi elif-haara tänne.
    """

    @staticmethod
    def create(name):

        # =========================================================
        # UNARMED  –  slot 1, aina pelaajalla
        # =========================================================

        if name == "Fists":
            return Weapon(
                name="Fists",
                category=WeaponCategory.UNARMED,
                cooldown=400,
                behavior=UnarmedBehavior(damage=5, reach=35, melee_bonus=0),
                image=None,
                droppable=False
            )

        if name == "Brass Knuckles":
            return Weapon(
                name="Brass Knuckles",
                category=WeaponCategory.UNARMED,
                cooldown=350,
                behavior=UnarmedBehavior(damage=10, reach=35, melee_bonus=5),
                image=None,
                droppable=False
            )

        if name == "Boxing Gloves":
            return Weapon(
                name="Boxing Gloves",
                category=WeaponCategory.UNARMED,
                cooldown=300,
                behavior=UnarmedBehavior(damage=8, reach=38, melee_bonus=3),
                image=None,
                droppable=False
            )

        # =========================================================
        # MELEE  –  poimitaan maasta
        # =========================================================

        if name == "Bat":
            bat_image = pygame.image.load(
                "assets/sprites/melee_weapons/Baseballbat.png"
            ).convert_alpha()
            bat_image = pygame.transform.scale(bat_image, (24, 24))

            return Weapon(
                name="Bat",
                category=WeaponCategory.MELEE,
                cooldown=500,
                behavior=MeleeBehavior(damage=20, reach=55, arc=90),
                image=bat_image,
                weapon_distance=12,
                hand_offset_x=4,
                hand_offset_y=5,
                droppable=True
            )

        if name == "Knife":
            return Weapon(
                name="Knife",
                category=WeaponCategory.MELEE,
                cooldown=250,
                behavior=MeleeBehavior(damage=15, reach=40, arc=60),
                image=None,
                weapon_distance=10,
                droppable=True
            )

        if name == "Mace":
            return Weapon(
                name="Mace",
                category=WeaponCategory.MELEE,
                cooldown=700,
                behavior=MeleeBehavior(damage=35, reach=50, arc=100),
                image=None,
                weapon_distance=14,
                droppable=True
            )

        # =========================================================
        # RANGED  –  poimitaan maasta
        # =========================================================

        if name == "Pistol":
            return Weapon(
                name="Pistol",
                category=WeaponCategory.RANGED,
                cooldown=300,
                behavior=RangedBehavior(damage=20, bullet_speed=12, fire_mode="single"),
                image=None,
                weapon_distance=20,
                droppable=True
            )

        if name == "AK-47":
            return Weapon(
                name="AK-47",
                category=WeaponCategory.RANGED,
                cooldown=120,
                behavior=RangedBehavior(damage=15, bullet_speed=14, fire_mode="auto"),
                image=None,
                weapon_distance=20,
                droppable=True
            )

        raise ValueError(f"WeaponFactory: tuntematon ase '{name}'")