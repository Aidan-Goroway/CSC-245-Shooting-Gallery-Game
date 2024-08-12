"""
This program is a shooting gallery game.
"""

import random

from Images_Sfx import *
import Cowboy
import Can

def run_game():
    """
    Does this really need a docstring?
    """

    pygame.init()

    width = 1200  # grid game by units of 5 only
    height = 765
    my_win = pygame.display.set_mode((width, height))

    # Objects and Initialization

    clock = pygame.time.Clock()
    fps = 60
    current_time = 0
    over_time = 60 * 1000  # milliseconds
    time_left = int(over_time / 1000)
    frame_total = 0
    final_frame = time_left * fps  # 60 frames/second

    ammo_count = 6
    score = 0
    hitmarker_location = -1000,-1000

    position_list = [0,1,2,3,4,5,6,7,8]
    ran_positions(position_list)
    cycle_time = time_left - 3
    ran_can = random.randrange(5, time_left - 5)
    ran_can_y = random.randrange(0, 90)

    # The game loop starts here.
    # INITIALIZE 9 COWBOYS (and a can of heinz beans)
    r1c1 = Cowboy.Cowboy(200, 540, False, CBclean1,CBhurt1, 57)
    r2c1 = Cowboy.Cowboy(200, 390, False, CBclean2,CBhurt2, 57)
    r3c1 = Cowboy.Cowboy(200, 240, False, CBclean3,CBhurt3, 57)

    r1c2 = Cowboy.Cowboy(600, 540, False, CBclean1,CBhurt1, 57)
    r2c2 = Cowboy.Cowboy(600, 390, False, CBclean2,CBhurt2, 57)
    r3c2 = Cowboy.Cowboy(600, 240, False, CBclean3,CBhurt3, 57)

    r1c3 = Cowboy.Cowboy(1000, 540, False, CBclean1,CBhurt1, 57)
    r2c3 = Cowboy.Cowboy(1000, 390, False, CBclean2,CBhurt2, 57)
    r3c3 = Cowboy.Cowboy(1000, 240, False, CBclean3,CBhurt3, 57)
    cowboy_list = [r1c1,r1c2,r1c3,r2c1,r2c2,r2c3,r3c1,r3c2,r3c3]

    can = Can.Can(-300,50,Can1,Can2,Can3,Can4,0)
    pygame.mixer.music.load("../Final Project (Attempt 2)/Assets/075.-Fast-Paced-Popguns-_-Quick-Draw-Kirby.wav")
    pygame.mixer.music.play(-1)

    keep_going = True
    while (keep_going):

        # 1. Handle events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_going = False

            if event.type != pygame.MOUSEBUTTONDOWN: # when moving mouse
                mousepos = pygame.mouse.get_pos()
                crosshair_position = (mousepos[0] - 50, mousepos[1] - 50)

            if event.type == pygame.MOUSEBUTTONDOWN:  # when clicking
                ammo_count -= 1
                if ammo_count < 0:
                    ammo_count = -1

                if not ((mousepos[0] >= 290) and (mousepos[0] <= 385) and
                        (mousepos[1] >= 655) and (mousepos[1] <= 750)) and ammo_count >= 0:
                    pygame.mixer.Sound.play(Shoot_sfx)

                if (mousepos[0] >= 290) and (mousepos[0] <= 385) and \
                        (mousepos[1] >= 655) and (mousepos[1] <= 750):
                    # reload
                    pygame.mixer.Sound.play(Reload_sfx)
                    ammo_count = 6

                if (mousepos[0] >= can.x) and (mousepos[0] <= can.x + 100) and \
                        (mousepos[1] >= can.y) and (mousepos[1] <= can.y + 100) and ammo_count >= 0:
                    pygame.mixer.Sound.play(Snipe_sfx)
                    score += 1000

                if not (340 >= mousepos[1] >= 240) and \
                        not (490 >= mousepos[1] >= 390) and \
                        not (640 >= mousepos[1] >= 540):

                    for cowboy in cowboy_list:
                        if (cowboy.x <= mousepos[0] <= cowboy.x + 100) and (cowboy.y <= mousepos[1] <= cowboy.y + 100) and ammo_count >= 0:
                            cowboy.get_shot()
                            score += 10

                hitmarker_location = (mousepos[0] - 50, mousepos[1] - 50)



        # 2. Apply rules of game world

        superspawn(r1c1, r2c1, r3c1, r1c2, r2c2, r3c2, r1c3, r2c3, r3c3, my_win)  # spawn first so they exist, but arent seen.

        my_win.blit(BG, [0, 0])  # spawn next so background hides initial spawns
        my_win.blit(HUD, [0, height - 125])  # the first blits, all others will layer OVER this

        # 3. Simulate the world
        # print(frame_total)

        if frame_total % 180 == 0 and frame_total != 0: # RANDOMIZE POSITIONS
            ran_positions(position_list)
            cycle_time = time_left # Sets a consistent schedule for the cycle
            for cowboy in cowboy_list:
                if cowboy.hit_status:
                    cowboy.base_sprite,cowboy.hit_sprite = cowboy.hit_sprite,cowboy.base_sprite
                    cowboy.hit_status = False

        super_cycle(r1c1,r1c2,r1c3,r2c1,r2c2,r2c3,r3c1,r3c2,r3c3,
                    position_list[0],position_list[1],position_list[2],position_list[3],
                    position_list[4],position_list[5],position_list[6],position_list[7],position_list[8],
                    0,400,800,540,390,240,time_left,cycle_time,cycle_time - 1, my_win)

        if time_left == ran_can + 2:
            my_win.blit(WarningGraphic, (100, ran_can_y) )

        if time_left <= ran_can:
            can.fly(ran_can_y,frame_total,my_win)

        if event.type == pygame.MOUSEBUTTONDOWN:  # HITMARKER
            for cowboy in cowboy_list:
                if (cowboy.x <= mousepos[0] <= cowboy.x + 100) and (cowboy.y <= mousepos[1] <= cowboy.y + 100) and ammo_count >= 0:
                    my_win.blit(Hitmarker, hitmarker_location)

            if (mousepos[0] >= can.x) and (mousepos[0] <= can.x + 100) and \
                    (mousepos[1] >= can.y) and (mousepos[1] <= can.y + 100) and ammo_count >= 0:
                my_win.blit(Hitmarker, hitmarker_location)

        # 4. Draw frame

        bullet_count(ammo_count,width,height,my_win)

        my_win.blit(Visual_Crosshair, crosshair_position)  # this should be the last blit

        # Swap display

        current_time = pygame.time.get_ticks()  # our global timer. Counts up from 0 to 60000

        clock.tick(fps)

        frame_total += 1  # a sort of frame, not quite 100% accurate(?), but good enough. Reaches 3600 by the games end
        if frame_total % 60 == 0:
            time_left -= 1

        time_text = pygame.font.SysFont('Goudy Stout', 48)
        time_text_surface = time_text.render(str(time_left), False, 'black')
        my_win.blit(time_text_surface, (0 + 595, height - 72))

        score_text = pygame.font.SysFont('Goudy Stout', 36)
        score_text_surface = score_text.render(str(score), False, 'black')
        my_win.blit(score_text_surface, (740, height - 85))

        pygame.display.update()

        if current_time > over_time:  # sends game to pygame.quit()
            keep_going = False

    # The game loop ends here.
    pygame.quit()
    print(f'Final score: {score}!')

