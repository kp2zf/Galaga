# Chintan Sheth (cps2cg)
# Partner: Kush Patel (kp2zf)

import pygame, gamebox, random
# imports necessary packages


def starry_background():
    global starry_counter
    starry_counter += 1        # counter increments at tick speed (30 per sec)

    if starry_counter % 5 == 0:    # approx 1/6 sec
        numstars = random.randint(0, 7)  # number of stars to generate for a row each 1/6 sec
        for num in range(numstars):
            # append a star (another gamebox) "character" (3x3 white box) at location random x, 0) to stars list
            stars.append(gamebox.from_color(random.randint(5, WINDOW_WIDTH - 5), 0, "white", 3, 3))

    for star in stars:
        # move the star down the window by increasing y.
        star.y += 3
        if star.y > WINDOW_HEIGHT:
            stars.remove(star)
        camera.draw(star)
# function makes starry background
# remade from Dill Lecture


def enemy_generator(x, y):
    global loop_count
    loop_count = 0

    while loop_count < enemy_count:
        enemies.append(enemy_1.copy_at(x, y))
        x += 50
        enemies.append(enemy_2.copy_at(x, y))
        x += 50
        enemies.append(enemy_3.copy_at(x, y))
        x += 50
        loop_count += 1
        if x >= 450:
            x = 30
            y += 50
# function generates the enemies


def initial_move_enemy():
    for enemy in enemies:
        enemy.speedx = 2
        enemy.move_speed()
# function moves the enemies at the start of the game


def enemy_move_check():
    global overall_enemy_speed
    for enemy in enemies:
        for border in borders:
            if enemy.right_touches(border):
                overall_enemy_speed = -2
                enemy_move_down()
            elif enemy.left_touches(border):
                overall_enemy_speed = 2
                enemy_move_down()
# function makes the sure that the enemies stay in the frame


def all_enemy_move():
    for enemy in enemies:
        enemy.speedx = overall_enemy_speed
        enemy.move_speed()
# function makes the enemies move as a unit, without overlap


def enemy_move_down():
    for enemy in enemies:
        enemy.y += 8
# function makes the enemies move down after one cycle


def border_check():
    for border in borders:
        camera.draw(border)
        if ship.touches(border):
            ship.move_to_stop_overlapping(border)
# function makes sure ship does not move off screen


def move(keys):
    if pygame.K_RIGHT in keys:
        ship.x += 16
    if pygame.K_LEFT in keys:
        ship.x -= 16
    ship.move_speed()
# function makes ship move left and right


def shoot(keys):
    global shoot_timer
    if pygame.K_SPACE in keys:
        if shoot_timer > 3:
            missiles.append(gamebox.from_color(ship.x + 1, ship.y - 25, "red", 7, 7))
            gamebox.load_sound('pew.wav').play()
            shoot_timer = 0
        keys.clear()
    for missile in missiles:
        missile.y -= 22
        camera.draw(missile)
# function helps ship shoot missiles and makes 'pew' sound


def start_screen(keys):
    global intro
    camera.draw(logo)
    camera.draw(space)
    if pygame.K_SPACE in keys:
        intro = False
# function sets up the start up screen


def meteor_generator():
    global frames
    if (frames/30) % 5 == 0:
        rand_meteor = random.randint(1, 8)
        run = 0
        while run < rand_meteor:
            meteors.append(meteor_gb.copy_at(random.randint(1, 11)*50, 0))
            run += 1
# function generates the meteors


def kill():
    global score, round_num, enemy_count, missiles, x_pos, y_pos, explosion_bool
    for missile in missiles:
        for enemy in enemies:
            if missile.touches(enemy, -5) is True:
                missile_index = int(missiles.index(missile))
                enemy_index = int(enemies.index(enemy))
                missiles.pop(missile_index)
                x_pos = missile.x
                y_pos = missile.y
                explosion_bool = True
                enemies.pop(enemy_index)
                score += 1
    if enemies == []:
        round_num += 1
        missiles = []
        enemy_count = 3 * (3 + round_num)
        enemy_generator(30, 50)
        initial_move_enemy()
# function removes the enemy when hit


def enemy_hit():
    global live_count
    for meteor in meteors:
        if meteor.touches(ship, -40, -40) is True:
            meteor_index = int(meteors.index(meteor))
            meteors.pop(meteor_index)
            live_count = live_count - 1

    for enemy in enemies:
        if enemy.touches(ship, -5, -5) is True:
            enemy_index = int(enemies.index(enemy))
            enemies.pop(enemy_index)
            live_count = live_count - 1
# function keeps track of the ship's lives


