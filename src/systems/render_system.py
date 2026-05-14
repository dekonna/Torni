import pygame
from src import asetukset


class RenderSystem:

    # =========================================================
    # DRAW PIPELINE
    # =========================================================

    @staticmethod
    def draw(game):

        RenderSystem.draw_map(game)

        RenderSystem.draw_pickups(game)

        RenderSystem.draw_entities(game)

        RenderSystem.draw_body_parts(game)
        RenderSystem.draw_blood_particles(game)
        RenderSystem.draw_blood_decals(game)

        RenderSystem.scale_to_screen(game)

    # =========================================================
    # MAP RENDERING
    # =========================================================

    @staticmethod
    def draw_map(game):

        for layer in game.map.visible_layers:

            if hasattr(layer, "tiles"):

                for x, y, surf in layer.tiles():

                    rect = pygame.Rect(
                        x * asetukset.TILE_SIZE,
                        y * asetukset.TILE_SIZE,
                        asetukset.TILE_SIZE,
                        asetukset.TILE_SIZE
                    )

                    game.game_surface.blit(
                        surf,
                        game.camera.apply(rect)
                    )

    # =========================================================
    # ENTITY RENDERING
    # =========================================================

    @staticmethod
    def draw_entities(game):

        entities = [game.player] + game.enemies

        entities.sort(
            key=lambda entity: entity.rect.bottom
        )

        for entity in entities:

            entity.draw(
                game.game_surface,
                game.camera
            )

    # =========================================================
    # BODY PART RENDERING
    # =========================================================

    @staticmethod
    def draw_body_parts(game):

        for body_part in game.body_parts:
            body_part.draw()

    @staticmethod
    def draw_blood_particles(game):

        for particle in game.blood_particles:
            particle.draw()

    @staticmethod
    def draw_blood_decals(game):

        for decal in game.blood_decals:
            decal.draw()

    # =========================================================
    # PICKUP RENDERING
    # =========================================================

    @staticmethod
    def draw_pickups(game):

        for pickup in game.pickups:
            pickup.draw(
                game.game_surface,
                game.camera
            )

    # =========================================================
    # SCREEN SCALING
    # =========================================================

    @staticmethod
    def scale_to_screen(game):

        scaled_surface = pygame.transform.scale(
            game.game_surface,
            (
                asetukset.SCREEN_WIDTH,
                asetukset.SCREEN_HEIGHT
            )
        )

        scaled_width = asetukset.SCREEN_WIDTH

        scaled_height = int(
            asetukset.SCREEN_WIDTH
            * asetukset.RENDER_HEIGHT
            / asetukset.RENDER_WIDTH
        )

        scaled_surface = pygame.transform.scale(
            game.game_surface,
            (scaled_width, scaled_height)
        )

        offset_y = (
            asetukset.SCREEN_HEIGHT
            - scaled_height
        ) // 2

        game.screen.blit(
            scaled_surface,
            (0, offset_y)
        )

