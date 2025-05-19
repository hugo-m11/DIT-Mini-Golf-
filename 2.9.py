import pygame
import math 
import sys 

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
player_pos = pygame.Vector2(150, 350)
ball_velocity = [0, 0]
friction = 0.98
max_power = 20
is_dragging = False
start_drag_pos = None
ball_radius = 10 

#the coordinates of each hole 
hole_placements = [["hole 1", 1150,350]
                   
                   ]


# all code should happen in here, this is what happens when you run the program 
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #makes the window green (to mimic a golf green)
    screen.fill("green")
    golf_ball = pygame.draw.circle(screen, "white", player_pos, 10)
    #places the hole on each level 
    for hole in hole_placements:
        pygame.draw.circle(screen, "black", (hole[1],hole[2]),16)
    
if event.type == pygame.MOUSEBUTTONDOWN:
            if math.sqrt((event.pos[0] - player_pos[0])**2 + (event.pos[1] - player_pos[1])**2) < ball_radius * 2:
                is_dragging = True
                start_drag_pos = event.pos
                
            if event.type == pygame.MOUSEBUTTONUP and is_dragging:
                is_dragging = False
                end_drag_pos = event.pos
                
                dx = start_drag_pos[0] - end_drag_pos[0]
                dy = start_drag_pos[1] - end_drag_pos[1]
                distance = math.sqrt(dx*dx + dy*dy)
                power = min(distance / 10, max_power)
                
                if distance > 5:
                    ball_velocity[0]=dx*0.1
                    ball_velocity[1]=dy*0.1
                
                        





    
            pygame.display.flip()
            dt = clock.tick(60) / 1000

pygame.quit()