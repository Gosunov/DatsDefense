
from main import *
import time
import json
def visual():
    import pygame
    pygame.init()

    screen = pygame.display.set_mode([1000, 1000])

    while True:
        data = units()

        myFile = open(f'{time.time()}.txt', 'w')

        myFile.write(json.dumps(data))
        myFile.close()

        #build = get_build(data)
        #attack = get_attack(data)
        #move_base = get_move_base(data)

        #r = command(
        #    {
        #        'attack': attack,
        #        'build': build,
        #        'moveBase': move_base
        #    }
        #)

        #pprint(r)

        # Fill the background with white
        screen.fill((255, 255, 255))

        base = get_base(data)
        zombies = get_zombies(data)
        enemy_blocks = get_enemy_blocks(data)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False



        x_d = 500
        y_d = 500


        print(type(base))
        if (base is not None):
            for tower in base:
                # Draw a solid blue circle in the center
                pygame.draw.circle(screen, (0, 0, 255),(x_d + tower.get('x') * 2, y_d + tower.get('y') * 2), 2)

        if (zombies is not None):
            for zombie in zombies:
                # Draw a solid blue circle in the center
                pygame.draw.circle(screen, (0, 255, 0), (x_d + zombie.get('x') * 2, y_d + zombie.get('y') * 2), 2)


        if (enemy_blocks is not None):
            for enemy_block in enemy_blocks:
                # Draw a solid blue circle in the center
                pygame.draw.circle(screen, (255, 0, 0), (x_d + enemy_block.get('x') * 2,y_d + enemy_block.get('y') * 2), 2)

        # Flip the display
        pygame.display.flip()

        time.sleep(1)



visual()