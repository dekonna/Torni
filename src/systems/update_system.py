from src.systems.combat_system import CombatSystem
from src.systems.ui_system import UISystem
from src.systems.world_logic import WorldSystem
from src.systems.camera import CameraSystem
import pygame
from src import asetukset


class UpdateSystem:

    # =========================================================
    # UPDATE PIPELINE
    # =========================================================

    @staticmethod
    def update(game):

        # =====================================================
        # PLAYER UPDATE
        # =====================================================

        UpdateSystem.update_player(game)

        # =====================================================
        # DAMAGE COOLDOWN
        # =====================================================

        CombatSystem.update_damage_cooldown(game)

        # =====================================================
        # COMBAT UPDATE
        # =====================================================

        CombatSystem.update(game)

        # =====================================================
        # MESSAGE TIMER
        # =====================================================

        UISystem.update_messages(game)

        # =====================================================
        # PLAYER DEATH
        # =====================================================

        CombatSystem.check_player_death(game)

        # =====================================================
        # MAP BOUNDS
        # =====================================================

        WorldSystem.clamp_player_to_map(game)

        # =====================================================
        # BODY PARTS
        # =====================================================

        for body_part in game.body_parts[:]:

            body_part.update()

            if body_part.timer <= 0:
                game.body_parts.remove(body_part)

        # =====================================================
        # BLOOD PARTICLES
        # =====================================================

        for particle in game.blood_particles[:]:

            particle.update()

            if particle.timer <= 0:
                game.blood_particles.remove(particle)

        # =====================================================
        # BLOOD DECALS
        # =====================================================

        for decal in game.blood_decals[:]:

            decal.update()

            if decal.timer <= 0:
                game.blood_decals.remove(decal)

        # =====================================================
        # CAMERA UPDATE
        # =====================================================

        CameraSystem.update(game)

    # =========================================================
    # PLAYER UPDATE
    # =========================================================

    @staticmethod
    def update_player(game):

        mouse_x, mouse_y = pygame.mouse.get_pos()

        mouse_x = (
            asetukset.SCREEN_WIDTH // 2
            - mouse_x
        )

        mouse_y = (
            asetukset.SCREEN_HEIGHT // 2
            - mouse_y
        )

        game.player.update(
            mouse_x,
            mouse_y
        )