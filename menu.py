# Import necessary libraries
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
pygame.display.set_caption("Game Menu")

# Load and scale the menu background image
background_image = pygame.image.load("images/background.jpg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Define button dimensions
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_MARGIN = 20

# Create font for buttons
button_font = pygame.font.Font(None, 40)

# Create font for the title
title_font = pygame.font.Font("images/pixel_font.ttf", 72)  # Replace "title_font.ttf" with your chosen font file

# Create "Start Game" button
start_button = pygame.Rect(
    WIDTH // 2 - BUTTON_WIDTH // 2,
    HEIGHT // 2 + BUTTON_MARGIN,
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
)

# Create "Quit" button
quit_button = pygame.Rect(
    WIDTH // 2 - BUTTON_WIDTH // 2,
    HEIGHT // 2 + BUTTON_HEIGHT + BUTTON_MARGIN * 2,
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
            # Quit the game if the window is closed
            running = False
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            # Check if "Start Game" button is clicked
            if start_button.collidepoint(mouse_pos):
                # Start the game if the button is clicked
                print("Start Game clicked")
                in_game = True
                main()
                in_game = False

            # Check if "Quit" button is clicked
            if quit_button.collidepoint(mouse_pos):
                # Quit the game if the button is clicked
                print("Quit clicked")
                running = False
                pygame.quit()
                sys.exit()

    # Blit the background image onto the screen
    screen.blit(background_image, (0, 0))

    # Draw buttons
    pygame.draw.rect(screen, BLACK, start_button)
    pygame.draw.rect(screen, BLACK, quit_button)

    # Render text for buttons
    start_text = button_font.render("Start Game", True, WHITE)
    quit_text = button_font.render("Quit", True, WHITE)

    # Center the text on buttons
    start_text_rect = start_text.get_rect(center=start_button.center)
    quit_text_rect = quit_text.get_rect(center=quit_button.center)

    # Draw text on buttons
    screen.blit(start_text, start_text_rect)
    screen.blit(quit_text, quit_text_rect)

    # Render and position the title text
    title_lines = ["Survive", "The", "Savana"]
    title_texts = [title_font.render(line, True, BLACK) for line in title_lines]
    title_height = sum([text.get_height() for text in title_texts])
    title_y = (HEIGHT - title_height - BUTTON_HEIGHT * 2 - BUTTON_MARGIN * 4) // 2

    for i, text in enumerate(title_texts):
        text_rect = text.get_rect(center=(WIDTH // 2, title_y + text.get_height() // 2))
        screen.blit(text, text_rect)
        title_y += text.get_height()

    # Update the display
    pygame.display.update()
