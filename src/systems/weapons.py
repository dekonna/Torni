import math
from enum import Enum


class WeaponCategory(Enum):
    UNARMED = "unarmed"
    MELEE   = "melee"
    RANGED  = "ranged"


# =============================================================
# BEHAVIOR-LUOKAT
# Jokainen ase kantaa mukanaan oman logiikkansa.
# player.py kutsuu vain weapon.use(player) tietämättä
# yksityiskohdista mitään.
# =============================================================

class UnarmedBehavior:
    """
    Nyrkit, nyrkkiraudat, hanskat.
    Antaa pelaajalle melee-bonuksia statseihin.
    Aina slot 1:ssä – ei voi pudottaa.
    """

    def __init__(self, damage, reach, melee_bonus=0):
        self.damage      = damage
        self.reach       = reach
        self.melee_bonus = melee_bonus  # bonus muiden melee-aseiden vahinkoon


    def use(self, player):
        self._hit_enemies(player, self.damage + self.melee_bonus)


    def _hit_enemies(self, player, total_damage):
        angle = player.angle
        for enemy in player.game.enemies:
            dx = enemy.rect.centerx - player.rect.centerx
            dy = enemy.rect.centery - player.rect.centery
            distance = math.hypot(dx, dy)

            if distance > self.reach:
                continue

            # tarkistaa että vihollinen on edessä (±70°)
            enemy_angle = math.atan2(dy, dx)
            angle_diff  = abs(math.degrees(enemy_angle - angle)) % 360
            if angle_diff > 180:
                angle_diff = 360 - angle_diff

            if angle_diff < 70:
                enemy.take_damage(total_damage)


class MeleeBehavior:
    """
    Puukot, miekat, nuijat, pesäpallomaila jne.
    Laajempi osuma-alue ja suurempi vahinko kuin nyrkeillä.
    Melee-bonus slot 1:stä lisätään vahinkoon automaattisesti.
    """

    def __init__(self, damage, reach, arc=80):
        self.damage = damage
        self.reach  = reach
        self.arc    = arc   # osuma-kaaren leveys asteina


    def use(self, player):
        bonus        = player.get_melee_bonus()
        total_damage = self.damage + bonus
        angle        = player.angle

        for enemy in player.game.enemies:
            dx = enemy.rect.centerx - player.rect.centerx
            dy = enemy.rect.centery - player.rect.centery
            distance = math.hypot(dx, dy)

            if distance > self.reach:
                continue

            enemy_angle = math.atan2(dy, dx)
            angle_diff  = abs(math.degrees(enemy_angle - angle)) % 360
            if angle_diff > 180:
                angle_diff = 360 - angle_diff

            if angle_diff < self.arc / 2:
                enemy.take_damage(total_damage)


class RangedBehavior:
    """
    Pistooli, AK-47 jne.
    Ampuu luodin pelaajan tähtäyssuuntaan.
    fire_mode: 'single' | 'burst' | 'auto'  (laajennetaan myöhemmin)
    """

    def __init__(self, damage, bullet_speed=10, fire_mode="single"):
        self.damage       = damage
        self.bullet_speed = bullet_speed
        self.fire_mode    = fire_mode


    def use(self, player):
        from src.entities.bullet import Bullet

        dx = math.cos(player.angle)
        dy = math.sin(player.angle)

        bullet = Bullet(
            player.rect.centerx,
            player.rect.centery,
            dx,
            dy,
            damage=self.damage,
            speed=self.bullet_speed
        )

        player.bullets.append(bullet)


# =============================================================
# WEAPON-LUOKKA
# Kantaa nimen, kategorian, cooldownin, kuvan ja behaviorin.
# =============================================================

class Weapon:

    def __init__(
        self,
        name,
        category,
        cooldown,
        behavior,
        image=None,
        weapon_distance=10,
        hand_offset_x=0,
        hand_offset_y=0,
        rotation_offset=0,
        droppable=True
    ):
        self.name             = name
        self.category         = category
        self.cooldown         = cooldown
        self.behavior         = behavior
        self.image            = image
        self.weapon_distance  = weapon_distance
        self.hand_offset_x    = hand_offset_x
        self.hand_offset_y    = hand_offset_y
        self.rotation_offset  = rotation_offset
        self.droppable        = droppable   # nyrkit eivät putoa


    def use(self, player):
        self.behavior.use(player)