def bullet_count(ammo_count,width,height,window):
    """
    Keeps track of ammo usage.
    :param ammo_count: Your ammo_count.
    :param width: screen width.
    :param height: screen height (from the top down)
    :param window: blitting window
    """
    if ammo_count == 6:
        window.blit(Bullet6, [0 + 390, height - 100])
    if ammo_count == 5:
        window.blit(Bullet5, [0 + 390, height - 100])
    if ammo_count == 4:
        window.blit(Bullet4, [0 + 390, height - 100])
    if ammo_count == 3:
        window.blit(Bullet3, [0 + 390, height - 100])
    if ammo_count == 2:
        window.blit(Bullet2, [0 + 390, height - 100])
    if ammo_count == 1:
        window.blit(Bullet1, [0 + 390, height - 100])

def ran_positions(position_list):
    """
    randomizes the x positions of each cowboy.
    :param position_list: The positions being randomized, in a list.
    :return: The now randomized list.
    """
    position_list[0] = random.randrange(0, 400 - 100)
    position_list[1] = random.randrange(400, 800 - 100)
    position_list[2] = random.randrange(800, 1200 - 100)

    position_list[3] = random.randrange(0, 400 - 100)
    position_list[4] = random.randrange(400, 800 - 100)
    position_list[5] = random.randrange(800, 1200 - 100)

    position_list[6] = random.randrange(0, 400 - 100)
    position_list[7] = random.randrange(400, 800 - 100)
    position_list[8] = random.randrange(800, 1200 - 100)
    return position_list

def superspawn(c1,c2,c3,c4,c5,c6,c7,c8,c9,window):
    """
    Spanws all 9 cowboys.
    """
    c1.spawn(window)
    c2.spawn(window)
    c3.spawn(window)
    c4.spawn(window)
    c5.spawn(window)
    c6.spawn(window)
    c7.spawn(window)
    c8.spawn(window)
    c9.spawn(window)


