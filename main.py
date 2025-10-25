import pygame, random
from settings import *
from objects import Coin, Bomb, ALL_COINS, ALL_BOMBS
from render import render_game, render_health_bar, render_game_over
from utils import load_session, save_session
from player import handle_player_movement

player_pos = pygame.Vector2(SCREEN.get_width() / 2, SCREEN.get_height() / 2)
player_health, player_max_health = 10, 10
player_hurt_time = 0
coins_collected = 0
record = load_session()

speed = 400
space_bar_held = False
boost_end = 0
boost_cd = 2000
dt = 0
game_over = False
running = True

def spawn_objects():
    if random.random() < 0.02:
        ALL_COINS.add(Coin(random.randint(0, SCREEN.get_width()), -32))
    if random.random() < 0.02:
        ALL_BOMBS.add(Bomb(random.randint(0, SCREEN.get_width()), -32))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        spawn_objects()
        ALL_COINS.update()
        ALL_BOMBS.update()

        # collisions
        player_rect = pygame.Rect(player_pos.x - 64, player_pos.y - 64, 128, 128)
        for coin in ALL_COINS:
            if player_rect.colliderect(coin.rect):
                coins_collected += 1
                coin.kill()
        for bomb in ALL_BOMBS:
            if player_rect.colliderect(bomb.rect):
                player_health -= 1
                player_hurt_time = 222
                bomb.kill()

        render_game(CHARACTER_IMG, player_pos, ALL_COINS, ALL_BOMBS, coins_collected, record, space_bar_held)
        render_health_bar(player_health, player_max_health, player_hurt_time)

        player_pos, speed, space_bar_held, boost_end = handle_player_movement(
            player_pos, dt, speed, space_bar_held, boost_end, boost_cd
        )

        if player_health <= 0:
            game_over = True
    else:
        render_game_over(coins_collected, record)
        if coins_collected > record:
            record = coins_collected
            save_session(record)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            coins_collected = 0
            player_health = player_max_health
            player_pos = pygame.Vector2(SCREEN.get_width()/2, SCREEN.get_height()/2)
            ALL_COINS.empty()
            ALL_BOMBS.empty()
            game_over = False
            speed = 400
        elif keys[pygame.K_ESCAPE]:
            running = False

    pygame.display.flip()
    dt = CLOCK.tick(60) / 1000
    if player_hurt_time > 0:
        player_hurt_time -= 2

pygame.quit()
