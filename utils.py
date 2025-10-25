import json, os, colorsys, pygame

def load_session():
    try:
        with open(".gamedata/session.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("No previous session found.")
        return 0

def save_session(data):
    os.makedirs(".gamedata", exist_ok=True)
    with open(".gamedata/session.json", "w") as file:
        json.dump(data, file)

def get_color_from_percentage(percentage):
    percentage = max(0, min(100, percentage))
    hue = (percentage / 100.0) / 3.0
    r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
    return (int(r*255), int(g*255), int(b*255))

def draw_rect_with_outline(
    surface,
    rect,
    fill_color=(0, 0, 0),
    outline_color=(255, 255, 255),
    outline_thickness=2,
    alpha=255,
    radius=0
):
    # Create a temporary surface with per-pixel alpha
    temp_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)

    # Fill rectangle (if fill_color is not None)
    if fill_color:
        inner_rect = pygame.Rect(
            outline_thickness,
            outline_thickness,
            rect.width - outline_thickness * 2,
            rect.height - outline_thickness * 2,
        )
        pygame.draw.rect(temp_surface, (*fill_color, alpha), inner_rect, border_radius=radius)

    # Draw outline
    pygame.draw.rect(temp_surface, (*outline_color, alpha), temp_surface.get_rect(), outline_thickness, border_radius=radius)

    # Blit onto the main surface
    surface.blit(temp_surface, rect.topleft)