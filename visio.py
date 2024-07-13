
import time
import json

import main

import human_controls

default_scale_id = 10
scale_id = default_scale_id
scales = [(i/10)**2 for i in range(1,1000,10)]
scale = None
def update_scale(delta):
    global scale, scale_id

    new_scale_id = scale_id + delta

    if new_scale_id < 0 or new_scale_id >= len(scales): return

    scale_id = new_scale_id
    scale = scales[scale_id]


min_x = 1
min_y = 1



def rescale(x, y):
    return (100 + (x - min_x) * 700 / scale, 100 + (y - min_y) * 700 / scale,)

def reverse_scale(point):

    r_x = 1e10
    l_x = -1e10

    while(r_x - l_x > 0.1):
        m_x = (r_x + l_x) / 2

        if rescale(m_x,0)[0] < point[0]:
            l_x = m_x
        else:
            r_x = m_x

    r_y = 1e10
    l_y = -1e10

    while (r_y - l_y > 0.1):
        m_y = (r_y + l_y) / 2

        if rescale(0, m_y)[1] < point[1]:
            l_y = m_y
        else:
            r_y = m_y



    return (r_x, r_y)

def euclid_dist(p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

def to_rect(x,y, size_mult = 1):
    new_list = list(rescale(x, y))

    if (size_mult != 1):
        new_list[0] -= int(600 / scale) * size_mult / 2
        new_list[1] -= int(600 / scale) * size_mult / 2

    new_list.append(int(600 / scale) * size_mult)
    new_list.append(int(600 / scale) * size_mult)
    return tuple(new_list)

mouse_down = 'None'

import pygame
FPS=30
fpsClock=pygame.time.Clock()

pygame.font.init() # you have to call this at the start,
                   # if you want to use this module.
my_font = pygame.font.SysFont('Comic Sans MS', 40)

brush_radius = 5
motion_reverse = -1

def draw(event):
    global mouse_down

    if mouse_down == 'None': return

    print(event.pos)

    (board_x, board_y) = reverse_scale(event.pos)

    (board_x, board_y) = (int(board_x), int(board_y))

    print((board_x, board_y))
    global brush_radius

    radius = brush_radius

    if mouse_down == 'Erase':
        radius *= 2

    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            (board_dx, board_dy) = (board_x + dx, board_y + dy)
            if euclid_dist((board_x, board_y), (board_dx, board_dy)) < radius:


                if mouse_down == 'Draw':
                    human_controls.clicked_squares.add((board_dx, board_dy))
                if mouse_down == 'Erase':
                    if (board_dx, board_dy) in human_controls.clicked_squares:
                        human_controls.clicked_squares.remove((board_dx, board_dy))

def visual():
    global min_x, min_y, scale, scale_id, mouse_down, motion_reverse, brush_radius

    pygame.init()

    screen = pygame.display.set_mode([1000, 1000])

    running = True

    while running:
        fpsClock.tick(FPS)  # frame rate
        #myFile = open(f'{time.time()}.txt', 'w')
        #myFile.write(json.dumps(data))
        #myFile.close()

        screen.fill((255, 255, 255))



        #print(main.data, main.world, main.bruh)
        if main.data is None or main.world is None:
            time.sleep(0.1)
            continue

        base = main.data.base
        zombies = main.data.zombies
        enemy_blocks = main.data.enemy_towers

        if scale is None or pressed_keys[pygame.K_r]:

            min_x = 100000
            max_x = -100000

            min_y = 1000000
            max_y = -1000000

            for obj in (base + zombies + enemy_blocks):
                min_x = min(min_x, obj.x)
                max_x = max(max_x, obj.x)

                min_y = min(min_y, obj.y)
                max_y = max(max_y, obj.y)
            scale_id = default_scale_id
            scale = scales[scale_id]

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_w]:
            min_y += 0.01 * scale * motion_reverse * (1 + pressed_keys[pygame.K_LSHIFT] * 5)

        if pressed_keys[pygame.K_s]:
            min_y -= 0.01 * scale * motion_reverse * (1 + pressed_keys[pygame.K_LSHIFT] * 5)

        if pressed_keys[pygame.K_a]:
            min_x += 0.01 * scale * motion_reverse * (1 + pressed_keys[pygame.K_LSHIFT] * 5)

        if pressed_keys[pygame.K_d]:
            min_x -= 0.01 * scale * motion_reverse * (1 + pressed_keys[pygame.K_LSHIFT] * 5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4: # Вверх колесо мыши

                    if pressed_keys[pygame.K_LSHIFT]:
                        brush_radius += 1
                    else:
                        if scale is not None:
                            update_scale(-1)

                if event.button == 5:  # Вниз колесо мыши
                    if pressed_keys[pygame.K_LSHIFT]:
                        brush_radius -= 1
                    else:
                        if scale is not None:
                            update_scale(1)


                    print(scale)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # левая кнопка мыши

                    if pressed_keys[pygame.K_b]:
                        human_controls.auto_dodge ^= 1
                    elif pressed_keys[pygame.K_LSHIFT]:
                        human_controls.player_move_x = reverse_scale(event.pos)[0]
                        human_controls.player_move_y = reverse_scale(event.pos)[1]
                    else:
                        mouse_down = 'Draw'
                        draw(event)

                if event.button == 3:  # правая кнопка мыши
                    mouse_down = 'Erase'
                    draw(event)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # левая кнопка мыши

                    mouse_down = 'None'
                    draw(event)

                if event.button == 3:  # правая кнопка мыши
                    mouse_down = 'None'
                    draw(event)

            if event.type == pygame.MOUSEMOTION:
                draw(event)


        if (main.world.zpots is not None):
            for spawner in main.world.zpots:
                if spawner.type != 'default': continue
                pygame.draw.rect(screen, (0, 100, 100), to_rect(spawner.x, spawner.y, 30))

        for cl_sq in human_controls.clicked_squares:
            pygame.draw.rect(screen, (255, 255, 0), to_rect(cl_sq[0], cl_sq[1], 1.5))



        if (base is not None):
            for tower in base:
                if tower.is_head:
                    pygame.draw.rect(screen, (100, 0, 100), to_rect(tower.x, tower.y, 14))

        if (base is not None):
            for tower in base:
                if not tower.is_head:
                    pygame.draw.rect(screen, (0, 0, 255), to_rect(tower.x, tower.y))
                else:
                    pygame.draw.rect(screen, (150, 0, 150), to_rect(tower.x, tower.y))
        if (zombies is not None):
            for zombie in zombies:
                if (zombie.type != 'liner'):
                    pygame.draw.rect(screen, (0, 255, 0), to_rect(zombie.x, zombie.y))
                else:
                    pygame.draw.rect(screen, (150,150, 150), to_rect(zombie.x, zombie.y))

        if (enemy_blocks is not None):
            for enemy_block in enemy_blocks:
                pygame.draw.rect(screen, (255, 0, 0), to_rect(enemy_block.x, enemy_block.y))



        if (main.world.zpots is not None):
            for spawner in main.world.zpots:
                if spawner.type != 'default': continue
                pygame.draw.rect(screen, (0, 255, 255), to_rect(spawner.x, spawner.y))

        if human_controls.player_move_x is not None and human_controls.player_move_y is not None:
            pygame.draw.rect(screen, (0, 0, 0), to_rect(human_controls.player_move_x, human_controls.player_move_y, 2))

        text_surface = my_font.render(f'Brush Radius: {brush_radius}' , False, (0, 0, 0))
        screen.blit(text_surface, (0, 0))

        text_surface = my_font.render(f'Motion Reverse: {motion_reverse}', False, (0, 0, 0))
        screen.blit(text_surface, (0, 80))

        text_surface = my_font.render(f'AutoDodge: {human_controls.auto_dodge}', False, (0, 0, 0))
        screen.blit(text_surface, (0, 160))

        # Flip the display
        pygame.display.flip()




from threading import Thread




t_visual = Thread(target=visual)

t_visual.start()

main.main()