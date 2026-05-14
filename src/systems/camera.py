import pygame

from src import asetukset


class Camera:

    # =========================================================
    # INIT
    # =========================================================

    def __init__(self, width, height):

        self.camera = pygame.Rect(0, 0, width, height)

    # =========================================================
    # APPLY
    # =========================================================

    def apply(self, rect):

        return rect.move(self.camera.topleft)

    # =========================================================
    # UPDATE
    # =========================================================

    def update(self, target):

        x = (
            -target.rect.x
            + asetukset.RENDER_WIDTH // 2
            - target.rect.width // 2
        )

        y = (
            -target.rect.y
            + asetukset.RENDER_HEIGHT // 2
            - target.rect.height // 2
        )

        self.camera = pygame.Rect(
            x,
            y,
            self.camera.width,
            self.camera.height
        )

# =========================================================
# CAMERA SYSTEM
# =========================================================

class CameraSystem:

    # =====================================================
    # UPDATE
    # =====================================================

    @staticmethod
    def update(game):

        game.camera.update(
            game.player
        )