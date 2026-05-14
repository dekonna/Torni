import pygame


class BloodParticle:

    def __init__(
        self,
        game,
        x,
        y,
        velocity_x,
        velocity_y
    ):

        self.game = game

        self.x = x
        self.y = y

        self.velocity_x = velocity_x
        self.velocity_y = velocity_y

        self.radius = 6

        self.timer = 40

    def update(self):

        self.x += self.velocity_x
        self.y += self.velocity_y

        self.velocity_x *= 0.92
        self.velocity_y *= 0.92

        self.timer -= 1

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