
import pygame
from board import Board
from button import Button
from ui import UI
from ai import AI
from constants import (
    WIDTH, HEIGHT, MARGIN, CELL_SIZE,
    X_COLOR, O_COLOR, BUTTON_COLOR, BUTTON_HOVER_COLOR,
    UI_BUTTONS_Y, UI_MODE_BUTTON_Y, MODE_BUTTON_COLOR, AI_THINK_DELAY,
    UI_RESET_SCORE_Y, X_HOVER_COLOR, O_HOVER_COLOR, MODE_BUTTON_HOVER_COLOR,
    RESET_BUTTON_COLOR, RESET_BUTTON_HOVER_COLOR, UI_BUTTON_X_X,
    UI_BUTTON_O_X, UI_BUTTON_RESTART_X, UI_BUTTON_RESTART_X, UI_RESET_SCORE_X,
    UI_MODE_BUTTON_X, UI_BUTTONS_WIDTH, UI_BUTTONS_HEIGHT,
    UI_BUTTON_RESTART_WIDTH, UI_BUTTON_MODE_WIDTH, UI_BUTTON_RESET_SCORE_WIDTH
)


class Game:
    def __init__(self):
        self.board = Board()
        self.ui = UI()
        self.current_player = 1
        self.scores = {1: 0, 2: 0}
        self.game_over = False
        self.winner = None
        self.winning_line = None
        self.selected_symbol = None

        # Режим игры
        self.vs_bot = False
        self.bot = AI(difficulty='medium')
        self.bot_turn = False
        self.bot_think_timer = 0
        self.bot_player = 2
        self.bot.set_symbols('X', 'O')

        # Кнопки
        self.btn_x = Button(UI_BUTTON_X_X, UI_BUTTONS_Y, UI_BUTTONS_WIDTH,
                            UI_BUTTONS_HEIGHT, "X", X_COLOR, X_HOVER_COLOR, self.select_x)
        self.btn_o = Button(UI_BUTTON_O_X, UI_BUTTONS_Y, UI_BUTTONS_WIDTH,
                            UI_BUTTONS_HEIGHT, "O", O_COLOR, O_HOVER_COLOR, self.select_o)
        self.btn_restart = Button(UI_BUTTON_RESTART_X, UI_BUTTONS_Y, UI_BUTTON_RESTART_WIDTH,
                                  UI_BUTTONS_HEIGHT, "Новая игра", BUTTON_COLOR, BUTTON_HOVER_COLOR, self.restart)
        self.btn_mode = Button(UI_MODE_BUTTON_X, UI_MODE_BUTTON_Y, UI_BUTTON_MODE_WIDTH, UI_BUTTONS_HEIGHT,
                               "Против Бота", MODE_BUTTON_COLOR, MODE_BUTTON_HOVER_COLOR, self.toggle_mode)
        self.btn_reset_score = Button(UI_RESET_SCORE_X, UI_RESET_SCORE_Y, UI_BUTTON_RESET_SCORE_WIDTH,
                                      UI_BUTTONS_HEIGHT, "Сброс счёта", RESET_BUTTON_COLOR, RESET_BUTTON_HOVER_COLOR, self.reset_score)

        self.reset_selection()

    def reset_selection(self):
        self.selected_symbol = None
        self.btn_x.is_pressed = False
        self.btn_o.is_pressed = False

    def reset_score(self):
        self.scores = {1: 0, 2: 0}
        self.restart()

    def select_x(self):
        if not self.game_over and not self.bot_turn:
            self.selected_symbol = 'X'
            self.btn_x.is_pressed = True
            self.btn_o.is_pressed = False

    def select_o(self):
        if not self.game_over and not self.bot_turn:
            self.selected_symbol = 'O'
            self.btn_o.is_pressed = True
            self.btn_x.is_pressed = False

    def toggle_mode(self):
        self.vs_bot = not self.vs_bot
        self.btn_mode.set_toggle(self.vs_bot)
        self.btn_mode.text = "Против Игрока" if self.vs_bot else "Против Бота"
        self.restart()
        if self.vs_bot:
            self.bot.set_symbols('X', 'O')

    def restart(self):
        self.board.reset()
        self.game_over = False
        self.winner = None
        self.winning_line = None
        self.current_player = 1
        self.bot_turn = False
        self.reset_selection()

    def handle_click(self, pos):
        if self.game_over or self.bot_turn:
            return
        if self.selected_symbol is None:
            return

        row, col = self.board.get_cell_from_pos(pos, MARGIN, CELL_SIZE)
        if row is not None and self.board.place_symbol(row, col, self.selected_symbol):
            line = self.board.check_win(self.selected_symbol)
            if line:
                self.game_over = True
                self.winner = self.current_player
                self.winning_line = line
                self.scores[self.current_player] += 1
            elif self.board.is_full():
                self.game_over = True
            else:
                self.current_player = 2 if self.current_player == 1 else 1
                self.reset_selection()
                if self.vs_bot and self.current_player == self.bot_player:
                    self.bot_turn = True
                    self.bot_think_timer = pygame.time.get_ticks()

    def bot_make_move(self):
        if not self.bot_turn or not self.vs_bot:
            return
        if pygame.time.get_ticks() - self.bot_think_timer < AI_THINK_DELAY:
            return

        move = self.bot.get_move(self.board)
        if move:
            row, col, symbol = move
            self.board.place_symbol(row, col, symbol)
            line = self.board.check_win(symbol)
            if line:
                self.game_over = True
                self.winner = self.current_player
                self.winning_line = line
                self.scores[self.current_player] += 1
            elif self.board.is_full():
                self.game_over = True
            else:
                self.current_player = 2 if self.current_player == 1 else 1
        self.bot_turn = False

    def draw(self, surface):
        self.ui.draw_grid(surface, self.board, self.winning_line)
        self.ui.draw_info(surface, self.current_player, self.selected_symbol,
                          self.game_over, self.winner, self.scores,
                          self.vs_bot, self.bot_turn)
        self.btn_x.draw(surface)
        self.btn_o.draw(surface)
        self.btn_restart.draw(surface)
        self.btn_mode.draw(surface)
        self.btn_reset_score.draw(surface)

    def handle_event(self, event):
        self.btn_x.handle_event(event)
        self.btn_o.handle_event(event)
        self.btn_restart.handle_event(event)
        self.btn_mode.handle_event(event)
        self.btn_reset_score.handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.handle_click(event.pos)
        if self.bot_turn:
            self.bot_make_move()
