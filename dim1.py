import pygame
import math

def calculateState(a,b,c):
    neighborhood = ''.join([str(i) for i in [a,b,c]])
    value = 7 - int(neighborhood, 2)
    newState = int(ruleSet[value])
    return newState

# setup the rendering engine
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

# setup the ruleset
ruleValue = 60
ruleSet = str(bin(ruleValue))[2:].rjust(8, '0')
# cell width
cw = 4
# y axis
y = 0

# number of cells
total = math.floor(screen.get_width() / cw)
print(total)

# populate cell list
cells = []
for i in range(total):
    cells.append(0)
cells[math.floor(total / 2)] = 1

screen.fill('white')
while(running):
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        running = False

    # fill the screen with a color to wipe away anything from last frame
    # screen.fill("purple")

    # RENDER YOUR GAME HERE
    l = len(cells)
    for i in range(l):
        x = i * cw
        cell = pygame.Rect(x, y, cw, cw)
        if cells[i] == 1:
            pygame.draw.rect(screen, "black", cell)
    y += cw

    # next generation
    nextCells = []
    for i in range(l):
        # calculate neighborhood
        left = cells[(i - 1 + l) % l]
        right = cells[(i + 1) % l]
        state = cells[i]
        newState = calculateState(left,state,right)
        nextCells.append(newState)
    cells = nextCells[:]

    # flip() the display to put your work on screen
    pygame.display.flip()
    # limits FPS to 60
    clock.tick(60)