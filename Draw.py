import pygame
import time
POSITIONS=[(120,150),(100,200),(400,100),(400,100)]



def drawCards(screen,cards):
    if cards:
        for ind,card in enumerate(cards):
            card_game=pygame.image.load(f"IMGCards/{card}.png")
            card_image = pygame.transform.scale(card_game, (75, 100))
            screen.blit(card_image, (350+55*ind, 360))


def drawflop(screen,flop):
    if flop:
        for ind,card in enumerate(flop):
            card_game=pygame.image.load(f"IMGCards/{card}.png")
            card_image = pygame.transform.scale(card_game, (75, 100))
            screen.blit(card_image, (200+80*ind, 200))


def drawPlayers(screen,players,player_bet):
    if players:
        font = pygame.font.SysFont(None, 24)

        for ind,player in enumerate(players):
            pygame.draw.circle(screen, (255, 80, 100), POSITIONS[ind], 30)
            name_surface = font.render(player[0], True, (250, 250, 250))
            name_rect = name_surface.get_rect()
            name_rect.center = (POSITIONS[ind][0],POSITIONS[ind][1]-60)
            screen.blit(name_surface, name_rect)
            color=(0, 255, 255)
            if(int(player[1])>player_bet):
                color=(231, 201, 13)
            bet_circle = pygame.Rect((POSITIONS[ind][0]+80,POSITIONS[ind][1], 60, 30))
            pygame.draw.ellipse(screen, color, bet_circle)

            screen.blit(name_surface, name_rect)
            name_surface = font.render(f"{player[1]}", True, (0, 0, 0))
            name_rect = name_surface.get_rect(center=(bet_circle.centerx, bet_circle.centery))
            screen.blit(name_surface, name_rect)


def drawChoiceButton(screen,network,fold_circle, check_circle,rise_circle):
        check_color=(0, 255, 255)
        rise_color=(231, 201, 13)
        fold_color=(242, 33, 23)

        font = pygame.font.SysFont(None, 16)


        mouse_x, mouse_y = pygame.mouse.get_pos()
        if fold_circle.collidepoint(mouse_x, mouse_y ):
                fold_color = (147, 8, 8)
        elif check_circle.collidepoint(mouse_x, mouse_y ):
                check_color = (37, 150, 190)
        elif rise_circle.collidepoint(mouse_x, mouse_y ):
                rise_color = (119, 108, 18)

        pygame.draw.ellipse(screen, fold_color, fold_circle)
        name_surface = font.render("Fold", True, (0, 0, 0))
        name_rect = name_surface.get_rect(center=(fold_circle.centerx, fold_circle.centery))
        screen.blit(name_surface, name_rect)

        pygame.draw.ellipse(screen, check_color, check_circle)
        name_surface = font.render("Check", True, (0, 0, 0))
        name_rect = name_surface.get_rect(center=(check_circle.centerx, check_circle.centery))
        screen.blit(name_surface, name_rect)

        pygame.draw.ellipse(screen, rise_color, rise_circle)
        name_surface = font.render("Rise", True, (0, 0, 0))
        name_rect = name_surface.get_rect(center=(rise_circle.centerx, rise_circle.centery))
        screen.blit(name_surface, name_rect)




