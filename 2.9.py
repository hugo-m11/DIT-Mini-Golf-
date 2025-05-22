import pygame
import math 
import button 

pygame.init()
WIDTH,HEIGHT = 1280,720
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
running = True
game_paused = False
dt = 0
player_pos = pygame.Vector2(150, 350)
ball_velocity = [0, 0]
friction = 0.98
max_power = 10
is_dragging = False
start_drag_pos = None
ball_radius = 10 
font = pygame.font.SysFont("arialBlack", 20)
TEXT_COLOUR = [255, 255, 255]
hole_placements = [["hole 1", 1150,350]
                   
                   ]
#defines a function that allows me to use text 
def draw_text (text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# all code should happen in here, this is what happens when you run the program 



while running:

#makes the window green (to mimic a golf green)
    screen.fill("green")
    golf_ball = pygame.draw.circle(screen, "white", player_pos, 10)
#puts the text on the screen
    if game_paused == True:
        pass
    else: 
        draw_text("Press SPACE to pause the game", font, TEXT_COLOUR, 20, 20)
    
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_paused = True
        

#this checks if the user clicks on the ball, and starts a drag action 
        if event.type == pygame.MOUSEBUTTONDOWN:
                if math.sqrt((event.pos[0] - player_pos[0])**2 + (event.pos[1] - player_pos[1])**2) < ball_radius * 2:
                    is_dragging = True
                    start_drag_pos = event.pos

#this checks when the user releases from the ball         
        if event.type == pygame.MOUSEBUTTONUP and is_dragging:
            is_dragging = False
            end_drag_pos = event.pos

# calculates the drag vector using dx and dy and converts the drag distance to velocity          
            dx = start_drag_pos[0] - end_drag_pos[0]
            dy = start_drag_pos[1] - end_drag_pos[1]
            distance = math.sqrt(dx*dx + dy*dy)
            power = min(distance / 10, max_power)
 #this makes sure that the user dragged back enought to launch           
            if distance > 5:
                ball_velocity[0] = -(end_drag_pos[0] - start_drag_pos[0]) * 15 * dt
                ball_velocity[1] = -(end_drag_pos[1] - start_drag_pos[1]) * 15 * dt


#out of the while running loop, this moves the ball adding velocity to the position 
    player_pos[0]+=ball_velocity[0]
    player_pos[1]+=ball_velocity[1]

#slows the ball down using friction       
    ball_velocity[0]*=friction
    ball_velocity[1]*=friction

#stops the ball        
    if abs(ball_velocity[0]) < 0.1 and abs(ball_velocity[1]) < 0.1:
        ball_velocity = [0, 0]
    
#checks for collsions on the left
    if player_pos[0]<ball_radius:
        player_pos[0]= ball_radius
        ball_velocity[0]*=-0.5
        
#checks for collsions on the right         
    if player_pos[0]>WIDTH-ball_radius:
        player_pos[0]=WIDTH-ball_radius
        ball_velocity[0]*=-0.5

#checks for collsions on the bottom         
    if player_pos[1]<ball_radius:
        player_pos[1]= ball_radius
        ball_velocity[1]*=-0.5

#checks for collsions on the top          
    if player_pos[1]>HEIGHT-ball_radius:
        player_pos[1]=HEIGHT-ball_radius
        ball_velocity[1]*=-0.5
        

    
    
    #places the hole on each level 
    for hole in hole_placements:
        pygame.draw.circle(screen, "black", (hole[1],hole[2]),16)
    
    pygame.display.flip()
    dt = clock.tick(120) / 1000

pygame.quit()