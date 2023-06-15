import pygame
import sys
from game import main
# Initialize Pygame
pygame.init()

# Set window dimensions
WIDTH = 512
HEIGHT = 512

# Set colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu Example")

# Define button dimensions
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_MARGIN = 20

# Create font
font = pygame.font.Font(None, 40)

# Create "Start Game" button
start_button = pygame.Rect(
    WIDTH // 2 - BUTTON_WIDTH // 2,
    HEIGHT // 2 - BUTTON_HEIGHT - BUTTON_MARGIN // 2,
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
)

# Create "Quit" button
quit_button = pygame.Rect(
    WIDTH // 2 - BUTTON_WIDTH // 2,
    HEIGHT // 2 + BUTTON_MARGIN // 2,
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
)

# Game loop
running = True
in_game = False  # Flag to indicate if the game is in progress

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            # Check if "Start Game" button is clicked
            if start_button.collidepoint(mouse_pos):
                print("Start Game clicked")
                in_game = True
                main()
                in_game = False

            # Check if "Quit" button is clicked
            if quit_button.collidepoint(mouse_pos):
                print("Quit clicked")
                running = False
                pygame.quit()
                sys.exit()

    # Clear the screen
    screen.fill(WHITE)

    # Draw buttons
    pygame.draw.rect(screen, BLACK, start_button)
    pygame.draw.rect(screen, BLACK, quit_button)

    # Render text
    start_text = font.render("Start Game", True, WHITE)
    quit_text = font.render("Quit", True, WHITE)

    # Center the text on buttons
    start_text_rect = start_text.get_rect(center=start_button.center)
    quit_text_rect = quit_text.get_rect(center=quit_button.center)

    # Draw text on buttons
    screen.blit(start_text, start_text_rect)
    screen.blit(quit_text, quit_text_rect)

    # Update the display
    pygame.display.update()
