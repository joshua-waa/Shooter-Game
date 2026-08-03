import random
from math import floor

import pygame
import math

#
#swd
#
pygame.init()

# Screen
screenwidth = 800
screenheight = 600
screen = pygame.display.set_mode((screenwidth, screenheight))




t_rad = 25
width = t_rad
height = t_rad * 3
turrent_image = pygame.image.load("turrent.png").convert_alpha()
turrent_image = pygame.transform.scale(turrent_image, (width, height))
rotated_turrent = turrent_image

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
enemys = []


max_ammo = 10
ammo = max_ammo
reload_timer = 0
ammo_rad = 5
bullet_speed = 8
mspread = 0.15
mgun = False
mgun_r = 0
mgun_r_time = fps / 15

flank = False
flankspread = 0

espeed = 1  # how fast enemy moves
e_spawn = 0
e_spawn_ps = 3 # how many spawn per second
e_rad = 20
distance = 0


max_lives = 3
lives = 3
scene = "main"


#shop
money = 0    ############################
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
player_outline = False
player_outline_color = (0, 255, 255)
bg_color = (0, 0, 0)
bullet_color = (255, 255, 0)
bullet_outline = False
bullet_outline_color = (0, 0, 0)
enemy_color = (255, 0, 0)
enemy_outline = False
enemy_outline_color = (255, 50, 50)

player_color_rect = pygame.Rect(200, 150, 100, 50)

settings_box_draw = False
settings_box = pygame.Rect(screenwidth/2 - 275, screenheight/2 - 200, 550, 390)
settings_box_exit = pygame.Rect(screenwidth/2 + 250, screenheight/2 -225, 50, 50)
settings_box_draw_task = None
save_main = pygame.Rect(585, 250, 40, 40)
undo_main = pygame.Rect(525, 250, 40, 40)

color_slider_r = screen,(255, 0, 0),[(170, 150), (425, 130), (425, 170)]
color_slider_g = screen,(0, 255, 0),[(170, 200), (425, 180), (425, 220)]
color_slider_b = screen,(0, 0, 255),[(170, 250), (425, 230), (425, 270)]

color_line_r_pos = 255
color_line_g_pos = 255
color_line_b_pos = 255

drag_r = False
drag_g = False
drag_b = False

