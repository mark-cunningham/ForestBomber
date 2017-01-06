# Forest Bomber

import pygame, sys
from pygame.locals import *

# Define the colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARKBLUE = (63, 111, 182)
SKYBLUE = (199, 231, 254)
GREEN = (57, 180, 22)

# Define constants
SCREENWIDTH = 640
SCREENHEIGHT = 480
SCOREBOARDMARGIN = 4
TEXTLINEHEIGHT = 18

TOTALLEVELS = 4
MAXTREES = 12
TREESPACING = 40
FIRSTTREEX = 140
GROUNDHEIGHT = 4


PLANE_START_X = 0
PLANE_START_Y = 62

# Setup
pygame.init()
game_screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("Forest Bomber")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Helvetica", 16)

# Load images
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
bomb_height = bomb_rectangle.height

burning_tree = 0
burning_tree_time = 0

plane_rectangle = plane_image.get_rect()
plane_width = plane_rectangle.width
plane_height = plane_rectangle.height

tree_rectangle = tree_image.get_rect()
tree_width = tree_rectangle.width
tree_height = tree_rectangle.height

tree_y = SCREENHEIGHT - tree_height - 3

burning_trees = []


# Set up forests
forest_1 = ["T", "-", "T", "-", "-", "-", "T", "-", "-", "-", "-", "T"]
forest_2 = ["-", "T", "-", "-", "T", "-", "T", "-", "T", "T", "-", "T"]
forest_3 = ["T", "T", "-", "-", "T", "-", "T", "T", "T", "T", "-", "-"]
forest_4 = ["T", "T", "-", "-", "T", "T", "T", "-", "T", "T", "T", "-"]
forest = list(forest_1)

