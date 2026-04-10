import pygame
from src.UI.button import Button

class Menu:

    def __init__(self, screen):

        self.screen = screen

        self.font_title = pygame.font.SysFont(None, 80)
        self.font_item = pygame.font.SysFont(None, 50)

        self.items = [
            "New Game",
            "Character",
            "Load Game",
            "Save Game",
            "Options",
            "Quit"
        ]

        self.item_rects = []

        self.selected_index = 0

        screen_height = screen.get_height()
        self.start_y = screen_height // 2 - 150

        self.spacing = 60

    def draw(self):

        self.screen.fill((20, 20, 20))

        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        title = self.font_title.render("TORNI 1", True, (255, 255, 255))
        title_rect = title.get_rect(center=(screen_width // 2, 150))
        self.screen.blit(title, title_rect)

        self.item_rects = []

        mouse_pos = pygame.mouse.get_pos()

        start_y = screen_height // 2 - 120
        spacing = 60

        for i, item in enumerate(self.items):

            y = start_y + i * spacing

            rect = self.font_item.render(item, True, (255, 255, 255)).get_rect(center=(screen_width // 2, y))

            if rect.collidepoint(mouse_pos):
                self.selected_index = i

            if i == self.selected_index:
                text = self.font_item.render(item, True, (255, 0, 0))
            else:
                text = self.font_item.render(item, True, (255, 255, 255))

            rect = text.get_rect(center=(screen_width // 2, y))

            self.item_rects.append(rect)

            self.screen.blit(text, rect)

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.items)

            elif event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.items)

            elif event.key == pygame.K_RETURN:
                return self.items[self.selected_index]

        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse_pos = pygame.mouse.get_pos()

            for i, rect in enumerate(self.item_rects):

                if rect.collidepoint(mouse_pos):
                    return self.items[i]

        return None