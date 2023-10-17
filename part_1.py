import pygame
import sys
import math

SCREEN_HEIGHT = 480
SCREEN_WIDTH = SCREEN_HEIGHT * 2
MAP_SIZE = 8
TILE_SIZE = (SCREEN_WIDTH / 2) / MAP_SIZE
PLAYER_SIZE=8

pygame.init()

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("RayCasting Example")
clock = pygame.time.Clock()

#global var
player_x = (SCREEN_WIDTH/2) / 2
player_y = (SCREEN_WIDTH/2) / 2

MAP = (
    '########'
    '# #    #'
    '# #  ###'
    '#      #'
    '#      #'
    '#  ##  #'
    '#   #  #'
    '########'
)


RED = (255, 0, 0)

def draw_map():
    for row in range(8):
        for col in range(8):
            # calculate square index
            square = row * MAP_SIZE + col
            # draw map
            pygame.draw.rect(win,
                             (200, 200, 200) if MAP[square] == '#' else (100, 100, 100),
                             (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE-2, TILE_SIZE-2)
                             )
    #draw player
    pygame.draw.circle(win, RED, (int(player_x), int(player_y)), PLAYER_SIZE)


run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            run = False

    draw_map()

    # flip() update the full display window and update(surface) updates only a surface received by parameter,
    # if parameter is null update updates all display surface
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
