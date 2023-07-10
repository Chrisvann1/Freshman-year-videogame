import pgzrun

import random

import sys


TITLE = 'Wizard 102'
WIDTH = 1440
HEIGHT = 719

game = Actor('title_screen')
game.state = ['title', 'game', 'gameover', 'about', 'win', 'about_2']
game.current_state = game.state[0]

fires = []
bolts = []
fire = Actor('fireball')
bolt = Actor('bolt')

dragon2 = Actor('small_dragon')
dragon = Actor('dragon')
wizard = Actor('wizard')
wizard.pos = (WIDTH // 2, HEIGHT - 100)
wizard.score = 0
wizard.lives = 3

dragons2 = []


bolt = Actor('bolt')
bolt.pos = (WIDTH // 2, HEIGHT - 100)


def draw_title():
    screen.blit('title_screen', (0,0))

def draw_game():
    screen.blit('background', (0,0))
    wizard.draw()
    dragon.draw()

def draw_game_over():
    screen.blit('game_over', (0,0))
    screen.blit('about_button', (500, 500))
    sounds.game_over.play()

def draw_about_screen():
    screen.blit('about_screen', (0,0))

def draw_win_screen():
    screen.blit('win', (0,0))
    screen.blit('about_button', (500, 500))

def draw_about_screen2():
    screen.blit('about_screen', (0,0))

def draw():
    if game.current_state == 'title':
        draw_title()
        screen.draw.text("Press esc to quit", bottomright = (WIDTH//2 + 50, HEIGHT - 100))
    elif game.current_state == 'game':
        draw_game()
        screen.draw.text("Score: " + str(wizard.score), bottomright=(WIDTH-10, HEIGHT-5))
        screen.draw.text("lives: " + str(wizard.lives), bottomleft=(10, HEIGHT - 5))
        draw_fire()
        draw_dragons2()
        draw_bolt()
        screen.draw.text("Press esc to quit", topleft = (10, 10))
    elif game.current_state == 'gameover':
        draw_game_over()
    elif game.current_state == 'about':
        draw_about_screen()
    elif game.current_state == 'win':
        draw_win_screen()
    elif game.current_state == 'about_2':
        draw_about_screen2()

def on_key_down(key):
    if game.current_state == 'title':
        if key == keys.RETURN:
            game.current_state = game.state[1]
            sounds.main_track.play()
            clock.unschedule(spawn_fireball)
            clock.unschedule(spawn_dragon2)
            clock.schedule_interval(spawn_fireball, .5)
            clock.schedule_interval(spawn_dragon2, 1.2)
            dragon.pos = (20, 65)
    elif game.current_state == 'game':
        if wizard.score == 1000:
            clock.unschedule(spawn_fireball)
            clock.unschedule(spawn_dragon2)
            clock.schedule_interval(spawn_fireball, .40)
            clock.schedule_interval(spawn_dragon2, .50)
        if wizard.score == 2000:
            clock.unschedule(spawn_fireball)
            clock.unschedule(spawn_dragon2)
            clock.schedule_interval(spawn_fireball, .35)
            clock.schedule_interval(spawn_dragon2, .12)
        if wizard.score == 5000:
            clock.unschedule(spawn_fireball)
            clock.unschedule(spawn_dragon2)
            clock.schedule_interval(spawn_fireball, .35)
            clock.schedule_interval(spawn_dragon2, .08)
        if wizard.score >= 7500:
            sounds.main_track.stop()
            sounds.win_music.play()
            game.current_state = game.state[4]
        print(wizard.score)

        if key == keys.SPACE and len(bolts) < 3:
            spawn_bolt()
            print(wizard.score)

        if wizard.lives == 0:
            sounds.main_track.stop()
            game.current_state = game.state[2]


    elif game.current_state == 'gameover':
        clock.unschedule(spawn_dragon2)
        wizard.score = 0
        wizard.lives = 3
        if key == keys.RETURN:
            game.current_state = game.state[0]
            sounds.game_over.stop()
            fires = []
            dragons2 = []
        if key == keys.SPACE:
            game.current_state = game.state[3]
            sounds.game_over.stop()

    elif game.current_state == 'about':
        if key == keys.SPACE:
             game.current_state = game.state[2]

    elif game.current_state == 'win':
        clock.unschedule(spawn_dragon2)
        wizard.score = 0
        wizard.lives = 3
        fires = []
        dragons2 = []
        if key == keys.RETURN:
            game.current_state = game.state[0]
            sounds.win_music.stop()
        if key == keys.SPACE:
            game.current_state = game.state[5]
    elif game.current_state == 'about_2':
        if key == keys.SPACE:
             game.current_state = game.state[4]

    if key == keys.ESCAPE:
        sys.exit()

def draw_fire():
    global fires
    for fire in fires:
        fire.draw()

def draw_bolt():
    global bolts
    for bolt in bolts:
        bolt.draw()

def draw_dragons2():
    global dragons2
    for dragon2 in dragons2:
        dragon2.draw()

def move_dragon(time):
    if game.current_state == 'game':
        if dragon.left < WIDTH:
            dragon.x += time * 400
        if dragon.left > WIDTH:
            dragon.x = 0

def move_dragons2(time):
    global dragons2
    for dragon2 in dragons2:
        dragon2.y += time * 400

def spawn_fireball():
    if game.current_state == 'game':
        global fires
        fire = Actor('fireball')
        fire.pos = (dragon.x, dragon.y+60)
        fire.render = True
        fires.append(fire)

def spawn_bolt():
    if game.current_state == 'game':
        global bolts
        bolt = Actor('bolt')
        bolt.pos = (wizard.x - 20, wizard.y - 50)
        bolt.render = True
        bolts.append(bolt)
        sounds.player_attack.play()


def move_fire(time):
    global fires
    for fire in fires:
        fire.y += time * 100

def move_bolt(time):
    global bolts
    for bolt in bolts:
        bolt.y -= time * 100

def clean_up():
    global fires
    global dragons2
    new_fires = []
    for fire in fires:
        if not fire.bottom < 0 and fire.render:
            new_fires.append(fire)
        if game.current_state =='gameover':
            fires = new_fires
    fires = new_fires
    new_dragons = []
    for dragon2 in dragons2:
        if not dragon2.top > HEIGHT and dragon2.render:
            new_dragons.append(dragon2)
    dragons2 = new_dragons
    global bolts
    new_bolts = []
    for bolt in bolts:
        if not bolt.top < 0 and bolt.render:
            new_bolts.append(bolt)
        if game.current_state =='gameover':
            bolts = new_bolts
    bolts = new_bolts



def check_collisions():
    global fires

    for fire in fires:
        if wizard.colliderect(fire):
            wizard.lives -= 1
            fire.render = False
            sounds.hit_sound.play()
            sounds.player_attack.stop()
        if wizard.colliderect(fire) and wizard.lives == 0 or game.current_state == 'gameover':
            fires =[]
            sounds.main_track.stop()
        if game.current_state == "win":
            fires =[]
            sounds.main_track.stop()
    global dragons2
    for dragon2 in dragons2:
        if wizard.colliderect(dragon2):
            wizard.lives -= 1
            dragon2.render = False
            sounds.hit_sound.play()
            sounds.player_attack.stop()
        if wizard.colliderect(dragon2) and wizard.lives == 0 or game.current_state == 'gameover':
            dragons2 =[]
            sounds.main_track.stop()
        if game.current_state == 'win':
            dragons2 =[]
            sounds.main_track.stop()
    global bolts
    for bolt in bolts:
        if dragon.colliderect(bolt):
            wizard.score += 50
            bolt.render = False
            print(1)
        for dragon2 in dragons2:
            if dragon2.colliderect(bolt):
                wizard.score += 50
                bolt.render = False
                dragon2.render = False
                print(1)

def gameover():
    if wizard.lives <= 0:
        fires = []
        dragons2 = []
        game.current_state = game.state[2]



def check_keys(time):
    if game.current_state == 'game':
        if keyboard.LEFT:
            wizard.x -= time * 450
            if wizard.left < 0:
                wizard.left = 0
        if keyboard.RIGHT:
            wizard.x += time * 450
            if wizard.right > WIDTH:
                wizard.right = WIDTH

def spawn_dragon2():
    global dragons2
    dragon2 = Actor('small_dragon')
    xpos = random.randint(dragon2.width, WIDTH - dragon2.width)
    dragon2.midbottom = (xpos, 0)
    dragon2.render = True
    dragons2.append(dragon2)

def update(time):
    check_keys(time)
    move_dragon(time)
    move_fire(time)
    move_bolt(time * 6)
    check_collisions()
    gameover()
    dragon.draw()
    move_dragons2(time)
    clean_up()


pgzrun.go()
