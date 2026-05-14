import pygame


class WeaponPickup:
    def __init__(self, x, y, weapon, image):
        self.rect   = pygame.Rect(x, y, 32, 32)
        self.weapon = weapon
        self.image  = image

        # Varakuva aseille joilla ei ole spritea
        if self.image is None:
            self.image = pygame.Surface((24, 24), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (180, 180, 60), (0, 0, 24, 24), border_radius=4)
            pygame.draw.rect(self.image, (220, 220, 100), (0, 0, 24, 24), 2, border_radius=4)


    def draw(self, surface, camera):
        surface.blit(self.image, camera.apply(self.rect))