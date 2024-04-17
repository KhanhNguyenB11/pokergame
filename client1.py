import sys
import  Draw
import pygame
from Network import Network
HOST = 'localhost'
PORT = 65432

WIDTH, HEIGHT = 800, 600
WINDOW_SIZE = (WIDTH, HEIGHT)
SCREEN = pygame.display.set_mode(WINDOW_SIZE)
# Load background image
background_image = pygame.image.load("Images/Table.jpg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

menu_image = pygame.image.load("Images/menu.jpg")
menu_image = pygame.transform.scale(menu_image, (WIDTH, HEIGHT))
# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()
pygame.font.init()
font = pygame.font.SysFont(None, 32)

# Text field properties
text_color = BLACK

text_field_name = "Name:"
input_rect1 = pygame.Rect(300, 200, 200, 30)
input_rect2 = pygame.Rect(300, 250, 200, 30)
Enter_rect = pygame.Rect(300, 300, 200, 30)

input_color2 = BLACK
input_color1 = BLACK


room_id = ""
name = ""
def Waiting(network,host):
    pygame.display.set_caption("Waiting")
    running = True
    dragging = False

    print(HOST)
    SCREEN.fill((0, 0, 0))


    current_value=0
    max_value=5000
    slider_x=550
    thumb_radius=10
    slider_width=200
    slider_y=570

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the mouse click is on the thumb
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if (slider_x - 10 <= mouse_x <= slider_x + slider_width + thumb_radius and
                        slider_y - thumb_radius <= mouse_y <= slider_y + thumb_radius):
                    dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False
            elif event.type == pygame.MOUSEMOTION and dragging:
                # Update thumb position when dragging
                mouse_x, mouse_y = pygame.mouse.get_pos()
                current_value = min(
                    max((mouse_x - slider_x) / slider_width * (max_value - 0) +0, 0),
                    max_value)

        SCREEN.blit(background_image, (0, 0))
        number=(int)(network.sendData(f"get_number"))

        Draw.drawChoiceButton(SCREEN,True,font)

        pygame.draw.rect(SCREEN, (206, 228, 19), (slider_x,slider_y , slider_width, 10))
        thumb_x = int(slider_x + (current_value - 0) / (max_value - 0) * slider_width)
        pygame.draw.circle(SCREEN, (19, 228, 23), (thumb_x, slider_y+5), thumb_radius)
        current_valueSur = font.render(f'{int(current_value)}', True, (250, 250, 250))
        current_valueText = current_valueSur.get_rect()
        current_valueText.center = (slider_x-50, slider_y)
        SCREEN.blit(current_valueSur, current_valueText)






        pygame.draw.circle(SCREEN, (255,80,100), (350,450), 50)
        if(number<2):
            name_surface = font.render('Waiting for People', True, (250, 250, 250))
            name_rect = name_surface.get_rect()
            name_rect.center=(400,250)
            SCREEN.blit(name_surface, name_rect)
        else:
            if(host):
                network.sendData("START")

            Play(network)
            break
        pygame.display.update()


def Play(network):
    pygame.display.set_caption("Play")
    running = True
    SCREEN.fill((0, 0, 0))
    list_player=(network.GetObs(f"get_players"))

    while running:
        data = (network.GetObs(f"get_hands"))
        # turn=(network.sendData(f"getTurn")) == "True"
        if not data:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        SCREEN.blit(background_image, (0, 0))
        Draw.drawCards(SCREEN,data)
        Draw.drawPlayers(SCREEN,list_player,font)
        # Draw.drawChoiceButton(SCREEN,turn,font)
        name_surface = font.render('Playing', True, (250, 250, 250))
        name_rect = name_surface.get_rect()
        name_rect.center = (400, 250)
        SCREEN.blit(name_surface, name_rect)

        pygame.display.update()
        pygame.display.flip()


def Menu():
    # Get room ID from user\
    pygame.display.set_caption("Simple Pygame Window")
    game_state = "menu"
    hover_Color = (100, 100, 100)

    running = True
    text_input1 = ""
    input_active1 = False
    text_input2 = ""
    input_active2 = False
    n=Network()
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type ==  pygame.MOUSEMOTION:
                if Enter_rect.collidepoint(event.pos):
                    hover_Color = (100, 100, 50)
                elif input_rect2.collidepoint(event.pos):
                    input_color2=(90,150,190)
                elif input_rect1.collidepoint(event.pos):
                    input_color1 = (90, 150, 190)
                else:
                    hover_Color = (100, 100, 100)
                    input_color1=BLACK
                    input_color2=BLACK

            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicks on the input box, toggle input_active
                if Enter_rect.collidepoint(event.pos):
                    room_id=text_input2
                    name = text_input1
                    game_state = "play"
                if input_rect1.collidepoint(event.pos):
                    input_active1 = True
                    input_active2 = False
                elif input_rect2.collidepoint(event.pos):
                    input_active2 = True
                    input_active1 = False
                else:
                    input_active1 = False
                    input_active2 = False
            if event.type == pygame.KEYDOWN:
                # If input_active is True, handle key presses
                if input_active1:
                    if event.key == pygame.K_BACKSPACE :
                        # If Backspace is pressed, remove the last character from the input
                        text_input1 = text_input1[:-1]
                        # If Backspace is pressed, remove the last character from the input

                    else:
                        # Add the pressed key to the input
                        text_input1 += event.unicode
                if input_active2:
                    if event.key == pygame.K_BACKSPACE  or event.key == pygame.K_BACKSPACE:
                        # If Backspace is pressed, remove the last character from the input
                        text_input2 = text_input2[:-1]
                        # If Backspace is pressed, remove the last character from the input

                    else:
                        # Add the pressed key to the input
                        text_input2 += event.unicode

        if game_state == "menu":
            SCREEN.blit(menu_image, (0, 0))
            pygame.draw.rect(SCREEN, (200, 200, 200), input_rect1)
            pygame.draw.rect(SCREEN, BLACK, input_rect1, 2)
            text_surface = font.render(text_input1, True, WHITE)
            SCREEN.blit(text_surface, (input_rect1.x + 5, input_rect1.y + 5))

            name_surface = font.render('Name:', True, BLACK)
            name_rect = name_surface.get_rect(midleft=(input_rect1.left - 70, input_rect1.centery))
            SCREEN.blit(name_surface, name_rect)

            pygame.draw.rect(SCREEN, (200, 200, 200), input_rect2)
            pygame.draw.rect(SCREEN, BLACK, input_rect2, 2)
            text_surface = font.render(text_input2, True, WHITE)
            SCREEN.blit(text_surface, (input_rect2.x + 5, input_rect2.y + 5))

            name_surface1 = font.render('Id Table:', True, BLACK)
            name_rect1 = name_surface1.get_rect(midleft=(input_rect2.left - 95, input_rect2.centery))
            SCREEN.blit(name_surface1, name_rect1)

            name_surface1 = font.render('START', True, BLACK)
            name_rect1 = name_surface1.get_rect(midleft=(Enter_rect.left + 50, Enter_rect.centery))
            pygame.draw.rect(SCREEN, hover_Color, Enter_rect)
            SCREEN.blit(name_surface1, name_rect1)

        elif game_state == "play":
            host=n.setNAR(room_id,name)
            Waiting(n,host)
            break
        pygame.display.update()
        pygame.display.flip()
Menu()
pygame.quit()





    # Connect and join the room

