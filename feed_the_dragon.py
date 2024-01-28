#Feed the Dragon

import pygame
import random
#initialize pygame
pygame.init()

#GAME CONSTANTS
GAME_FOLDER = 'd:/batches/py21/feed_the_dragon/'
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 600
FPS = 60

BUFFER_DISTANCE = -150

DRAGON_VELOCITY = 30
DEFAULT_COIN_VELOCITY = 5
MAX_LIVES = 5

GREEN = pygame.Color(0,255,0)
RED = pygame.Color(255,0,0)

#create the window
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Feed the Dragon')

#background_image
background_image = pygame.image.load(GAME_FOLDER + 'dragon_night.jpg')
#background_music
pygame.mixer.music.load(GAME_FOLDER + 'background_feed_the_dragon.mp3')
pygame.mixer.music.set_volume(0.7)
pygame.mixer.music.play(-1)

#assets
coin = pygame.image.load(GAME_FOLDER + 'coin.png')
coin_rect = coin.get_rect()
coin_rect.left = BUFFER_DISTANCE
coin_rect.centery = random.randint(50, WINDOW_HEIGHT-50)

dragon = pygame.image.load(GAME_FOLDER + 'dragon.png')
dragon_rect = dragon.get_rect()
dragon_rect.right = WINDOW_WIDTH - 10
dragon_rect.centery = WINDOW_HEIGHT//2

#sounds
loss = pygame.mixer.Sound(GAME_FOLDER + 'loss.wav')
loss.set_volume(0.4)
catch = pygame.mixer.Sound(GAME_FOLDER + 'catch.wav')
catch.set_volume(0.4)
#game_values
current_coin_velocity = DEFAULT_COIN_VELOCITY
game_score = 0
game_lives = MAX_LIVES
game_status = 1 #active

#generate texts
game_font = pygame.font.Font(GAME_FOLDER + 'AttackGraffiti.ttf', 30)
title_font = pygame.font.Font(GAME_FOLDER + 'AttackGraffiti.ttf', 40)

title_text = title_font.render('Feed the Dragon', True, GREEN)
title_text_rect = title_text.get_rect()
title_text_rect.top = 10
title_text_rect.centerx = WINDOW_WIDTH//2


score_text = game_font.render('Score: ' + str(game_score), True, GREEN)
score_text_rect = score_text.get_rect()
score_text_rect.left = 50
score_text_rect.top =10

lives_text = game_font.render('Lives: ' + str(game_lives), True, GREEN)
lives_text_rect = lives_text.get_rect()
lives_text_rect.right = WINDOW_WIDTH - 50
lives_text_rect.top = 10

game_over_text = title_font.render('GAME OVER!!!', True, RED)
game_over_text_rect = game_over_text.get_rect()
game_over_text_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

restart_text = game_font.render('Press r to RESTART!!!', True, GREEN)
restart_text_rect = restart_text.get_rect()
restart_text_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 +60)


#clock
clock = pygame.time.Clock()
running = True
while running: #main game loop- defines life of the game
    #blit the background
    display_surface.blit(background_image, (0,0))

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_UP and dragon_rect.top > 50 and game_status ==1:
                dragon_rect.top -= DRAGON_VELOCITY
            elif ev.key == pygame.K_DOWN and dragon_rect.bottom < WINDOW_HEIGHT and game_status ==1:
                dragon_rect.top += DRAGON_VELOCITY
            elif ev.key == pygame.K_r:
                game_status = 1
                current_coin_velocity = DEFAULT_COIN_VELOCITY

                game_score = 0
                score_text = game_font.render('Score: ' + str(game_score), True, pygame.Color(0, 255, 0))

                game_lives = MAX_LIVES
                lives_text = game_font.render('Lives: ' + str(game_lives), True, GREEN)

                dragon_rect.right = WINDOW_WIDTH - 10
                dragon_rect.centery = WINDOW_HEIGHT // 2

                coin_rect.left = BUFFER_DISTANCE
                coin_rect.centery = random.randint(50, WINDOW_HEIGHT - 50)

                pygame.mixer.music.play(-1)

    #shoot the coin
    if game_status == 1:
        coin_rect.right += current_coin_velocity
        if coin_rect.colliderect(dragon_rect):
            game_score+=1
            score_text = game_font.render('Score: ' + str(game_score), True, pygame.Color(0, 255, 0))
            catch.play()
            current_coin_velocity += 0.3
            # reset the coin (as if a new coin is coming next)
            coin_rect.left = BUFFER_DISTANCE
            coin_rect.centery = random.randint(50, WINDOW_HEIGHT - 50)
        elif coin_rect.right > WINDOW_WIDTH:
            loss.play()
            game_lives-=1
            lives_text = game_font.render('Lives: ' + str(game_lives), True, GREEN)

            if game_lives == 0:
                game_status = 2

            #reset the coin (as if a new coin is coming next)
            coin_rect.left = BUFFER_DISTANCE
            coin_rect.centery = random.randint(50, WINDOW_HEIGHT-50)

        #blit the assets
        display_surface.blit(coin, coin_rect)
        display_surface.blit(dragon, dragon_rect)

    elif game_status == 2:
        display_surface.blit(game_over_text, game_over_text_rect)
        display_surface.blit(restart_text, restart_text_rect)
        pygame.mixer.music.stop()

    #blit the HUD
    display_surface.blit(title_text, title_text_rect)
    display_surface.blit(score_text, score_text_rect)
    display_surface.blit(lives_text, lives_text_rect)

    #update the display
    pygame.display.update()
    #moderate the rate of iteration
    clock.tick(FPS)

#dispose the resource
pygame.quit()