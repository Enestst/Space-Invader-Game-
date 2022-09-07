import pygame
import math
import random


# for intialize pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((600, 600))

# background
background = pygame.image.load("background.jpg")

# caption and icon
pygame.display.set_caption("first game")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

score = 0
font = pygame.font.Font('freesansbold.ttf', 24)

game__over = pygame.font.Font('freesansbold.ttf', 50)

testX = 8
testY = 8


def show_score(x, y):
    scorevalue = font.render("Score : " + str(score), True, (255, 255, 255))
    screen.blit(scorevalue, (x, y))


def game_over():
    gameover = game__over.render("Game Over : " + str(score), True, (255, 255, 255))
    screen.blit(gameover, (90, 250))


# rocket
rocketimg = pygame.image.load("rocket.png")
rocketX = 270
rocketY = 480
rocketX_change = 0

# enemy
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 536))
    enemyY.append(random.randint(60, 160))
    enemyX_change.append(0.2)
    enemyY_change.append(40)

# bullet
bulletimg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 0.8
bullet_state = "ready"


def rocket(x, y):
    screen.blit(rocketimg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))


def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# game loop


running = True
while running:
    screen.fill((128, 128, 128))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                rocketX_change = -0.3
            if event.key == pygame.K_RIGHT:
                rocketX_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = rocketX
                    fire_bullet(rocketX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                rocketX_change = 0
            if event.key == pygame.K_RIGHT:
                rocketX_change = 0

    rocketX += rocketX_change

    if rocketX <= 0:
        rocketX = 0
    if rocketX >= 536:
        rocketX = 536

    for i in range(num_of_enemies):
        if enemyY[i] > 400:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        if enemyX[i] >= 536:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]
        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score += 1
            enemyX[i] = random.randint(0, 536)
            enemyY[i] = random.randint(60, 160)

        enemy(enemyX[i], enemyY[i], i)

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY = bulletY - bulletY_change




    rocket(rocketX, rocketY)
    show_score(testX, testY)

    pygame.display.update()
