import os
import pygame

from pytmx.util_pygame import load_pygame
from src.entities.enemies.skeleton import Skeleton


class WorldSystem:

    # =========================================================
    # LOAD MAP
    # =========================================================

    @staticmethod
    def load_map(game, map_name):

        game.collision_rects = []

        base_path = os.path.dirname(
            os.path.dirname(
                os.path.dirname(__file__)
            )
        )

        map_path = os.path.join(
            base_path,
            "maps",
            map_name
        )

        game.map = load_pygame(map_path)

        game.map_width = (
            game.map.width
            * game.map.tilewidth
        )

        game.map_height = (
            game.map.height
            * game.map.tileheight
        )

        game.player_spawn = (100, 100)
        game.exit_rect = None
        game.enemy_spawns = []

        # =====================================================
        # OBJECT LAYERS
        # =====================================================

        for layer in game.map.objectgroups:

            # =================================================
            # COLLISIONS
            # =================================================

            if layer.name == "Collisions":

                for obj in layer:

                    game.collision_rects.append(
                        pygame.Rect(
                            obj.x,
                            obj.y,
                            obj.width,
                            obj.height
                        )
                    )

            # =================================================
            # OTHER OBJECTS
            # =================================================

            else:

                for obj in layer:

                    # PLAYER SPAWN
                    if obj.name == "PlayerSpawn":

                        game.player_spawn = (
                            obj.x,
                            obj.y
                        )

                    # EXIT
                    elif obj.name == "Exit":

                        game.exit_rect = pygame.Rect(
                            obj.x,
                            obj.y,
                            obj.width,
                            obj.height
                        )

                    # ENEMY SPAWN
                    elif obj.name == "EnemySpawn":

                        game.enemy_spawns.append(
                            (obj.x, obj.y)
                        )
        # =====================================================
        # ENEMIES
        # =====================================================

        game.enemies = []

        for x, y in game.enemy_spawns:

            game.enemies.append(
                Skeleton(game, x, y)
            )

    # =========================================================
    # NEXT FLOOR
    # =========================================================

    @staticmethod
    def next_floor(game):

        game.current_floor += 1

        next_map = game.floor_maps[
            game.current_floor
        ]

        WorldSystem.load_map(
            game,
            next_map
        )

    # =========================================================
    # MAP BOUNDS
    # =========================================================

    @staticmethod
    def clamp_player_to_map(game):

        game.player.rect.x = max(
            0,
            min(
                game.player.rect.x,
                game.map_width
                - game.player.rect.width
            )
        )

        game.player.rect.y = max(
            0,
            min(
                game.player.rect.y,
                game.map_height
                - game.player.rect.height
            )
        )