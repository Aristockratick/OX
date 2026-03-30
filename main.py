# main.py

import pygame
import sys
from game import Game
from constants import WIDTH, HEIGHT, BG_COLOR

def main():
    print("Инициализация Pygame...")
    pygame.init()
    print("Создание окна...")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Крестики-Нолики 5x5: Свобода Выбора")
    clock = pygame.time.Clock()

    print("Создание игры...")
    game = Game()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_event(event)

        screen.fill(BG_COLOR)
        game.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    print("Завершение работы...")
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()