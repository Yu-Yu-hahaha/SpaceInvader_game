import pygame
import random
import math
from pygame import mixer

#initialize the pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode((800, 600)) #(width, height)

#title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

#background
background = pygame.image.load("background.png")

#create background sound
mixer.music.load("background.wav")
mixer.music.play(-1)

#create player
playerImg = pygame.image.load("player.png")
#initial playerImg position
playerX = 370
playerY = 500
playerX_change = 0

#create muliple enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemy = 4
for i in range(num_of_enemy):
    enemyImg.append(pygame.image.load("alien.png"))
    #initial enemyImg position
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(2)
    enemyY_change.append(30)

#create bullet
bulletImg = pygame.image.load("bullet.png")
#initial bulletImg position
bulletX = 0
bulletY = 500
bulletX_change = 0
bulletY_change = 8
bullet_state = "ready"

#score
score_val = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10

#game over text
game_over_font = pygame.font.Font("freesansbold.ttf", 64)

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x+16, y+10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2))+(math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False

def show_score(x, y):
    score = font.render("Score: " + str(score_val), True, (255,255,255))
    screen.blit(score, (x,y))

def show_game_over():
    game_over_text = game_over_font.render("GAME OVER!", True, (255,255,255))
    screen.blit(game_over_text, (200,250))

#game loop
running = True
while running:  
    
    # set RGB
    screen.fill((0,0,0))
    # set background
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #if keystroke is pressed, ck it's left or right or space
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    #create bullet shoot sound
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    
    #move player
    playerX += playerX_change
    #create boundary for space invader
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    #move enemy
    for i in range(num_of_enemy):
        #game over
        if enemyY[i] > 400:
            for j in range(num_of_enemy):
                enemyY[j] = 2000
            show_game_over()
            break

        enemyX[i] += enemyX_change[i]
        #create boundary for enemy
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i] 
        elif enemyX[i] >= 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i] 
        
        #ck collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            #create collision sound
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()

            bulletY = 500
            bullet_state = "ready"
            score_val += 1
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50,150)
        
        enemy(enemyX[i], enemyY[i], i)
    
    #move bullet
    if bulletY <= 0:
        bulletY = 500
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    
    player(playerX,playerY)
    show_score(textX, textY)
    pygame.display.update()