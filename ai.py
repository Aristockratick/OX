import random
from constants import GRID_SIZE

class AI:
    """Искусственный интеллект для игры в крестики-нолики"""
    
    def __init__(self, difficulty='medium'):
        self.difficulty = difficulty
        self.symbol = None
        self.player_symbol = None
    
    def set_symbols(self, ai_symbol, player_symbol):
        """Установка символов для бота и игрока"""
        self.symbol = ai_symbol
        self.player_symbol = player_symbol
    
    def get_move(self, board):
        """
        Получение хода от ИИ.
        Возвращает кортеж (row, col, symbol)
        """
        # 1. Попытка выиграть
        win_move = self._find_winning_move(board, self.symbol)
        if win_move:
            return win_move
        
        # 2. Блокировка игрока
        block_move = self._find_winning_move(board, self.player_symbol)
        if block_move:
            return block_move
        
        # 3. Создание угрозы (2 в ряд)
        threat_move = self._find_threat_move(board, self.symbol)
        if threat_move:
            return threat_move
        
        # 4. Блокировка угрозы игрока
        block_threat = self._find_threat_move(board, self.player_symbol)
        if block_threat:
            return block_threat
        
        # 5. Занять центр
        center = GRID_SIZE // 2
        if board.is_cell_empty(center, center):
            symbol = self._choose_symbol(board, center, center)
            return (center, center, symbol)
        
        # 6. Случайный ход
        empty_cells = []
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if board.is_cell_empty(r, c):
                    empty_cells.append((r, c))
        
        if empty_cells:
            row, col = random.choice(empty_cells)
            symbol = self._choose_symbol(board, row, col)
            return (row, col, symbol)
        
        return None
    
    def _find_winning_move(self, board, symbol):
        """Поиск хода, который приведёт к победе"""
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if board.is_cell_empty(r, c):
                    # Проверяем, сколько уже есть символов в линиях через эту клетку
                    if self._count_in_line(board, r, c, symbol) >= 4:
                        return (r, c, symbol)
        return None
    
    def _find_threat_move(self, board, symbol):
        """Поиск хода для создания угрозы (3-4 в ряд)"""
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if board.is_cell_empty(r, c):
                    if self._count_in_line(board, r, c, symbol) >= 3:
                        return (r, c, symbol)
        return None
    
    def _count_in_line(self, board, row, col, symbol):
        """Подсчёт количества символов в линиях через указанную клетку"""
        max_count = 0
        
        # Горизонталь
        count = 1
        for c in range(col - 1, -1, -1):
            if board.grid[row][c] == symbol:
                count += 1
            else:
                break
        for c in range(col + 1, GRID_SIZE):
            if board.grid[row][c] == symbol:
                count += 1
            else:
                break
        max_count = max(max_count, count)
        
        # Вертикаль
        count = 1
        for r in range(row - 1, -1, -1):
            if board.grid[r][col] == symbol:
                count += 1
            else:
                break
        for r in range(row + 1, GRID_SIZE):
            if board.grid[r][col] == symbol:
                count += 1
            else:
                break
        max_count = max(max_count, count)
        
        # Диагональ (слева направо)
        count = 1
        for i in range(1, GRID_SIZE):
            r, c = row - i, col - i
            if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and board.grid[r][c] == symbol:
                count += 1
            else:
                break
        for i in range(1, GRID_SIZE):
            r, c = row + i, col + i
            if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and board.grid[r][c] == symbol:
                count += 1
            else:
                break
        max_count = max(max_count, count)
        
        # Диагональ (справа налево)
        count = 1
        for i in range(1, GRID_SIZE):
            r, c = row - i, col + i
            if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and board.grid[r][c] == symbol:
                count += 1
            else:
                break
        for i in range(1, GRID_SIZE):
            r, c = row + i, col - i
            if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and board.grid[r][c] == symbol:
                count += 1
            else:
                break
        max_count = max(max_count, count)
        
        return max_count
    
    def _choose_symbol(self, board, row, col):
        """Выбор символа для хода"""
        # Приоритет: символ, который уже есть в линии
        for symbol in [self.symbol, self.player_symbol]:
            if self._count_in_line(board, row, col, symbol) >= 2:
                return symbol
        
        # Иначе случайный выбор
        return random.choice([self.symbol, self.player_symbol])