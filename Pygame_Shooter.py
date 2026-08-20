import random
from math import floor

import pygame
import math

#
#swd
#
pygame.init()


def make_enemy(n):
    if n:
        side = random.randint(1, 4)
        if side == 1:  ## LEFT
            ex = 0
            ey = random.randint(0, screenheight)
        elif side == 2:  ## TOP
            ex = random.randint(0, screenwidth)
            ey = 0
        elif side == 3:  ##RIGHT
            ex = screenwidth
            ey = random.randint(0, screenheight)
        elif side == 4:  ###BOTTOM
            ex = random.randint(0, screenwidth)
            ey = screenheight
        diff_x = x - ex
        diff_y = y - ey

        distance = (diff_x ** 2 + diff_y ** 2) ** 0.5

        edx = (diff_x / distance) * espeed
        edy = (diff_y / distance) * espeed
        enemies.append({"x": ex, "y": ey, "edx": edx, "edy": edy, "t": 0})
    else:
        enemies.append({"x": 600, "y": screenheight / 2, "edx": 0, "edy": 0, "t": 0})
def make_text(tx, ty, color, yap, size):
    font = pygame.font.SysFont("Comic Sans MS", size)
    text_surface = font.render(str(yap), True, color)
    screen.blit(text_surface, (tx, ty))

# Screen
screenwidth = 800
screenheight = 600
screen = pygame.display.set_mode((screenwidth, screenheight))

pygame.display.set_caption("Shooter Game")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)


t_rad = 25
width = t_rad
height = t_rad * 3
turret_image = pygame.image.load("Turret.png").convert_alpha()
turret_image = pygame.transform.scale(turret_image, (width, height))
rotated_turret = turret_image

arrow_image = pygame.image.load("Arrow.png").convert_alpha()
arrow_image = pygame.transform.scale(arrow_image, (90, 77))


x, y = screenwidth/2, screenheight/2
speed = 2


clock = pygame.time.Clock()
fps = 60
playing = True


move_up = move_down = move_left = move_right = False


# Bullets
bullets = []  # {"x","y","dx","dy"}
enemies = []


max_ammo = 10
ammo = max_ammo
reload_timer = 0
bullet_rad = 5
bullet_speed = 8
m_spread = 0.15
mgun = False
mgun_r = 0
mgun_r_time = fps / 15

flank = False
flank_spread = 0

espeed = 1  # how fast enemy moves
e_spawn = 0
e_spawn_ps = 3 # how much spawn per second
e_rad = 20
distance = 0


max_lives = 3
lives = 3
scene = "main"


#shop
money = 0   ############################
total_money = money
multi_cost = 100
multi_bullet = 1

spd_cost = 50
time_to_reload = 0.4

pierce = 1
pierce_cost = 150
lives_cost = 100


not_enough = 0
maxed = 0


white = (255,255,255)
black = (0,0,0)


w = a = s = d = shoot = lives_money = enemy_h = 0


rect_back = pygame.Rect(screenwidth/2 - 50, 500, 100, 50)

#settings color control
player_color = [255, 255, 255]
player_outline_width = 0
player_outline_color = [0, 255, 255]
bg_color = [0, 0, 0]
bullet_color = [255, 255, 0]
bullet_outline_width = 0
bullet_outline_color = [0, 0, 0]
enemy_color = [255, 0, 0]
enemy_outline_width = 0
enemy_outline_color = [255, 50, 50]

prev_player_color = [255, 255, 255]
prev_player_outline_width = 0
prev_player_outline_color = [0, 255, 255]
prev_bg_color = [0, 0, 0]
prev_bullet_color = [255, 255, 0]
prev_bullet_outline_width = 0
prev_bullet_outline_color = [0, 0, 0]
prev_enemy_color = [255, 0, 0]
prev_enemy_outline_width = 0
prev_enemy_outline_color = [255, 50, 50]

main_color_rect = [250, 350, 100, 100]
secondary_color_rect = [450, 350, 100, 100]


player_color_rect = pygame.Rect(200, 150, 100, 50)
enemy_color_rect = pygame.Rect(500, 150, 100, 50)
bullet_color_rect = pygame.Rect(200, 300, 100, 50)


settings_box_draw = False
settings_box = pygame.Rect(screenwidth/2 - 275, screenheight/2 - 200, 550, 390)
settings_box_exit = pygame.Rect(screenwidth/2 + 250, screenheight/2 -225, 50, 50)
settings_box_draw_task = None
settings_box_select_main = True
save_main = pygame.Rect(585, 250, 40, 40)
undo_main = pygame.Rect(525, 250, 40, 40)
turret_elevation_rect = [600, 400, 40, 40]
turret_elevation = 1

color_slider_r = screen,(255, 0, 0),[(170, 150), (425, 130), (425, 170)]
color_slider_g = screen,(0, 255, 0),[(170, 200), (425, 180), (425, 220)]
color_slider_b = screen,(0, 0, 255),[(170, 250), (425, 230), (425, 270)]

color_line_r_pos = 255
color_line_g_pos = 255
color_line_b_pos = 255
color_line_outline_pos = 0

drag_r = False
drag_g = False
drag_b = False
drag_outline = False

