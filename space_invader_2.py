import pygame, random
from pygame import mixer
from sys import exit
from pygame.locals import *


# Game Variables
player_speed = 4
no_of_enemies = 5
enemy_start_speed = 0.1
enemy_incr_speed = 0.005
no_of_bullets = 2


# Only things under this is included in our Game
pygame.init()

p = pygame.display

# Game screen
screen = p.set_mode((1280, 680))

# Changing Title , Icon
p.set_caption("SPACE FIGHTER")

iconImage = pygame.image.load("logo.png")
p.set_icon(iconImage)

playerImage = pygame.image.load("player.png")
enemyImage = pygame.image.load("enemy.png")
backgroundImage = pygame.image.load("background.jpg")
bulletImage = pygame.image.load("bullets.png")


def player(x, y):
    screen.blit(playerImage, (x, y))


def enemy(x, y):
    screen.blit(enemyImage, (x, y))


def bullet(x, y):
    screen.blit(bulletImage, (x, y))


# Font setting
score_font = pygame.font.SysFont("freesansbold.ttf", 75, bold=True, italic=True)
game_over_font = pygame.font.SysFont("freesansbold.ttf", 150, bold=True, italic=True)
retry_font = pygame.font.SysFont("freesansbold.ttf", 150, bold=True, italic=True)


def GameOver(x, y):
    gameOver = game_over_font.render("GAME OVER", True, (255, 10, 10))
    screen.blit(gameOver, (x, y))


def FIRSTGAME():
    playerX = 550
    playerY = 520
    change_playerX = 0

    enemyX = []
    enemyY = []

    for i in range(no_of_enemies):
        enemyX.append(random.randint(5, 1210))
        enemyY.append(random.randint(-115, -65))

    bulletX = []
    bulletY = []

    for i in range(no_of_bullets):
        bulletX.append(0)
        bulletY.append(535)

    game_over = False
    score_value = 0

    def scoreBox(x, y):
        if game_over:
            score = score_font.render("YOUR SCORE : {}".format(score_value), True, (255, 255, 255))
            retry = retry_font.render("TRY AGAIN", True, (0, 0, 0))
            screen.blit(retry, (x - 60, y + 115))
        else:
            score = score_font.render("YOUR SCORE : {}".format(score_value), True, (90, 90, 90))
        screen.blit(score, (x, y))

    # Background music
    mixer.music.load("background_music.wav")
    mixer.music.play(-1)

    bullet_move = False

    while True:
        cursorX, cursorY = pygame.mouse.get_pos()
        # Background fill
        screen.fill((0, 0, 0))
        screen.blit(backgroundImage, (0, 0))

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif (event.type == MOUSEBUTTONDOWN and game_over) and (350 <= cursorX <= 920) and (400 <= cursorY <= 550):
                FIRSTGAME()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE and not game_over:
                    bullet_move = True
                elif event.key == K_RIGHT:
                    change_playerX = player_speed
                elif event.key == K_LEFT:
                    change_playerX = -player_speed
            elif event.type == KEYUP:
                change_playerX = 0
                if event.key == K_SPACE:
                    bullet_move = False

        # Player display
        if 10 <= playerX <= 1140:
            playerX += change_playerX
        elif playerX > 1140:
            playerX = 1135
        else:
            playerX = 15

        # Game Over display
        if game_over:
            GameOver(310, 135)
            enemyX = enemyY = [2500 for i in range(no_of_enemies)]
            scoreBox(405, 280)
        # Score display
        else:
            scoreBox(25, 25)
            player(playerX, playerY)

        # Continuous flow of Bullets
        if bullet_move:
            # Bullet sound play 
            Bullet_sound = mixer.Sound("bullet_sound.wav")
            Bullet_sound.play()
            for n in bulletX:
                if n == 0:
                    bulletX[bulletX.index(n)] = playerX + 5
                    break

        # Bullet movement
        for n in range(no_of_bullets):
            if bulletX[n] != 0:
                bullet(bulletX[n], bulletY[n])
                bullet(bulletX[n] + 87, bulletY[n])
                bulletY[n] -= 10

        # Obtaining enemys data from their data lists
        for i in range(no_of_enemies):
            # Enemy display
            enemy(enemyX[i], enemyY[i])
            if enemyY[i] >= 450:
                game_over = True
            enemyY[i] += (score_value * enemy_incr_speed) + enemy_start_speed
            for n in range(no_of_bullets):
                # Accuracy of the flow of Bullet
                if ((bulletX[n] - 60 <= enemyX[i] <= bulletX[n] + 145) and (bulletY[n] <= enemyY[i] + 10)) or (
                        bulletY[n] <= -50):
                    # Enemy attacked by our Bullet
                    if bulletY[n] > -50:
                        # Attack sound play
                        Attack_sound = mixer.Sound("attack_sound.wav")
                        Attack_sound.play()

                        enemyX[i] = random.randint(5, 1210)
                        enemyY[i] = -65
                        score_value += 1
                    bulletX[n] = 0
                    bulletY[n] = 535

        pygame.display.update()


FIRSTGAME()
