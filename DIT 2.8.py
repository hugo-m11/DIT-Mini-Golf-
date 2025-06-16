import pygame
import math 
import button 

pygame.init()
WIDTH,HEIGHT = 1280,720
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
running = True
game_paused = False
menu_state = "main"
dt = 0
player_score = 0 
player_pos = pygame.Vector2(150, 350)
ball_velocity = [0, 0]
friction = 0.97
max_power = 15
is_dragging = False
start_drag_pos = None
BALL_RADIUS = 10 
font = pygame.font.SysFont("arialBlack", 20)
TEXT_COLOUR = [255, 255, 255]
current_level = 0
levels = [
    { 
        "hole_pos": (1150, 350),
        "start_pos": (150, 350),
        "obstacles": []
    },
    {
        "hole_pos": (800, 600),
        "start_pos": (150, 350),
        "obstacles": [pygame.Rect(400, 300, 200, 20)]
    },
    {
        "hole_pos": (1100, 70),
        "start_pos": (150, 350),
        "obstacles": [pygame.Rect(400, 30, 200, 20)]
    }
]

#loads an image 
resume_image = pygame.image.load("button_resume.png").convert_alpha()
quit_image = pygame.image.load("button_quit.png").convert_alpha()

resume_button = button.Button(550, 200, resume_image, 1)
quit_button = button.Button(575, 400, quit_image, 1)

#defines a function that allows me to use text 
def draw_text (text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#checks if the ball is in the hole
def check_win():
    distance = math.sqrt((player_pos[0] - hole_pos[0])**2 + (player_pos[1] - hole_pos[1])**2) 
    return distance < (hole_radius + 10) - BALL_RADIUS
    


# all code should happen in here, this is what happens when you run the program 

while running:

    for obstacle in levels[current_level]["obstacles"]:
        pygame.draw.rect(screen, (120, 120, 120), obstacle)

    for obstacle in levels[current_level]["obstacles"]:
        if obstacle.collidepoint(player_pos):
            ball_velocity[0] *= -0.5
            ball_velocity[1] *= -0.5

    #makes the window green (to mimic a golf green)
    screen.fill(pygame.Color(51, 171, 81))
    hole_pos = levels[current_level]["hole_pos"]
    hole_radius = 20
    pygame.draw.circle(screen, "black", hole_pos, hole_radius - 2)

# Check if player won the level
    if check_win():
        current_level += 1
        if current_level >= len(levels):
            running = False
        else:
            player_pos = pygame.Vector2(levels[current_level]["start_pos"])
            ball_velocity = [0, 0]


    
    golf_ball = pygame.draw.circle(screen, "white", player_pos, 9)
#puts the text on the screen
    if game_paused == True:
      screen.fill(pygame.Color(54, 54, 54))
      if menu_state == "main":
        if resume_button.draw(screen):
            game_paused = False
        if quit_button.draw(screen):
            running = False 

    else: 
        rect = pygame.Rect(10, 15, 365, 40)
        pygame.draw.rect(screen, "black", rect)
        draw_text("Press SPACE to pause the game", font, TEXT_COLOUR, 20, 20)
    
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_paused = True

        if not game_paused:
        #this checks if the user clicks on the ball, and starts a drag action 
            if event.type == pygame.MOUSEBUTTONDOWN:
                    if math.sqrt((event.pos[0] - player_pos[0])**2 + (event.pos[1] - player_pos[1])**2) < BALL_RADIUS * 2:
                        is_dragging = True
                        start_drag_pos = event.pos
    

        #this checks when the user releases from the ball         
            if event.type == pygame.MOUSEBUTTONUP and is_dragging:
                is_dragging = False
                end_drag_pos = event.pos

        #calculates the drag vector using dx and dy and converts the drag distance to velocity          
                dx = start_drag_pos[0] - end_drag_pos[0]
                dy = start_drag_pos[1] - end_drag_pos[1]
                distance = math.sqrt(dx*dx + dy*dy)
                power = min(distance / 10, max_power)
        #this makes sure that the user dragged back enought to launch           
                if distance > 5:
                    ball_velocity[0] = -(end_drag_pos[0] - start_drag_pos[0]) * 15 * dt
                    ball_velocity[1] = -(end_drag_pos[1] - start_drag_pos[1]) * 15 * dt

    if not game_paused:
    #out of the while running loop, this moves the ball adding velocity to the position 
        player_pos[0]+=ball_velocity[0]
        player_pos[1]+=ball_velocity[1]

    #slows the ball down using friction       
        ball_velocity[0]*=friction
        ball_velocity[1]*=friction

    #stops the ball        
        if abs(ball_velocity[0]) < 0.1 and abs(ball_velocity[1]) < 0.1:
            ball_velocity = [0, 0]
        

    #checks for collsions on the left wall
        if player_pos[0]<BALL_RADIUS:
            player_pos[0]= BALL_RADIUS
            ball_velocity[0]*=-0.5
            
    #checks for collsions on the right wall        
        if player_pos[0]>WIDTH-BALL_RADIUS:
            player_pos[0]=WIDTH-BALL_RADIUS
            ball_velocity[0]*=-0.5

    #checks for collsions on the bottom wall        
        if player_pos[1]<BALL_RADIUS:
            player_pos[1]= BALL_RADIUS
            ball_velocity[1]*=-0.5

    #checks for collsions on the top wall       
        if player_pos[1]>HEIGHT-BALL_RADIUS:
            player_pos[1]=HEIGHT-BALL_RADIUS
            ball_velocity[1]*=-0.5
        


    

    pygame.display.flip()
    dt = clock.tick(120) / 1000

pygame.quit()