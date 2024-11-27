import pygame, sys
import math


def ball_animation():
    global ball_speed_x, ball_speed_y, p1, ai

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Keep ball in the screen height
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1

    # Ball collision with player paddle
    if ball.colliderect(player):
        paddle_collision(player)

    # Ball collision with opponent paddle
    if ball.colliderect(opponent):
        paddle_collision(opponent)

    # Ball reset and scoring
    if ball.left <= 0:  # Player scores
        p1 += 1
        ball_restart()

    if ball.right >= WIDTH:  # Opponent scores
        ai += 1
        ball_restart()


def paddle_collision(paddle):
    # Adjust ball angle based on paddle collision.
    global ball_speed_x, ball_speed_y

    paddle_center = paddle.centery
    impact_point = ball.centery - paddle_center
    normalized_impact = impact_point / (paddle.height / 2)

    # Calculate new angle
    max_angle = math.radians(45)
    new_angle = normalized_impact * max_angle

    # Update ball speed
    speed = math.sqrt(ball_speed_x ** 2 + ball_speed_y ** 2)
    ball_speed_x = -speed * math.cos(new_angle) if paddle == player else speed * math.cos(new_angle)
    ball_speed_y = speed * math.sin(new_angle)


def ball_restart():
    # reset ball to center
    global ball_speed_x, ball_speed_y
    ball.center = (WIDTH / 2, HEIGHT / 2)
    ball_speed_x *= -1  # Reverse direction

asdfasdf
pygame.init()

# Screen setup
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('PONG')

# Font and colors
font = pygame.font.Font(None, 32)
white = (255, 255, 255)
red = (255, 0, 0)

# Game elements
ball = pygame.Rect(WIDTH / 2 - 15, HEIGHT / 2 - 15, 20, 20)
player = pygame.Rect(WIDTH - 20, HEIGHT / 2 - 70, 10, 140)
opponent = pygame.Rect(10, HEIGHT / 2 - 70, 10, 140)

# Game variables
ball_speed_x = 7
ball_speed_y = 7
player_speed = 0
opponent_speed = 7
p1, ai = 0, 0

# Game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Player paddle movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed = 7
            if event.key == pygame.K_UP:
                player_speed = -7
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_DOWN, pygame.K_UP):
                player_speed = 0

    # Update paddle positions
    player.y += player_speed
    player.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))  # keeps paddle in screen

    # Opponent AI
    if opponent.centery < ball.centery:
        opponent.y += opponent_speed - 3
    elif opponent.centery > ball.centery:
        opponent.y -= opponent_speed - 3
    opponent.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))  # keeps paddle in screen

    # Ball animation
    ball_animation()

    # Draw everything
    screen.fill((0, 0, 0))  # Clear screen
    score_text = font.render(f"Computer: {ai} | You: {p1}", True, white)
    screen.blit(score_text, (WIDTH // 2 - 100, 20))  # Centered score
    pygame.draw.ellipse(screen, red, ball)  # Ball
    pygame.draw.rect(screen, white, player)  # Player paddle
    pygame.draw.rect(screen, white, opponent)  # Opponent paddle

    # Update display
    pygame.display.flip()
    # frames per second
    clock.tick(60)
