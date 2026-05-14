import pygame
from src import asetukset
from src.systems.debug_system import DebugSystem


class UISystem:

    # =========================================================
    # UI PIPELINE
    # =========================================================

    @staticmethod
    def draw(game):

        # =====================================================
        # CURSOR
        # =====================================================

        UISystem.draw_cursor(game)

        # =====================================================
        # PICKUP PROMPT
        # =====================================================

        UISystem.draw_pickup_prompt(game)

        # =====================================================
        # HP BAR
        # =====================================================

        UISystem.draw_hp_bar(game)

        # =====================================================
        # WEAPON UI
        # =====================================================

        UISystem.draw_weapon_ui(game)

        # =====================================================
        # MESSAGE BOX
        # =====================================================

        UISystem.draw_message_box(game)

        # =====================================================
        # INVENTORY
        # =====================================================

        if game.inventory_open:

            UISystem.draw_inventory(game)

        # =====================================================
        # DEBUG
        # =====================================================

        DebugSystem.draw(game)

    # =========================================================
    # CURSOR
    # =========================================================

    @staticmethod
    def draw_cursor(game):

        mouse_x, mouse_y = pygame.mouse.get_pos()

        pygame.draw.circle(

            game.game_surface,

            (255, 0, 0),

            (
                int(mouse_x),
                int(mouse_y)
            ),

            5
        )

    # =========================================================
    # INVENTORY
    # =========================================================

    @staticmethod
    def draw_inventory(game):

        overlay = pygame.Surface((
            asetukset.INVENTORY_WIDTH,
            asetukset.INVENTORY_HEIGHT
        ))

        overlay.set_alpha(asetukset.INVENTORY_ALPHA)

        overlay.fill((30, 30, 30))

        x = (
            asetukset.SCREEN_WIDTH // 2
            - asetukset.INVENTORY_WIDTH // 2
        )

        y = (
            asetukset.SCREEN_HEIGHT // 2
            - asetukset.INVENTORY_HEIGHT // 2
        )

        game.screen.blit(
            overlay,
            (x, y)
        )

        title = game.font_big.render(
            "INVENTORY",
            True,
            (255, 255, 255)
        )

        game.screen.blit(
            title,
            (x + 120, y + 20)
        )

        for i, weapon in enumerate(game.player.inventory):

            item_text = game.font.render(
                f"{i + 1}. {weapon.name}",
                True,
                (255, 255, 255)
            )

            game.screen.blit(
                item_text,
                (x + 40, y + 100 + i * 40)
            )

    # =========================================================
    # MESSAGE BOX
    # =========================================================

    @staticmethod
    def draw_message_box(game):

        if not game.messages or game.message_timer <= 0:
            return

        box_width = asetukset.MESSAGE_BOX_WIDTH
        box_height = asetukset.MESSAGE_BOX_HEIGHT

        x = (
            asetukset.RENDER_WIDTH // 2
            - box_width // 2
        )

        y = (
            asetukset.RENDER_HEIGHT
            - asetukset.MESSAGE_BOX_OFFSET_Y
        )

        pygame.draw.rect(
            game.game_surface,
            asetukset.MESSAGE_BOX_BG_COLOR,
            (x, y, box_width, box_height)
        )

        pygame.draw.rect(
            game.game_surface,
            (200, 200, 200),
            (x, y, box_width, box_height),
            2
        )

        text = game.font.render(
            game.messages[-1],
            True,
            (255, 255, 255)
        )

        game.game_surface.blit(
            text,
            (x + 20, y + 25)
        )

    # =========================================================
    # HP BAR
    # =========================================================

    @staticmethod
    def draw_hp_bar(game):

        pygame.draw.rect(
            game.screen,
            (255, 0, 0),
            (
                10,
                10,
                asetukset.PLAYER_HP_BAR_WIDTH,
                asetukset.PLAYER_HP_BAR_HEIGHT
            )
        )

        hp_width = (
                asetukset.PLAYER_HP_BAR_WIDTH
                * (game.player.hp / 100)
        )

        pygame.draw.rect(
            game.screen,
            (0, 255, 0),
            (
                10,
                10,
                hp_width,
                asetukset.PLAYER_HP_BAR_HEIGHT
            )
        )

        hp_text = game.font.render(
            f"HP: {game.player.hp}",
            True,
            (255, 255, 255)
        )

        game.screen.blit(
            hp_text,
            (220, 10)
        )

    # =========================================================
    # WEAPON UI
    # =========================================================

    @staticmethod
    def draw_weapon_ui(game):

        weapon = game.player.current_weapon

        weapon_text = game.font.render(

            f"Weapon: {weapon.name}",

            True,

            (255, 255, 255)
        )

        game.screen.blit(

            weapon_text,

            (10, 40)
        )

    # =========================================================
    # PICKUP PROMPT
    # =========================================================

    @staticmethod
    def draw_pickup_prompt(game):

        for pickup in game.pickups:

            if game.player.rect.colliderect(
                pickup.rect
            ):

                text = game.font.render(
                    f"Press F to pick up {pickup.weapon.name}",
                    True,
                    (255, 255, 255)
                )

                text_rect = text.get_rect(
                    center=(
                        asetukset.RENDER_WIDTH // 2,
                        asetukset.RENDER_HEIGHT - 30
                    )
                )

                game.game_surface.blit(
                    text,
                    text_rect
                )

                break

    # =========================================================
    # GAME OVER
    # =========================================================

    @staticmethod
    def draw_game_over(game):

        game.screen.fill((0, 0, 0))

        text = game.font_big.render(
            "GAME OVER",
            True,
            (255, 0, 0)
        )

        restart = game.font.render(
            "Press R to restart",
            True,
            (255, 255, 255)
        )

        text_rect = text.get_rect(
            center=(
                asetukset.SCREEN_WIDTH // 2,
                asetukset.SCREEN_HEIGHT // 2 - 30
            )
        )

        restart_rect = restart.get_rect(
            center=(
                asetukset.SCREEN_WIDTH // 2,
                asetukset.SCREEN_HEIGHT // 2 + 20
            )
        )

        game.screen.blit(
            text,
            text_rect
        )

        game.screen.blit(
            restart,
            restart_rect
        )

        # =========================================================
        # MESSAGE TIMER
        # =========================================================

    @staticmethod
    def update_messages(game):

        if game.message_timer > 0:
            game.message_timer -= 1