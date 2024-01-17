import pygame
import numpy as np
import math

# setup the rendering engine
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
start = False
draw = False

def blank_cells(cell_width: int):
    # number of cells per row
    total_x = math.floor(screen.get_width() / cell_width)
    # total number of cells per column
    total_y = math.floor(screen.get_height() / cell_width)
    return np.zeros((total_x,total_y), dtype=int)

def add_glider(cells: np.ndarray, centered_on: (int,int)):
    x,y = centered_on
    cells[x, y-1] = 1
    cells[x+1, y] = 1
    cells[x-1, y+1] = 1
    cells[x, y+1] = 1
    cells[x+1, y+1] = 1
    return cells
    
def add_square(cells: np.ndarray, top_left: (int,int)):
    x,y = top_left
    cells[x,y] = 1
    cells[x,y+1] = 1
    cells[x+1,y] = 1
    cells[x+1,y+1] = 1
    return cells

# cells of x within radius d of cell n
def n_closest(x,n,d=1):
    return x[n[0]-d:n[0]+d+1,n[1]-d:n[1]+d+1]

# rules of conways game of life
def conway(cells: np.ndarray) -> np.ndarray:
    # next generation
    nextCells = np.copy(cells)
    # calculate sum of neighbors
    for x in range(w):
        for y in range(h):
            c = cells[x,y]
            n = (x,y)
            nc = n_closest(cells, n).sum() - c
            if c == 1 and (nc < 2 or nc > 3):
                nextCells[x,y] = 0
            elif c == 0 and nc == 3:
                nextCells[x,y] = 1
            # if c == 1 and (nc == 2 or nc == 3):
            #   pass
    return np.copy(nextCells)

# includes each cell as part of its own neighborhood
def conway_self_neighbor(cells: np.ndarray) -> np.ndarray:
    # next generation
    nextCells = np.copy(cells)
    # calculate sum of neighbors
    for x in range(w):
        for y in range(h):
            c = cells[x,y]
            n = (x,y)
            nc = n_closest(cells, n).sum()
            if c == 1 and (nc < 2 or nc > 3):
                nextCells[x,y] = 0
            elif c == 0 and nc == 3:
                nextCells[x,y] = 1
            # if c == 1 and (nc == 2 or nc == 3):
            #   pass
    return np.copy(nextCells)

def conway_double_radius(cells: np.ndarray) -> np.ndarray:
    # next generation
    nextCells = np.copy(cells)
    # calculate sum of neighbors
    for x in range(w):
        for y in range(h):
            c = cells[x,y]
            n = (x,y)
            nc = n_closest(cells, n, d=2).sum() - c
            if c == 1 and (nc < 2 or nc > 3):
                nextCells[x,y] = 0
            elif c == 0 and nc == 3:
                nextCells[x,y] = 1
            # if c == 1 and (nc == 2 or nc == 3):
            #   pass
    return np.copy(nextCells)

# cell width
cw = 8
# initialize cells
cells = blank_cells(cw)
# populate cells with glider
cells = add_glider(cells, (80,40))
# populate cells with square
# cells = add_square(cells, (102,60))

reset_to = cells.copy()
while(running):
    # poll for events
    for event in pygame.event.get():
        # user clicked X to close the window
        if event.type == pygame.QUIT:
            running = False
        # user draws to the grid
        if event.type == pygame.MOUSEBUTTONDOWN:
            draw = True
        if event.type == pygame.MOUSEBUTTONUP:
            draw = False

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_ESCAPE]:
        running = False
    if pressed[pygame.K_SPACE] and not start:
        start = True
    if pressed[pygame.K_r]:
        cells = reset_to.copy()

    m_left,m_right,_ = pygame.mouse.get_pressed()
    if draw:
        m_x,m_y = pygame.mouse.get_pos()
        cell_x,cell_y = (math.floor(m_x / cw),math.floor(m_y / cw))
        cells[cell_x,cell_y] = 1 if m_left else 0

    # fill the screen with a color to wipe away anything from last frame
    screen.fill('white')

    # RENDER YOUR GAME HERE
    w,h = cells.shape
    for x in range(w):
        for y in range(h):
            if cells[x,y] == 1:
                # coordinate of the top left corner 
                pos = (x*cw, y*cw)
                # square dimensions
                sqdim = (cw, cw)
                # draw the black square
                cell = pygame.Rect(pos, sqdim)
                pygame.draw.rect(screen, "black", cell)

    if start:
        cells = conway_double_radius(cells)

    # flip() the display to put your work on screen
    pygame.display.flip()
    # limits FPS to 60
    clock.tick(60)