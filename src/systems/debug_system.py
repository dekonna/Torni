import pygame


class DebugSystem:

    # =========================================================
    # DEBUG OVERLAY
    # =========================================================

    @staticmethod
    def draw(game):

        if not game.debug_mode:
            return

        lines = [

            f"FPS: {int(game.clock.get_fps())}",

            f"Enemies: {len(game.enemies)}",
            f"Pickups: {len(game.pickups)}",

            f"Player: {game.player.rect.x}, "
            f"{game.player.rect.y}",

            f"HP: {game.player.hp}",

            f"Weapon: "
            f"{game.player.current_weapon.name}",

            f"Inventory Size: "
            f"{len(game.player.inventory)}",

            f"Floor: {game.current_floor}",

            f"State: {game.state}",

            f"Camera: "
            f"{game.camera.camera.x}, "
            f"{game.camera.camera.y}",

            f"Inventory: "
            f"{'OPEN' if game.inventory_open else 'CLOSED'}",

            f"Damage Cooldown: "
            f"{game.player.damage_cooldown}",

            f"Collision Rects: "
            f"{len(game.collision_rects)}",
        ]

        mouse_x, mouse_y = pygame.mouse.get_pos()

        world_mouse_x = (
            mouse_x - game.camera.camera.x
        )

        world_mouse_y = (
            mouse_y - game.camera.camera.y
        )

        lines.append(
            f"Mouse World: "
            f"{world_mouse_x}, "
            f"{world_mouse_y}"
        )

        x = 10
        y = 10

        line_height = 18

        panel_width = 260

        panel_height = (
                               len(lines) * line_height
                       ) + 10

        pygame.draw.rect(

            game.screen,

            (0, 0, 0),

            (
                x - 5,
                y - 5,
                panel_width,
                panel_height
            )
        )

        for line in lines:
            text = game.font.render(

                line,

                True,

                (80, 220, 255)
            )

            game.screen.blit(

                text,

                (x, y)
            )

            y += line_height

            # =====================================================
            # HITBOX RENDERING
            # =====================================================

            DebugSystem.draw_hitboxes(game)

    # =========================================================
    # HITBOXES
    # =========================================================

    @staticmethod
    def draw_hitboxes(game):

        if not game.debug_mode:
            return

        # =====================================================
        # PLAYER HITBOX
        # =====================================================

        pygame.draw.rect(

            game.screen,

            (0, 255, 0),

            game.camera.apply(
                game.player.rect
            ),

            2
        )

        # =====================================================
        # ENEMY HITBOXES
        # =====================================================

        for enemy in game.enemies:

            pygame.draw.rect(

                game.screen,

                (255, 0, 0),

                game.camera.apply(
                    enemy.rect
                ),

                2
            )

            state_text = game.font.render(

                enemy.state,

                True,

                (255, 120, 120)
            )

            state_rect = state_text.get_rect(

                center=(

                    game.camera.apply(
                        enemy.rect
                    ).centerx,

                    game.camera.apply(
                        enemy.rect
                    ).top - 12
                )
            )

            game.screen.blit(

                state_text,

                state_rect
            )

        # =====================================================
        # COLLISION RECTS
        # =====================================================

        for rect in game.collision_rects:

            pygame.draw.rect(

                game.screen,

                (0, 120, 255),

                game.camera.apply(
                    rect
                ),

                2
            )