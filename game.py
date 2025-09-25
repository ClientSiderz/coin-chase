# Example file showing a circle moving on screen
import colorsys
import pygame
import random
import json
import os

from pygame.locals import *

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
game_over = False

font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 30)

character = pygame.image.load('assets/character.png')
character = pygame.transform.scale(character, (128, 128))
character_width, character_height = character.get_size()

space_bar_key_held = False

coin_image = pygame.image.load('assets/gold_coin.png')
coin_image = pygame.transform.scale(coin_image, (64, 64))
coins_collected = 0
highest_record_coins_collected = 0

bomb_image = pygame.image.load('assets/bomb.png')
bomb_image = pygame.transform.scale(bomb_image, (64, 64))

difficulty = 0

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):   
        super().__init__()
        self.image = coin_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = random.randint(2, 5)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > screen.get_height():
            self.kill()
            
class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y):   
        super().__init__()
        self.image = bomb_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = random.randint(2, 5)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > screen.get_height():
            self.kill()

all_coins = pygame.sprite.Group()
all_bombs = pygame.sprite.Group()

dt = 0
speed = 400

boost_cooldown_end = 0
boost_cooldown_time = 2000

window_width, window_height = screen.get_size()

# Grass assets import
grass = pygame.image.load('assets/grass_field.png')
grass = pygame.transform.scale(grass, (window_width, window_height))

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

player_health = 10
player_max_health = 10

player_hurt_time = 0

def load_session():
    """Loads the session data from a file."""
    try:
        with open(".gamedata/session.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: Last session not found. A new session file will be made when exited.")
        return 0

def save_session(data):
    """Saves the session data to a file."""
    os.makedirs(".gamedata", exist_ok=True)
    with open(".gamedata/session.json", "w") as file:
        json.dump(data, file)

