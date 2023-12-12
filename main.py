"""
Author: bogpok
Chess images: https://dani-maccari.itch.io/pixel-chess
"""

# from logic import checkChess
import pygame
import math
import spritesheet
import logic


def drawBoard(screen, x0 = 0, y0 = 0, n = 8, a = 50):
    """
    x0, y0 - starting point of whole deck
    nxn - the default size is 8x8
    a - size of one square
    """
    
    # first color is white
    colorid = True # True for white; False for black
    cellrect = pygame.Rect(x0, y0, a, a)
    for i in range(n):
        for j in range(n):
            if colorid:
                c = '#c2953d' # dex (r,g,b)
            else:
                c = '#46020a'
            pygame.draw.rect(screen, c, cellrect)
            cellrect.left += a
            colorid = not colorid
        cellrect.left = x0
        cellrect.top += a
        colorid = not colorid

def defineCell(xy, x0, y0, n, a):
    x = xy[0] - x0
    y = xy[1] - y0

    # Not on game board
    if x < 0 or y < 0 or x > n*a or y > n*a:
        return (0, 0)
    else:
        nx = math.ceil(x/a)
        ny = math.ceil(y/a)
        return (nx, ny)

def moveByClick(event, fig):
    if event.type == pygame.MOUSEBUTTONDOWN:
            nx, ny = defineCell(event.pos, 50, 50, 8, 50)
            if nx == 0 and ny == 0:
                pass
            else:
                fig.left = nx*50
                fig.top = ny*50


class Figure:
    def __init__(self, nx0, ny0, image, name, team, offset = (50, 50), a = 50):        
        self.image = image
        self.image = spritesheet.changesize(self.image, a/16*0.9)
        self.rect = self.image.get_rect(topleft=(offset[0] + nx0*a+3,
                                                offset[1] + ny0*a))
        self.name = name # e.g. 'pawn'
        self.team = team # 'black' or 'white'

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Board:
    def __init__(self, figImgs, n = 8, a = 50):
        self.n = n
        self.a = a
        self.figImgs = figImgs
        self.cells = []
        self.movecounter = [0, 0]
        for i in range(n):
            row = []
            for j in range(n):
                row.append(Cell(i, j))
            self.cells.append(row)

        self.setFiguresDefault()

    def setFiguresDefault(self):
        """
        self.figImgs:
            2-dimesion array of blackImage figures and whiteImage

        0. pawn
        1. knight
        2. rook
        3. king
        4. bishop
        5. queen
        """

        # put pawns
        for i in range(8):
            self.cells[i][1].figure = Figure(i, 1, self.figImgs[0][0], name = 'pawn', team = 'black')
            self.cells[i][6].figure = Figure(i, 6, self.figImgs[1][0], name = 'pawn', team = 'white')

        # rooks
        self.cells[0][0].figure = Figure(0, 0, self.figImgs[0][2], name = 'rook', team = 'black')
        self.cells[self.n-1][0].figure = Figure(self.n-1, 0, self.figImgs[0][2], name = 'rook', team = 'black')

        self.cells[0][self.n-1].figure = Figure(0, self.n-1, self.figImgs[1][2], name = 'rook', team = 'white')
        self.cells[self.n-1][self.n-1].figure = Figure(self.n-1, self.n-1, self.figImgs[1][2], name = 'rook', team = 'white')

        # knights
        self.cells[1][0].figure = Figure(1, 0, self.figImgs[0][1], name = 'knight', team = 'black')
        self.cells[self.n-2][0].figure = Figure(self.n-2, 0, self.figImgs[0][1], name = 'knight', team = 'black')

        self.cells[1][self.n-1].figure = Figure(1, self.n-1, self.figImgs[1][1], name = 'knight', team = 'white')
        self.cells[self.n-2][self.n-1].figure = Figure(self.n-2, self.n-1, self.figImgs[1][1], name = 'knight', team = 'white')

        # bishop
        self.cells[2][0].figure = Figure(2, 0, self.figImgs[0][4], name = 'bishop', team = 'black')
        self.cells[self.n-3][0].figure = Figure(self.n-3, 0, self.figImgs[0][4], name = 'bishop', team = 'black')

        self.cells[2][self.n-1].figure = Figure(2, self.n-1, self.figImgs[1][4], name = 'bishop', team = 'white')
        self.cells[self.n-3][self.n-1].figure = Figure(self.n-3, self.n-1, self.figImgs[1][4], name = 'bishop', team = 'white')

        # queens
        self.cells[3][0].figure = Figure(3, 0, self.figImgs[0][5], name = 'queen', team = 'black')
        self.cells[3][self.n-1].figure = Figure(3, self.n-1, self.figImgs[1][5], name = 'queen', team = 'white')

        # kings
        self.cells[4][0].figure = Figure(4, 0, self.figImgs[0][3], name = 'king', team = 'black')
        self.cells[4][self.n-1].figure = Figure(4, self.n-1, self.figImgs[1][3], name = 'king', team = 'white')

    def draw(self, screen):
        for row in self.cells:
            for cell in row:
                if cell.figure is not None:
                    cell.figure.draw(screen)

    def move(self, nx1, ny1, nx2, ny2):
        i1, j1, i2, j2 = nx1-1, ny1-1, nx2-1, ny2-1
        isfig1 = self.cells[i1][j1].figure is not None
        isfig2 = self.cells[i2][j2].figure is not None
        if isfig1: 
            if logic.chessrules.canmove(nx1, ny1, nx2, ny2, self.cells[i1][j1].figure.name, self.cells[i1][j1].figure.team, isfig2):   
                if isfig2: 
                    if self.cells[i1][j1].figure.team == self.cells[i2][j2].figure.team:
                        print('Can not overtake the same team')     
                    else:
                        self.takenput(self.cells[i1][j1],
                                      self.cells[i2][j2])
                else:
                    self.takenput(self.cells[i1][j1],
                                  self.cells[i2][j2])
            # TODO identify blocking figures
                    
    def takenput(self, cell1, cell2):
        cell2.figure = cell1.figure
        cell2.positioning()
        cell1.figure = None