click = False
while playing:


    screen.fill(bg_color)
    clock.tick(fps)


    #PLAYER
    if move_left: x -= speed
    if move_right: x += speed
    if move_up: y -= speed
    if move_down: y += speed

    x = max(0 + 10, min(x, screenwidth - width - 10))
    y = max(0 + 10, min(y, screenheight - height - 10))

    turret_center_x = x + width // 2
    turret_center_y = y + height // 2
    turret_center = (turret_center_x, turret_center_y)
    #PLAYER END

    #EVENTS
    mouse_buttons = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_w, pygame.K_UP):
                move_up = True
            elif event.key in (pygame.K_s, pygame.K_DOWN):
                move_down = True
            elif event.key in (pygame.K_a, pygame.K_LEFT):
                move_left = True
            elif event.key in (pygame.K_d, pygame.K_RIGHT):
                move_right = True
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_w, pygame.K_UP):
                move_up = False
                w = 1
            elif event.key in (pygame.K_s, pygame.K_DOWN):
                move_down = False
                s = 1
            elif event.key in (pygame.K_a, pygame.K_LEFT):
                move_left = False
                a = 1
            elif event.key in (pygame.K_d, pygame.K_RIGHT):
                move_right = False
                d = 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            if ammo > 0 and mgun == False and scene != "settings":
                mouse_x, mouse_y = pygame.mouse.get_pos()

                turret_center_x = x + width // 2
                turret_center_y = y + height // 2

                dx = mouse_x - turret_center_x
                dy = mouse_y - turret_center_y
                angle = math.atan2(-dy, dx)
                ammo -= 1
                reload_timer = 0
                spread = m_spread
                if scene == "game":
                    for a in range(pierce):
                        for i in range(multi_bullet):
                            # Calculate offset without overwriting the 'spread' variable
                            random_inaccuracy = random.uniform(-0.08, 0.08)
                            offset = (i - (multi_bullet - 1) / 2) * spread
                            shot_angle = angle + offset + random_inaccuracy

                            bullets.append({
                                "x": turret_center_x,
                                "y": turret_center_y,
                                "dx": math.cos(shot_angle) * bullet_speed,
                                "dy": -math.sin(shot_angle) * bullet_speed
                            })

                            if flank:
                                f_spread = spread / 2
                                flank_spread += 1
                                if flank_spread >= 2:
                                    flank_spread = 0
                                    f_offset = (i - (multi_bullet - 1) / 2) * f_spread
                                    bullets.append({
                                        "x": turret_center_x,
                                        "y": turret_center_y,
                                        "dx": -math.cos(angle + f_offset) * bullet_speed,
                                        "dy": math.sin(angle + f_offset) * bullet_speed
                                    })
                else:
                    offset = (1 - multi_bullet // 2) * spread
                    bullets.append({"x": turret_center_x, "y": turret_center_y, "dx": math.cos(angle) * bullet_speed,
                                    "dy": -math.sin(angle) * bullet_speed})
                shoot = 1
            if scene == "settings":
                color_line_r = screen, (0, 0, 0), (170 + color_line_r_pos, 150 - color_line_r_pos / 255 * 20), (170 + color_line_r_pos, 150 + color_line_r_pos / 255 * 20), 5
                color_line_g = screen, (0, 0, 0), (170 + color_line_g_pos, 200 - color_line_g_pos / 255 * 20), (170 + color_line_g_pos, 200 + color_line_g_pos / 255 * 20), 5
                color_line_b = screen, (0, 0, 0), (170 + color_line_b_pos, 250 - color_line_b_pos / 255 * 20), (170 + color_line_b_pos, 250 + color_line_b_pos / 255 * 20), 5
                if rect_back.collidepoint(event.pos):
                    scene = "main"
                    settings_box_draw = False
                    turret_center = (screenwidth/2, screenheight/2)
                    bullets.clear()
                elif settings_box_draw:
                    if save_main.collidepoint(event.pos):
                        if settings_box_draw_task == "p_color":
                            if settings_box_select_main:
                                player_color = prev_player_color.copy()
                            else:
                                player_outline_color = prev_player_outline_color.copy()
                                player_outline_width = prev_player_outline_width
                        elif settings_box_draw_task == "e_color":
                            if settings_box_select_main:
                                enemy_color = prev_enemy_color.copy()
                            else:
                                enemy_outline_color = prev_enemy_outline_color.copy()
                                enemy_outline_width = prev_enemy_outline_width
                        elif settings_box_draw_task == "b_color":
                            if settings_box_select_main:
                                bullet_color = prev_bullet_color.copy()
                            else:
                                bullet_outline_color = prev_bullet_outline_color.copy()
                                bullet_outline_width = prev_bullet_outline_width
                    elif undo_main.collidepoint(event.pos):
                        if settings_box_draw_task == "p_color":
                            if settings_box_select_main:
                                prev_player_color = player_color.copy()
                                color_line_r_pos = player_color[0]
                                color_line_g_pos = player_color[1]
                                color_line_b_pos = player_color[2]
                            else:
                                prev_player_outline_color = player_outline_color.copy()
                                color_line_r_pos = player_outline_color[0]
                                color_line_g_pos = player_outline_color[1]
                                color_line_b_pos = player_outline_color[2]
                        elif settings_box_draw_task == "e_color":
                            if settings_box_select_main:
                                prev_enemy_color = enemy_color.copy()
                                color_line_r_pos = enemy_color[0]
                                color_line_g_pos = enemy_color[1]
                                color_line_b_pos = enemy_color[2]
                            else:
                                prev_enemy_outline_color = enemy_outline_color.copy()
                                color_line_r_pos = enemy_outline_color[0]
                                color_line_g_pos = enemy_outline_color[1]
                                color_line_b_pos = enemy_outline_color[2]
                        elif settings_box_draw_task == "b_color":
                            if settings_box_select_main:
                                prev_bullet_color = bullet_color.copy()
                                color_line_r_pos = bullet_color[0]
                                color_line_g_pos = bullet_color[1]
                                color_line_b_pos = bullet_color[2]
                            else:
                                prev_bullet_outline_color = bullet_outline_color.copy()
                                color_line_r_pos = bullet_outline_color[0]
                                color_line_g_pos = bullet_outline_color[1]
                                color_line_b_pos = bullet_outline_color[2]
                    elif pygame.Rect(170, 130, 255, 40).collidepoint(event.pos):
                        drag_r = True
                    elif pygame.Rect(170, 180, 255, 40).collidepoint(event.pos):
                        drag_g = True
                    elif pygame.Rect(170, 230, 255, 40).collidepoint(event.pos):
                        drag_b = True
                    elif pygame.Rect(main_color_rect[0],main_color_rect[1],main_color_rect[2],main_color_rect[3]).collidepoint(event.pos):
                        settings_box_select_main = True
                        if settings_box_draw_task == "p_color":
                            color_line_r_pos = prev_player_color[0]
                            color_line_g_pos = prev_player_color[1]
                            color_line_b_pos = prev_player_color[2]
                        elif settings_box_draw_task == "e_color":
                            color_line_r_pos = prev_enemy_color[0]
                            color_line_g_pos = prev_enemy_color[1]
                            color_line_b_pos = prev_enemy_color[2]
                        elif settings_box_draw_task == "b_color":
                            color_line_r_pos = prev_bullet_color[0]
                            color_line_g_pos = prev_bullet_color[1]
                            color_line_b_pos = prev_bullet_color[2]
                    elif pygame.Rect(secondary_color_rect[0],secondary_color_rect[1],secondary_color_rect[2],secondary_color_rect[3]).collidepoint(event.pos):
                        settings_box_select_main = False
                        if settings_box_draw_task == "p_color":
                            color_line_r_pos = prev_player_outline_color[0]
                            color_line_g_pos = prev_player_outline_color[1]
                            color_line_b_pos = prev_player_outline_color[2]
                        elif settings_box_draw_task == "e_color":
                            color_line_r_pos = prev_enemy_outline_color[0]
                            color_line_g_pos = prev_enemy_outline_color[1]
                            color_line_b_pos = prev_enemy_outline_color[2]
                        elif settings_box_draw_task == "b_color":
                            color_line_r_pos = prev_bullet_outline_color[0]
                            color_line_g_pos = prev_bullet_outline_color[1]
                            color_line_b_pos = prev_bullet_outline_color[2]
                    elif pygame.Rect(secondary_color_rect[0], secondary_color_rect[1] + secondary_color_rect[3] , 100, 20).collidepoint(event.pos):
                        drag_outline = True
                        settings_box_select_main = False
                    elif pygame.Rect(turret_elevation_rect[0],turret_elevation_rect[1],turret_elevation_rect[2],turret_elevation_rect[3]).collidepoint(event.pos) and click == False and settings_box_draw_task == "p_color":
                        turret_elevation +=1
                        if turret_elevation > 3:
                            turret_elevation = 1
                    elif settings_box_exit.collidepoint(event.pos):
                        settings_box_draw = False
                elif not settings_box_draw:
                    if player_color_rect.collidepoint(event.pos):
                        settings_box_draw = True
                        settings_box_draw_task = "p_color"
                        settings_box_select_main = True
                        color_line_r_pos = prev_player_color[0]
                        color_line_g_pos = prev_player_color[1]
                        color_line_b_pos = prev_player_color[2]
                        color_line_outline_pos = prev_player_outline_width
                    elif enemy_color_rect.collidepoint(event.pos):
                        settings_box_draw = True
                        settings_box_draw_task = "e_color"
                        settings_box_select_main = True
                        color_line_r_pos = prev_enemy_color[0]
                        color_line_g_pos = prev_enemy_color[1]
                        color_line_b_pos = prev_enemy_color[2]
                        color_line_outline_pos = prev_enemy_outline_width
                    elif bullet_color_rect.collidepoint(event.pos):
                        settings_box_draw = True
                        settings_box_draw_task = "b_color"
                        settings_box_select_main = True
                        color_line_r_pos = prev_bullet_color[0]
                        color_line_g_pos = prev_bullet_color[1]
                        color_line_b_pos = prev_bullet_color[2]
                        color_line_outline_pos = prev_bullet_outline_width
            click = True
        if event.type == pygame.MOUSEBUTTONUP:
            drag_r = False
            drag_g = False
            drag_b = False
            drag_outline = False
            click = False
    mouse_x, mouse_y = pygame.mouse.get_pos()

    #SETTINGS CODE
    if drag_r:
        if settings_box_draw_task == "p_color":
            if settings_box_select_main:
                prev_player_color[0] = int(color_line_r_pos)
            else:
                prev_player_outline_color[0] = int(color_line_r_pos)
        elif settings_box_draw_task == "e_color":
            if settings_box_select_main:
                prev_enemy_color[0] = int(color_line_r_pos)
            else:
                prev_enemy_outline_color[0] = int(color_line_r_pos)
        elif settings_box_draw_task == "b_color":
            if settings_box_select_main:
                prev_bullet_color[0] = int(color_line_r_pos)
            else:
                prev_bullet_outline_color[0] = int(color_line_r_pos)
        color_line_r_pos = max(0, min(255, mouse_x - 170))
    if drag_g:
        if settings_box_draw_task == "p_color":
            if settings_box_select_main:
                prev_player_color[1] = int(color_line_g_pos)
            else:
                prev_player_outline_color[1] = int(color_line_g_pos)
        elif settings_box_draw_task == "e_color":
            if settings_box_select_main:
                prev_enemy_color[1] = int(color_line_g_pos)
            else:
                prev_enemy_outline_color[1] = int(color_line_g_pos)
        elif settings_box_draw_task == "b_color":
            if settings_box_select_main:
                prev_bullet_color[1] = int(color_line_g_pos)
            else:
                prev_bullet_outline_color[1] = int(color_line_g_pos)
        color_line_g_pos = max(0, min(255, mouse_x - 170))
    if drag_b:
        if settings_box_draw_task == "p_color":
            if settings_box_select_main:
                prev_player_color[2] = int(color_line_b_pos)
            else:
                prev_player_outline_color[2] = int(color_line_b_pos)
        elif settings_box_draw_task == "e_color":
            if settings_box_select_main:
                prev_enemy_color[2] = int(color_line_b_pos)
            else:
                prev_enemy_outline_color[2] = int(color_line_b_pos)
        elif settings_box_draw_task == "b_color":
            if settings_box_select_main:
                prev_bullet_color[2] = int(color_line_b_pos)
            else:
                prev_bullet_outline_color[2] = int(color_line_b_pos)
        color_line_b_pos = max(0, min(255, mouse_x - 170))

    if drag_outline:
        if settings_box_draw_task == "p_color":
            color_line_outline_pos = max(0, min(100, mouse_x - secondary_color_rect[0]))
            prev_player_outline_width = color_line_outline_pos/10
        if settings_box_draw_task == "e_color":
            color_line_outline_pos = max(0, min(100, mouse_x - secondary_color_rect[0]))
            prev_enemy_outline_width = color_line_outline_pos/10
        if settings_box_draw_task == "b_color":
            color_line_outline_pos = max(0, min(100, mouse_x - secondary_color_rect[0]))
            prev_bullet_outline_width = color_line_outline_pos/10


    if settings_box_draw:
        color_line_r = screen, (0, 0, 0), (170 + color_line_r_pos, 150 - color_line_r_pos / 255 * 20), (170 + color_line_r_pos, 150 + color_line_r_pos / 255 * 20), 5
        color_line_g = screen, (0, 0, 0), (170 + color_line_g_pos, 200 - color_line_g_pos / 255 * 20), (170 + color_line_g_pos, 200 + color_line_g_pos / 255 * 20), 5
        color_line_b = screen, (0, 0, 0), (170 + color_line_b_pos, 250 - color_line_b_pos / 255 * 20), (170 + color_line_b_pos, 250 + color_line_b_pos / 255 * 20), 5
        pygame.draw.rect(screen, white, settings_box)
        pygame.draw.rect(screen, (255, 0, 0), settings_box_exit)

        pygame.draw.rect(screen, (0, 255, 0), save_main)
        pygame.draw.rect(screen, (255, 0, 0), undo_main)

        pygame.draw.polygon(color_slider_r[0], color_slider_r[1], color_slider_r[2])
        pygame.draw.polygon(color_slider_g[0], color_slider_g[1], color_slider_g[2])
        pygame.draw.polygon(color_slider_b[0], color_slider_b[1], color_slider_b[2])
        pygame.draw.rect(screen, black, pygame.Rect(525, 150, 100, 100))

        make_text(color_slider_r[2][0][0] + 265, color_slider_r[2][0][1] - 15, (0, 0, 0), color_line_r_pos, 20)
        make_text(color_slider_b[2][0][0] + 265, color_slider_b[2][0][1] - 15, (0, 0, 0), color_line_b_pos, 20)
        make_text(color_slider_g[2][0][0] + 265, color_slider_g[2][0][1] - 15, (0, 0, 0), color_line_g_pos, 20)

        pygame.draw.line(color_line_r[0], color_line_r[1], color_line_r[2], color_line_r[3], color_line_r[4])
        pygame.draw.line(color_line_g[0], color_line_g[1], color_line_g[2], color_line_g[3], color_line_g[4])
        pygame.draw.line(color_line_b[0], color_line_b[1], color_line_b[2], color_line_b[3], color_line_b[4])

        if settings_box_draw_task == "p_color":
            pygame.draw.rect(screen, prev_player_color, pygame.Rect(main_color_rect[0],main_color_rect[1],main_color_rect[2],main_color_rect[3]))
            pygame.draw.rect(screen, black, pygame.Rect(main_color_rect[0],main_color_rect[1],main_color_rect[2],main_color_rect[3]), 5)

            pygame.draw.rect(screen, black, pygame.Rect(turret_elevation_rect[0],turret_elevation_rect[1],turret_elevation_rect[2],turret_elevation_rect[3]))
            make_text((turret_elevation_rect[0]+turret_elevation_rect[2]/2-5),turret_elevation_rect[1]+turret_elevation_rect[3]/2-18,white,turret_elevation, 30)

            pygame.draw.rect(screen, prev_player_outline_color, pygame.Rect(secondary_color_rect[0],secondary_color_rect[1],secondary_color_rect[2],secondary_color_rect[3]))
            pygame.draw.rect(screen, black, pygame.Rect(secondary_color_rect[0],secondary_color_rect[1],secondary_color_rect[2],secondary_color_rect[3]), 5)
            pygame.draw.line(screen,black,(secondary_color_rect[0], secondary_color_rect[1] + secondary_color_rect[3] + 10),(secondary_color_rect[0] + secondary_color_rect[2],secondary_color_rect[1] + secondary_color_rect[3] + 10), 5)
            pygame.draw.circle(screen, prev_player_outline_color,(secondary_color_rect[0]+color_line_outline_pos , secondary_color_rect[1] + secondary_color_rect[3] + 10) ,10)
            preview_pos = (575, 200)
            make_text(150, 100, (0, 0, 0), "Player Color", 20)
            turret_rect = rotated_turret.get_rect(center=preview_pos)
            if turret_elevation == 3:
                pygame.draw.circle(screen, prev_player_outline_color, preview_pos, t_rad + prev_player_outline_width)
                pygame.draw.circle(screen, prev_player_color, preview_pos, t_rad)
                screen.blit(rotated_turret, turret_rect.topleft)
            if turret_elevation == 2:
                pygame.draw.circle(screen, prev_player_outline_color, preview_pos, t_rad + prev_player_outline_width)
                screen.blit(rotated_turret, turret_rect.topleft)
                pygame.draw.circle(screen, prev_player_color, preview_pos, t_rad)
            if turret_elevation == 1:
                screen.blit(rotated_turret, turret_rect.topleft)
                pygame.draw.circle(screen, prev_player_outline_color, preview_pos, t_rad + prev_player_outline_width)
                pygame.draw.circle(screen, prev_player_color, preview_pos, t_rad)
        elif settings_box_draw_task == "e_color":
            pygame.draw.rect(screen, prev_enemy_color, pygame.Rect(main_color_rect[0],main_color_rect[1],main_color_rect[2],main_color_rect[3]))
            pygame.draw.rect(screen, black, pygame.Rect(main_color_rect[0],main_color_rect[1],main_color_rect[2],main_color_rect[3]), 5)

            pygame.draw.rect(screen, prev_enemy_outline_color, pygame.Rect(secondary_color_rect[0],secondary_color_rect[1],secondary_color_rect[2],secondary_color_rect[3]))
            pygame.draw.rect(screen, black, pygame.Rect(secondary_color_rect[0],secondary_color_rect[1],secondary_color_rect[2],secondary_color_rect[3]), 5)
            pygame.draw.line(screen,black,(secondary_color_rect[0], secondary_color_rect[1] + secondary_color_rect[3] + 10),(secondary_color_rect[0] + secondary_color_rect[2],secondary_color_rect[1] + secondary_color_rect[3] + 10), 5)
            pygame.draw.circle(screen, prev_enemy_outline_color,(secondary_color_rect[0]+color_line_outline_pos , secondary_color_rect[1] + secondary_color_rect[3] + 10) ,10)
            make_text(150, 100, (0, 0, 0), "Enemy Color", 20)

            pygame.draw.circle(screen, prev_enemy_outline_color, (575, 200), e_rad + prev_enemy_outline_width)
            pygame.draw.circle(screen, prev_enemy_color, (575, 200), e_rad)
        elif settings_box_draw_task == "b_color":
            pygame.draw.rect(screen, prev_bullet_color, pygame.Rect(main_color_rect[0],main_color_rect[1],main_color_rect[2],main_color_rect[3]))
            pygame.draw.rect(screen, black, pygame.Rect(main_color_rect[0],main_color_rect[1],main_color_rect[2],main_color_rect[3]), 5)

            pygame.draw.rect(screen, prev_bullet_outline_color, pygame.Rect(secondary_color_rect[0],secondary_color_rect[1],secondary_color_rect[2],secondary_color_rect[3]))
            pygame.draw.rect(screen, black, pygame.Rect(secondary_color_rect[0],secondary_color_rect[1],secondary_color_rect[2],secondary_color_rect[3]), 5)
            pygame.draw.line(screen,black,(secondary_color_rect[0], secondary_color_rect[1] + secondary_color_rect[3] + 10),(secondary_color_rect[0] + secondary_color_rect[2],secondary_color_rect[1] + secondary_color_rect[3] + 10), 5)
            pygame.draw.circle(screen, prev_bullet_outline_color,(secondary_color_rect[0]+color_line_outline_pos , secondary_color_rect[1] + secondary_color_rect[3] + 10) ,10)
            make_text(150, 100, (0, 0, 0), "Bullet Color", 20)

            pygame.draw.circle(screen, prev_bullet_outline_color, (575, 200), bullet_rad + prev_bullet_outline_width)
            pygame.draw.circle(screen, prev_bullet_color, (575, 200), bullet_rad)

    #SETTINGS CODE END

    # GAME LOGIC
    mgun_r += 1
    if mouse_buttons[0] and mgun and mgun_r > mgun_r_time:
        mgun_r = 0
        mouse_x, mouse_y = pygame.mouse.get_pos()

        turret_center_x = x + width // 2
        turret_center_y = y + height // 2

        dx = mouse_x - turret_center_x
        dy = mouse_y - turret_center_y
        angle = math.atan2(-dy, dx)
        ammo -= 1
        reload_timer = 0
        spread = m_spread
        if scene == "game":
            for a in range(pierce):
                for i in range(multi_bullet):
                    offset = (
                                     i - multi_bullet // 2) * spread  #####  I think sin and cos translates angle and spd to lik movement(dx,dy) or smth
                    shot_angle = angle + offset + random.uniform(-0.08, 0.08)
                    bullets.append(
                        {"x": turret_center_x, "y": turret_center_y, "dx": math.cos(shot_angle) * bullet_speed,
                         "dy": -math.sin(shot_angle) * bullet_speed})
                    if flank:
                        f_spread = spread / 2
                        flank_spread += 1
                        if flank_spread >= 2:
                            flank_spread = 0
                            offset = (i - multi_bullet // 2) * f_spread
                            bullets.append({"x": turret_center_x, "y": turret_center_y,
                                            "dx": -math.cos(angle + offset) * bullet_speed,
                                            "dy": math.sin(angle + offset) * bullet_speed})
        else:

            offset = (1 - multi_bullet // 2) * spread
            bullets.append({"x": turret_center_x, "y": turret_center_y, "dx": math.cos(angle) * bullet_speed,
                            "dy": -math.sin(angle) * bullet_speed})
        shoot = 1
    if scene == "game":
        e_spawn += 1
        if e_spawn >= fps / e_spawn_ps:
            make_enemy(True)
            e_spawn = 0
    if lives <= 0:
        for bullet in bullets[:]:
            bullets.remove(bullet)
        scene = "main"
        lives = max_lives


    # RELOAD
    reload_timer += 1
    if reload_timer > time_to_reload * fps and ammo < max_ammo:
        ammo += 1
        reload_timer = 0
    #RELOAD END

    #GAME LOGIC END
    #SHOP
    if settings_box_draw or scene != "settings":
        turret_center_x = turret_center[0]
        turret_center_y = turret_center[1]
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if settings_box_draw:
            preview_pos = [575, 200]

            # I got this online      the angle thing


            dx = mouse_x - preview_pos[0]
            dy = mouse_y - preview_pos[1]
            angle = math.degrees(math.atan2(-dy, dx))  #########dis too

            rotated_turret = pygame.transform.rotate(turret_image, angle - 90)
        else:
            # I got this online      the angle thing

            dx = mouse_x - turret_center_x
            dy = mouse_y - turret_center_y
            angle = math.degrees(math.atan2(-dy, dx))  #########dis too

            rotated_turret = pygame.transform.rotate(turret_image, angle - 90)
            turret_cir = pygame.draw.circle(screen, white, turret_center, t_rad)
    if not_enough > 0:
        make_text(200, 50, white, "Not Enough Money!", 50)
        not_enough -= 1
    if maxed > 0:
        make_text(screenwidth / 2 - 75, 50, white, "Max!", 50)
        maxed -= 1
    #SHOP END

    if scene == "main":
        rect_play = pygame.Rect(350, 200, 100, 50)
        rect_how = pygame.Rect(500, 200, 100, 50)
        rect_shop = pygame.Rect(200, 200, 100, 50)
        rect_settings = pygame.Rect(600, 500, 100, 50)
        pygame.draw.rect(screen, white, rect_play)
        pygame.draw.rect(screen, white, rect_how)
        pygame.draw.rect(screen, white, rect_shop)
        pygame.draw.rect(screen, white, rect_settings)
        make_text(375, 200, black, "Play", 30)
        make_text(510, 205, black, "How 2?", 25)
        make_text(215, 200, black, "Shop", 30)
        make_text(600, 500, black, "Settings", 20)
        enemies.clear()
    if scene == "shop":
        # multi shot
        rect_upg_multi_s = pygame.Rect(200, 150, 100, 50)
        pygame.draw.rect(screen, white, rect_upg_multi_s)
        make_text(205, 150, black, "Multishot", 20)
        if multi_bullet < 13:
            make_text(205, 170, black, f"{multi_cost}$", 10)
            make_text(205, 180, black, f"{multi_bullet} -> {multi_bullet + 2}", 10)

        if multi_bullet == 13 and not flank:
            multi_cost = 5000
            make_text(205, 170, black, "???", 10)
            make_text(205, 180, black, f"{multi_cost}", 10)

        if multi_bullet > 13 or flank:
            make_text(205, 170, black, "Sold", 20)

        # atk speed
        rect_upg_atk_spd = pygame.Rect(500, 150, 100, 50)
        pygame.draw.rect(screen, white, rect_upg_atk_spd)
        make_text(505, 150, black, "Atk Speed", 20)
        if time_to_reload > 0.2:
            make_text(505, 170, black, f"{spd_cost}$", 10)
            make_text(505, 180, black, f"{time_to_reload} -> {floor(100 * time_to_reload - 5) / 100}", 10)

        if floor(time_to_reload * 100) / 100 == 0.2:
            spd_cost = 10000
            make_text(505, 170, black, "???", 10)
            make_text(505, 180, black, f"{spd_cost}$", 10)

        if time_to_reload < 0.19 and spd_cost == 10000:
            make_text(505, 170, black, "Sold", 20)

        # Pierce
        rect_upg_pierce = pygame.Rect(500, 350, 100, 50)
        pygame.draw.rect(screen, white, rect_upg_pierce)
        make_text(505, 350, black, "Pierce", 20)
        if pierce < 5:
            make_text(505, 370, black, f"{pierce_cost}$", 10)
            make_text(505, 380, black, f"{pierce} -> {pierce + 2}", 10)

        elif pierce >= 5:
            make_text(505, 370, black, "Sold", 20)

        # lives
        rect_upg_lives = pygame.Rect(200, 350, 100, 50)
        pygame.draw.rect(screen, white, rect_upg_lives)
        make_text(205, 350, black, "Lives", 20)
        if max_lives < 8:
            make_text(205, 370, black, f"{lives_cost}$", 10)
            make_text(205, 380, black, f"{max_lives} -> {max_lives + 1}", 10)

        if max_lives >= 8:
            make_text(205, 370, black, "Sold", 20)

        make_text(50, 50, white, str(round(money)) + "$", 30)

        pygame.draw.rect(screen, white, rect_back)
        make_text(screenwidth / 2 - 50, 500, black, "Back", 30)
    if scene == "game":
        e_spawn_ps = 3 + total_money / 400
        if e_spawn_ps > 75:
            e_spawn_ps = 75
        espeed = 1 + total_money / 500
        if espeed > 4:
            espeed = 4
        turret_center = (x + width // 2, y + height // 2)
        make_text(50, 50, white, lives, 30)
        make_text(x, y, black, ammo, 20)
    if scene == "how":
        if w == 0:
            make_text(180, 50, white, "Press [w] or UP ARROW to go up.", 30)
        elif w == 1 and a == 0:
            make_text(180, 50, white, "Press [a] or LEFT ARROW to go left.", 30)
        elif a == 1 and s == 0:
            make_text(180, 50, white, "Press [s] or DOWN ARROW to go down.", 30)
        elif s == 1 and d == 0:
            make_text(180, 50, white, "Press [d] or RIGHT ARROW to go right.", 30)
        elif w == a == s == d == 1 and shoot != 1:
            make_text(180, 50, white, "Press mouse to shoot.", 30)
        elif w == a == s == d == shoot == 1 and enemy_h == 0:
            screen.blit(arrow_image, (100, 50))
            screen.blit(arrow_image, (x + 50, y))
            make_text(50, 50, white, str(money) + "$", 30)
            make_text(200, 50, white, "Right now it is money, in a game it is lives!", 20)
            make_text(x + 100, y, white, "Ammo", 30)
            pygame.draw.rect(screen, white, rect_back)
            make_text(screenwidth / 2 - 50, 500, black, "Next", 30)
        elif w == a == s == d == shoot == 1 and enemy_h == 1:
            x, y = screenwidth / 2, screenheight / 2
            make_text(50, 50, white, str(money) + "$", 30)
            make_text(250, 50, white, "Shoot at it.", 50)
        elif w == a == s == d == shoot == 1 and enemy_h == 2:
            screen.blit(arrow_image, (100, 50))
            make_text(50, 50, white, str(money) + "$", 30)
            make_text(200, 50, white, "LOOK! You got a buck!", 20)
            pygame.draw.rect(screen, white, rect_back)
            make_text(screenwidth / 2 - 50, 500, black, "Back", 30)

        elif enemy_h == 2:
            pygame.draw.rect(screen, white, rect_back)
            make_text(screenwidth / 2 - 50, 500, black, "Back", 30)
    if scene == "settings":
        pygame.draw.rect(screen, white, rect_back)
        make_text(screenwidth / 2 - 50, 500, black, "Back", 30)
        make_text(screenwidth / 2 - 250, 50, white, "Outlines are not counted as hitboxes!", 30)
        if not settings_box_draw:
            pygame.draw.rect(screen, white, player_color_rect)
            make_text(205, 150, black, "Player", 20)
            make_text(205, 175, black, "Color", 20)

            pygame.draw.rect(screen, white, enemy_color_rect)
            make_text(505, 150, black, "Enemy", 20)
            make_text(505, 175, black, "Color", 20)

            pygame.draw.rect(screen, white, bullet_color_rect)
            make_text(205, 300, black, "Bullet", 20)
            make_text(205, 325, black, "Color", 20)

            enemies.clear()
    for enemy in enemies[:]:
        enemy["x"] += enemy["edx"]
        enemy["y"] += enemy["edy"]
        enemy["t"] += 1

        if enemy["t"] >= 20:
            # off-screen cleanup
            if (enemy["x"] < 0 or enemy["x"] > screenwidth or
                    enemy["y"] < 0 or enemy["y"] > screenheight):
                enemies.remove(enemy)
                continue

            # draw enemy
        pygame.draw.circle(screen, enemy_outline_color, (int(enemy["x"]), int(enemy["y"])),e_rad+enemy_outline_width)
        pygame.draw.circle(screen, enemy_color, (int(enemy["x"]), int(enemy["y"])), e_rad)

        # player collision
        dx = enemy["x"] - turret_center_x
        dy = enemy["y"] - turret_center_y
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance <= e_rad + t_rad:
            enemies.remove(enemy)
            lives -= 1
            enemy_h = 2
    for bullet in bullets[:]:
        bullet["x"] += bullet["dx"]
        bullet["y"] += bullet["dy"]

        if bullet["x"] < 0 or bullet["x"] > screenwidth or bullet["y"] < 0 or bullet["y"] > screenheight:
            bullets.remove(bullet)
            continue

        bullet["rect"] = pygame.Rect(int(bullet["x"]) - bullet_rad, int(bullet["y"]) - bullet_rad, bullet_rad * 2, bullet_rad * 2)

        pygame.draw.circle(screen, bullet_outline_color, bullet["rect"].center, bullet_rad + bullet_outline_width)
        pygame.draw.circle(screen, bullet_color, bullet["rect"].center, bullet_rad)

        if scene == "main" or scene == "shop" or scene == "game" or scene == "how":
            if scene == "main":
                if bullet["rect"].colliderect(rect_shop):
                    scene = "shop"
                    bullets.remove(bullet)
                    continue

                elif bullet["rect"].colliderect(rect_play):
                    scene = "game"
                    ammo = max_ammo
                    lives = max_lives
                    reload_timer = 0
                    bullets.remove(bullet)
                    continue

                elif bullet["rect"].colliderect(rect_how):
                    w = 0
                    a = 0
                    s = 0
                    d = 0
                    shoot = 0
                    lives_money = 0
                    enemy_h = 0
                    scene = "how"
                    bullets.remove(bullet)
                    continue

                elif bullet["rect"].colliderect(rect_settings):
                    scene = "settings"
            if scene == "shop":
                if bullet["rect"].colliderect(rect_upg_multi_s):
                    if money >= multi_cost and not flank:
                        if multi_bullet < 13:
                            money -= multi_cost
                            multi_cost = floor(multi_cost ** 1.1)
                            multi_bullet += 2
                        elif multi_bullet == 13:
                            flank = True

                    elif multi_bullet > 13 or flank:
                        maxed = fps * 3

                    else:
                        not_enough = fps * 3

                    bullets.remove(bullet)
                    continue
                elif bullet["rect"].colliderect(rect_upg_atk_spd):
                    if money >= spd_cost and time_to_reload != 0.01:
                        if time_to_reload > 0.2:
                            money -= spd_cost
                            spd_cost = floor(spd_cost ** 1.3)
                            time_to_reload = (floor((time_to_reload - 0.05) * 100)) / 100

                        elif floor(time_to_reload * 100) / 100 == 0.2:
                            mgun = True
                            m_spread = 0.1
                            money -= spd_cost
                            time_to_reload = 0.01

                    elif time_to_reload < 0.2:
                        maxed = fps * 3

                    else:
                        not_enough = fps * 3

                    bullets.remove(bullet)
                    continue
                elif bullet["rect"].colliderect(rect_upg_pierce):
                    if money >= pierce_cost:
                        if pierce < 5:
                            money -= pierce_cost
                            pierce_cost = floor(pierce_cost + 50)
                            pierce += 1
                    elif pierce >= 5:
                        maxed = fps * 3
                    else:
                        not_enough = fps * 3
                    bullets.remove(bullet)
                    continue
                elif bullet["rect"].colliderect(rect_upg_lives):
                    if money >= lives_cost:
                        if max_lives < 8:
                            money -= lives_cost
                            lives_cost = floor(lives_cost * 2)
                            max_lives += 1

                    elif max_lives >= 8:
                        maxed = fps * 3

                    else:
                        not_enough = fps * 3
                    bullets.remove(bullet)

                    continue
                elif bullet["rect"].colliderect(rect_back):
                    scene = "main"
                    bullets.remove(bullet)
                    not_enough = 0
                    continue
            if scene == "game" or scene == "how":
                for enemy in enemies[:]:
                    dx = bullet["x"] - enemy["x"]
                    dy = bullet["y"] - enemy["y"]
                    distance = (dx ** 2 + dy ** 2) ** 0.5

                    if distance <= bullet_rad + e_rad:
                        bullets.remove(bullet)
                        enemies.remove(enemy)
                        money += round(1 + total_money / 500, 0)
                        total_money += round(1 + total_money / 500, 0)
                        enemy_h = 2
                        break
            if scene == "how":
                if bullet["rect"].colliderect(rect_back):
                    if enemy_h == 0:
                        make_enemy(False)
                        enemy_h = 1

                    if enemy_h == 2:
                        scene = "main"

                    bullets.remove(bullet)
                    continue
        else:
            bullets.clear()

    if scene != "settings":
        turret_rect = rotated_turret.get_rect(center=turret_center)
        if turret_elevation == 3:
            pygame.draw.circle(screen, (player_outline_color[0], player_outline_color[1], player_outline_color[2]),turret_center, t_rad + player_outline_width)
            pygame.draw.circle(screen, (player_color[0],player_color[1],player_color[2]), turret_center, t_rad)
            screen.blit(rotated_turret, turret_rect.topleft)
        elif turret_elevation == 2:
            pygame.draw.circle(screen, (player_outline_color[0], player_outline_color[1], player_outline_color[2]),turret_center, t_rad + player_outline_width)
            screen.blit(rotated_turret, turret_rect.topleft)
            pygame.draw.circle(screen, (player_color[0],player_color[1],player_color[2]), turret_center, t_rad)

        elif turret_elevation == 1:
            screen.blit(rotated_turret, turret_rect.topleft)
            pygame.draw.circle(screen, (player_outline_color[0], player_outline_color[1], player_outline_color[2]),turret_center, t_rad + player_outline_width)
            pygame.draw.circle(screen, (player_color[0],player_color[1],player_color[2]), turret_center, t_rad)

        make_text(x + t_rad / 12.5 - 2.5, y + t_rad / 3, black, ammo, 30)

    pygame.display.update()
pygame.quit()
