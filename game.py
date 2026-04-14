##removed curses and swapped it so its understandable by js so i can ship it - same project though

import sys
from random import randint

UP = "UP"
DOWN = "DOWN"
LEFT = "LEFT"
RIGHT = "RIGHT"

class Board:
    def __init__(self, size):
        self.size = size
        self.tiles = {
            0: ".",
            1: "*",
            2: "#",
            3: "&",
        }
        self.snake_positions = []
        self._make_board()
        self.spawn_apple()

    def spawn_apple(self):
        while True:
            i = randint(0, self.size - 1)
            j = randint(0, self.size - 1)
            pos = [i, j]
            if pos not in self.snake_positions:
                self.board[i][j] = 3
                break

    def _make_board(self):
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]

    def _wipe_snake(self):
        self.board = [[cell if cell not in (1, 2) else 0 for cell in row] for row in self.board]


    def place_snake(self):
        self._wipe_snake()

        if not self.snake_positions:
            return

        for i, j in self.snake_positions:
        self.board[i][j] = 1

        head = self.snake_positions[-1]
        self.board[head[0]][head[1]] = 2
    
    def get_apple(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 3:
                    return [i, j]
        return [-1, -1]

    def snake_ate_apple(self):
        apple = self.get_apple()
        head = self.snake_positions[-1]
        return apple == head

    def render_text(self, score):
        self.place_snake()
        lines = [f"Score: {score}"]
        for i in range(self.size):
            row = "".join(self.tiles[self.board[i][j]] for j in range(self.size))
            lines.append(row)
        return "\n".join(lines)


class Snake:
    def __init__(self, name):
        self.name = name
        self.direction = RIGHT
        self.segments = [[0, 0], [0, 1], [0, 2], [0, 3]]

    def set_direction(self, d):
        if d == LEFT and self.direction == RIGHT:
            return
        if d == RIGHT and self.direction == LEFT:
            return
        if d == UP and self.direction == DOWN:
            return
        if d == DOWN and self.direction == UP:
            return
        self.direction = d

    def grow(self):
        a = self.segments[0]
        b = self.segments[1]
        tail = a[:]

        if a[0] < b[0]:
            tail[0] -= 1
        elif a[1] < b[1]:
            tail[1] -= 1
        elif a[0] > b[0]:
            tail[0] += 1
        elif a[1] > b[1]:
            tail[1] += 1

        tail = self._wrap(tail)
        self.segments.insert(0, tail)

    def alive(self):
        head = self.segments[-1]
        body = self.segments[:-1]
        return head not in body

    def _wrap(self, p):
        if p[0] > self.board.size - 1:
            p[0] = 0
        elif p[0] < 0:
            p[0] = self.board.size - 1
        elif p[1] < 0:
            p[1] = self.board.size - 1
        elif p[1] > self.board.size - 1:
            p[1] = 0
        return p

    def move(self):
        head = self.segments[-1][:]

        if self.direction == UP:
            head[0] -= 1
        elif self.direction == DOWN:
            head[0] += 1
        elif self.direction == RIGHT:
            head[1] += 1
        elif self.direction == LEFT:
            head[1] -= 1

        head = self._wrap(head)

        del self.segments[0]
        self.segments.append(head)
        self.board.snake_positions = self.segments

        if not self.alive():
            return "dead"

        if self.board.snake_ate_apple():
            self.grow()
            self.board.spawn_apple()
            return "apple"

        return "ok"

    def set_board(self, board):
        self.board = board


class Game:
    def __init__(self, size=10):
        self.board = Board(size)
        self.snake = Snake("Joe")
        self.snake.set_board(self.board)
        self.board.snake_positions = self.snake.segments[:]
        self.board.snake_positions = self.snake.segments[:]
        self.score = 0
        self.status = "ok"

    def set_direction(self, d):
        self.snake.set_direction(d)

    def tick(self):
        self.status = self.snake.move()
        if self.status == "apple":
            self.score += 1
        return self.status

    def render(self):
        return self.board.render_text(self.score)
