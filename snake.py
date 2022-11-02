from random import randint
from itertools import product
from argparse import ArgumentParser

import pygame as pg

SPEED = 3

# the size of a tile
TILE_X = 30
TILE_Y = 20

# how many tiles
BOARD_WIDTH = 30
BOARD_HEIGHT = 40

COLOR_WHITE = (250, 250, 250)
COLOR_BLACK = (240, 240, 240)
COLOR_SNAKE = (128, 128, 0)
COLOR_FRUIT = (192, 16, 16)

DIRECTIONS = {
    'DOWN':  (0, +1),
    'UP':    (0, -1),
    'RIGHT': (+1, 0),
    'LEFT':  (-1, 0),
}


# the state of the game is primarily these 3 globals
snake = [
    (10, 15),
    (11, 15),
    (12, 15),
]

direction = (1, 0)

fruit = (10, 10)


def tile(col, line):
    """
    return a Rect element corresponding to tile (col. line)
    """
    return pg.Rect(TILE_X*col, TILE_Y*line, TILE_X, TILE_Y)

def draw_tile(col, line, color):
    """
    same as tile() but draws it in the specified color
    """
    pg.draw.rect(screen, color, tile(col, line))


def checkers_background():
    """
    paint the background
    """
    for col, line in product(range(BOARD_WIDTH),
                             range(BOARD_HEIGHT)):
        color = COLOR_WHITE if (line+col)%2 else COLOR_BLACK
        draw_tile(col, line, color)


def move_snake(snake, direction, fruit):
    """
    computes the new snake, and tells if the fruit was hit

    so for that it returns a tuple (hit:bool, snake)
    """
    head_x, head_y = snake[0]
    dx, dy = direction
    new_head = (head_x+dx, head_y+dy)
    if new_head == fruit:
        return (True, [fruit] + snake)
    else:
        return (False, [new_head] + snake[:-1])


def random_fruit(snake, fruit):
    """
    returns the new position of the fruit
    that must not be on the snake, nor the current fruit
    """
    while True:
        new_fruit = (randint(0, BOARD_WIDTH-1), randint(0, BOARD_HEIGHT-1))
        if new_fruit in snake or new_fruit == fruit:
            pass
        else:
            return new_fruit


def handle_events():
    """
    return True if we see a 'quit-game' event
    """
    global direction
    # on itère sur tous les évênements qui ont eu lieu depuis le précédent appel
    # ici donc tous les évènements survenus durant la seconde précédente
    for event in pg.event.get():
        # chaque évênement à un type qui décrit la nature de l'évênement
        # un type de pg.QUIT signifie que l'on a cliqué sur la "croix" de la fenêtre
        if event.type == pg.QUIT:
            return True
        # un type de pg.KEYDOWN signifie que l'on a appuyé une touche du clavier
        elif event.type == pg.KEYDOWN:
            # si la touche est "Q" on veut quitter le programme
            if event.key == pg.K_q:
                return True
            elif event.key == pg.K_DOWN:
                direction = DIRECTIONS['DOWN']
            elif event.key == pg.K_UP:
                direction = DIRECTIONS['UP']
            elif event.key == pg.K_RIGHT:
                direction = DIRECTIONS['RIGHT']
            elif event.key == pg.K_LEFT:
                direction = DIRECTIONS['LEFT']


# all this could/should go into a main() function
parser = ArgumentParser()
parser.add_argument("--tiles", default="30x30", help="define number of tiles in X/Y")
parser.add_argument("--pixels", default="30x30", help="define number of tiles in X/Y")
parser.add_argument("--speed", default=3, type=int)
args = parser.parse_args()

BOARD_WIDTH, BOARD_HEIGHT = (int (x) for x in args.tiles.split('x'))
TILE_X, TILE_Y = (int (x) for x in args.pixels.split('x'))
SPEED = args.speed


pg.init()
screen = pg.display.set_mode((BOARD_WIDTH*TILE_X,
                            BOARD_HEIGHT*TILE_Y))
clock = pg.time.Clock()


while True:

    clock.tick(SPEED)
    if handle_events():
        break

    # game logic
    hit, snake = move_snake(snake, direction, fruit)
    if hit:
        fruit = random_fruit(snake, fruit)

    # draw
    checkers_background()
    for col, line in snake:
        draw_tile(col, line, COLOR_SNAKE)
    draw_tile(*fruit, COLOR_FRUIT)

    # flush to video
    pg.display.update()


# Enfin on rajoute un appel à pg.quit()
# Cet appel va permettre à Pygame de "bien s'éteindre" et éviter des bugs sous Windows
pg.quit()
