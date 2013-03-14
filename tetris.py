import pygame, sys, random
from pygame.locals import *

class Piece:
    O = (((0,0,0,0,0), (0,0,0,0,0),(0,0,1,1,0),(0,0,1,1,0),(0,0,0,0,0)),) * 4

    I = (((0,0,0,0,0),(0,0,0,0,0),(0,1,1,1,1),(0,0,0,0,0),(0,0,0,0,0)),
         ((0,0,0,0,0),(0,0,1,0,0),(0,0,1,0,0),(0,0,1,0,0),(0,0,1,0,0)),
         ((0,0,0,0,0),(0,0,0,0,0),(1,1,1,1,0),(0,0,0,0,0),(0,0,0,0,0)),
         ((0,0,1,0,0),(0,0,1,0,0),(0,0,1,0,0),(0,0,1,0,0),(0,0,0,0,0)))

    L = (((0,0,0,0,0),(0,0,1,0,0),(0,0,1,0,0),(0,0,1,1,0),(0,0,0,0,0)),
         ((0,0,0,0,0),(0,0,0,0,0),(0,1,1,1,0),(0,1,0,0,0),(0,0,0,0,0)),
         ((0,0,0,0,0),(0,1,1,0,0),(0,0,1,0,0),(0,0,1,0,0),(0,0,0,0,0)),
         ((0,0,0,0,0),(0,0,0,1,0),(0,1,1,1,0),(0,0,0,0,0),(0,0,0,0,0)))

    J = (((0,0,0,0,0),(0,0,1,0,0),(0,0,1,0,0),(0,1,1,0,0),(0,0,0,0,0)),
         ((0,0,0,0,0),(0,1,0,0,0),(0,1,1,1,0),(0,0,0,0,0),(0,0,0,0,0)),
         ((0,0,0,0,0),(0,0,1,1,0),(0,0,1,0,0),(0,0,1,0,0),(0,0,0,0,0)),
         ((0,0,0,0,0),(0,0,0,0,0),(0,1,1,1,0),(0,0,0,1,0),(0,0,0,0,0)))

    Z = (((0,0,0,0,0),(0,0,0,1,0),(0,0,1,1,0),(0,0,1,0,0),(0,0,0,0,0)),
         ((0,0,0,0,0),(0,0,0,0,0),(0,1,1,0,0),(0,0,1,1,0),(0,0,0,0,0)),
         ((0,0,0,0,0),(0,0,1,0,0),(0,1,1,0,0),(0,1,0,0,0),(0,0,0,0,0)),
         ((0,0,0,0,0),(0,1,1,0,0),(0,0,1,1,0),(0,0,0,0,0),(0,0,0,0,0)))

    S = (((0,0,0,0,0),(0,0,1,0,0),(0,0,1,1,0),(0,0,0,1,0),(0,0,0,0,0)),
         ((0,0,0,0,0),(0,0,0,0,0),(0,0,1,1,0),(0,1,1,0,0),(0,0,0,0,0)),
         ((0,0,0,0,0),(0,1,0,0,0),(0,1,1,0,0),(0,0,1,0,0),(0,0,0,0,0)),
         ((0,0,0,0,0),(0,0,1,1,0),(0,1,1,0,0),(0,0,0,0,0),(0,0,0,0,0)))

    T = (((0,0,0,0,0),(0,0,1,0,0),(0,0,1,1,0),(0,0,1,0,0),(0,0,0,0,0)),
         ((0,0,0,0,0),(0,0,0,0,0),(0,1,1,1,0),(0,0,1,0,0),(0,0,0,0,0)),
         ((0,0,0,0,0),(0,0,1,0,0),(0,1,1,0,0),(0,0,1,0,0),(0,0,0,0,0)),
         ((0,0,0,0,0),(0,0,1,0,0),(0,1,1,1,0),(0,0,0,0,0),(0,0,0,0,0)))

    PIECES = {'O': O, 'I': I, 'L': L, 'J': J, 'Z': Z, 'S':S, 'T':T}

    def __init__(self, piece_name=None):
        if piece_name:
            self.piece_name = piece_name
        else:
            self.piece_name = random.choice(Piece.PIECES.keys())
        self.rotation = 0
        self.array2d = Piece.PIECES[self.piece_name][self.rotation]

    def __iter__(self):
        for row in self.array2d:
            yield row

    def rotate(self, clockwise=True):
        self.rotation = (self.rotation + 1) % 4 if clockwise else \
                        (self.rotation - 1) % 4
        self.array2d = Piece.PIECES[self.piece_name][self.rotation]

