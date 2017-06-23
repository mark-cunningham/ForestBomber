#!/usr/bin/python
# Forest Bomber
# Code Angel

import sys
import pygame
from pygame.locals import *

# Define the colours
WHITE = (255, 255, 255)
DARKBLUE = (63, 111, 182)
SKYBLUE = (199, 231, 254)
GREEN = (57, 180, 22)

# Define constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCOREBOARD_MARGIN = 4
LINE_HEIGHT = 18
BOX_WIDTH = 300
BOX_HEIGHT = 150

TOTAL_LEVELS = 4
MAX_TREES = 12
TREE_SPACING = 40
FIRST_TREE = 140
GROUND_HEIGHT = 4

PLANE_START_X = 0
PLANE_START_Y = 62

# Setup
pygame.init()
game_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Forest Bomber')
clock = pygame.time.Clock()
font = pygame.font.SysFont('Helvetica', 16)

# Load images
tree_image = pygame.image.load('tree.png').convert()
burning_tree_image = pygame.image.load('burning_tree.png').convert()
plane_image = pygame.image.load('plane.png').convert()
burning_plane_image = pygame.image.load('burning_plane.png').convert()
bomb_image = pygame.image.load('bomb.png').convert()

# Initialise variables
level = 1
score = 0
hi_score = 0
speed_boost = 0

plane_exploded = False
level_cleared = False
display_message = False


bombing = False
bomb = bomb_image.get_rect()

plane = plane_image.get_rect()
plane.x = PLANE_START_X
plane.y = PLANE_START_Y

tree = tree_image.get_rect()
tree.y = SCREEN_HEIGHT - tree.height - 3

burning_tree = 0
burning_tree_time = 0

burning_trees = []

# Set up different forests for each level
forest_1 = ['T', '-', 'T', '-', '-', '-', 'T', '-', '-', '-', '-', 'T']
forest_2 = ['-', 'T', '-', '-', 'T', '-', 'T', '-', 'T', 'T', '-', 'T']
forest_3 = ['T', 'T', '-', '-', 'T', '-', 'T', 'T', 'T', 'T', '-', '-']
forest_4 = ['T', 'T', '-', '-', 'T', 'T', 'T', '-', 'T', 'T', 'T', '-']
forest = list(forest_1)