while True: # main game loop

    # Keypress events
    for event in pygame.event.get():

        # Space key, drop bomb
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_SPACE] and bombing is False and level_cleared is False and plane_exploded is False:
            bombing = True  
            bomb_x = plane_x + 15
            bomb_y = plane_y + 10

        # Return key at end of game / level
        elif key_pressed[pygame.K_RETURN]:
            if plane_exploded is True or (level == TOTALLEVELS and level_cleared is True):
                plane_exploded = False
                score = 0
                speed_boost = 0
                level = 1
                forest = list(forest_1)
                plane_x = PLANE_START_X
                plane_y = PLANE_START_Y
                display_message = False
                level_cleared = False

            elif level_cleared is True:
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

                plane_x = PLANE_START_X
                plane_y = PLANE_START_Y
                display_message = False
                

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Draw background
    background_rect = (0, 0, SCREENWIDTH, SCREENHEIGHT)
    pygame.draw.rect(game_screen, SKYBLUE, background_rect)

    ground_rect = (0, SCREENHEIGHT - GROUNDHEIGHT, SCREENWIDTH, GROUNDHEIGHT)
    pygame.draw.rect(game_screen, GREEN, ground_rect)


    # Display plane
    if plane_exploded is False:
        game_screen.blit(plane_image, [plane_x, plane_y])
    else:
        game_screen.blit(burning_plane_image, [plane_x, plane_y])    

    #Display forest trees
    for counter in range(len(forest)):
        tree_x = FIRSTTREEX + counter * TREESPACING
        if forest[counter] == "T":
            game_screen.blit(tree_image, [tree_x, tree_y])
        elif forest[counter] == "B":
            game_screen.blit(burning_tree_image, [tree_x, tree_y])
    
    #Move plane
    if level_cleared is False and plane_exploded is False:
        plane_x = plane_x + 5 + speed_boost
        if plane_x >= SCREENWIDTH:
            plane_x = 0
            plane_y = plane_y + 100

    # Bomb
    if bombing is True:
        game_screen.blit(bomb_image, [bomb_x, bomb_y])

        # Check if bomb has hit any of the trees
        for counter in range(len(forest)):
            if forest[counter] == "T":
                tree_left = FIRSTTREEX + counter * TREESPACING
                tree_right = FIRSTTREEX + counter * TREESPACING + tree_width
                tree_top = tree_y
                tree_bottom = tree_y + tree_height

                bomb_left = bomb_x
                bomb_right = bomb_x + bomb_width
                bomb_top = bomb_y
                bomb_bottom = bomb_y + bomb_height

                if bomb_bottom >= tree_top and bomb_top <= tree_bottom and bomb_right >= tree_left and bomb_left <= tree_right:
                    forest[counter] = "B"
                    bombing = False
                    burning_trees.append(counter)
                    burning_tree_time = 10
                    score = score + 10 * level

        # Move the bomb
        bomb_y = bomb_y + 5
        bomb_x = bomb_x + 3
        if bomb_y > SCREENHEIGHT:
            bombing = False
        if bomb_x > SCREENWIDTH:
            bombing = False




    #Burn tree
    if burning_tree_time > 0:
        burning_tree_time = burning_tree_time - 1
        if burning_tree_time == 0:
            for counter in range(len(burning_trees)):
                forest[burning_trees[counter]] = "-"
            del burning_trees[:]
            

    # Plane landing or exploding
    if plane_y >= SCREENHEIGHT - plane_height - GROUNDHEIGHT:
        plane_front = plane_x + plane_width
        if plane_front >= SCREENWIDTH:
            level_cleared = True
        else:
            for counter in range(len(forest)):
                if forest[counter] == "T" or forest[counter] == "B":
                    tree_left = FIRSTTREEX + counter * TREESPACING
                    if plane_front >= tree_left:
                        plane_exploded = True

        if score > hi_score:
            hi_score = score


    # Display scores and level
    scoreboard_background_rect = (0, 0, SCREENWIDTH, TEXTLINEHEIGHT + 2 * SCOREBOARDMARGIN)
    pygame.draw.rect(game_screen, DARKBLUE, scoreboard_background_rect)

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

            text_line_2 = font.render("RETURN for new game", True, (WHITE))
            text_rect_2 = text_line_2.get_rect()

        elif level == TOTALLEVELS:
            text_line_1 = font.render("GAME OVER - ALL LEVELS CLEARED", True, (WHITE))
            text_rect_1 = text_line_1.get_rect()

            text_line_2 = font.render("RETURN for new game", True, (WHITE))
            text_rect_2 = text_line_2.get_rect()

        else:
            text_line_1 = font.render("LEVEL " + str(level) + " CLEARED", True, (WHITE))
            text_rect_1 = text_line_1.get_rect()

            text_line_2 = font.render("RETURN for new level", True, (WHITE))
            text_rect_2 = text_line_2.get_rect()


        longest_text_width = 0
        if text_rect_1.width > text_rect_2.width:
            longest_text_width = text_rect_1.width
        else:
            longest_text_width = text_rect_2.width

        msg_bk_left = (SCREENWIDTH - longest_text_width) / 2 - 2 * SCOREBOARDMARGIN
        msg_bk_top = (SCREENHEIGHT - text_rect_1.height) / 2 - TEXTLINEHEIGHT - 2 * SCOREBOARDMARGIN
        msg_bk_width = longest_text_width + 4 * SCOREBOARDMARGIN
        msg_bk_height = text_rect_1.height + text_rect_2.height + TEXTLINEHEIGHT + 4 * SCOREBOARDMARGIN
        msg_bk_rect = (msg_bk_left, msg_bk_top, msg_bk_width, msg_bk_height)
        pygame.draw.rect(game_screen, DARKBLUE, msg_bk_rect)

        game_screen.blit(text_line_1, [(SCREENWIDTH - text_rect_1.width) / 2,
                                       (SCREENHEIGHT - text_rect_1.height) / 2 - TEXTLINEHEIGHT])
        game_screen.blit(text_line_2, [(SCREENWIDTH - text_rect_2.width) / 2,
                                       (SCREENHEIGHT - text_rect_2.height) / 2 + TEXTLINEHEIGHT])



    pygame.display.update()
    clock.tick(30)
