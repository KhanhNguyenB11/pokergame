import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Slider Range")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)

# Slider parameters
slider_x = 100  # X-coordinate of the slider track
slider_y = HEIGHT // 2  # Y-coordinate of the slider track
slider_width = 600  # Width of the slider track
slider_height = 10  # Height of the slider track
thumb_radius = 15  # Radius of the slider thumb
min_value = 0
max_value = 100
current_value = min_value  # Initial value of the slider

# Main game loop
running = True
dragging = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse click is on the thumb
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if (slider_x - thumb_radius <= mouse_x <= slider_x + slider_width + thumb_radius and
                    slider_y - thumb_radius <= mouse_y <= slider_y + thumb_radius):
                dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
        elif event.type == pygame.MOUSEMOTION and dragging:
            # Update thumb position when dragging
            mouse_x, mouse_y = pygame.mouse.get_pos()
            current_value = min(max((mouse_x - slider_x) / slider_width * (max_value - min_value) + min_value, min_value), max_value)

    # Clear the screen
    screen.fill(WHITE)

    # Draw the slider track
    pygame.draw.rect(screen, GRAY, (slider_x, slider_y - slider_height // 2, slider_width, slider_height))

    # Draw the thumb
    thumb_x = int(slider_x + (current_value - min_value) / (max_value - min_value) * slider_width)
    pygame.draw.circle(screen, GREEN, (thumb_x, slider_y), thumb_radius)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
