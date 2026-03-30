# ui.py

import pygame
from constants import (
    WIDTH, HEIGHT, MARGIN, CELL_SIZE, GRID_SIZE,
    LINE_COLOR, X_COLOR, O_COLOR, WIN_COLOR, TEXT_COLOR,
    FONT_NAME, FONT_SIZE, BIG_FONT_SIZE,
    UI_TITLE_Y, UI_MODE_Y, UI_STATUS_Y, UI_SCORE_Y, UI_BUTTONS_Y,
    MODE_BUTTON_COLOR
)

class UI:
    def __init__(self):
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE, bold=True)
        self.big_font = pygame.font.SysFont(FONT_NAME, BIG_FONT_SIZE, bold=True)

    def draw_grid(self, surface, board, winning_line=None):
        grid_bottom = UI_STATUS_Y - 50
        
        for i in range(1, GRID_SIZE):
            x = MARGIN + i * CELL_SIZE
            y = MARGIN + i * CELL_SIZE
            pygame.draw.line(surface, LINE_COLOR, (x, MARGIN), (x, grid_bottom), 3)
            pygame.draw.line(surface, LINE_COLOR, (MARGIN, y), (WIDTH - MARGIN, y), 3)

        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                symbol = board.grid[r][c]
                if symbol:
                    x = MARGIN + c * CELL_SIZE + CELL_SIZE // 2
                    y = MARGIN + r * CELL_SIZE + CELL_SIZE // 2
                    color = X_COLOR if symbol == 'X' else O_COLOR
                    
                    if symbol == 'X':
                        offset = 20
                        pygame.draw.line(surface, color, (x - offset, y - offset), (x + offset, y + offset), 5)
                        pygame.draw.line(surface, color, (x + offset, y - offset), (x - offset, y + offset), 5)
                    else:
                        pygame.draw.circle(surface, color, (x, y), 30, 5)

        if winning_line:
            for r, c in winning_line:
                rect = pygame.Rect(MARGIN + c * CELL_SIZE + 5, MARGIN + r * CELL_SIZE + 5, CELL_SIZE - 10, CELL_SIZE - 10)
                pygame.draw.rect(surface, WIN_COLOR, rect, 5)

    def draw_info(self, surface, current_player, selected_symbol, game_over, winner, scores, vs_bot=False, bot_turn=False):
        title = self.big_font.render("Свобода Выбора (5x5)", True, TEXT_COLOR)
        surface.blit(title, (WIDTH//2 - title.get_width()//2, UI_TITLE_Y))

        mode_text = "Игрок против Бота" if vs_bot else "Игрок против Игрока"
        mode_surf = self.font.render(mode_text, True, MODE_BUTTON_COLOR)
        surface.blit(mode_surf, (WIDTH//2 - mode_surf.get_width()//2, UI_MODE_Y))

        if not game_over:
            if vs_bot and bot_turn:
                status = "Бот думает..."
                color = (142, 68, 173)
            else:
                status = f"Ход Игрока {current_player}"
                color = X_COLOR if current_player == 1 else O_COLOR
            if selected_symbol is None and not (vs_bot and bot_turn):
                status += " (Выберите символ!)"
        else:
            if winner:
                if vs_bot and winner == 2:
                    status = "Бот победил!"
                else:
                    status = f"Победил Игрок {winner}!"
                color = WIN_COLOR
            else:
                status = "Ничья!"
                color = TEXT_COLOR
        
        status_surf = self.font.render(status, True, color)
        surface.blit(status_surf, (WIDTH//2 - status_surf.get_width()//2, UI_STATUS_Y))

        if vs_bot:
            score_text = f"Вы ({scores[1]}) : Бот ({scores[2]})"
        else:
            score_text = f"Игрок 1 ({scores[1]}) : Игрок 2 ({scores[2]})"
        score_surf = self.font.render(score_text, True, TEXT_COLOR)
        surface.blit(score_surf, (WIDTH//2 - score_surf.get_width()//2, UI_SCORE_Y))