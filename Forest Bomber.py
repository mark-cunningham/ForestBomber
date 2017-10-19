#!/usr/bin/python
# Forest Bomber
# Code Angel

import sys
import os
import pygame
from pygame.locals import *

# Define the colours
WHITE = (255, 255, 255)
PURPLE = (96, 85, 154)
LIGHT_BLUE = (157, 220, 241)
DARK_BLUE = (63, 111, 182)
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
GROUND_HEIGHT = 8
TREE_OFF_GROUND = 4

PLANE_START_X = 0
PLANE_START_Y = 54

# Setup
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()
game_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Forest Bomber')
clock = pygame.time.Clock()
font = pygame.font.SysFont('Helvetica', 16)

# Load images
background_image = pygame.image.load('background.png').convert()
tree_image = pygame.image.load('tree.png').convert_alpha()
burn_tree_image = pygame.image.load('burning_tree.png').convert_alpha()
plane_image = pygame.image.load('plane.png').convert_alpha()
burn_plane_image = pygame.image.load('burning_plane.png').convert_alpha()
bomb_image = pygame.image.load('bomb.png').convert_alpha()

# Load sounds
explosion_sound = pygame.mixer.Sound('explosion.ogg')
tree_sound = pygame.mixer.Sound('tree_explosion.ogg')

# Initialise variables
level = 1
score = 0
hi_score = 0
speed_boost = 0

plane_exploded = False
level_cleared = False
plane_front = 0
plane_explode_sound_played = False


bomb_dropped = False
bomb = bomb_image.get_rect()

plane = plane_image.get_rect()
plane.x = PLANE_START_X
plane.y = PLANE_START_Y

tree = tree_image.get_rect()
tree.y = SCREEN_HEIGHT - tree.height - TREE_OFF_GROUND

burning_tree = 0
tree_timer = 0

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
            if bomb_dropped is False and level_cleared is False and plane_exploded is False:
                bomb_dropped = True
                bomb.x = plane.x + 15
                bomb.y = plane.y + 10

        # Return key at end of game / level pressed
        elif key_pressed[pygame.K_RETURN]:

            # Plane has exploded or all levels completed - so go back to start
            if plane_exploded is True or (level == TOTAL_LEVELS and level_cleared is True):
                plane_exploded = False
                plane_explode_sound_played = False
                score = 0
                speed_boost = 0
                level = 1
                forest = list(forest_1)
                plane.x = PLANE_START_X
                plane.y = PLANE_START_Y
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
                else:
                    forest = list(forest_4)
                    speed_boost = 1

                plane.x = PLANE_START_X
                plane.y = PLANE_START_Y
                
        # User quits
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Update plane location
    if level_cleared is False and plane_exploded is False:
        plane.x = plane.x + 5 + speed_boost

        if plane.x >= SCREEN_WIDTH:
            plane.x = 0
            plane.y += 100

    # Update bomb location
    if bomb_dropped is True:
        bomb.y += 5
        bomb.x += 3

        if bomb.y > SCREEN_HEIGHT:
            bomb_dropped = False

        if bomb.x > SCREEN_WIDTH:
            bomb_dropped = False

        # Check if bomb has hit a tree
        for column, forest_item in enumerate(forest):
            if forest_item == 'T':
                tree.x = FIRST_TREE + column * TREE_SPACING

                if bomb.colliderect(tree):
                    forest[column] = 'B'
                    bomb_dropped = False
                    burning_trees.append(column)
                    tree_timer = 10
                    score += 10 * level
                    tree_sound.play()

    # Update burning trees tree status
    if tree_timer > 0:
        tree_timer -= 1
        if tree_timer == 0:
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
    game_screen.blit(background_image, [0, 0])

    # Draw forest
    for column, forest_item in enumerate(forest):
        tree.x = FIRST_TREE + column * TREE_SPACING
        if forest_item == 'T':
            game_screen.blit(tree_image, [tree.x, tree.y])
        elif forest_item == 'B':
            game_screen.blit(burn_tree_image, [tree.x, tree.y])

    # Draw plane
    if plane_exploded is False:
        game_screen.blit(plane_image, [plane.x, plane.y])
    else:
        plane.y = SCREEN_HEIGHT - burn_plane_image.get_height() - TREE_OFF_GROUND
        game_screen.blit(burn_plane_image, [plane.x, plane.y])

    # Draw bomb
    if bomb_dropped is True:
        game_screen.blit(bomb_image, [bomb.x, bomb.y])

    # Display scoreboard - score, level, high score
    scoreboard_background_rect = (0, 0, SCREEN_WIDTH, LINE_HEIGHT + 2 * SCOREBOARD_MARGIN)
    pygame.draw.rect(game_screen, LIGHT_BLUE, scoreboard_background_rect)

    score_text = 'Score: ' + str(score)
    text = font.render(score_text, True, PURPLE)
    game_screen.blit(text, [SCOREBOARD_MARGIN, SCOREBOARD_MARGIN])

    hi_text = 'Hi Score: ' + str(hi_score)
    text = font.render(hi_text, True, PURPLE)
    text_rect = text.get_rect()
    game_screen.blit(text, [SCREEN_WIDTH - text_rect.width - SCOREBOARD_MARGIN, SCOREBOARD_MARGIN])

    level_text = 'Level: ' + str(level)
    text = font.render(level_text, True, PURPLE)
    text_rect = text.get_rect()
    game_screen.blit(text, [(SCREEN_WIDTH - text_rect.width) / 2, SCOREBOARD_MARGIN])

    # End of game / level message
    if plane_exploded is True or level_cleared is True:

        if plane_exploded is True:
            text_line_1 = font.render('GAME OVER', True, WHITE)
            text_rect_1 = text_line_1.get_rect()

            text_line_2 = font.render('RETURN for new game', True, WHITE)
            text_rect_2 = text_line_2.get_rect()

            if plane_explode_sound_played is False:
                explosion_sound.play()
                plane_explode_sound_played = True

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
        pygame.draw.rect(game_screen, DARK_BLUE, msg_bk_rect)

        # Display 2 lines of text, centred
        game_screen.blit(text_line_1, [(SCREEN_WIDTH - text_rect_1.width) / 2,
                                       (SCREEN_HEIGHT - text_rect_1.height) / 2 - LINE_HEIGHT])
        game_screen.blit(text_line_2, [(SCREEN_WIDTH - text_rect_2.width) / 2,
                                       (SCREEN_HEIGHT - text_rect_2.height) / 2 + LINE_HEIGHT])

    pygame.display.update()
    clock.tick(30)
