import pygame
import math 
import button 

pygame.init()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
game_paused = False
menu_state = "main"
dt = 0
player_score = 0 
player_pos = pygame.Vector2(150, 350)
ball_velocity = [0, 0]
friction = 0.97
max_power = 8
is_dragging = False
start_drag_pos = None
BALL_RADIUS = 10 
font = pygame.font.SysFont("arialBlack", 20)
TEXT_COLOUR = [255, 255, 255]
current_level = 0

is_colliding = False

levels = [
    { 
        "hole_pos": (1150, 350),
        "start_pos": (150, 350),
        "obstacles": [pygame.Rect(90, 75, 1150, 15), pygame.Rect(1240, 75, 15, 540), pygame.Rect(90, 600, 1150, 15), pygame.Rect(75, 75, 15, 540)]
    },
    {
        "hole_pos": (1150, 350),
        "start_pos": (150, 350),
        "obstacles": [pygame.Rect(90, 75, 1150, 15), pygame.Rect(1240, 75, 15, 540), pygame.Rect(90, 600, 1150, 15), pygame.Rect(75, 75, 15, 540), pygame.Rect(400, 300, 200, 200), pygame.Rect(900, 200, 100, 300)],
    },
    {
        "hole_pos": (1150, 350),
        "start_pos": (150, 350),
        "obstacles": [pygame.Rect(90, 75, 1150, 15), pygame.Rect(1240, 75, 15, 540), pygame.Rect(90, 600, 1150, 15), pygame.Rect(75, 75, 15, 540) ,pygame.Rect(400, 200, 700, 200)]
    },
    {
        "hole_pos": (1150, 350),
        "start_pos": (150, 350),
        "obstacles": [pygame.Rect(90, 75, 1150, 15), pygame.Rect(1240, 75, 15, 540), pygame.Rect(90, 600, 1150, 15), pygame.Rect(75, 75, 15, 540), pygame.Rect(400, 300, 450, 200)]
    },
    {
        "hole_pos": (1150, 350),
        "start_pos": (150, 350),
        "obstacles": [pygame.Rect(90, 75, 1150, 15), pygame.Rect(1240, 75, 15, 540), pygame.Rect(90, 600, 1150, 15), pygame.Rect(75, 75, 15, 540), pygame.Rect(800, 200, 190, 200)]

    }
]

resume_image = pygame.image.load("button_resume.png").convert_alpha()
quit_image = pygame.image.load("button_quit.png").convert_alpha()
resume_button = button.Button(550, 200, resume_image, 1)
quit_button = button.Button(575, 400, quit_image, 1)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def check_win():
    distance = math.sqrt((player_pos.x - hole_pos[0])**2 + (player_pos.y - hole_pos[1])**2) 
    return distance < (hole_radius + 10) - BALL_RADIUS

# Obstacle collision detection
def obstacle_collision():
    for obstacle in levels[current_level]["obstacles"]:
        closest_x = max(obstacle.left, min(player_pos.x, obstacle.right))
        closest_y = max(obstacle.top, min(player_pos.y, obstacle.bottom))

        distance_x = player_pos.x - closest_x
        distance_y = player_pos.y - closest_y
        distance = math.hypot(distance_x, distance_y)

        if distance < BALL_RADIUS and distance != 0:
            is_colliding = True
            overlap = BALL_RADIUS - distance
            norm_x = distance_x / distance
            norm_y = distance_y / distance
            player_pos.x += norm_x * overlap
            player_pos.y += norm_y * overlap

            dot = ball_velocity[0] * norm_x + ball_velocity[1] * norm_y
            ball_velocity[0] -= 2 * dot * norm_x
            ball_velocity[1] -= 2 * dot * norm_y

            ball_velocity[0] *= 0.5
            ball_velocity[1] *= 0.5
        else:
            is_colliding = False


while running:
    screen.fill(pygame.Color(51, 171, 81))

    for obstacle in levels[current_level]["obstacles"]:
        pygame.draw.rect(screen, (120, 120, 120), obstacle)

    hole_pos = levels[current_level]["hole_pos"]
    hole_radius = 20
    pygame.draw.circle(screen, "black", hole_pos, hole_radius - 2)

    if check_win():
        current_level += 1
        if current_level >= len(levels):
            running = False
        else:
            player_pos = pygame.Vector2(levels[current_level]["start_pos"])
            ball_velocity = [0, 0]

    pygame.draw.circle(screen, "white", player_pos, 9)

    if game_paused:
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                if math.hypot(event.pos[0] - player_pos.x, event.pos[1] - player_pos.y) < BALL_RADIUS * 2:
                    is_dragging = True
                    start_drag_pos = event.pos

            if event.type == pygame.MOUSEBUTTONUP and is_dragging:
                is_dragging = False
                end_drag_pos = event.pos

                dx = start_drag_pos[0] - end_drag_pos[0]
                dy = start_drag_pos[1] - end_drag_pos[1]
                distance = math.hypot(dx, dy)
                power = min(distance / 10, max_power)

                if distance > 5:
                    if not is_colliding:
                        ball_velocity[0] = -(end_drag_pos[0] - start_drag_pos[0]) * 15 * dt
                        ball_velocity[1] = -(end_drag_pos[1] - start_drag_pos[1]) * 15 * dt
                    else:
                        ball_velocity[0] = -(end_drag_pos[0] - start_drag_pos[0]) * 15 * dt * - 1
                        ball_velocity[1] = -(end_drag_pos[1] - start_drag_pos[1]) * 15 * dt * - 1

    if not game_paused:
        noclip_thingy = 9
        for _ in range(noclip_thingy):
            player_pos.x += ball_velocity[0] / noclip_thingy
            player_pos.y += ball_velocity[1] / noclip_thingy

            #when the game is unpaused, this function checks for obstacle colliions 
            obstacle_collision()

            #checks for collsions on the left
            if player_pos.x < BALL_RADIUS:
                player_pos.x = BALL_RADIUS
                ball_velocity[0] *= -0.5
            #checks for collsions on the right 
            if player_pos.x > WIDTH - BALL_RADIUS:
                player_pos.x = WIDTH - BALL_RADIUS
                ball_velocity[0] *= -0.5
            #checks for collsions on the bottom      
            if player_pos.y < BALL_RADIUS:
                player_pos.y = BALL_RADIUS
                ball_velocity[1] *= -0.5
            #checks for collsions on the top   
            if player_pos.y > HEIGHT - BALL_RADIUS:
                player_pos.y = HEIGHT - BALL_RADIUS
                ball_velocity[1] *= -0.5

        # Apply friction and stop when velocity is low
        ball_velocity[0] *= friction
        ball_velocity[1] *= friction
        if abs(ball_velocity[0]) < 0.1 and abs(ball_velocity[1]) < 0.1:
            ball_velocity = [0, 0]

    pygame.display.flip()
    dt = clock.tick(120) / 1000

pygame.quit()