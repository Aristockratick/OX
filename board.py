# board.py

from constants import GRID_SIZE

class Board:
    def __init__(self):
        self.reset()

    def reset(self):
        """Очистка игрового поля"""
        self.grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    def is_cell_empty(self, row, col):
        """Проверка, пуста ли клетка"""
        return self.grid[row][col] is None

    def place_symbol(self, row, col, symbol):
        """Установка символа в клетку"""
        if self.is_cell_empty(row, col):
            self.grid[row][col] = symbol
            return True
        return False

    def check_win(self, symbol):
        """Проверка победы"""
        # Горизонтали
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE - 4):
                if all(self.grid[r][c+i] == symbol for i in range(5)):
                    return [(r, c+i) for i in range(5)]
        
        # Вертикали
        for c in range(GRID_SIZE):
            for r in range(GRID_SIZE - 4):
                if all(self.grid[r+i][c] == symbol for i in range(5)):
                    return [(r+i, c) for i in range(5)]
        
        # Диагональ (слева направо)
        for r in range(GRID_SIZE - 4):
            for c in range(GRID_SIZE - 4):
                if all(self.grid[r+i][c+i] == symbol for i in range(5)):
                    return [(r+i, c+i) for i in range(5)]

        # Диагональ (справа налево)
        for r in range(GRID_SIZE - 4):
            for c in range(4, GRID_SIZE):
                if all(self.grid[r+i][c-i] == symbol for i in range(5)):
                    return [(r+i, c-i) for i in range(5)]
        
        return None

    def is_full(self):
        """Проверка на заполненность поля"""
        return all(cell is not None for row in self.grid for cell in row)

    def get_cell_from_pos(self, pos, margin, cell_size):
        """Преобразование координат мыши в координаты сетки"""
        x, y = pos
        if margin <= x <= margin + GRID_SIZE * cell_size and \
           margin <= y <= margin + GRID_SIZE * cell_size:
            col = (x - margin) // cell_size
            row = (y - margin) // cell_size
            return row, col
        return None, None