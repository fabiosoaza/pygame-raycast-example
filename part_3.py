import pygame
import sys
import math


SCREEN_HEIGHT = 480
SCREEN_WIDTH = SCREEN_HEIGHT * 2
HALF_SCREEN=int(SCREEN_WIDTH/2)
MAP_SIZE = 8
TILE_SIZE = (SCREEN_WIDTH / 2) / MAP_SIZE
MAX_DEPTH = int(MAP_SIZE * TILE_SIZE)
PLAYER_SIZE = 8
NUM_COLS=8
NUM_ROWS=8
# Field of View
FOV = math.pi / 3

# FOV SOLAR EFFECT
# FOV = math.pi * 2


HALF_FOV = FOV / 2
# number of rays to cast
CASTED_RAYS = 120
STEP_ANGLE = FOV / CASTED_RAYS
RAY_SIZE = 3
RAY_LENGTH = 50
PLAYER_SPEED = 5
SCALE = (SCREEN_WIDTH / 2) / CASTED_RAYS

#doom framerate lock back the day was 35
FPS = 60

pygame.init()

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("RayCasting Example")
clock = pygame.time.Clock()


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
GRAY = (100, 100, 100)
LIGHT_GRAY = (200, 200, 200)
WHITE = (255, 255, 255)
BLUE_SKY=(135, 206, 235)

font = pygame.font.SysFont('Monospace Regular', 30)

def draw_map():
    for row in range(NUM_ROWS):
        for col in range(NUM_ROWS):
            # calculate square index
            square = row * MAP_SIZE + col
            # draw map
            pygame.draw.rect(win,
                             LIGHT_GRAY if MAP[square] == '#' else GRAY,
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
                # comment to not show casted ray and view only field of view representation
                pygame.draw.line(win,
                                 YELLOW, (player_x, player_y),
                                 (
                                     target_x,
                                     target_y
                                 ))

                # wall shading if player is further from wall color is dark
                # 0.0001 small constant to avoid divide by zero
                color_shading = 255 / (1 + depth * depth * 0.0001)


                #color shading must be calculate before wall height
                # fix fishbowl effect
                depth *= math.cos(player_angle-start_angle)

                # calculate wall height
                wall_height = 21000 / (depth + 0.0001)

                #fix stuck at the wall
                if wall_height > SCREEN_HEIGHT:
                    wall_height = SCREEN_HEIGHT

                # draw 3d prjection rectangle by rectangle
                rect = pygame.Rect(
                    # left
                    SCREEN_HEIGHT + ray * SCALE,
                    # top
                    (SCREEN_HEIGHT / 2) - wall_height / 2,
                    # width
                    SCALE,
                    # height
                    wall_height
                )

                # color = (0, 0, color_shading)
                color = (color_shading, color_shading, color_shading)
                pygame.draw.rect(win, color, rect)

                break

        # increment angle by single step
        start_angle += STEP_ANGLE



#moving direction
forward = True

run = True


while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            run = False

    # collision detection with map
    row = int(player_y / TILE_SIZE)
    col = int(player_x / TILE_SIZE)
    # calculate map square index
    square = row * MAP_SIZE + col

    # player hits the wall (collision detection)
    if MAP[square] == '#':
        if forward:
            player_x -= -math.sin(player_angle) * PLAYER_SPEED
            player_y -= math.cos(player_angle) * PLAYER_SPEED
        else:
            player_x += -math.sin(player_angle) * PLAYER_SPEED
            player_y += math.cos(player_angle) * PLAYER_SPEED


    # update 2d backgound
    pygame.draw.rect(win, BLACK, (0, 0, SCREEN_HEIGHT, SCREEN_HEIGHT))

    # update 3d map
    # ceiling
    pygame.draw.rect(win, LIGHT_GRAY, (480, -SCREEN_HEIGHT / 2, SCREEN_HEIGHT, SCREEN_HEIGHT))

    # floor
    pygame.draw.rect(win, GRAY, (480, SCREEN_HEIGHT / 2, SCREEN_HEIGHT, SCREEN_HEIGHT))

    # draw 2d map
    draw_map()
    cast_rays()

    keys = pygame.key.get_pressed()
    # turn fov left
    if keys[pygame.K_LEFT]: player_angle -= 0.1
    # turn fov right
    if keys[pygame.K_RIGHT]: player_angle += 0.1

    if keys[pygame.K_UP]:
        forward = True
        player_x += -math.sin(player_angle) * PLAYER_SPEED
        player_y += math.cos(player_angle) * PLAYER_SPEED

    if keys[pygame.K_DOWN]:
        forward = False
        player_x -= -math.sin(player_angle) * PLAYER_SPEED
        player_y -= math.cos(player_angle) * PLAYER_SPEED

    clock.tick(FPS)

    #display fps
    fps = str(int(clock.get_fps()))
    fps_surface = font.render(fps, False, WHITE)
    win.blit(fps_surface, (HALF_SCREEN,0))

    # flip() update the full display window and update(surface) updates only a surface received by parameter,
    # if parameter is null update updates all display surface
    pygame.display.flip()


pygame.quit()
