import time

import pygame
from snake import *
from food import Food
from node import *
from queue import Queue

pygame.init()
# Constants
bounds = (480, 480)
block_size = 20
grid_size = (bounds[0] / block_size) * (bounds[1] / block_size)
blks_in_Rows = bounds[1] / block_size
blks_in_columns = bounds[0] / block_size
INTIAL_SNAKE_SPEED = 15
# Set Up Window
window = pygame.display.set_mode(bounds)
pygame.display.set_caption("SnakeyBoi")
# Set up player, food block and the font for the end of game message
player_snake = snake(block_size, bounds, INTIAL_SNAKE_SPEED)
food = Food(block_size, bounds)
font = pygame.font.SysFont('comicsans', 60, True)
pygame.event.clear()


path = astar(blks_in_Rows, blks_in_columns, food.get_food_position(), player_snake.get_snake_head(),
             player_snake.get_snake_body(), pygame, window)
player_snake.AI_Steer(path)
player_snake.move()
window.fill((255, 255, 255))  # Reset frame
player_snake.draw(pygame, window)  # Draw Snake in the window
food.draw(pygame, window)  # draw food in window
pygame.display.flip()  # Send from frame buffer to the screen

run = True
while run:  # Main Game Loop
    clock = pygame.time.Clock()
    dt = clock.tick(15) / 1000  # Delta time. Converts the fps into how long each frame is takes to render

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if player_snake.check_for_food(food):
        food.respawn(player_snake, grid_size, blks_in_columns, blks_in_Rows)
        food.draw(pygame, window)
        pygame.display.flip()
        path = astar(blks_in_Rows, blks_in_columns, food.get_food_position(), player_snake.get_snake_head(),
                     player_snake.get_snake_body(), pygame, window)
    player_snake.AI_Steer(path)
    player_snake.move()

    if player_snake.check_bounds() or player_snake.check_if_eaten_ourselfs():  # Check if we died
        if player_snake.check_bounds():
            print("You ran into a wall....")
        if player_snake.check_if_eaten_ourselfs():
            print("You ran into yourself...")
        text = font.render('You Died', True, (255, 255, 255))
        window.blit(text, (250, 250))
        pygame.display.update()
        pygame.time.delay(3000)
        player_snake.respawn()
        slots = [(0, 0)]
        food.respawn(player_snake, grid_size, blks_in_columns, blks_in_Rows)
    window.fill((0, 0, 0))  # Reset frame
    player_snake.draw(pygame, window)  # Draw Snake in the window
    food.draw(pygame, window)  # draw food in window
    pygame.display.flip()  # Send from frame buffer to the screen