def r1_super_up(c1,c2,c3,x1, x2, x3, time_left, start_time, pause_time, window):
    """
    Moves all cowboys in row 1 up.
    """
    c1.cycle_move_up(x1, time_left, start_time, pause_time, window)
    c2.cycle_move_up(x2, time_left, start_time, pause_time, window)
    c3.cycle_move_up(x3, time_left, start_time, pause_time, window)

def r1_super_down(c1,c2,c3,x1, x2, x3, time_left, start_time, pause_time, window):
    """
    Moves all cowboys in row 1 down.
    """
    c1.cycle_move_down(x1, time_left, start_time, pause_time, window)
    c2.cycle_move_down(x2, time_left, start_time, pause_time, window)
    c3.cycle_move_down(x3, time_left, start_time, pause_time, window)

def r2_super_up(c4,c5,c6,x4, x5, x6, time_left, start_time, pause_time, window):
    """
        Moves all cowboys in row 2 up.
        """
    c4.cycle_move_up(x4, time_left, start_time, pause_time, window)
    c5.cycle_move_up(x5, time_left, start_time, pause_time, window)
    c6.cycle_move_up(x6, time_left, start_time, pause_time, window)

def r2_super_down(c4,c5,c6,x4, x5, x6, time_left, start_time, pause_time, window):
    """
        Moves all cowboys in row 2 down.
        """
    c4.cycle_move_down(x4, time_left, start_time, pause_time, window)
    c5.cycle_move_down(x5, time_left, start_time, pause_time, window)
    c6.cycle_move_down(x6, time_left, start_time, pause_time, window)

def r3_super_up(c7,c8,c9,x7, x8, x9, time_left, start_time, pause_time, window):
    """
        Moves all cowboys in row 3 up.
        """
    c7.cycle_move_up(x7, time_left, start_time, pause_time, window)
    c8.cycle_move_up(x8, time_left, start_time, pause_time, window)
    c9.cycle_move_up(x9, time_left, start_time, pause_time, window)

def r3_super_down(c7,c8,c9,x7, x8, x9, time_left, start_time, pause_time, window):
    """
        Moves all cowboys in row 3 down.
        """
    c7.cycle_move_down(x7, time_left, start_time, pause_time, window)
    c8.cycle_move_down(x8, time_left, start_time, pause_time, window)
    c9.cycle_move_down(x9, time_left, start_time, pause_time, window)


def r1_sandblit(x1,x2,x3,y,window):
    """
    blits the row1 sandbars
    """
    window.blit(Sandbar, (x1, y))
    window.blit(Sandbar, (x2, y))
    window.blit(Sandbar, (x3, y))

def r2_sandblit(x1,x2,x3,y,window):
    """
        blits the row2 sandbars
        """
    window.blit(Sandbar, (x1, y))
    window.blit(Sandbar, (x2, y))
    window.blit(Sandbar, (x3, y))

def r3_sandblit(x1,x2,x3,y,window):
    """
        blits the row2 sandbars
        """
    window.blit(Sandbar, (x1, y))
    window.blit(Sandbar, (x2, y))
    window.blit(Sandbar, (x3, y))


def super_cycle(r1c1,r1c2,r1c3,r2c1,r2c2,r2c3,r3c1,r3c2,r3c3,
                pos0,pos1,pos2,pos3,pos4,pos5,pos6,pos7,pos8,
                sandx1,sandx2,sandx3,sandy1,sandy2,sandy3,
                time_left,start_time,end_time,window):
    """
    Combines all prior methods to a supermethod that accomplishes all tasks in one call.
    I'm not writting out every parameter for this.
    """

    r1_super_up(r1c1,r1c2,r1c3,pos0,pos1,pos2,time_left,start_time,end_time,window)
    r1_super_down(r1c1,r1c2,r1c3,pos0,pos1,pos2,time_left,start_time-1,end_time-1,window)
    r1_sandblit(sandx1,sandx2,sandx3,sandy1,window)

    r2_super_up(r2c1,r2c2,r2c3,pos3,pos4,pos5,time_left,start_time,end_time, window)
    r2_super_down(r2c1,r2c2,r2c3,pos3,pos4,pos5,time_left,start_time-1,end_time-1,window)
    r2_sandblit(sandx1,sandx2,sandx3,sandy2,window)

    r3_super_up(r3c1,r3c2,r3c3,pos6,pos7,pos8,time_left,start_time,end_time, window)
    r3_super_down(r3c1,r3c2,r3c3,pos6,pos7,pos8,time_left,start_time-1,end_time-1,window)
    r3_sandblit(sandx1,sandx2,sandx3,sandy3,window)


# Start game
run_game()
