from src.entities.enemies.zombie_basic import ZombieBase

class CombatSystem:

    # =========================================================
    # UPDATE
    # =========================================================

    @staticmethod
    def update(game):

        CombatSystem.update_enemy_collisions(game)
        CombatSystem.update_bullets(game)

    # =========================================================
    # PLAYER DEATH
    # =========================================================

    @staticmethod
    def check_player_death(game):

        if game.player.hp <= 0:

            print("KUOLEMA TRIGGER")

            game.state = "GAME_OVER"

    # =========================================================
    # ENEMY COLLISIONS
    # =========================================================

    @staticmethod
    def update_enemy_collisions(game):

        for enemy in game.enemies[:]:

            enemy.update(game.player)

            # player vs enemy kontaktivahinko
            if game.player.rect.colliderect(enemy.rect):

                if game.player.damage_cooldown == 0:

                    game.player.hp -= enemy.contact_damage

                    game.player.damage_cooldown = (
                        game.asetukset.PLAYER_DAMAGE_COOLDOWN
                    )

            # poista kuollut enemy
            if not enemy.alive:

                game.enemies.remove(enemy)

    # =========================================================
    # BULLETS
    # =========================================================

    @staticmethod
    def update_bullets(game):

        # =====================================================
        # MOVE BULLETS
        # =====================================================

        for bullet in game.player.bullets:

            bullet.update(game.map_width, game.map_height)

        # =====================================================
        # BULLET VS WALL
        # =====================================================

        for bullet in game.player.bullets[:]:

            for rect in game.collision_rects:

                if bullet.rect.colliderect(rect):

                    bullet.alive = False
                    break

        # =====================================================
        # BULLET VS ENEMY
        # =====================================================

        for enemy in game.enemies[:]:

            for bullet in game.player.bullets[:]:

                if bullet.rect.colliderect(enemy.rect):

                    enemy.take_damage(bullet.damage)

                    enemy.enter_hit_state()

                    # vain zombit voivat menettää käden
                    if hasattr(enemy, "remove_right_arm"):
                        enemy.remove_right_arm()

                    bullet.alive = False

                    if enemy.hp <= 0:
                        enemy.alive = False

                    break

        # =====================================================
        # CLEANUP
        # =====================================================

        game.player.bullets = [
            b for b in game.player.bullets
            if b.alive
        ]

    # =========================================================
    # DAMAGE COOLDOWN
    # =========================================================

    @staticmethod
    def update_damage_cooldown(game):

        if game.player.damage_cooldown > 0:

            game.player.damage_cooldown -= 1