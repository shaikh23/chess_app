import pygame
import sys

# Constants
WIDTH, HEIGHT = 640, 640
ROWS, COLS = 8, 8
TILE_SIZE = WIDTH // COLS

# Colors
WHITE = (240, 217, 181)
BLACK = (181, 136, 99)

def draw_board(screen):
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess Board")

    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw the board
        draw_board(screen)

        # Update the display
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()