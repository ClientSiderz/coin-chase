import pygame
from settings import SCREEN, TITLE_FONT, FONT, SMALL_FONT, GRASS_IMG
from utils import get_color_from_percentage, draw_rect_with_outline

def render_game(character, player_pos, all_coins, all_bombs, coins_collected, record, space_bar_held):
    SCREEN.blit(GRASS_IMG, (0, 0))
    all_coins.draw(SCREEN)
    all_bombs.draw(SCREEN)
    SCREEN.blit(character, (player_pos.x - 64, player_pos.y - 64))

    # Score & record
    SCREEN.blit(FONT.render(f"coins: {coins_collected}", True, (255, 255, 255)), (10, 40))
    if record:
        SCREEN.blit(FONT.render(f"record: {record}", True, (255, 255, 255)), (10, 10))

    # Boost indicator
    if not space_bar_held:
        boost_text = FONT.render("press SPACE to boost", True, (255, 255, 255))
        SCREEN.blit(boost_text, (10, SCREEN.get_height() - 70))


def render_health_bar(health, max_health, hurt_time):
    health_rect = pygame.Rect(12, SCREEN.get_height() - 33, (health / max_health) * 296, 21)
    pygame.draw.rect(SCREEN, (54, 89, 51), (10, SCREEN.get_height() - 35, 300, 25))
    pygame.draw.rect(SCREEN, get_color_from_percentage((health / max_health) * 100), health_rect)
    SCREEN.blit(SMALL_FONT.render(f"{health}/{max_health}", True, (hurt_time, 0, 0)), (15, SCREEN.get_height() - 31))

def render_game_over(coins, record):
    SCREEN.blit(GRASS_IMG, (0, 0))
    
    draw_rect_with_outline(
        SCREEN,
        pygame.Rect((SCREEN.get_width() / 2) - 220, (SCREEN.get_height() / 2) - 160, 220 * 2, 160 * 2),
        fill_color=(60, 60, 60),
        outline_color=(30, 30, 30),
        radius=10
    )
    
    # texts = [
    #     ("Game Over", (255, 0, 0)),
    #     (f"Coins: {coins}", (255, 255, 255)),
    #     (f"Record: {record}", (255, 255, 255)),
    #     ("Press R to Restart or ESC to Quit", (255, 255, 255)),
    # ]
    # for i, (txt, color) in enumerate(texts):
    #     text_surface = FONT.render(txt, True, color)
    #     SCREEN.blit(text_surface, (SCREEN.get_width()//2 - 200, SCREEN.get_height()//2 - 100 + 50*i))game_over_text = font.render("Game Over", True, (255, 0, 0))
    string = "game over!"
    game_over_text = TITLE_FONT.render(string, True, (255, 40, 40))
    SCREEN.blit(
        game_over_text,
        (SCREEN.get_width() // 2 - (TITLE_FONT.size(string)[0] // 2),
        SCREEN.get_height() // 2 - 120)
    )