def render_game_over():
    screen.blit(grass, (0, 0))
    
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    coins_text = font.render(f"Coins Collected: {coins_collected}", True, (255, 255, 255))
    highest_record_coins_text = font.render(f"Highest Record Coins Collected: {highest_record_coins_collected}", True, (255, 255, 255))
    restart_text = font.render("Press R to Restart or ESC to Quit", True, (255, 255, 255))

    screen.blit(game_over_text, (screen.get_width() // 2 - 100, screen.get_height() // 2 - 100))
    screen.blit(highest_record_coins_text, (screen.get_width() // 2 - 200, screen.get_height() // 2 - 50))
    screen.blit(coins_text, (screen.get_width() // 2 - 130, screen.get_height() // 2))
    screen.blit(restart_text, (screen.get_width() // 2 - 200, screen.get_height() // 2 + 50))

def render_game():
    screen.blit(grass, (0, 0)) # Renders the grass field
    
    all_coins.draw(screen) # Renders the coins
    
    all_bombs.draw(screen) # Renders the bombs
    
    screen.blit(character, (player_pos.x - character_width / 2, player_pos.y - character_height / 2)) # Renders the main character
    
    coins_text = font.render(f"Coins: {coins_collected}", True, (255, 255, 255))
    screen.blit(coins_text, (10, 40 if highest_record_coins_collected != 0 else 10))
    
    highest_record_coins_collected_text = font.render(f"Highest Record Coins Collected: {highest_record_coins_collected}", True, (255, 255, 255))
    if highest_record_coins_collected != 0:
        screen.blit(highest_record_coins_collected_text, (10, 10))
    
    boost_indicator = font.render("Press SPACE to Boost", True, (255, 255, 255))
    if not space_bar_key_held:
        screen.blit(boost_indicator, (10, screen.get_height() - 70))

def get_color_from_percentage(percentage):
    percentage = max(0, min(100, percentage))

    hue = (percentage / 100.0) / 3.0
    
    rgb_float = colorsys.hsv_to_rgb(hue, 1.0, 1.0)

    red = int(rgb_float[0] * 255)
    green = int(rgb_float[1] * 255)
    blue = int(rgb_float[2] * 255)

    return (red, green, blue)
        
healthRectOverlay = Rect(10, screen.get_height() - 35, 300, 25)
def render_health_bar():
    health_text = small_font.render(f"{player_health} / {player_max_health}", True, (player_hurt_time, 0, 0))
    
    healthRect = Rect(12, screen.get_height() - 33, (player_health / player_max_health) * 296, 21)
    pygame.draw.rect(screen, (54, 89, 51), healthRectOverlay)
    pygame.draw.rect(screen, get_color_from_percentage((player_health / player_max_health) * 100), healthRect)
    
    screen.blit(health_text, (15, screen.get_height() - 31))
    
    
def collisions():
    global coins_collected, game_over, player_health, player_hurt_time
    # Check for coin collisions
    player_rect = pygame.Rect(player_pos.x - character_width / 2, player_pos.y - character_height / 2, character_width, character_height)
    for coin in all_coins:
        if player_rect.colliderect(coin.rect):
            coins_collected += 1
            coin.kill()
            
    for bomb in all_bombs:
        if player_rect.colliderect(bomb.rect):
            # game_over = True
            player_hurt_time = 222
            player_health -= 1
            bomb.kill()
            break

def spawn_obsticles():
    if random.random() < 0.02:
        x_pos = random.randint(0, screen.get_width())
        new_coin = Coin(x_pos, -32)
        all_coins.add(new_coin)
        
    if random.random() < 0.02:
        x_pos = random.randint(0, screen.get_width())
        new_bomb = Bomb(x_pos, -32)
        all_bombs.add(new_bomb)
        
def update_position():
    all_coins.update() # Updates the coins position
    all_bombs.update()
    
def main_character_movement():
    global player_pos, speed, space_bar_key_held, boost_cooldown_end

    # Handle input and build direction vector
    keys = pygame.key.get_pressed()
    move_dir = pygame.Vector2(0, 0)

    if keys[pygame.K_w] | keys[pygame.K_UP]:
        move_dir.y -= 1
    if keys[pygame.K_s] | keys[pygame.K_DOWN]:
        move_dir.y += 1
    if keys[pygame.K_a] | keys[pygame.K_LEFT]:
        move_dir.x -= 1
    if keys[pygame.K_d] | keys[pygame.K_RIGHT]:
        move_dir.x += 1

    # Normalize diagonal movement
    if move_dir.length_squared() > 0:
        move_dir = move_dir.normalize()

    # Move player
    player_pos += move_dir * speed * dt

    # Clamp player within window
    player_pos.x = max(character_width / 2, min(player_pos.x, window_width - character_width / 2))
    player_pos.y = max(character_height / 2, min(player_pos.y, window_height - character_height / 2))

    # Player Boost
    if keys[pygame.K_SPACE] and not space_bar_key_held and pygame.time.get_ticks() >= boost_cooldown_end:
        speed = 900
        space_bar_key_held = True
        boost_cooldown_end = pygame.time.get_ticks() + boost_cooldown_time

    if speed > 400:
        speed -= 20

    if pygame.time.get_ticks() >= boost_cooldown_end:
        space_bar_key_held = False
        
highest_record_coins_collected = load_session()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        
        spawn_obsticles()
        
        update_position()
        
        collisions()
        
        render_game()
        
        render_health_bar()
        
        main_character_movement()
        
        if player_health <= 0:
            game_over = True
    else:
        render_game_over()

        if highest_record_coins_collected < coins_collected:
            highest_record_coins_collected = coins_collected
            save_session(highest_record_coins_collected)

        # Handle Game Over input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            # Reset the game
            coins_collected = 0
            
            player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
            
            all_coins.empty()
            all_bombs.empty()
            
            player_health = player_max_health
            
            game_over = False
            
            speed = 400
            boost_cooldown_end = 0
        elif keys[pygame.K_ESCAPE]:
            running = False

    pygame.display.flip()
    dt = clock.tick(60) / 1000
    if player_hurt_time > 0:
        player_hurt_time -= 2

pygame.quit()
