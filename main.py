import pygame
from cell import (
    Cell,
    CellType,
)  # Assuming your Cell class and CellType enum are in a separate module

# INIT
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 10
SCALE_FACTOR = 1

pygame.init()
window = pygame.display.set_mode(
    (WIDTH, HEIGHT), pygame.SRCALPHA
)  # Enable alpha channel
pygame.display.set_caption("AutoCelU")

screen = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

GRID_WIDTH = int(WIDTH / CELL_SIZE)
GRID_HEIGHT = int(HEIGHT / CELL_SIZE)

GRID = [[Cell() for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

paused = False
show_controls = True
font = pygame.font.Font(None, 22)  # You can adjust the font size as needed

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                SCALE_FACTOR += 1
            elif event.y < 0:
                SCALE_FACTOR -= 1
            SCALE_FACTOR = max(1, SCALE_FACTOR)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 2:
                paused = not paused
                print(paused)
            # Get the position of the mouse click
            x, y = event.pos
            # Convert the position to grid coordinates
            i = y // CELL_SIZE
            j = x // CELL_SIZE
            # Toggle the state of the clicked cell
            GRID[i][j].make_this_of_type(
                CellType.GREENS
                if event.button == 1
                else (CellType.REDS if event.button == 3 else CellType.EMPTY)
            )
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            show_controls = not show_controls

    # UPDATE
    if not paused:
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                GRID[i][j].tick(GRID, i, j)

    # DRAW
    if not paused:
        screen.fill((255, 255, 255, 0))  # Clear the screen
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                x = j * CELL_SIZE
                y = i * CELL_SIZE
                GRID[i][j].draw(screen, x, y, CELL_SIZE)

        # Display controls information
        if show_controls:
            control_text = (
                f"Mouse-> Left: Add Greens, Right: Add Reds, Middle: Toggle Simulation"
            )
            scale_text = f"Mouse Wheel: Adjust Blur (Current: {SCALE_FACTOR})"
            controls_rendered = font.render(control_text, True, (0, 0, 255))
            scale_rendered = font.render(scale_text, True, (0, 0, 255))
            screen.blit(controls_rendered, (10, 10))
            screen.blit(scale_rendered, (10, 50))

            escape_text = font.render("Press Esc: Toggle Controls", True, (0, 0, 255))
            screen.blit(escape_text, (10, 90))

    if paused:
        pause_text = font.render("Paused", True, (255, 0, 0))
        screen.blit(pause_text, (10, 120))

    scale = 1.0 / float(SCALE_FACTOR)

    surf_size = screen.get_size()
    scale_size = (int(surf_size[0] * scale), int(surf_size[1] * scale))
    surf = pygame.transform.smoothscale(screen, scale_size)
    screen = pygame.transform.smoothscale(surf, surf_size)

    # CLEAR SCREEN
    window.blit(screen, (0, 0))
    pygame.display.flip()
    # time.sleep(0.1)

# Quit Pygame
pygame.quit()
