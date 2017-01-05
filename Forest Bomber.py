# Forest Bomber

import pygame, sys
from pygame.locals import *

# Define the colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (63, 111, 182)

# Define constants
SCREENWIDTH = 640
SCREENHEIGHT = 480
SCOREBOARDMARGIN = 4
TEXTLINEHEIGHT = 18


MAXTREES = 12
TREE_Y = 266
LANDING_HEIGHT = 285
PLANE_START_X = 0
PLANE_START_Y = 35

# Setup
pygame.init()
game_screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("Forest Bomber")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Helvetica", 16)

# Load images
background_image = pygame.image.load("forest_bomber_background.png").convert()
tree_image = pygame.image.load("tree.png").convert()
burning_tree_image = pygame.image.load("burning_tree.png").convert()
plane_image = pygame.image.load("plane.png").convert()
burning_plane_image = pygame.image.load("burning_plane.png").convert()
bomb_image = pygame.image.load("bomb.png").convert()


# Initialise variables
level = 1
score = 0
hi_score = 0

plane_x = PLANE_START_X
plane_y = PLANE_START_Y
plane_exploded = False
level_cleared = False
display_message = False
speed_boost = 0

bombing = False
bomb_x = 0
bomb_y = 0
bomb_rectangle = bomb_image.get_rect()
bomb_width = bomb_rectangle.width

burning_tree = 0
burning_tree_time = 0

plane_rectangle = plane_image.get_rect()
plane_width = plane_rectangle.width


# Set up forest
forest_1 = [1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1]
forest_2 = [0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1]
forest_3 = [1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0]
forest_4 = [1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0]
forest_5 = [0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1]
forest_6 = [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1]
forest_7 = [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1]
forest_8 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
forest = list(forest_1)

