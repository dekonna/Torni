import pygame
import random

from src.entities.body_part import BodyPart
from src.entities.blood_particle import BloodParticle
from src.entities.blood_decal import BloodDecal

class BaseEnemy:

    # =========================================================
    # INIT
    # =========================================================

    def __init__(self, game, x, y):

        self.game = game

        # collision rect
        self.rect = pygame.Rect(x, y, 20, 20)

        # state
        self.alive = True

        # AI state
        self.state = "IDLE"

        # =====================================================
        # ATTACK
        # =====================================================

        self.attack_cooldown = 60
        self.attack_timer = 0
        self.attack_damage = 10

        # =====================================================
        # HIT STATE
        # =====================================================

        self.hit_timer = 0
        self.hit_duration = 20

        # =====================================================
        # GORE
        # =====================================================

        self.right_arm_removed = False

    # =========================================================
    # PLAYER DISTANCE
    # =========================================================

    def get_distance_to_player(self, player):

        dx = (
            player.rect.centerx
            - self.rect.centerx
        )

        dy = (
            player.rect.centery
            - self.rect.centery
        )

        return (dx ** 2 + dy ** 2) ** 0.5

    # =========================================================
    # ATTACK
    # =========================================================

    def attack_player(self, player):

        if self.attack_timer > 0:

            self.attack_timer -= 1

            return

        player.hp -= self.attack_damage

        self.attack_timer = self.attack_cooldown

    # =========================================================
    # HIT STATE
    # =========================================================

    def enter_hit_state(self):

        self.state = "HIT"

        self.hit_timer = self.hit_duration

    # =========================================================
    # GORE
    # =========================================================

    def remove_right_arm(self):

        if self.right_arm_removed:

            return

        self.right_arm_removed = True

        arm_image = pygame.image.load(

            "assets/sprites/monsters/"
            "zombie_basic/"
            "zombie_basic_right_arm.png"

        ).convert_alpha()

        body_part = BodyPart(

            self.game,

            self.rect.centerx,
            self.rect.centery,

            arm_image,

            random.uniform(-4, 4),
            random.uniform(-4, 4)
        )

        self.game.body_parts.append(
            body_part
        )

        # =====================================================
        # BLOOD EFFECT
        # =====================================================

        for _ in range(12):
            blood = BloodParticle(

                self.game,

                self.rect.centerx,
                self.rect.centery,

                random.uniform(-4, 4),
                random.uniform(-4, 4)

            )

            self.game.blood_particles.append(
                blood
            )

        blood_decal = BloodDecal(

            self.game,

            self.rect.centerx,
            self.rect.centery

        )

        self.game.blood_decals.append(
            blood_decal
        )

        print("ARM REMOVED")
        print(len(self.game.body_parts))
        print(len(self.game.blood_particles))

    # =========================================================
    # AI STATE
    # =========================================================

    def update_state(self, player):

        distance = self.get_distance_to_player(
            player
        )

        if distance < 40:

            self.state = "ATTACK"

        elif distance < 250:

            self.state = "CHASE"

        else:

            self.state = "IDLE"

    # =========================================================
    # UPDATE
    # =========================================================

    def update(self, player):

        # =====================================================
        # HIT STATE UPDATE
        # =====================================================

        if self.state == "HIT":

            self.hit_timer -= 1

            if self.hit_timer <= 0:

                self.state = "IDLE"

            return

        # =====================================================
        # AI STATE UPDATE
        # =====================================================

        self.update_state(player)

        # =====================================================
        # ATTACK STATE
        # =====================================================

        if self.state == "ATTACK":

            self.attack_player(player)

        # =====================================================
        # MOVE TOWARDS PLAYER
        # =====================================================

        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery

        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance != 0:
            dx /= distance
            dy /= distance

        move_x = 0
        move_y = 0

        if self.state == "CHASE":
            move_x = dx * self.speed
            move_y = dy * self.speed

        # =====================================================
        # X COLLISION
        # =====================================================

        self.rect.x += move_x

        for rect in self.game.collision_rects:

            if self.rect.colliderect(rect):

                if move_x > 0:
                    self.rect.right = rect.left

                elif move_x < 0:
                    self.rect.left = rect.right

        # =====================================================
        # Y COLLISION
        # =====================================================

        self.rect.y += move_y

        for rect in self.game.collision_rects:

            if self.rect.colliderect(rect):

                if move_y > 0:
                    self.rect.bottom = rect.top

                elif move_y < 0:
                    self.rect.top = rect.bottom

        # =====================================================
        # ANIMATION UPDATE
        # =====================================================

        self.frame_index += self.animation_speed

        if self.frame_index >= len(self.frames):
            self.frame_index = 0

    # =========================================================
    # DRAW
    # =========================================================

    def draw(self, surface, camera):

        # =====================================================
        # ENEMY SPRITE
        # =====================================================

        rect = camera.apply(self.rect)

        frame = self.frames[int(self.frame_index)]

        frame_rect = frame.get_rect(center=rect.center)

        surface.blit(frame, frame_rect)

        # =====================================================
        # HP BAR
        # =====================================================

        bar_width = 32
        bar_height = 6

        bar_x = rect.x
        bar_y = rect.y - 14

        hp_ratio = self.hp / self.max_hp
        current_width = bar_width * hp_ratio

        # outline
        pygame.draw.rect(
            surface,
            (0, 0, 0),
            (bar_x - 1, bar_y - 1, bar_width + 2, bar_height + 2),
            border_radius=3
        )

        # background
        pygame.draw.rect(
            surface,
            (60, 60, 60),
            (bar_x, bar_y, bar_width, bar_height),
            border_radius=3
        )

        # hp
        pygame.draw.rect(
            surface,
            (50, 220, 50),
            (bar_x, bar_y, current_width, bar_height),
            border_radius=3
        )

    # =========================================================
    # DAMAGE
    # =========================================================

    def take_damage(self, amount):

        self.hp -= amount

        self.hp = max(0, self.hp)

        print("HIT!", self.hp)

        if self.hp <= 0:
            self.alive = False