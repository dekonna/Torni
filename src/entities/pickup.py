import pygame


class WeaponPickup:
    def __init__(self, x, y, weapon, image):
        self.rect = pygame.Rect(x, y, 32, 32)
        self.weapon = weapon
        self.image = image

    def draw(self, surface, camera):
        surface.blit(self.image, camera.apply(self.rect))