def keep_score():
    round_display = gamebox.from_text(550, 20, "Round: " + str(round_num), 'Arial', 20, 'white', bold=True)
    score_board = gamebox.from_text(50, 20, "Score: " + str(score), "Arial", 20, 'white', bold=True)
    lives = gamebox.from_text(275, 20, "Lives left: " + str(live_count), "Arial", 20, "cyan", bold=True)
    camera.draw(round_display)
    camera.draw(score_board)
    camera.draw(lives)
# function keeps track of the score and round count


def check_explosion():
    global explosion_bool, x_pos, y_pos
    if explosion_bool:
        for i in explosion:
            pew = gamebox.from_image(x_pos, y_pos, i)
            pew.scale_by(0.30)
            camera.draw(pew)
        gamebox.load_sound('sound effects explosion_1.wav').play()
    explosion_bool = False
# function makes the explosion animation and explosion sound


def regular_action(keys):
    global shoot_timer
    move(keys)
    border_check()
    shoot(keys)
    enemy_move_check()
    all_enemy_move()
    meteor_generator()
    shoot_timer += 1
    for enemy in enemies:
        camera.draw(enemy)
    for meteor in meteors:
        meteor.speedy = 6
        meteor.move_speed()
        camera.draw(meteor)
    kill()
    enemy_hit()
    check_explosion()
    keep_score()
# function calls all of the different functions that should be called in one tick


def game_over():
    gamebox.pause()
    final_score = gamebox.from_text(camera.x, camera.y, "Game Over! Final Score: " + str(score), "Times New Roman", 30, "red", bold=True)
    camera.draw(final_score)
# function displays the game over screen


def tick(keys):
    global frames

    frames += 1
    camera.clear('black')
    starry_background()

    if intro:
        start_screen(keys)
    else:
        regular_action(keys)

    if live_count == 0:
        game_over()

    camera.draw(ship)
    camera.display()
# tick

ticks_per_second = 30
WINDOW_WIDTH = 600  # width of the frame
WINDOW_HEIGHT = 800  # height of the frame
camera = gamebox.Camera(WINDOW_WIDTH, WINDOW_HEIGHT)  # sets the camera
stars = []  # list of stars in the background
missiles = [] # list of missiles shot by the ship
meteors = []  # list of meteor enemies
enemies = []  # list of alien enemies
score = 0  # score count
frames = 0  # counter used to spawn meteors
starry_counter = 0  # counter used for spawning stars in the background
shoot_timer = 0  # counter used to make the ship shoot in a certain interval
loop_count = 0  # counter used for a loop
round_num = 1  # counter used to keep track of the rounds
overall_enemy_speed = 2  # controls the speed of the enemies
enemy_count = 10 + (2 * round_num)  # keeps track of the number of enemies
borders = [gamebox.from_color(0, camera.y, 'black', 5, 800),
           gamebox.from_color(600, camera.y, 'black', 5, 800)]  # list containing the borders the the ship can't cross
explosion = ['regularExplosion00.png',
             'regularExplosion01.png',
             'regularExplosion02.png',
             'regularExplosion03.png',
             'regularExplosion04.png',
             'regularExplosion05.png',
             'regularExplosion06.png',
             'regularExplosion07.png',
             'regularExplosion08.png']  # sprite list that contains the images used for the explosion animation
intro = True  # boolean used for the start screen
ship = gamebox.from_image(300, 600, 'ship.png')  # ship
logo = gamebox.from_image(300, 280, 'E:/Qt/logo_galaga.png')  # galaga logo
space = gamebox.from_image(300, 370, 'space.png')  # push space to play
ship.scale_by(0.23)  # scale ship
logo.scale_by(0.25) # scale logo
enemy_1 = gamebox.from_image(random.randint(50, 550), random.randint(50, 400), 'enemy1.png')  # enemy 1
enemy_1.scale_by(0.025)  # scale enemy 1
enemy_2 = gamebox.from_image(random.randint(50, 550), random.randint(50, 400), 'enemy2.png')  # enemy 2
enemy_2.scale_by(0.15)  # scale enemy 2
enemy_3 = gamebox.from_image(random.randint(50, 550), random.randint(50, 400), 'enemy3.png')  # enemy 3
enemy_3.scale_by(.35)  # scale enemy 3
meteor_gb = gamebox.from_image(random.randint(50, 550), 0, 'meteor.png')  # meteor
meteor_gb.scale_by(.13)  # scale meteor
music = gamebox.load_sound('Soundtrack Galaga.wav')  # load soundtrack
music.play(-1)  # plays soundtrack for the duration of the game
live_count = 4  # lives counter
enemy_generator(30, 50)  # generates the initial enemies
initial_move_enemy()  # moves the initial enemies
x_pos = 0  # x position used for explosion sprite
y_pos = 0  # y position used for explosion sprite
explosion_bool = False   # bool used for explosion sprite

for i in range(0, 275):  # generates the starry background
    starry_background()

gamebox.timer_loop(ticks_per_second, tick)  # game loop
