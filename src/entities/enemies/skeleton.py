import pygame

from src.entities.enemies.base_enemy import BaseEnemy
from src.systems.asset_system import AssetManager


class Skeleton(BaseEnemy):

    # =========================================================
    # SHARED ASSETS
    # =========================================================

    SPRITE_SHEET = None

    FRAMES = []

    # =========================================================
    # INIT
    # =========================================================

    def __init__(self, game, x, y):

        super().__init__(game, x, y)

        # =====================================================
        # STATS
        # =====================================================

        self.speed = 1
        self.contact_damage = 15
        self.max_hp = 50
        self.hp = self.max_hp

        # =====================================================
        # LOAD SPRITES
        # =====================================================

        if Skeleton.SPRITE_SHEET is None:

            Skeleton.SPRITE_SHEET = AssetManager.load_image(
                "assets/sprites/monsters/skeleton/skeleton_o1.png"
            )

        # =====================================================
        # ANIMATION
        # =====================================================

        self.frame_index = 0

        self.animation_speed = 0.2

        if not Skeleton.FRAMES:

            frame_width = 32
            frame_height = 32

            for i in range(4):

                frame = Skeleton.SPRITE_SHEET.subsurface(
                    (0, i * frame_height, frame_width, frame_height)
                )

                frame = pygame.transform.scale(frame, (32, 32))

                Skeleton.FRAMES.append(frame)

        self.frames = Skeleton.FRAMES