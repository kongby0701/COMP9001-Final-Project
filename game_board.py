import random
from player import Player

class Cell:
    def __init__(self, position, type_, name="", price=0, rent=0):
        self.position = position
        self.type = type_  # 'start', 'jail', 'bank', 'property', 'chance', 'special', 'normal'
        self.name = name
        self.price = price
        self.rent = rent
        self.owner = None
        self.symbol = str(position) if type_ == 'normal' else self._get_symbol()

    def _get_symbol(self):
        if self.type == 'start':
            return '0'
        elif self.type == 'jail':
            return '&'
        elif self.type == 'bank':
            return '#'
        elif self.type == 'property':
            return '$'
        elif self.type == 'chance':
            return '?'
        elif self.type == 'special':
            return '!'
        return '.'

class GameBoard:
    def __init__(self, size=10):
        self.size = size
        self.board = []
        self.cells = []
        self.generate_board()

    def generate_board(self):
        self.board = [['.' for _ in range(self.size)] for _ in range(self.size)]

        self.board[0][self.size-1] = '0'
        self.cells.append(Cell(0, 'start', 'Go', 0, 0))

        self.board[self.size-1][0] = '&'
        self.cells.append(Cell(30, 'jail', 'Jail', 0, 0))

        self.board[self.size-1][self.size-1] = '#'
        self.board[0][0] = '#'
        self.cells.append(Cell(9, 'bank', 'Bank', 0, 0))
        self.cells.append(Cell(29, 'bank', 'Bank', 0, 0))

        position = 1
        for x in range(1, self.size-1):
            y = self.size - 1
            self.board[x][y] = str(position)
            self.cells.append(Cell(position, 'normal', f'Space {position}', 0, 0))
            position += 1

        for y in range(self.size-2, -1, -1):
            x = self.size - 1
            if self.board[x][y] == '.':
                self.board[x][y] = str(position)
                self.cells.append(Cell(position, 'normal', f'Space {position}', 0, 0))
                position += 1

        for x in range(self.size-2, -1, -1):
            y = 0
            if self.board[x][y] == '.':
                self.board[x][y] = str(position)
                self.cells.append(Cell(position, 'normal', f'Space {position}', 0, 0))
                position += 1

        for y in range(1, self.size-1):
            x = 0
            if self.board[x][y] == '.':
                self.board[x][y] = str(position)
                self.cells.append(Cell(position, 'normal', f'Space {position}', 0, 0))
                position += 1

        self.add_properties_and_events()

    def add_properties_and_events(self):
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x][y] != '.':
                    continue

                has_adjacent = False
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.size and 0 <= ny < self.size:
                        if self.board[nx][ny].isdigit():
                            has_adjacent = True
                            break

                if has_adjacent:
                    rand = random.random()
                    if rand < 0.4:
                        self.board[x][y] = '$'
                        self.cells.append(Cell(len(self.cells), 'property', f'Property {len(self.cells)}',
                                               price=random.randint(100, 500), rent=random.randint(10, 100)))
                    elif rand < 0.6:
                        self.board[x][y] = '?'
                        self.cells.append(Cell(len(self.cells), 'chance', 'Chance', 0, 0))
                    elif rand < 0.7:
                        self.board[x][y] = '!'
                        self.cells.append(Cell(len(self.cells), 'special', 'Special', 0, 0))

    def display_board(self, players):
        cell_width = 3
        border = "+" + "-" * (self.size * cell_width + 1) + "+"

        print("\n" + border)
        for y in range(self.size-1, -1, -1):
            row = "|"
            for x in range(self.size):
                cell = self.board[x][y]
                player_here = None
                for p in players:
                    pos = p.position
                    if self._position_to_coords(pos) == (x, y):
                        player_here = p.symbol
                        break

                display = player_here if player_here else cell
                row += display.center(cell_width)
            row += "|"
            print(row)
        print(border)

    def _position_to_coords(self, position):
        size = self.size
        if position == 0:
            return (0, size-1)

        if 1 <= position <= size-2:
            return (position, size-1)

        if size-1 <= position <= 2*size-3:
            return (size-1, 2*size-3 - position)

        if 2*size-2 <= position <= 3*size-4:
            return (3*size-4 - position, 0)

        if 3*size-3 <= position <= 4*size-5:
            return (0, position - (3*size-3))

        return (size-1, 0)

    def _coords_to_position(self, x, y):
        size = self.size
        if x == 0 and y == size-1:
            return 0
        elif y == size-1:
            return x
        elif x == size-1:
            return (size-1) + (size-1 - y)
        elif y == 0:
            return (2*size-2) + (size-1 - x)
        elif x == 0:
            return (3*size-3) + y
        return -1

    def get_cell_at_position(self, position):
        for cell in self.cells:
            if cell.position == position:
                return cell
        return None
