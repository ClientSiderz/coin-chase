import pygame

pygame.init()

display_info = pygame.display.Info()
NATIVE_WIDTH, NATIVE_HEIGHT = display_info.current_w, display_info.current_h

SCREEN = pygame.display.set_mode((NATIVE_WIDTH, NATIVE_HEIGHT), (pygame.FULLSCREEN | pygame.DOUBLEBUF))
CLOCK = pygame.time.Clock()

TITLE_FONT = pygame.font.SysFont(["consolas", "courier new", "monospace"], 32, bold=True, italic=True)
FONT = pygame.font.SysFont(["consolas", "courier new", "monospace"], 22, italic=True)
SMALL_FONT = pygame.font.SysFont(["consolas", "courier new", "monospace"], 16, italic=True)

RUNNING = True
GAME_OVER = False

# Load assets
CHARACTER_IMG = pygame.transform.scale(pygame.image.load('assets/character.png'), (128, 128))
COIN_IMG = pygame.transform.scale(pygame.image.load('assets/gold_coin.png'), (64, 64))
BOMB_IMG = pygame.transform.scale(pygame.image.load('assets/bomb.png'), (64, 64))
GRASS_IMG = pygame.transform.scale(pygame.image.load('assets/grass_field.png'), (NATIVE_WIDTH, NATIVE_HEIGHT))
