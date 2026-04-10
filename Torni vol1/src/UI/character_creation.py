import pygame


class CharacterCreation:

    def __init__(self, screen):

        self.screen = screen
        self.font = pygame.font.SysFont(None, 60)

    def draw(self):

        self.screen.fill((30, 30, 30))

        title = self.font.render("Character Creation", True, (255,255,255))

        self.screen.blit(title, (420, 200))