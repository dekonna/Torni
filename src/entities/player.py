import pygame
import math

from src.entities.bullet import Bullet
from src.systems.weapons import WeaponCategory
from src.systems.asset_system import AssetManager


class Player:

    # =========================================================
    # SHARED ANIMATIONS
    # =========================================================

    ANIMATIONS = {
        "down": [],
        "up": [],
        "left": [],
        "right": []
    }

    # =========================================================
    # INIT
    # =========================================================

    def __init__(self, game, x, y):

        from src.systems.weapon_factory import WeaponFactory

        self.game = game

        # =====================================================
        # PLAYER
        # =====================================================

        self.rect = pygame.Rect(x, y, 20, 20)
        self.speed = 4
        self.direction = "down"
        self.hp = 100
        self.damage_cooldown = 0

        # =====================================================
        # ANIMATION
        # =====================================================

        self.frame_index = 0
        self.animation_speed = 0.2

        # ladataan animaatiot vain kerran
        if not Player.ANIMATIONS["down"]:

            for i in range(1, 7):

                # DOWN
                Player.ANIMATIONS["down"].append(
                    pygame.transform.scale(
                        AssetManager.load_image(
                            f"assets/sprites/player/Run/Down/Base_run_down_{i}.png"
                        ),
                        (32, 32)
                    )
                )

                # UP
                Player.ANIMATIONS["up"].append(
                    pygame.transform.scale(
                        AssetManager.load_image(
                            f"assets/sprites/player/Run/Up/Base_run_up_{i}.png"
                        ),
                        (32, 32)
                    )
                )

                # LEFT
                Player.ANIMATIONS["left"].append(
                    pygame.transform.scale(
                        AssetManager.load_image(
                            f"assets/sprites/player/Run/Left/Base_run_left_{i}.png"
                        ),
                        (32, 32)
                    )
                )

                # RIGHT
                Player.ANIMATIONS["right"].append(
                    pygame.transform.scale(
                        AssetManager.load_image(
                            f"assets/sprites/player/Run/Right/Base_run_right_{i}.png"
                        ),
                        (32, 32)
                    )
                )

        self.animations = Player.ANIMATIONS

        # =====================================================
        # COMBAT
        # =====================================================

        self.bullets = []
        self.angle = 0
        self.last_attack = 0

        # =====================================================
        # WEAPON SLOTS
        # =====================================================

        # slot 0 = aina unarmed
        self.unarmed_slot = WeaponFactory.create("Fists")

        # kerätyt aseet
        self.weapon_slots = []

        # 0 = unarmed, 1+ = weapon slots
        self.current_slot = 0

        # =====================================================
        # UI
        # =====================================================

        self.ui_font = pygame.font.Font(None, 24)

    # =========================================================
    # UPDATE
    # =========================================================

    def update(self, mouse_x, mouse_y):

        moving = False

        keys = pygame.key.get_pressed()

        # =====================================================
        # MOVEMENT
        # =====================================================

        dx = 0
        dy = 0

        if keys[pygame.K_w]:
            dy -= self.speed
            self.direction = "up"

        if keys[pygame.K_s]:
            dy += self.speed
            self.direction = "down"

        if keys[pygame.K_a]:
            dx -= self.speed
            self.direction = "left"

        if keys[pygame.K_d]:
            dx += self.speed
            self.direction = "right"

        # =====================================================
        # X COLLISION
        # =====================================================

        self.rect.x += dx

        for rect in self.game.collision_rects:

            if self.rect.colliderect(rect):

                if dx > 0:
                    self.rect.right = rect.left

                elif dx < 0:
                    self.rect.left = rect.right

        # =====================================================
        # Y COLLISION
        # =====================================================

        self.rect.y += dy

        for rect in self.game.collision_rects:

            if self.rect.colliderect(rect):

                if dy > 0:
                    self.rect.bottom = rect.top

                elif dy < 0:
                    self.rect.top = rect.bottom

        # =====================================================
        # ANIMATION
        # =====================================================

        moving = dx != 0 or dy != 0

        if moving:

            self.frame_index += self.animation_speed

            if self.frame_index >= len(self.animations[self.direction]):
                self.frame_index = 0

        else:
            self.frame_index = 0

        # =====================================================
        # MOUSE AIM
        # =====================================================

        self.angle = math.atan2(mouse_y, mouse_x) + math.pi

        # =====================================================
        # ARROW KEY AIM
        # =====================================================

        if (
            keys[pygame.K_UP]
            or keys[pygame.K_DOWN]
            or keys[pygame.K_LEFT]
            or keys[pygame.K_RIGHT]
        ):

            if keys[pygame.K_UP]:
                self.angle = -math.pi / 2

            elif keys[pygame.K_DOWN]:
                self.angle = math.pi / 2

            elif keys[pygame.K_LEFT]:
                self.angle = math.pi

            elif keys[pygame.K_RIGHT]:
                self.angle = 0

    # =========================================================
    # DRAW
    # =========================================================

    def draw(self, screen, camera):

        # =====================================================
        # PLAYER
        # =====================================================

        frame = self.animations[self.direction][int(self.frame_index)]

        screen.blit(frame, camera.apply(self.rect))

        # =====================================================
        # BULLETS
        # =====================================================

        for bullet in self.bullets:
            bullet.draw(screen, camera)

        # =====================================================
        # CURRENT WEAPON
        # =====================================================

        weapon = self.current_weapon

        # =====================================================
        # RANGED AIM LINE
        # =====================================================

        if weapon.category.value == "ranged":

            start = camera.apply(self.rect).center

            end = (
                start[0] + math.cos(self.angle) * 200,
                start[1] + math.sin(self.angle) * 200
            )

            pygame.draw.line(
                screen,
                (255, 0, 0),
                start,
                end,
                2
            )

        # =====================================================
        # WEAPON IN HAND
        # =====================================================

        if weapon.image:

            weapon_distance = weapon.weapon_distance

            hand_offset_x = weapon.hand_offset_x
            hand_offset_y = weapon.hand_offset_y

            weapon_x = (
                self.rect.centerx
                + hand_offset_x
                + math.cos(self.angle) * weapon_distance
            )

            weapon_y = (
                self.rect.centery
                + hand_offset_y
                + math.sin(self.angle) * weapon_distance
            )

            rotated_weapon = pygame.transform.rotate(
                weapon.image,
                -math.degrees(self.angle) + weapon.rotation_offset
            )

            weapon_rect = rotated_weapon.get_rect(
                center=camera.apply(
                    pygame.Rect(weapon_x, weapon_y, 0, 0)
                ).center
            )

            screen.blit(rotated_weapon, weapon_rect)

    # =========================================================
    # CURRENT WEAPON
    # =========================================================

    @property
    def current_weapon(self):

        if self.current_slot == 0:
            return self.unarmed_slot

        index = self.current_slot - 1

        if index < len(self.weapon_slots):
            return self.weapon_slots[index]

        return self.unarmed_slot

    # =========================================================
    # INVENTORY
    # =========================================================

    @property
    def inventory(self):
        """Yhteensopivuus save_manager.py:n kanssa."""
        return self.weapon_slots

    # =========================================================
    # MELEE BONUS
    # =========================================================

    def get_melee_bonus(self):
        """Palauttaa unarmed-slotin melee-bonuksen."""
        return self.unarmed_slot.behavior.melee_bonus

    # =========================================================
    # ADD WEAPON
    # =========================================================

    def add_weapon(self, weapon):

        self.weapon_slots.append(weapon)

    # =========================================================
    # ATTACK
    # =========================================================

    def attack(self):

        weapon = self.current_weapon

        now = pygame.time.get_ticks()

        if now - self.last_attack < weapon.cooldown:
            return

        self.last_attack = now

        weapon.use(self)