prev_player_color = [255, 255, 255]
while playing:
    color_line_r = screen, (0, 0, 0), (170 + color_line_r_pos, 150 - color_line_r_pos / 255 * 20), (170 + color_line_r_pos, 150 + color_line_r_pos / 255 * 20), 5
    color_line_g = screen, (0, 0, 0), (170 + color_line_g_pos, 200 - color_line_g_pos / 255 * 20 ), (170 + color_line_g_pos, 200 + color_line_g_pos / 255 * 20), 5
    color_line_b = screen, (0, 0, 0), (170 + color_line_b_pos, 250 - color_line_b_pos / 255 * 20 ), (170 + color_line_b_pos, 250 + color_line_b_pos / 255 * 20), 5
    screen.fill(bg_color)
    clock.tick(fps)

    e_spawn_ps = 3 + total_money / 400
    if e_spawn_ps > 75:
        e_spawn_ps = 75
    espeed= 1 + total_money / 500
    if espeed > 2.5:
        espeed = 4


    #MOVEMENT
    if move_left: x -= speed
    if move_right: x += speed
    if move_up: y -= speed
    if move_down: y += speed

    x = max(0 + 10, min(x, screenwidth - width - 10))
    y = max(0 + 10, min(y, screenheight - height - 10))

    turrent_center_x = x + width // 2
    turrent_center_y = y + height // 2
    turrent_center = (turrent_center_x, turrent_center_y)

    def make_enemy(n):
        if n:
            side=random.randint(1,4)
            if side == 1:  ## LEFT
                ex = 0
                ey = random.randint(0,screenheight)
            elif side == 2:   ## TOP
                ex = random.randint(0,screenwidth)
                ey = 0
            elif side == 3: ##RIGHT
                ex = screenwidth
                ey = random.randint(0, screenheight)
            elif side == 4: ###BOTTOM
                ex = random.randint(0,screenwidth)
                ey = screenheight
            diff_x = x - ex
            diff_y = y - ey

            distance = (diff_x ** 2 + diff_y ** 2) ** 0.5

            edx = (diff_x / distance) * espeed
            edy = (diff_y / distance) * espeed
            enemys.append({"x": ex, "y": ey,"edx": edx, "edy": edy ,"t":0 })
        else:
            enemys.append({"x": 600, "y": screenheight/2, "edx": 0, "edy": 0, "t": 0})
    def make_text(tx,ty,color,yap,size):
        font = pygame.font.SysFont("Comic Sans MS", size)
        text_surface = font.render(str(yap), True, color)
        screen.blit(text_surface, (tx, ty))
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

                turrent_center_x = x + width // 2
                turrent_center_y = y + height // 2

                dx = mouse_x - turrent_center_x
                dy = mouse_y - turrent_center_y
                angle = math.atan2(-dy, dx)
                ammo -= 1
                reload_timer = 0
                spread = mspread
                if scene == "game":
                    for a in range(pierce):
                        for i in range(multi_bullet):
                            offset = (i - multi_bullet // 2) * spread  #####  I think sin and cos translates angle and spd to lik movement(dx,dy) or smth
                            spread = random.uniform(-0.08, 0.08)
                            shot_angle = angle + offset
                            bullets.append({"x": turrent_center_x, "y": turrent_center_y,
                                            "dx": math.cos(shot_angle) * bullet_speed,
                                            "dy": -math.sin(shot_angle) * bullet_speed})
                            if flank:
                                fspread = spread / 2
                                flankspread += 1
                                if flankspread >= 2:
                                    flankspread = 0
                                    offset = (
                                                         i - multi_bullet // 2.5) * fspread  #####  I think sin and cos translates angle and spd to lik movement(dx,dy) or smth
                                    bullets.append({"x": turrent_center_x, "y": turrent_center_y,
                                                    "dx": -math.cos(angle + offset) * bullet_speed,
                                                    "dy": math.sin(angle + offset) * bullet_speed})
                else:
                    offset = (1 - multi_bullet // 2) * spread
                    bullets.append({"x": turrent_center_x, "y": turrent_center_y, "dx": math.cos(angle) * bullet_speed,
                                    "dy": -math.sin(angle) * bullet_speed})
                shoot = 1
            if scene == "settings":
                if rect_back.collidepoint(event.pos):
                    scene = "main"
                    settings_box_draw = False
                    turrent_center = (screenwidth/2, screenheight/2)
                elif settings_box_exit.collidepoint(event.pos) and settings_box_draw:
                    settings_box_draw = False
                elif player_color_rect.collidepoint(event.pos) and not settings_box_draw:
                    settings_box_draw = True
                    settings_box_draw_task = "p_color"
                elif save_main.collidepoint(event.pos):
                    if settings_box_draw_task == "p_color":
                        player_color = prev_player_color.copy()
                elif undo_main.collidepoint(event.pos):
                    if settings_box_draw_task == "p_color":
                        prev_player_color = player_color.copy()
                        color_line_r_pos = player_color[0]
                        color_line_g_pos = player_color[1]
                        color_line_b_pos = player_color[2]
                elif pygame.Rect(170, 130, 255, 40).collidepoint(event.pos) and settings_box_draw:
                    drag_r = True
                elif pygame.Rect(170, 180, 255, 40).collidepoint(event.pos) and settings_box_draw:
                    drag_g = True
                elif pygame.Rect(170, 230, 255, 40).collidepoint(event.pos) and settings_box_draw:
                    drag_b = True

        if event.type == pygame.MOUSEBUTTONUP:
            drag_r = False
            drag_g = False
            drag_b = False

    if drag_r:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        color_line_r_pos = mouse_x - 170
        color_line_r_pos = max(0, min(255, color_line_r_pos))
        prev_player_color[0] = int(color_line_r_pos)
    if drag_g:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        color_line_g_pos = max(0, min(255, mouse_x - 170))
        prev_player_color[1] = int(color_line_g_pos)
    if drag_b:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        color_line_b_pos = max(0, min(255, mouse_x - 170))
        prev_player_color[2] = int(color_line_b_pos)
    if settings_box_draw:
        pygame.draw.rect(screen, white, settings_box)
        pygame.draw.rect(screen, (255, 0, 0), settings_box_exit)

        pygame.draw.rect(screen, (0, 255, 0), save_main)
        pygame.draw.rect(screen, (255, 0, 0), undo_main)

        pygame.draw.polygon(color_slider_r[0], color_slider_r[1], color_slider_r[2])
        pygame.draw.polygon(color_slider_g[0], color_slider_g[1], color_slider_g[2])
        pygame.draw.polygon(color_slider_b[0], color_slider_b[1], color_slider_b[2])
        pygame.draw.rect(screen, black, pygame.Rect(525, 150, 100, 100))

        make_text(color_slider_r[2][0][0] + 265, color_slider_r[2][0][1] - 15, (0, 0, 0), color_line_r_pos, 20)

        pygame.draw.line(color_line_r[0], color_line_r[1], color_line_r[2], color_line_r[3], color_line_r[4])
        pygame.draw.line(color_line_g[0], color_line_g[1], color_line_g[2], color_line_g[3], color_line_g[4])
        pygame.draw.line(color_line_b[0], color_line_b[1], color_line_b[2], color_line_b[3], color_line_b[4])

        if settings_box_draw_task == "p_color":
            preview_pos = (575, 200)
            make_text(150, 100, (0, 0, 0), "Player Color", 20)
            turrent_rect = rotated_turrent.get_rect(center=preview_pos)
            screen.blit(rotated_turrent, turrent_rect.topleft)
            pygame.draw.circle(screen, prev_player_color, preview_pos, t_rad)

    # game logic
    mgun_r += 1
    if mouse_buttons[0] and mgun and mgun_r > mgun_r_time:
        mgun_r = 0
        mouse_x, mouse_y = pygame.mouse.get_pos()

        turrent_center_x = x + width // 2
        turrent_center_y = y + height // 2

        dx = mouse_x - turrent_center_x
        dy = mouse_y - turrent_center_y
        angle = math.atan2(-dy, dx)
        ammo -= 1
        reload_timer = 0
        spread = mspread
        if scene == "game":
            for a in range(pierce):
                for i in range(multi_bullet):
                    offset = (
                                         i - multi_bullet // 2) * spread  #####  I think sin and cos translates angle and spd to lik movement(dx,dy) or smth
                    shot_angle = angle + offset + random.uniform(-0.08, 0.08)
                    bullets.append(
                        {"x": turrent_center_x, "y": turrent_center_y, "dx": math.cos(shot_angle) * bullet_speed,
                         "dy": -math.sin(shot_angle) * bullet_speed})
                    if flank:
                        fspread = spread / 2
                        flankspread += 1
                        if flankspread >= 2:
                            flankspread = 0
                            offset = (i - multi_bullet // 2) * fspread
                            bullets.append({"x": turrent_center_x, "y": turrent_center_y,
                                            "dx": -math.cos(angle + offset) * bullet_speed,
                                            "dy": math.sin(angle + offset) * bullet_speed})
        else:

            offset = (1 - multi_bullet // 2) * spread
            bullets.append({"x": turrent_center_x, "y": turrent_center_y, "dx": math.cos(angle) * bullet_speed,
                            "dy": -math.sin(angle) * bullet_speed})
        shoot = 1
    # enemy spawn
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

    if settings_box_draw or scene != "settings":
        if settings_box_draw:
            preview_pos = [575, 200]
            turrent_center_x = turrent_center[0]
            turrent_center_y = turrent_center[1]
            # I got this online      the angle thing
            mouse_x, mouse_y = pygame.mouse.get_pos()

            dx = mouse_x - preview_pos[0]
            dy = mouse_y - preview_pos[1]
            angle = math.degrees(math.atan2(-dy, dx))  #########dis too

            rotated_turrent = pygame.transform.rotate(turrent_image, angle - 90)
            turrent_cir = pygame.draw.circle(screen, white, turrent_center, t_rad)
        else:
            turrent_center_x = turrent_center[0]
            turrent_center_y = turrent_center[1]
            # I got this online      the angle thing
            mouse_x, mouse_y = pygame.mouse.get_pos()

            dx = mouse_x - turrent_center_x
            dy = mouse_y - turrent_center_y
            angle = math.degrees(math.atan2(-dy, dx))  #########dis too

            rotated_turrent = pygame.transform.rotate(turrent_image, angle - 90)
            turrent_cir = pygame.draw.circle(screen, white, turrent_center, t_rad)
    if not_enough > 0:
        make_text(200, 50, white, "Not Enough Money!", 50)
        not_enough -= 1
    if maxed > 0:
        make_text(screenwidth / 2 - 75, 50, white, "Max!", 50)
        maxed -= 1

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
        for enemy in enemys[:]:
            enemys.remove(enemy)
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
        turrent_center = (x + width // 2, y + height // 2)
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

    for enemy in enemys[:]:
        enemy["x"] += enemy["edx"]
        enemy["y"] += enemy["edy"]
        enemy["t"] += 1

        if enemy["t"] >= 20:
            # off-screen cleanup
            if (enemy["x"] < 0 or enemy["x"] > screenwidth or
                    enemy["y"] < 0 or enemy["y"] > screenheight):
                enemys.remove(enemy)
                continue

            # draw enemy
        pygame.draw.circle(screen, enemy_color, (int(enemy["x"]), int(enemy["y"])), e_rad)

        # player collision
        dx = enemy["x"] - turrent_center_x
        dy = enemy["y"] - turrent_center_y
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance <= e_rad + t_rad:
            enemys.remove(enemy)
            lives -= 1
            enemy_h = 2
    for bullet in bullets[:]:
        bullet["x"] += bullet["dx"]
        bullet["y"] += bullet["dy"]

        if bullet["x"] < 0 or bullet["x"] > screenwidth or bullet["y"] < 0 or bullet["y"] > screenheight:
            bullets.remove(bullet)
            continue

        bullet["rect"] = pygame.Rect(int(bullet["x"]) - ammo_rad, int(bullet["y"]) - ammo_rad, ammo_rad * 2,
                                     ammo_rad * 2)
        pygame.draw.circle(screen, bullet_color, bullet["rect"].center, ammo_rad)

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
                            mspread = 0.1
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
                for enemy in enemys[:]:
                    dx = bullet["x"] - enemy["x"]
                    dy = bullet["y"] - enemy["y"]
                    distance = (dx ** 2 + dy ** 2) ** 0.5

                    if distance <= ammo_rad + e_rad:
                        bullets.remove(bullet)
                        enemys.remove(enemy)
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
        turrent_rect = rotated_turrent.get_rect(center=turrent_center)
        screen.blit(rotated_turrent, turrent_rect.topleft)
        pygame.draw.circle(screen, (player_color[0], player_color[1], player_color[2]), turrent_center, t_rad)
        make_text(x + t_rad / 12.5 - 2.5, y + t_rad / 3, black, ammo, 30)

    pygame.display.update()
pygame.quit()
