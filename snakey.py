import curses
import time
import sys
from random import randint

class Board:  
    def __init__(self, size):
        self.size = size
        self.tiles = {  
            0: ' . ',
            1: ' * ',
            2: ' # ',
            3: ' & ',
        }
        self.snake_positions = []  
        self._make_board()
        self.spawn_apple()         

    def spawn_apple(self):
        while True:
            i = randint(0, self.size-1)
            j = randint(0, self.size-1)
            pos = [i, j]
            if pos not in self.snake_positions:
                self.board[i][j] = 3
                break

    def _make_board(self):
        self.board = [[0 for j in range(self.size)] for i in range(self.size)]

    def _wipe_snake(self):
        self.board = [[cell if cell not in (1,2) else 0 for cell in row] for row in self.board]

    def draw(self, screen, score):
        self._wipe_snake()

        for i, j in self.snake_positions:
            self.board[i][j] = 1

        head = self.snake_positions[-1]
        self.board[head[0]][head[1]] = 2

        screen.addstr(0, 0, f"Score: {score}")

        for i in range(self.size):
            row = ''
            for j in range(self.size):
                row += self.tiles[self.board[i][j]]
            screen.addstr(i+1, 0, row)  

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


class Snake:
    def __init__(self, name):
        self.name = name
        self.direction = curses.KEY_RIGHT
        self.segments = [[0,0],[0,1],[0,2],[0,3]] 

    def set_direction(self, ch):
        if ch == curses.KEY_LEFT and self.direction == curses.KEY_RIGHT:
            return
        if ch == curses.KEY_RIGHT and self.direction == curses.KEY_LEFT:
            return
        if ch == curses.KEY_UP and self.direction == curses.KEY_DOWN:
            return
        if ch == curses.KEY_DOWN and self.direction == curses.KEY_UP:
            return
        self.direction = ch

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
        if p[0] > self.board.size-1:
            p[0] = 0
        elif p[0] < 0:
            p[0] = self.board.size-1
        elif p[1] < 0:
            p[1] = self.board.size-1
        elif p[1] > self.board.size-1:
            p[1] = 0
        return p

    def move(self):
        head = self.segments[-1][:]

        if self.direction == curses.KEY_UP:
            head[0] -= 1
        elif self.direction == curses.KEY_DOWN:
            head[0] += 1
        elif self.direction == curses.KEY_RIGHT:
            head[1] += 1
        elif self.direction == curses.KEY_LEFT:
            head[1] -= 1

        head = self._wrap(head)

        del self.segments[0]
        self.segments.append(head)
        self.board.snake_positions = self.segments

        if not self.alive():
            sys.exit()

        if self.board.snake_ate_apple():
            curses.beep()
            self.grow()
            self.board.spawn_apple()

    def set_board(self, board):
        self.board = board


def main(screen):
    screen.timeout(0)

    board = Board(10)
    snake = Snake("Joe")
    snake.set_board(board)

    score = 0 

    while True:
        ch = screen.getch()
        if ch != -1:
            snake.set_direction(ch)

        snake.move()

        if board.snake_ate_apple():
            score += 1   
        board.draw(screen, score)
        screen.refresh()

        time.sleep(.4)

if __name__ == '__main__':
    curses.wrapper(main)
