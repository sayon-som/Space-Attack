import pygame  # installing the pygame library
import random
import math
# for music
from pygame import  mixer
pygame.init()  # Initialsise the pygame
screen = pygame.display.set_mode((800, 600))  # creating the display
# If we create a infinite loop the window hangs as the quit method funcitionality is not being provided.
# ensure the game is running
# TITLE AND LOGO
pygame.display.set_caption("Space Attack")  # adding the title
icon = pygame.image.load('spaceship.png')  # adding the icon
pygame.display.set_icon(icon)

# Player
player_image = pygame.image.load('space-invaders (1).png')
player_X = 370
player_Y = 480
player_change = 0
# enemy
enemy_image = []
enemy_X = []
enemy_Y = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 7
for i in range(num_of_enemies):
    enemy_image.append(pygame.image.load('alien (3).png'))
    enemy_X.append(random.randint(0, 735))  # respawing into random places
    enemy_Y.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)
# bullets
bullets_image = pygame.image.load('bullet.png')
bullets_X = 0
bullets_Y = 480  # same level as the space ship
bullets_Xchange = 0
bullets_Ychange = 20
bullet_state = "ready"
# background

background_image = pygame.image.load('background.png')
#background sound

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 16)
score_x = 10
score_y = 10
#game over
over_font=pygame.font.Font('freesansbold.ttf',64)
#FOR score
def show_score(x,y):
    score = font.render("SCORE: " + str(score_value), True, (255, 255, 255))
    screen.blit(score,(x,y))

#Game over function
def text_over():
 text =over_font.render("GAME OVER", True, (255, 255, 255))
 screen.blit(text, (200, 250))


def player(x, y):
    screen.blit(player_image, (x, y))  # drawing the image


def enemy(x, y, i):
    screen.blit(enemy_image[i], (x, y))  # drawing the image


def fire(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullets_image, (x + 16, y + 10))


# collision function
def collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(enemy_x - bullet_x, 2)) + (math.pow(enemy_y - bullet_y, 2)))
    if distance < 27:  # condition for collison
        return True
    else:
        return False


# GAME WINDOW
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # checking if the event is the quit event or not
            running = False

        # checking the keystroke
        if event.type == pygame.KEYDOWN:  # pressing the key
            if event.key == pygame.K_LEFT:  # left key is being presses
                player_change = -5
            if event.key == pygame.K_RIGHT:
                player_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound=mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bullets_X = player_X  # getting the current cooordinate of the space ship.
                    fire(bullets_X, bullets_Y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_change = 0

    screen.fill((0, 0, 0))  # chaning the colour
    # background - color
    screen.blit(background_image, (0, 0))

    player_X = player_X + player_change
    if player_X <= 0:
        player_X = 0
    elif player_X >= 736:
        player_X = 736
    for i in range(num_of_enemies):#enemy movement
        #game over
        if enemy_Y[i]>330:
            for j in range(num_of_enemies):
                enemy_Y[j]=2000
            text_over()
            break



        enemy_X[i] = enemy_X[i] + enemyX_change[i]
        if enemy_X[i] <= 0:
            enemyX_change[i] = 4
            enemy_Y[i] += enemyY_change[i]
        elif enemy_X[i] >= 736:
            enemyX_change[i] = -4
            enemy_Y[i] += enemyY_change[i]
        collision1 = collision(enemy_X[i], enemy_Y[i], bullets_X, bullets_Y)
        if collision1:
            col_sound = mixer.Sound('explosion.wav')
            col_sound.play()
            bullets_Y = 480
            bullet_state = "ready"
            score_value = score_value + 1
            enemy_X[i] = random.randint(0, 735)  # respawing into random places
            enemy_Y[i] = random.randint(50, 150)
        enemy(enemy_X[i], enemy_Y[i], i)  # indentifying the enemy
        # bullet motion

        # multiple bullets
    if bullets_Y <= 0:
        bullets_Y = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire(bullets_X, bullets_Y)
        bullets_Y -= bullets_Ychange

    player(player_X, player_Y)  # player function is being called
    show_score(score_x,score_y)

    pygame.display.update()  # update the screen