class Board:
    COLLIDE_ERROR = {'no_error': 0, 'right_wall': 1, 'left_wall': 2,
                     'bottom': 3, 'overlap': 4}

    def __init__(self, screen):
        self.screen = screen
        self.width = 10
        self.height = 22
        self.block_size = 25
        self.board = []
        for _ in xrange(self.height):
            self.board.append([0] * self.width)
        self.generate_piece()

    def generate_piece(self):
        self.piece = Piece()
        self.piece_x, self.piece_y = 3, 0

    def absorb_piece(self):
        for y, row in enumerate(self.piece):
            for x, block in enumerate(row):
                if block:
                    self.board[y+self.piece_y][x+self.piece_x] = block
        self.generate_piece()

    def _block_collide_with_board(self, x, y):
        if x < 0: 
            return Board.COLLIDE_ERROR['left_wall']
        elif x >= self.width:
            return Board.COLLIDE_ERROR['right_wall']
        elif y >= self.height:
            return Board.COLLIDE_ERROR['bottom']
        elif self.board[y][x]:
            return Board.COLLIDE_ERROR['overlap']
        return Board.COLLIDE_ERROR['no_error'] 

    def collide_with_board(self, dx, dy):
        """Check if piece (offset dx, dy) collides with board"""
        for y, row in enumerate(self.piece):
            for x, block in enumerate(row):
                if block:
                    collision = self._block_collide_with_board(x=x+dx, y=y+dy)
                    if collision:
                        return collision
        return Board.COLLIDE_ERROR['no_error']

    def _can_move_piece(self, dx, dy):
        dx_ = self.piece_x + dx
        dy_ = self.piece_y + dy
        if self.collide_with_board(dx=dx_, dy=dy_):
            return False
        return True

    def _can_drop_piece(self):
        return self._can_move_piece(dx=0, dy=1)

    def _try_rotate_piece(self, clockwise=True):
        self.piece.rotate(clockwise)
        collision = self.collide_with_board(dx=self.piece_x, dy=self.piece_y)
        if not collision:
            pass
        elif collision == Board.COLLIDE_ERROR['left_wall']:
            if self._can_move_piece(dx=1, dy=0):
                self.move_piece(dx=1, dy=0)
            elif self._can_move_piece(dx=2, dy=0):
                self.move_piece(dx=2, dy=0)
            else:
                self.piece.rotate(not clockwise)
        elif collision == Board.COLLIDE_ERROR['right_wall']:
            if self._can_move_piece(dx=-1, dy=0):
                self.move_piece(dx=-1, dy=0)
            elif self._can_move_piece(dx=-2, dy=0):
                self.move_piece(dx=-2, dy=0)
            else:
                self.piece.rotate(not clockwise)
        else:
            self.piece.rotate(not clockwise)

    def move_piece(self, dx, dy):
        if self._can_move_piece(dx, dy):
            self.piece_x += dx
            self.piece_y += dy

    def drop_piece(self):
        if self._can_drop_piece():
            self.move_piece(dx=0, dy=1)
        else:
            self.absorb_piece()
            self.delete_lines()

    def full_drop_piece(self):
        while self._can_drop_piece():
            self.drop_piece()
        self.drop_piece()

    def rotate_piece(self, clockwise=True):
        self._try_rotate_piece(clockwise)

    def pos_to_pixel(self, x, y):
        return self.block_size*x, self.block_size*(y-2)

    def _delete_line(self, y):
        for y in reversed(xrange(1, y+1)):
            self.board[y] = list(self.board[y-1])

    def delete_lines(self):
        remove = [y for y, row in enumerate(self.board) if all(row)]
        for y in remove:
            self._delete_line(y)    

    def game_over(self):
        return sum(self.board[0]) > 0 or sum(self.board[1]) > 0

    def draw_blocks(self, array2d, color=(0,0,255), dx=0, dy=0):
        for y, row in enumerate(array2d):
            y += dy
            if y >= 2 and y < self.height:
                for x, block in enumerate(row):
                    if block:
                        x += dx
                        x_pix, y_pix = self.pos_to_pixel(x, y)
                        # draw block
                        pygame.draw.rect(self.screen, color,
                                         (  x_pix, y_pix,
                                            self.block_size,
                                            self.block_size))
                        # draw border
                        pygame.draw.rect(self.screen, (0, 0, 0),
                                         (  x_pix, y_pix,
                                            self.block_size,
                                            self.block_size), 1)

    def draw(self):
        self.draw_blocks(self.piece, dx=self.piece_x, dy=self.piece_y)
        self.draw_blocks(self.board)

class Tetris:
    DROP_EVENT = USEREVENT + 1

    def __init__(self):
        self.screen = pygame.display.set_mode((250, 500))
        self.clock = pygame.time.Clock()
        self.board = Board(self.screen)

    def handle_key(self, event_key):
        if event_key == K_DOWN:
            self.board.drop_piece()
        elif event_key == K_LEFT:
            self.board.move_piece(dx=-1, dy=0)
        elif event_key == K_RIGHT:
            self.board.move_piece(dx=1, dy=0)
        elif event_key == K_UP:
            self.board.rotate_piece()
        elif event_key == K_SPACE:
            self.board.full_drop_piece()

    def run(self):
        pygame.init()
        pygame.time.set_timer(Tetris.DROP_EVENT, 500)

        while True:
            if self.board.game_over():
                print "Game over"
                pygame.quit()
                sys.exit()
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    self.handle_key(event.key)
                elif event.type == Tetris.DROP_EVENT:
                    self.board.drop_piece()
            
            self.board.draw()
            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    Tetris().run()
