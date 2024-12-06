### modules ###

import pygame
import sys
import time
import numpy as np
import os
import random

from clases import Engine, Platform, Ball, UI

### set up ###

os.chdir(os.path.dirname(os.path.abspath(__file__)))  # changes working directory

pygame.init()

os.system('cls')
print(">>>Welcome to Bouncy Broda. ¡Bounce!\n\n>Source code: https://github.com/emilioreato/Bouncy-Broda/")

Engine.set_up()
UI()

### variables ###

global pause
pause = False

global score
score = 0

global platforms
platforms = []

global move
move = None

global first_collision
first_collision = True

global threshold
threshold = 100

global Gravity
Gravity = 0

global count
count = 0
global timer_for_count
timer_for_count = 0.007


### functions ###

def lose():
    global beginning_time, pause, timer_for_count, count, time_checkpoint
    time.sleep(0.5)
    if score > 69:
        text = "> Congrats, you won!"
    else:
        text = "\n> Good luck next time... Learn how to bounce."
    print(text + f"\n> You scored {score} points.")

    time_checkpoint = time.time()
    count = 0
    timer_for_count = 0.007
    beginning_time = time.time()
    set_up_match()
    update_score(0, True)
    pause = True


def update_score(change, rewrite=False):
    global score, score_text
    if rewrite:
        score = change
    else:
        score += change
    score_text = Engine.font1.render(f"Score: {score}", True, (140, 140, 140))
    Engine.screen.blit(score_text, (Engine.window_width / 3.6, Engine.window_height / 25))


def set_up_match():
    global ball, score, platforms, move, first_collision, Gravity, start_time
    ball = Ball(vel=0, radius=10, color=(177, 177, 177))
    score = 0
    Gravity = 0
    first_collision = True
    platforms = []
    move = None
    start_time = time.perf_counter()


def calculations(beginning_time, time_interval):
    time_interval_scaled = time_interval*45  # this is to make the game run at the same speed regardless of the fps

    global ball, count, pause, first_collision, Gravity, threshold, timer_for_count, start_time

    count += 1*Engine.fps_relation

    if move == None:
        pass
    elif move == "right" and ball.x < Engine.window_width - ball.radius:  # moving
        ball.x += 2.8*Engine.fps_relation
    elif move == "left" and ball.x > ball.radius:
        ball.x -= 2.8*Engine.fps_relation

    mult = 1
    if ball.active_boost:  # if the user activates the boost then it multiplies the new velocity
        ball.boost_timer -= time_interval
        if ball.boost_timer > 0:
            mult = 1.03
        else:
            ball.active_boost = False

    ball.vel += Gravity * time_interval_scaled*mult

    ball.y = ball.y + ball.vel * time_interval_scaled

    if ball.y > Engine.window_height:
        lose()

    if count > threshold:
        threshold = np.clip(np.random.normal(92, 52), 70, 180)  # this determines how much counts it has to wait to evoke a new platform
        count = 0

        width = int(np.clip(np.random.normal(118-(beginning_time-time.time())*0.62, 55), 62, 202))
        x = random.randint(0, Engine.window_width - width)

        r = np.clip(np.random.normal(210, 35), 5, 255)
        g = np.clip(np.random.normal(60, 60), 0, 250)
        b = np.clip(np.random.normal(170, 55), 0, 255)
        color = tuple(map(int, (r, g, b)))

        platforms.append(Platform(x, 0, width,  8, color))

    if ball.vel >= 0 or first_collision:  # only check for collitions when ascending
        for plat in platforms:
            if plat.check_collision((ball.x, ball.y), ball.radius):
                update_score(1)
                if first_collision:
                    first_collision = False
                    Gravity = 1.17
                    ball.vel = 32
                if ball.vel < 14:
                    ball.vel = 14
                elif ball.vel > 40:
                    ball.vel = 40

                ball.vel = -ball.vel * 0.95  # lets reduce the kinetic energy so it doesnt tends to infinity ad the user can also boost it up with the space key
                print("boing!")

    for plat in platforms:  # if the platform is out of the window then delete it
        plat.y += 1*Engine.fps_relation
        if plat.y > Engine.window_height + 100:
            platforms.remove(plat)


def draw():

    Engine.screen.fill((7, 7, 7))

    for plat in platforms:
        plat.draw()

    ball.draw()

    Engine.screen.blit(score_text, (Engine.window_width / 1.192, Engine.window_height / 53))

    Engine.screen.blit(UI.rect_surface, (0, Engine.window_height-Engine.window_height//74))

    pygame.display.flip()

# prepare for loop #


set_up_match()

update_score(0)

global time_checkpoint
time_checkpoint = time.time()

global beginning_time
beginning_time = time.time()


# PYGAME LOOP ###

while True:

    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            elif event.key == pygame.K_d:
                move = "right"

            elif event.key == pygame.K_a:
                move = "left"

            elif event.key == pygame.K_SPACE or event.key == pygame.K_w:
                if not first_collision:
                    ball.boost(0.6)  # 1.2

            elif event.key == pygame.K_p:
                pause = 1 - pause

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                if move == "right":
                    move = None
            elif event.key == pygame.K_a:
                if move == "left":
                    move = None

        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not pause:
        calculations(beginning_time, (time.time() - time_checkpoint))

    draw()

    time_checkpoint = time.time()

    Engine.timer.tick(Engine.fps)
