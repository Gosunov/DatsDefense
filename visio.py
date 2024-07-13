
from main import *
import time
import json


d_x = 1
d_y = 1

min_x = 1
min_y = 1

def rescale(x, y):
    return (100 + (x - min_x) * 700 / d_x, 100 + (y - min_y) * 700 / d_y,)


def visual():
    import pygame
    pygame.init()

    screen = pygame.display.set_mode([1000, 1000])

    running = True

    while running:
        data = units()

        #myFile = open(f'{time.time()}.txt', 'w')
        #myFile.write(json.dumps(data))
        #myFile.close()

        screen.fill((255, 255, 255))

        base = get_base(data)
        zombies = get_zombies(data)
        enemy_blocks = get_enemy_blocks(data)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False



        global min_x, min_y, d_x, d_y
        min_x = 100000
        max_x = -100000

        min_y = 1000000
        max_y = -1000000

        for obj in (base + zombies + enemy_blocks):
            min_x = min(min_x, obj.get('x'))
            max_x = max(max_x, obj.get('x'))

            min_y = min(min_y, obj.get('y'))
            max_y = max(max_y, obj.get('y'))


        d_x = max_x - min_x
        d_y = max_y - min_y



        if (base is not None):
            for tower in base:
                pygame.draw.circle(screen, (0, 0, 255), rescale(tower.get('x'), tower.get('y')), 6)

        if (zombies is not None):
            for zombie in zombies:
                pygame.draw.circle(screen, (0, 255, 0), rescale(zombie.get('x'), zombie.get('y')), 6)


        if (enemy_blocks is not None):
            for enemy_block in enemy_blocks:
                pygame.draw.circle(screen, (255, 0, 0), rescale(enemy_block.get('x'), enemy_block.get('y')), 6)

        # Flip the display
        pygame.display.flip()

        time.sleep(1)


#participate()
visual()