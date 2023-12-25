import pygame
import math
import random
from pygame import mixer

# CTRL + ALT + L Formats your code to make it look better

# initialize pygame
pygame.init()

# create screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load("space.jpg")

# background song
mixer.music.load('mainsong.mp3')
mixer.music.play(-1)

# title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# player
playerimg = pygame.image.load("jet.png")
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# enemy
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemies = 6

for i in range(num_enemies):
    enemyimg.append(pygame.image.load("character.png"))
    enemyX.append(random.randint(0, 800))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1.5)
    enemyY_change.append(40)

# bullet
bulletimg = pygame.image.load("bullet.png")
bX = 0
bY = 480
bX_change = 0
bY_change = 5
bullet_state = "ready"  # cant see bullet on screen


def player(x, y):
    screen.blit(playerimg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"

    screen.blit(bulletimg, (x + 16, y + 10))


def is_collision(enemyX, enemyY, bX, bY):
    distance = math.hypot(enemyX - bX, enemyY - bY)

    if distance < 27:
        return True
    else:
        return False


# score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10


def show_score(x, y):
    score = font.render("SCORE: " + str(score_value) , True , (255, 255, 255))
    screen.blit(score , (x , y))

# game over

over_font = pygame.font.Font('freesansbold.ttf', 64)

def game_over():
    over_text = font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


# game loop
running = True
while running:
    # filling colour in window
    # RGB -      red green blue
    screen.fill((0, 0, 0))
    # bg image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed , check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -2

            if event.key == pygame.K_RIGHT:
                playerX_change = 2

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    # get X coordinate of spaceship
                    bX = playerX
                    fire_bullet(bX, bY)

        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_LEFT) or (event.key == pygame.K_RIGHT):
                playerX_change = 0

    #  player movement
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # enemy movement
    for i in range(num_enemies):

        # game over
        if enemyY[i] > 440:
            for j in range(num_enemies):
                enemyY[j] = 2000

            game_over()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]
        # Collision
        collision = is_collision(enemyX[i], enemyY[i], bX, bY)
        if collision:
            boom_sound = mixer.Sound('explosion.wav')
            boom_sound.play()
            bY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 800)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bY <= 0:
        bY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bX, bY)
        bY -= bY_change

    player(playerX, playerY)
    show_score(textX , textY)

    # the second compulsary line
    pygame.display.update()
