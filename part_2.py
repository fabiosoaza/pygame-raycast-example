import pygame
import sys
import math

SCREEN_HEIGHT = 480
SCREEN_WIDTH = SCREEN_HEIGHT * 2
MAP_SIZE = 8
TILE_SIZE = (SCREEN_WIDTH / 2) / MAP_SIZE
MAX_DEPTH = int(MAP_SIZE * TILE_SIZE)
PLAYER_SIZE = 8
# Field of View
FOV = math.pi / 3

#FOV SOLAR EFFECT
#FOV = math.pi * 2


HALF_FOV = FOV / 2
# number of rays to cast
CASTED_RAYS = 120
STEP_ANGLE = FOV / CASTED_RAYS
RAY_SIZE = 3
RAY_LENGTH = 50
PLAYER_SPEED=5

pygame.init()

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("RayCasting Example")
clock = pygame.time.Clock()
FPS = 60

# global var
player_x = (SCREEN_WIDTH / 2) / 2
player_y = (SCREEN_WIDTH / 2) / 2
# line player is looking at or facing. Looks up
player_angle = math.pi

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
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)


def draw_map():
    for row in range(8):
        for col in range(8):
            # calculate square index
            square = row * MAP_SIZE + col
            # draw map
            pygame.draw.rect(win,
                             (200, 200, 200) if MAP[square] == '#' else (100, 100, 100),
                             (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2)
                             )
    # draw player
    pygame.draw.circle(win, RED, (int(player_x), int(player_y)), PLAYER_SIZE)
    # draw player direction, source ray
    pygame.draw.line(win,
                     BLUE, (player_x, player_y),
                     (
                         player_x - math.sin(player_angle) * RAY_LENGTH,
                         player_y + math.cos(player_angle) * RAY_LENGTH
                     ), RAY_SIZE)
    # draw player field ov view
    # left most
    pygame.draw.line(win,
                     GREEN, (player_x, player_y),
                     (
                         player_x - math.sin(player_angle - HALF_FOV) * RAY_LENGTH,
                         player_y + math.cos(player_angle - HALF_FOV) * RAY_LENGTH
                     ), RAY_SIZE)

    # right most
    pygame.draw.line(win,
                     GREEN, (player_x, player_y),
                     (
                         player_x - math.sin(player_angle + HALF_FOV) * RAY_LENGTH,
                         player_y + math.cos(player_angle + HALF_FOV) * RAY_LENGTH
                     ), RAY_SIZE)


# raycasting algoryth
def cast_rays():
    # left_most angle of FOV
    start_angle = player_angle - HALF_FOV

    # loop over casted rays
    for ray in range(CASTED_RAYS):
        # cast ray step by step
        for depth in range(MAX_DEPTH):
            # get ray target coordinates
            target_x = player_x - math.sin(start_angle) * depth
            target_y = player_y + math.cos(start_angle) * depth

            # convert target X, Y coordinate to map col, row
            row = int(target_y / TILE_SIZE)
            col = int(target_x / TILE_SIZE)
            # calculate map square index
            square = row * MAP_SIZE + col

            # change cel color to see rays hiting the walls
            if MAP[square] == '#':
                pygame.draw.rect(win,
                                 GREEN,
                                 (col * TILE_SIZE,
                                  row * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2)
                                 )


                # draw casted ray
                #comment to not show casted ray and view only field of view representation
                pygame.draw.line(win,
                                 YELLOW, (player_x, player_y),
                                 (
                                     target_x,
                                     target_y
                                 ))
                break

        # increment angle by single step
        start_angle += STEP_ANGLE


run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            run = False

    # update backgound
    pygame.draw.rect(win, BLACK, (0, 0, SCREEN_HEIGHT, SCREEN_HEIGHT))

    draw_map()
    cast_rays()

    keys = pygame.key.get_pressed()
    # turn fov left
    if keys[pygame.K_LEFT]: player_angle -= 0.1
    # turn fov right
    if keys[pygame.K_RIGHT]: player_angle += 0.1

    if keys[pygame.K_UP]:
        player_x += -math.sin(player_angle) * PLAYER_SPEED
        player_y += math.cos(player_angle) * PLAYER_SPEED

    if keys[pygame.K_DOWN]:
        player_x -= -math.sin(player_angle)  * PLAYER_SPEED
        player_y -= math.cos(player_angle) * PLAYER_SPEED


    # flip() update the full display window and update(surface) updates only a surface received by parameter,
    # if parameter is null update updates all display surface
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
