import numpy as np
import pygame
import sys
import math

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
antiquewhite = (250, 235, 215)

ROW_COUNT = 6
COLUMN_COUNT = 7


class Board:
    def __init__(self):
        self.board = self.create_board()

    def create_board(self):
        board = np.zeros((ROW_COUNT, COLUMN_COUNT))
        return board

    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece

    def is_valid_location(self, col):
        return self.board[ROW_COUNT - 1][col] == 0

    def get_next_open_row(self, col):
        for r in range(ROW_COUNT):
            if self.board[r][col] == 0:
                return r

    def print_board(self):
        print(np.flip(self.board, 0))

    def winning_move(self, piece):
        # Check horizontal locations for win
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT):
                if (
                        self.board[r][c] == piece
                        and self.board[r][c + 1] == piece
                        and self.board[r][c + 2] == piece
                        and self.board[r][c + 3] == piece
                ):
                    return True

        # Check vertical locations for win
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT - 3):
                if (
                        self.board[r][c] == piece
                        and self.board[r + 1][c] == piece
                        and self.board[r + 2][c] == piece
                        and self.board[r + 3][c] == piece
                ):
                    return True

        # Check positively sloped diaganols
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT - 3):
                if (
                        self.board[r][c] == piece
                        and self.board[r + 1][c + 1] == piece
                        and self.board[r + 2][c + 2] == piece
                        and self.board[r + 3][c + 3] == piece
                ):
                    return True

        # Check negatively sloped diaganols
        for c in range(COLUMN_COUNT - 3):
            for r in range(3, ROW_COUNT):
                if (
                        self.board[r][c] == piece
                        and self.board[r - 1][c + 1] == piece
                        and self.board[r - 2][c + 2] == piece
                        and self.board[r - 3][c + 3] == piece
                ):
                    return True


class Coin:
    def __init__(self, screen, color, position, radius):
        self.screen = screen
        self.color = color
        self.position = position
        self.radius = radius

    def draw(self):
        pygame.draw.circle(self.screen, self.color, self.position, self.radius)


class Button:
    def __init__(self, screen, color, rect, font, text):
        self.screen = screen
        self.color = color
        self.rect = rect
        self.font = font
        self.text = text

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        label = self.font.render(self.text, True, BLACK)
        self.screen.blit(
            label,
            (
                self.rect.x + self.rect.width // 2 - label.get_width() // 2,
                self.rect.y + self.rect.height // 2 - label.get_height() // 2,
            ),
        )


class Game:
    def __init__(self):
        pygame.init()
        self.SQUARESIZE = 100
        self.width = COLUMN_COUNT * self.SQUARESIZE
        self.height = (ROW_COUNT + 1) * self.SQUARESIZE
        self.size = (self.width, self.height)
        self.RADIUS = int(self.SQUARESIZE / 2 - 5)
        self.screen = pygame.display.set_mode(self.size)
        self.myfont = pygame.font.SysFont("monospace", 20)
        self.start_button = Button(
            self.screen, GREEN, pygame.Rect(10, 10, 100, 50), self.myfont, "Start"
        )
        self.quit_button = Button(
            self.screen,
            RED,
            pygame.Rect(self.width - 110, 10, 100, 50),
            self.myfont,
            "Quit",
        )
        self.restart_button = Button(
            self.screen,
            GREEN,
            pygame.Rect(self.width // 2 - 50, 10, 100, 50),
            self.myfont,
            "Restart",
        )
        self.board = Board()
        self.win = False
        self.turn = 0
        self.start_game = False
        self.full_board_message = self.myfont.render(
            "Board is full!", True, RED
        )  # Message to display when the board is full

    def draw_board(self):
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                pygame.draw.rect(
                    self.screen,
                    antiquewhite,
                    (
                        c * self.SQUARESIZE,
                        r * self.SQUARESIZE + self.SQUARESIZE,
                        self.SQUARESIZE,
                        self.SQUARESIZE,
                    ),
                )
                pygame.draw.circle(
                    self.screen,
                    BLACK,
                    (
                        int(c * self.SQUARESIZE + self.SQUARESIZE / 2),
                        int(r * self.SQUARESIZE + self.SQUARESIZE + self.SQUARESIZE / 2),
                    ),
                    self.RADIUS,
                )

        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                if self.board.board[r][c] == 1:
                    coin = Coin(
                        self.screen,
                        RED,
                        (
                            int(c * self.SQUARESIZE + self.SQUARESIZE / 2),
                            self.height
                            - int(r * self.SQUARESIZE + self.SQUARESIZE / 2),
                        ),
                        self.RADIUS,
                    )
                    coin.draw()
                elif self.board.board[r][c] == 2:
                    coin = Coin(
                        self.screen,
                        YELLOW,
                        (
                            int(c * self.SQUARESIZE + self.SQUARESIZE / 2),
                            self.height
                            - int(r * self.SQUARESIZE + self.SQUARESIZE / 2),
                        ),
                        self.RADIUS,
                    )
                    coin.draw()
        pygame.display.update()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button.rect.collidepoint(event.pos):
                        self.start_game = True
                        self.screen.fill(BLACK)
                        pygame.display.update()
                    elif self.quit_button.rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                    elif self.restart_button.rect.collidepoint(event.pos):
                        self.board = Board()
                        self.win = False
                        self.turn = 0
                        self.screen.fill(BLUE)
                        self.draw_board()
                        pygame.display.update()
                    elif self.start_game and not self.win:
                        self.screen.fill(BLUE)
                        posx = event.pos[0]
                        col = int(math.floor(posx / self.SQUARESIZE))
                        if self.board.is_valid_location(col):
                            row = self.board.get_next_open_row(col)
                            self.board.drop_piece(row, col, self.turn + 1)

                            if self.board.winning_move(self.turn + 1):
                                label = self.myfont.render(
                                    f"Player {self.turn + 1} wins!!", 1, RED
                                )
                                self.screen.blit(label, (40, 10))
                                self.win = True

                        self.board.print_board()
                        self.draw_board()

                        self.turn += 1
                        self.turn %= 2

                if self.start_game and not self.win:
                    if event.type == pygame.MOUSEMOTION:
                        self.screen.fill(BLUE)
                        posx = event.pos[0]
                        if self.turn == 0:
                            pygame.draw.circle(
                                self.screen, RED, (posx, int(self.SQUARESIZE / 2)), self.RADIUS
                            )
                        else:
                            pygame.draw.circle(
                                self.screen,
                                YELLOW,
                                (posx, int(self.SQUARESIZE / 2)),
                                self.RADIUS,
                            )
                        self.draw_board()

            if not self.start_game:
                self.start_button.draw()
            self.restart_button.draw()
            self.quit_button.draw()

            if np.count_nonzero(self.board.board) == ROW_COUNT * COLUMN_COUNT:
                # Display the message when the board is full
                self.screen.blit(self.full_board_message, (10, 10))

            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