# Main game loop
while True:

    for event in pygame.event.get():

        # Space key pressed, drop bomb
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_SPACE]:
            if bombing is False and level_cleared is False and plane_exploded is False:
                bombing = True
                bomb.x = plane.x + 15
                bomb.y = plane.y + 10

        # Return key at end of game / level pressed
        elif key_pressed[pygame.K_RETURN]:

            # Plane has exploded or all levels completed - so go back to start
            if plane_exploded is True or (level == TOTAL_LEVELS and level_cleared is True):
                plane_exploded = False
                score = 0
                speed_boost = 0
                level = 1
                forest = list(forest_1)
                plane.x = PLANE_START_X
                plane.y = PLANE_START_Y
                display_message = False
                level_cleared = False

            # Level cleared - go up 1 level and load a new forest
            elif level_cleared is True:
                level += 1
                level_cleared = False
                if level == 2:
                    forest = list(forest_2)
                elif level == 3:
                    forest = list(forest_3)
                    speed_boost = 1
                elif level == 4:
                    forest = list(forest_4)
                    speed_boost = 1

                plane.x = PLANE_START_X
                plane.y = PLANE_START_Y
                display_message = False
                
        # User quits
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Move plane
    if level_cleared is False and plane_exploded is False:
        plane.x = plane.x + 5 + speed_boost
        if plane.x >= SCREEN_WIDTH:
            plane.x = 0
            plane.y += 100

    # Move bomb
    if bombing is True:
        bomb.y += 5
        bomb.x += 3
        if bomb.y > SCREEN_HEIGHT:
            bombing = False
        if bomb.x > SCREEN_WIDTH:
            bombing = False

        # Check if bomb has hit a tree
        for column, forest_item in enumerate(forest):
            if forest_item == 'T':
                tree.x = FIRST_TREE + column * TREE_SPACING

                if bomb.colliderect(tree):
                    forest[column] = 'B'
                    bombing = False
                    burning_trees.append(column)
                    burning_tree_time = 10
                    score += 10 * level

    # Burn trees
    if burning_tree_time > 0:
        burning_tree_time -= 1
        if burning_tree_time == 0:
            for column in burning_trees:
                forest[column] = '-'
            del burning_trees[:]

    # Plane on ground level
    if plane.y >= SCREEN_HEIGHT - plane.height - GROUND_HEIGHT:
        plane_front = plane.x + plane.width

        # Edge of the screen reached so level cleared
        if plane_front >= SCREEN_WIDTH:
            level_cleared = True

        # Check to see if plane has collided with a tree
        else:
            for column, forest_item in enumerate(forest):
                if forest_item == 'T' or forest_item == 'B':
                    tree_left = FIRST_TREE + column * TREE_SPACING
                    if plane_front >= tree_left:
                        plane_exploded = True

        # If score is greater than high score, then new high score
        if score > hi_score:
            hi_score = score

    # Draw background
    background_rect = (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    pygame.draw.rect(game_screen, SKYBLUE, background_rect)

    ground_rect = (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT)
    pygame.draw.rect(game_screen, GREEN, ground_rect)

    # Draw plane
    if plane_exploded is False:
        game_screen.blit(plane_image, [plane.x, plane.y])
    else:
        game_screen.blit(burning_plane_image, [plane.x, plane.y])

    # Draw forest
    for column, forest_item in enumerate(forest):
        tree.x = FIRST_TREE + column * TREE_SPACING
        if forest_item == 'T':
            game_screen.blit(tree_image, [tree.x, tree.y])
        elif forest_item == 'B':
            game_screen.blit(burning_tree_image, [tree.x, tree.y])

    # Draw bomb
    if bombing is True:
        game_screen.blit(bomb_image, [bomb.x, bomb.y])

    # Display scoreboard - score, level, high score
    scoreboard_background_rect = (0, 0, SCREEN_WIDTH, LINE_HEIGHT + 2 * SCOREBOARD_MARGIN)
    pygame.draw.rect(game_screen, DARKBLUE, scoreboard_background_rect)

    score_text = 'Score: ' + str(score)
    text = font.render(score_text, True, WHITE)
    game_screen.blit(text, [SCOREBOARD_MARGIN, SCOREBOARD_MARGIN])

    hi_text = 'Hi Score: ' + str(hi_score)
    text = font.render(hi_text, True, WHITE)
    text_rect = text.get_rect()
    game_screen.blit(text, [SCREEN_WIDTH - text_rect.width - SCOREBOARD_MARGIN, SCOREBOARD_MARGIN])

    level_text = 'Level: ' + str(level)
    text = font.render(level_text, True, WHITE)
    text_rect = text.get_rect()
    game_screen.blit(text, [(SCREEN_WIDTH - text_rect.width) / 2, SCOREBOARD_MARGIN])

    # End of game / level message
    if plane_exploded is True or level_cleared is True:

        if plane_exploded is True:
            text_line_1 = font.render('GAME OVER', True, WHITE)
            text_rect_1 = text_line_1.get_rect()

            text_line_2 = font.render('RETURN for new game', True, WHITE)
            text_rect_2 = text_line_2.get_rect()

        elif level == TOTAL_LEVELS:
            text_line_1 = font.render('GAME OVER - ALL LEVELS CLEARED', True, WHITE)
            text_rect_1 = text_line_1.get_rect()

            text_line_2 = font.render('RETURN for new game', True, WHITE)
            text_rect_2 = text_line_2.get_rect()

        else:
            text_line_1 = font.render('LEVEL ' + str(level) + ' CLEARED', True, WHITE)
            text_rect_1 = text_line_1.get_rect()

            text_line_2 = font.render('RETURN for new level', True, WHITE)
            text_rect_2 = text_line_2.get_rect()

        # Display message box to sit text over
        msg_bk_rect = ((SCREEN_WIDTH - BOX_WIDTH) / 2, (SCREEN_HEIGHT - BOX_HEIGHT) / 2, BOX_WIDTH, BOX_HEIGHT)
        pygame.draw.rect(game_screen, DARKBLUE, msg_bk_rect)

        # Display 2 lines of text, centred
        game_screen.blit(text_line_1, [(SCREEN_WIDTH - text_rect_1.width) / 2,
                                       (SCREEN_HEIGHT - text_rect_1.height) / 2 - LINE_HEIGHT])
        game_screen.blit(text_line_2, [(SCREEN_WIDTH - text_rect_2.width) / 2,
                                       (SCREEN_HEIGHT - text_rect_2.height) / 2 + LINE_HEIGHT])

    pygame.display.update()
    clock.tick(30)
