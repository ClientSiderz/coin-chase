import pygame
from settings import SCREEN

def handle_player_movement(player_pos, dt, speed, space_bar_key_held, boost_end, boost_cooldown):
    keys = pygame.key.get_pressed()
    move_dir = pygame.Vector2(0, 0)

    if keys[pygame.K_w] or keys[pygame.K_UP]:
        move_dir.y -= 1
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        move_dir.y += 1
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        move_dir.x -= 1
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        move_dir.x += 1

    if move_dir.length_squared() > 0:
        move_dir = move_dir.normalize()

    player_pos += move_dir * speed * dt
    player_pos.x = max(64, min(player_pos.x, SCREEN.get_width() - 64))
    player_pos.y = max(64, min(player_pos.y, SCREEN.get_height() - 64))

    if keys[pygame.K_SPACE] and not space_bar_key_held and pygame.time.get_ticks() >= boost_end:
        speed = 900
        space_bar_key_held = True
        boost_end = pygame.time.get_ticks() + boost_cooldown

    if speed > 400:
        speed -= 20
    if pygame.time.get_ticks() >= boost_end:
        space_bar_key_held = False

    return player_pos, speed, space_bar_key_held, boost_end