while True: # main game loop

    # Keypress events
    for event in pygame.event.get():
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_SPACE] and bombing is False and level_cleared is False and plane_exploded is False:
            bombing = True  
            bomb_x = plane_x + 15
            bomb_y = plane_y + 10
        elif key_pressed[pygame.K_RETURN] and plane_exploded is True:
                plane_exploded = False
                score = 0
                speed_boost = 0
                level = 1
                forest = list(forest_1)
                plane_x = PLANE_START_X
                plane_y = PLANE_START_Y
        elif key_pressed[pygame.K_RETURN] and level_cleared is True:
                level_cleared = False
                level = level + 1
                if level == 2:
                    forest = list(forest_2)
                elif level == 3:
                    forest = list(forest_3)
                    speed_boost = 1
                elif level == 4:
                    forest = list(forest_4)
                    speed_boost = 1
                elif level == 5:
                    forest = list(forest_5)
                    speed_boost = 2
                elif level == 6:
                    forest = list(forest_6)
                    speed_boost = 2
                elif level == 7:
                    forest = list(forest_7)
                    speed_boost = 3
                elif level == 8:
                    forest = list(forest_8)
                    speed_boost = 3
                    
                plane_x = PLANE_START_X
                plane_y = PLANE_START_Y
                display_message = True
                

    if event.type == QUIT:
            pygame.quit()     
            sys.exit()

    game_screen.blit(background_image, [0,0])






    
    # Display plane
    if plane_exploded is False:
        game_screen.blit(plane_image, [plane_x, plane_y])
    else:
        game_screen.blit(burning_plane_image, [plane_x, plane_y])    

    #Display forest trees
    for counter in range(0, MAXTREES):
        tree_x = counter * 25 + 100
        if forest[counter] == 1:
            game_screen.blit(tree_image, [tree_x, TREE_Y])
        elif forest[counter] == 2:
            game_screen.blit(burning_tree_image, [tree_x, TREE_Y])  
    
    #Move plane
    if level_cleared is False and plane_exploded is False:
        plane_x = plane_x + 5 + speed_boost
        if plane_x >= SCREENWIDTH:
            plane_x = 0
            plane_y = plane_y + 50

    # Display bomb
    if bombing is True:
        game_screen.blit(bomb_image, [bomb_x, bomb_y])
        bomb_y = bomb_y + 5
        bomb_x = bomb_x + 3
        if bomb_y > SCREENHEIGHT:
            bombing = False
        if bomb_x > SCREENWIDTH:
            bombing = False

        if bomb_y > TREE_Y:
            tree_position = int((bomb_x + bomb_width - 100) / 25)
            if tree_position > MAXTREES - 1:
                tree_position = MAXTREES - 1
                
            if forest[tree_position] == 1:
                forest[tree_position] = 2
                bombing = False
                burning_tree = tree_position
                burning_tree_time = 10
                score = score + 10 * level

    #Burn tree
    if burning_tree_time > 0:
        burning_tree_time = burning_tree_time - 1
        if burning_tree_time == 0:
            forest[burning_tree] = 0
            burning_tree = 0
            

    # Plane landing or exploding            
    if plane_y == LANDING_HEIGHT:
        plane_front = plane_x + plane_width
        if plane_front >= SCREENWIDTH:
            level_cleared = True
        else:
            if plane_front > 100:
                tree_position = int((plane_front - 100) / 25)
                if forest[tree_position] > 0:
                    plane_exploded = True

        if score > hi_score:
            hi_score = score


    # Display scores and level
    scoreboard_background_rect = (0, 0, SCREENWIDTH, TEXTLINEHEIGHT + 2 * SCOREBOARDMARGIN)
    pygame.draw.rect(game_screen, BLUE, scoreboard_background_rect)

    score_text = "Score: " + str(score)
    text = font.render(score_text, True, (WHITE))
    game_screen.blit(text, [SCOREBOARDMARGIN, SCOREBOARDMARGIN])

    hi_text = "Hi Score: " + str(hi_score)
    text = font.render(hi_text, True, (WHITE))
    text_rect = text.get_rect()
    game_screen.blit(text, [SCREENWIDTH - text_rect.width - SCOREBOARDMARGIN, SCOREBOARDMARGIN])

    level_text = "Level: " + str(level)
    text = font.render(level_text, True, (WHITE))
    text_rect = text.get_rect()
    game_screen.blit(text, [(SCREENWIDTH - text_rect.width) / 2, SCOREBOARDMARGIN])

    if plane_exploded is True or level_cleared is True:
        display_message = True




    if display_message is True:

        if plane_exploded is True:
            text_line_1 = font.render("GAME OVER", True, (WHITE))
            text_rect_1 = text_line_1.get_rect()
        else:
            text_line_1 = font.render("LEVEL " + str(level) + " CLEARED", True, (WHITE))
            text_rect_1 = text_line_1.get_rect()

        text_line_2 = font.render("RETURN for new game", True, (WHITE))
        text_rect_2 = text_line_2.get_rect()

        msg_bk_left = (SCREENWIDTH - text_rect_2.width) / 2 - 2 * SCOREBOARDMARGIN
        msg_bk_top = (SCREENHEIGHT - text_rect_1.height) / 2 - TEXTLINEHEIGHT - 2 * SCOREBOARDMARGIN
        msg_bk_width = text_rect_2.width + 4 * SCOREBOARDMARGIN
        msg_bk_height = text_rect_1.height + text_rect_2.height + TEXTLINEHEIGHT + 4 * SCOREBOARDMARGIN
        msg_bk_rect = (msg_bk_left, msg_bk_top, msg_bk_width, msg_bk_height)
        pygame.draw.rect(game_screen, BLUE, msg_bk_rect)

        game_screen.blit(text_line_1, [(SCREENWIDTH - text_rect_1.width) / 2,
                                       (SCREENHEIGHT - text_rect_1.height) / 2 - TEXTLINEHEIGHT])
        game_screen.blit(text_line_2, [(SCREENWIDTH - text_rect_2.width) / 2,
                                       (SCREENHEIGHT - text_rect_2.height) / 2 + TEXTLINEHEIGHT])



    pygame.display.update()
    clock.tick(30)
