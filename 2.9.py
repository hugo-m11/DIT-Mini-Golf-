import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
player_pos = pygame.Vector2(150, 350)
ball_velocity = [0, 0]
friction = 0.98

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
    






    
    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()