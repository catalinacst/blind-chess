import pygame

class Chess():

    width = 900
    height = 600
    background = [82, 82, 82]
    board = [-1] * 64

    tiles = (
        pygame.image.load('img/white.png'),
        pygame.image.load('img/gray.png')
    )

    pieces = [
        pygame.image.load('img/whiteKing.png'),
        pygame.image.load('img/blackKing.png'),
        pygame.image.load('img/whiteQueen.png'),
        pygame.image.load('img/blackQueen.png'),
        pygame.image.load('img/whiteBishop.png'),
        pygame.image.load('img/blackBishop.png'),
        pygame.image.load('img/whiteKnight.png'),
        pygame.image.load('img/blackKnight.png'),
        pygame.image.load('img/whiteRook.png'),
        pygame.image.load('img/blackRook.png'),
        pygame.image.load('img/whitePawn.png'),
        pygame.image.load('img/blackPawn.png')
    ]

    positions = [
        [4],                                                  # Rey blanco
        [60],                                                 # Rey negro
        [3],                                                  # Reina blanco
        [59],                                                 # Reina negro
        [2, 5],                                               # Alfiles blancos
        [58, 61],                                             # Alfiles negros
        [1, 6],                                               # Caballos blancos
        [57, 62],                                             # Caballos negros
        [0, 7],                                               # Torres blancas
        [56, 63],                                             # Torres negras
        [8, 9, 10, 11, 12, 13, 14, 15],                       # Peones blancos
        [48, 49, 50, 51, 52, 53, 54, 55]                      # Peones negros
    ]

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([self.width, self.height])
        self.draw_board()

    def get_coord(self, pos):
        return (250 + (pos % 8) * 50, 450 - (pos // 8) * 50)

    def draw_board(self):
        """"""
        self.screen.fill(self.background)

        for k in range(64):
            self.screen.blit(self.tiles[((k + 1) + (k // 8)) % 2], self.get_coord(k))

        for i in range(12):
            for p in self.positions[i]:
                self.screen.blit(self.pieces[i], self.get_coord(p))
                self.board[p] = i

        pygame.display.flip()

    def move_piece(self, type_piece, id_piece, new_pos):
        self.board[self.positions[type_piece][id_piece]] = -1
        self.positions[type_piece][id_piece] = new_pos
        eaten = self.board[new_pos]
        if eaten != -1:
            idp = self.positions[eaten].index(new_pos)
            self.positions[eaten][idp] = -1
        self.board[new_pos] = type_piece
        self.draw_board()

    def moves_rey(self, pos, color):
        dx = [-1, -1, 0, 1, 1, 1, 0, -1];
        dy = [0, -1, -1, -1, 0, 1, 1, 1];
        movs = []
        x, y = pos % 8, pos // 8
        for k in range(8):
            nx, ny = x + dx[k], y + dy[k]
            if nx < 0 or nx > 7 or ny < 0 or ny > 7:
                continue
            np = 8 * ny + nx
            tp = self.board[np]
            if tp == -1 or tp % 2 != color:
                movs.append(np)
        return movs

    def moves_dama(self, pos, color):
        dx = [-1, 1, -1, 1, -1, 0, 1, 0]
        dy = [-1, -1, 1, 1, 0, -1, 0, 1]
        movs = []
        x, y = pos % 8, pos // 8
        for k in range(8):
            j = 1
            while True:
                nx, ny = x + j * dx[k], y + j * dy[k]
                if nx < 0 or nx > 7 or ny < 0 or ny > 7:
                    break
                np = 8 * ny + nx
                tp = self.board[np]
                if tp != -1:
                    if tp % 2 != color:
                        movs.append(np)
                    break
                movs.append(np)
                j += 1
        return movs

    def moves_alfil(self, pos, color):
        dx = [-1, 1, -1, 1]
        dy = [-1, -1, 1, 1]
        movs = []
        x, y = pos % 8, pos // 8
        for k in range(4):
            j = 1
            while True:
                nx, ny = x + j * dx[k], y + j * dy[k]
                if nx < 0 or nx > 7 or ny < 0 or ny > 7:
                    break
                np = 8 * ny + nx
                tp = self.board[np]
                if tp != -1:
                    if tp % 2 != color:
                        movs.append(np)
                    break
                movs.append(np)
                j += 1
        return movs

    def moves_caballo(self, pos, color):
        dx = [-2, -1, 1, 2, 2, 1, -1, -2]
        dy = [1, 2, 2, 1, -1, -2, -2, -1]
        movs = []
        x, y = pos % 8, pos // 8
        for k in range(8):
            nx, ny = x + dx[k], y + dy[k]
            if nx < 0 or nx > 7 or ny < 0 or ny > 7:
                continue
            np = 8 * ny + nx
            tp = self.board[np]
            if tp == -1 or tp % 2 != color:
                movs.append(np)
        return movs

    def moves_torre(self, pos, color):
        dx = [-1, 0, 1, 0]
        dy = [0, -1, 0, 1]
        movs = []
        x, y = pos % 8, pos // 8
        for k in range(4):
            j = 1
            while True:
                nx, ny = x + j * dx[k], y + j * dy[k]
                if nx < 0 or nx > 7 or ny < 0 or ny > 7:
                    break
                np = 8 * ny + nx
                tp = self.board[np]
                if tp != -1:
                    if tp % 2 != color:
                        movs.append(np)
                    break
                movs.append(np)
                j += 1
        return movs

    def moves_peon(self, pos, color):
        dx = [-1, 1, 0, 0]
        dy = [1, 1, 1, 2]
        x, y = pos % 8, pos // 8
        movs = []
        for k in range(4):
            nx, ny = x + dx[k], y + (dy[k] if color == 0 else -dy[k])
            if nx < 0 or nx > 7 or ny < 0 or ny > 7:
                continue
            np = 8 * ny + nx
            tp = self.board[np]
            if tp == -1:
                if k == 2:
                    movs.append(np)
                if k == 3 and (y == 1 and color == 0 or y == 6 and color == 1):
                    movs.append(np)
            else:
                if tp % 2 != color and k < 2:
                    movs.append(np)
                if k == 2:
                    break;
        return movs

    def get_moves(self, type_piece):
        tags = ['rey', 'dama', 'alfil', 'caballo', 'torre', 'peon']
        method = 'moves_' + tags[type_piece // 2]
        visitor = getattr(self, method)
        res = []
        for (id_piece, pos) in enumerate(self.positions[type_piece]):
            if pos != -1:
                movs = visitor(pos, type_piece % 2)
                for np in movs:
                    row, col = np // 8, np % 8
                    move = (type_piece, id_piece, row, col)
                    res.append(move)
        return res

    def get_all_valid_moves(self, color):
        valid_moves = []
        for piece in range(6):
            valid_moves += self.get_moves(2 * piece + color)
        return valid_moves
