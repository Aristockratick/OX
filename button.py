# button.py

import pygame
from constants import FONT_NAME, FONT_SIZE

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.action = action
        self.is_pressed = False
        self.is_toggle = False  # Для кнопок-переключателей
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE, bold=True)

    def draw(self, surface):
        """Отрисовка кнопки"""
        mouse_pos = pygame.mouse.get_pos()
        self.current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        
        if self.is_pressed:
            color = (80, 80, 80)
        elif self.is_toggle:
            color = (100, 200, 100)  # Зелёный для активной кнопки режима
        else:
            color = self.current_color
            
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)

        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        """Обработка нажатия"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()
                return True
        return False
    
    def set_toggle(self, value):
        """Установка состояния переключателя"""
        self.is_toggle = value