
import pygame
import sys
import math

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

screen.fill("green")
ball_pos = [150, 350]
ball_radius = 20
WHITE = (255, 255, 255)

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.draw.circle(screen, WHITE, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)
    pygame.display.update()
    clock.tick(60)


    
    
pygame.display.flip()
dt = clock.tick(60) / 1000

pygame.quit()