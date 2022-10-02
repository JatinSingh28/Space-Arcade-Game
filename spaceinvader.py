import pygame
import random
# initialize pygame
pygame.init()

# screen
screen = pygame.display.set_mode((800, 600))

background = pygame.image.load("Background.jpg")

#Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('alien.png')
pygame.display.set_icon(icon)

# Player
playerimg = pygame.image.load("Spaceship.png")
playerx = 370
playery = 480
playerx_change = 0

# Enemy
enemyimg = pygame.image.load("enemy1.png")
enemyx = random.randint(0, 736)
enemyy = random.randint(50, 150)
enemyx_change = 0.5
enemyy_change = 30

bulletimg = pygame.image.load("bullet.png")
bulletx = 0
bullety = 480
bulletx_change = 0
bullety_change = 4.5

# ready- you can't see the bullet on the screen
# fire- the bullet is currently moving
bullet_state = "ready"


def player(x, y):
    screen.blit(playerimg, (x, y))


def enemy(x, y):
    screen.blit(enemyimg, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x+16, y+10))


# game loop
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
                    bulletx = playerx
                    fire_bullet(playerx, bullety)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0

    playerx += playerx_change
    if playerx <= 0:
        playerx = 0
    if playerx >= 736:
        playerx = 736

    if bullety <= 0:
        bullety = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletx, bullety)
        bullety -= bullety_change

    enemyx += enemyx_change
    if enemyx <= 0:
        enemyx_change = 0.5
        enemyy += enemyy_change
    elif enemyx >= 736:
        enemyx_change = -0.5
        enemyy += enemyy_change

    player(playerx, playery)
    enemy(enemyx, enemyy)
    pygame.display.update()
