import pygame
from src.save_manager import SaveManager
from src.systems.world_logic import WorldSystem


class InputSystem:

    # =========================================================
    # GAME INPUT
    # =========================================================

    @staticmethod
    def handle_game_input(game, event):

        # =====================================================
        # MOUSE ATTACK
        # =====================================================

        if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
        ):

            if not game.inventory_open:
                game.player.attack()

        # =====================================================
        # KEYBOARD INPUT
        # =====================================================

        if event.type == pygame.KEYDOWN:

            # =================================================
            # INVENTORY TOGGLE
            # =================================================

            if event.key == pygame.K_i:
                game.inventory_open = (
                    not game.inventory_open
                )

            # =================================================
            # BLOCK GAMEPLAY INPUT
            # =================================================

            if game.inventory_open:
                return

            # =================================================
            # SPACE BAR ATTACK
            # =================================================

            if event.key == pygame.K_SPACE:

                game.player.attack()

            # =================================================
            # WEAPON SLOTS
            # =================================================

            elif event.key == pygame.K_1:

                game.player.current_slot = 0

            elif event.key == pygame.K_2:

                if len(game.player.weapon_slots) >= 1:
                    game.player.current_slot = 1

            elif event.key == pygame.K_3:

                if len(game.player.weapon_slots) >= 2:
                    game.player.current_slot = 2

            elif event.key == pygame.K_4:

                if len(game.player.weapon_slots) >= 3:
                    game.player.current_slot = 3

            # =================================================
            # PICKUP ITEMS
            # =================================================

            elif event.key == pygame.K_f:

                for pickup in game.pickups[:]:

                    if game.player.rect.colliderect(
                            pickup.rect
                    ):
                        game.player.add_weapon(
                            pickup.weapon
                        )

                        game.add_message(
                            f"Picked up {pickup.weapon.name}"
                        )

                        game.pickups.remove(pickup)

                        break

    # =========================================================
    # MENU INPUT
    # =========================================================

    @staticmethod
    def handle_menu_input(game, event):

        result = game.menu.handle_event(event)

        # =====================================================
        # NEW GAME
        # =====================================================

        if result == "New Game":

            game.reset_game()

            game.state = "GAME"

        # =====================================================
        # CONTINUE
        # =====================================================

        elif result == "Continue":

            game.load_game()

            game.state = "GAME"

        # =====================================================
        # SAVE GAME
        # =====================================================

        elif result == "Save Game":

            SaveManager.save(game)

            game.menu.refresh()

        # =====================================================
        # LOAD GAME
        # =====================================================

        elif result == "Load Game":

            game.load_game()

            game.state = "GAME"

        # =====================================================
        # CHARACTER
        # =====================================================

        elif result == "Character":

            game.state = "CHARACTER"

        # =====================================================
        # QUIT
        # =====================================================

        elif result == "Quit":

            game.running = False

    # =========================================================
    # GLOBAL INPUT
    # =========================================================

    @staticmethod
    def handle_global_input(game, event):

        # =====================================================
        # KEYBOARD INPUT
        # =====================================================

        if event.type == pygame.KEYDOWN:

            # =================================================
            # ESCAPE
            # =================================================

            if event.key == pygame.K_ESCAPE:

                if game.state == "GAME":

                    game.state = "MENU"

                elif game.state == "CHARACTER":

                    game.state = "MENU"

            # =================================================
            # RESTART
            # =================================================

            elif event.key == pygame.K_r:

                if game.state == "GAME_OVER":
                    game.reset_game()

                    game.state = "GAME"

            # =================================================
            # SAVE GAME
            # =================================================

            elif event.key == pygame.K_F5:

                SaveManager.save(game)

                game.add_message("Game Saved")

                game.menu.refresh()

            # =================================================
            # NEXT FLOOR
            # =================================================

            elif event.key == pygame.K_F6:

                WorldSystem.next_floor(game)

            # =================================================
            # DEBUG TOGGLE
            # =================================================

            elif event.key == pygame.K_F3:

                game.debug_mode = (
                    not game.debug_mode
                )