class Cell:
    def __init__(self, i, j, a=50):
        self.figure = None
        self.activated = False
        self.i = i
        self.j = j
        self.a = a
    def positioning(self):
        nx = self.i + 1
        ny = self.j + 1
        self.figure.rect.topleft = (nx*self.a, ny*self.a)



class Flag:
    def __init__(self, a = 50):
        self.active = False
        self.rect = pygame.Rect(0, 0, a, a)
        self.nx = 0
        self.ny = 0

    def move(self, event, board):
        if event.type == pygame.MOUSEBUTTONDOWN:
            nx, ny = defineCell(event.pos, 50, 50, 8, 50)
            if nx == 0 and ny == 0:
                pass
            elif nx == self.nx and ny == self.ny:
                self.active = not self.active
            else:
                if self.active:
                    board.move(self.nx, self.ny, nx, ny)
                self.nx = nx
                self.ny = ny
                self.active = not self.active
                self.rect.left = nx*50
                self.rect.top = ny*50


    def draw(self, screen):
        if self.active:
            pygame.draw.rect(screen, 'blue', self.rect, border_radius = 10, width = 7)

WIDTH = 500
HEIGHT = 500
def main():
    pygame.init()
    pygame.display.set_caption("pychess")
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    blacksprites = spritesheet.spritesheet('BlackPieces.png')
    blackfigures = blacksprites.images_at(((0, 0, 16, 16),
                                        (17, 0, 16, 16), 
                                        (33, 0, 16, 16), 
                                        (49, 0, 16, 16), 
                                        (65, 0, 16, 16), 
                                        (81, 0, 16, 16)), 
                                        colorkey=-1)

    whitesprites = spritesheet.spritesheet('WhitePieces.png')
    whitefigures = whitesprites.images_at(((0, 0, 16, 16),
                                        (17, 0, 16, 16), 
                                        (33, 0, 16, 16), 
                                        (49, 0, 16, 16), 
                                        (65, 0, 16, 16), 
                                        (81, 0, 16, 16)), 
                                        colorkey=-1)

    # initialize board
    board = Board((blackfigures, whitefigures))

    flag = Flag()

    cond = True
    while cond:
        clock.tick(60)
        screen.fill("#873431")
        drawBoard(screen, 50, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cond = False        
                    
            flag.move(event, board)                    
        
        flag.draw(screen)
        board.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()


"""
worklog
1. The deck: drawBoard
2. control - move figure by clicking two positions (from, to)
3. add chess images
4. Sound of replacing the figure
 id letters and numbers to board
5. add rules (restrictions) to them
6. Defeat and count point

"""
