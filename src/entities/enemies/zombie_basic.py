import pygame
import random

from src.entities.body_part import BodyPart
from src.entities.enemies.base_enemy import BaseEnemy
from src.systems.asset_system import AssetManager


class ZombieBase(BaseEnemy):

    # =========================================================
    # SHARED ASSETS
    # =========================================================

    SPRITE_SHEET = None

    FRAMES = []

    NO_ARM_FRAMES = []

    RIGHT_ARM = None

    # =========================================================
    # INIT
    # =========================================================

    def __init__(self, game, x, y):

        super().__init__(game, x, y)

        # =====================================================
        # STATS
        # =====================================================

        self.speed = 1

        self.contact_damage = 10

        self.max_hp = 100

        self.hp = self.max_hp

        # =====================================================
        # GORE
        # =====================================================

        self.right_arm_removed = False

        # =====================================================
        # LOAD SPRITES
        # =====================================================

        if ZombieBase.SPRITE_SHEET is None:

            ZombieBase.SPRITE_SHEET = AssetManager.load_image(
                "assets/sprites/monsters/"
                "zombie_basic/"
                "zombie_basic_idle.png"
            )

        if ZombieBase.RIGHT_ARM is None:

            ZombieBase.RIGHT_ARM = AssetManager.load_image(
                "assets/sprites/monsters/"
                "zombie_basic/"
                "zombie_basic_right_arm.png"
            )

        # =====================================================
        # ANIMATION
        # =====================================================

        self.frame_index = 0

        self.animation_speed = 0.15

        if not ZombieBase.FRAMES:

            frame_width = 96
            frame_height = 96

            # =================================================
            # NORMAL FRAMES
            # =================================================

            for i in range(8):

                frame = ZombieBase.SPRITE_SHEET.subsurface(

                    (
                        i * frame_width,
                        0,
                        frame_width,
                        frame_height
                    )
                )

                frame = pygame.transform.scale(
                    frame,
                    (48, 48)
                )

                ZombieBase.FRAMES.append(frame)

            # =================================================
            # NO ARM FRAMES
            # =================================================

            no_arm_sheet = AssetManager.load_image(
                "assets/sprites/monsters/"
                "zombie_basic/"
                "zombie_basic_idle_no_arm.png"
            )

            for i in range(8):

                no_arm_frame = no_arm_sheet.subsurface(

                    (
                        i * frame_width,
                        0,
                        frame_width,
                        frame_height
                    )
                )

                no_arm_frame = pygame.transform.scale(
                    no_arm_frame,
                    (48, 48)
                )

                ZombieBase.NO_ARM_FRAMES.append(
                    no_arm_frame
                )

        self.frames = ZombieBase.FRAMES

        self.image = self.frames[0]

        self.rect = self.image.get_rect(
            center=(x, y)
        )

    # =========================================================
    # GORE
    # =========================================================

    def remove_right_arm(self):

        if self.right_arm_removed:

            return

        self.right_arm_removed = True

        # =====================================================
        # SPAWN FLYING ARM
        # =====================================================

        body_part = BodyPart(

            self.game,

            self.rect.centerx,
            self.rect.centery,

            ZombieBase.RIGHT_ARM,

            random.uniform(-4, 4),
            random.uniform(-4, 4)
        )

        self.game.body_parts.append(
            body_part
        )

        # =====================================================
        # CHANGE ANIMATION
        # =====================================================

        self.frames = ZombieBase.NO_ARM_FRAMES

    # =========================================================
    # UPDATE
    # =========================================================

    def update(self, player):

        super().update(player)

        # =====================================================
        # ANIMATION UPDATE
        # =====================================================

        self.frame_index += self.animation_speed

        if self.frame_index >= len(self.frames):

            self.frame_index = 0

        self.image = self.frames[
            int(self.frame_index)
        ]