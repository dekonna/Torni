import pygame


class BloodDecal:

    def __init__(self, game, x, y):

        self.game = game

        self.x = x
        self.y = y

        self.radius = 12

        self.timer = 600

    def update(self):

        pass

    def draw(self):

        pygame.draw.circle(

            self.game.game_surface,

            (255, 0, 0),

            (
                int(self.x - self.game.camera.camera.x),
                int(self.y - self.game.camera.camera.y)
            ),

            self.radius
        )