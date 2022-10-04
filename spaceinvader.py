import pygame
import random
import math
from pygame import mixer
# initialize pygame
pygame.init()

# screen
screen = pygame.display.set_mode((800, 600))

background = pygame.image.load("Images/Background.jpg")

# Title and Icon
pygame.display.set_caption("Images/Space Invaders")
icon = pygame.image.load('Images/alien.png')
pygame.display.set_icon(icon)

# Backgound Sound
mixer.music.load("Sounds/background.wav")
mixer.music.play(-1)

# Player
playerimg = pygame.image.load("Images/Spaceship.png")
playerx = 370
playery = 480
playerx_change = 0

# Enemy
enemyimg = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load("Images/enemy1.png"))
    enemyx.append(random.randint(0, 735))
    enemyy.append(random.randint(50, 150))
    enemyx_change.append(0.5)
    enemyy_change.append(30)


# bullet
bulletimg = pygame.image.load("Images/bullet.png")
bulletx = 0
bullety = 480
bulletx_change = 0
bullety_change = 4.5

# ready- you can't see the bullet on the screen
# fire- the bullet is currently moving
bullet_state = "ready"


# score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textx = 10
texty = 10

# Game Over
over_font = pygame.font.Font("freesansbold.ttf", 64)


def show_score(x, y):
    score = font.render("Score :"+str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerimg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x+16, y+10))


def is_collision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt(math.pow(enemyx-bulletx, 2) +
                         math.pow(enemyy-bullety, 2))
    if distance < 27:
        return True
    return False


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


# Game loop
running = True
while running:

    screen.fill(((0, 0, 0)))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # print('A keystoke is pressed')
            if event.key == pygame.K_LEFT:
                playerx_change = -1
            if event.key == pygame.K_RIGHT:
                playerx_change = 1
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("Sounds/laser.wav")
                    bullet_sound.play()
                    # get the current x coordinate of the player
                    bulletx = playerx
                    fire_bullet(playerx, bullety)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0

    # player movement
    playerx += playerx_change
    if playerx <= 0:
        playerx = 0
    if playerx >= 736:
        playerx = 736

    # bullet
    if bullety <= 0:
        bullety = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletx, bullety)
        bullety -= bullety_change

    # enemy movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyy[i] > 440:
            for j in range(num_of_enemies):
                enemyy[j] = 2000
            game_over_text()
            break

        # enemy movement
        enemyx[i] += enemyx_change[i]
        if enemyx[i] <= 0:
            enemyx_change[i] = 0.5
            enemyy[i] += enemyy_change[i]
        elif enemyx[i] >= 736:
            enemyx_change[i] = -0.5
            enemyy[i] += enemyy_change[i]

        # collision
        collision = is_collision(enemyx[i], enemyy[i], bulletx, bullety)
        if collision:
            explosion_sound = mixer.Sound("Sounds/explosion.wav")
            explosion_sound.play()
            bullety = 480
            bullet_state = "ready"
            score_value += 1
            enemyx[i] = random.randint(0, 735)
            enemyy[i] = random.randint(50, 150)

            # print(score_value)

        enemy(enemyx[i], enemyy[i], i)

    player(playerx, playery)
    show_score(textx, texty)
    pygame.display.update()
