import pgzrun
import random
import math
from pgzhelper import *

WIDTH = 1024
HEIGHT = 768

player = Actor("playership2_blue")
player.pos = (WIDTH/2, HEIGHT/2)
player.hp = 100
player.score = 0

bg = Actor("space_bg")

enemies = []
lasers = []
elasers = []

mouse_pos = [0,0]

def update(): 

    global laser_count
    if player.hp>0:

        player.angle = player.angle_to(mouse_pos)-90

        if random.randint(0, 100)<3:
            enemy = Actor("enemy_green5")
            enemy.lv = 1
            enemy.hp = 1
            
            from_dir = random.randint(0,3)
            if from_dir == 0:
                enemy.x = random.randint(0, WIDTH)
                enemy.y = 0
            if from_dir == 1:
                enemy.x = 0
                enemy.y = random.randint(0, WIDTH)
            if from_dir == 2:
                enemy.x = random.randint(0, WIDTH)
                enemy.y = HEIGHT
            if from_dir == 3:
                enemy.x = WIDTH
                enemy.y = random.randint(0, WIDTH)
            

            enemy.point_towards(player)
            enemies.append(enemy)
        
        if random.randint(0, 100)<3 and player.score >= 100:
            enemy = Actor("enemy_red3")
            enemy.lv = 2
            enemy.hp = 3
            
            from_dir = random.randint(0,3)
            if from_dir == 0:
                enemy.x = random.randint(0, WIDTH)
                enemy.y = 0
            if from_dir == 1:
                enemy.x = 0
                enemy.y = random.randint(0, WIDTH)
            if from_dir == 2:
                enemy.x = random.randint(0, WIDTH)
                enemy.y = HEIGHT
            if from_dir == 3:
                enemy.x = WIDTH
                enemy.y = random.randint(0, WIDTH)
            

            enemy.point_towards(player)
            enemies.append(enemy)

        for e in enemies:
            #e.point_towards(player)
            if e.hp <= 0:
                enemies.remove(e)
                player.score += 10
                break
            e.move_forward(2)
            if e.left>WIDTH or e.right<0 or e.top>HEIGHT:
                enemies.remove(e)
            if player.colliderect(e):
                player.hp -= 5*e.lv
                enemies.remove(e)
            if random.randint(0, 100)<2   :
                elaser = Actor('laser_red07')
                elaser.pos = e.pos
                elaser.point_towards(player)
                elasers.append(elaser)

        if keyboard.space:
            laser = Actor('laser_blue01')
            laser.pos = player.pos
            laser.angle = player.angle+90
            lasers.append(laser)

        if keyboard.up:
            player.y -= 5
        if keyboard.down:
            player.y += 5
        if keyboard.left:
            player.x -= 5
        if keyboard.right:
            player.x += 5

        if player.left <= 0:
            player.left =0
        if player.right >= WIDTH:
            player.right = WIDTH
        if player.top <= 0:
            player.top =0
        if player.bottom >= HEIGHT:
            player.bottom = HEIGHT

        for l in lasers:
            rm_l = False
            l.move_forward(5)
            if l.bottom < 0 or l.top>HEIGHT or l.right<0 or l.left>WIDTH:
                rm_l = True
            else:
                for e in enemies:
                    if l.colliderect(e):
                        e.hp -= 1
                        rm_l = True
            if rm_l:
                lasers.remove(l)
                break
        for el in elasers:
            el.move_forward(5)
            if el.top > HEIGHT:
                elasers.remove(el)
                break
            if player.colliderect(el):
                elasers.remove(el)
                player.hp -= 1
                break
    
    else:
        player.hp = 100

def on_mouse_move(pos):
    global mouse_pos
    mouse_pos = pos


        

def draw():
    screen.clear()
    bg.draw()
    screen.draw.filled_rect(Rect((0,0),(WIDTH*player.hp/100,20)), 'green')
    screen.draw.text(str(player.score), (10,30), fontsize=30)

    for l in lasers:
        l.draw()

    for el in elasers:
        el.draw()

    player.draw()
   

    for e in enemies:
        e.draw()

pgzrun.go()