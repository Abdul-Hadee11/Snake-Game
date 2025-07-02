import pygame
import random
import time
import sys

pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GREEN = (34, 139, 34)
LIGHT_GREEN = (144, 238, 144)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
GRAY = (100, 100, 100)
BG_COLOR = (30, 30, 30)

# Screen
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()
snake_block = 20
font = pygame.font.SysFont("consolas", 24)
big_font = pygame.font.SysFont("consolas", 48)

# Globals
speed_multiplier = 1
shield_active = False
extra_life_used = False
effect_timer = 0

# Utility
def centered_text(msg, font, color, y):
    surface = font.render(msg, True, color)
    x = (WIDTH - surface.get_width()) // 2
    screen.blit(surface, (x, y))

def draw_snake(snake):
    for i, block in enumerate(snake):
        color = LIGHT_GREEN if i == len(snake) - 1 else DARK_GREEN
        pygame.draw.rect(screen, color, (*block, snake_block, snake_block), border_radius=4)

def draw_obstacles(obs):
    for o in obs:
        pygame.draw.rect(screen, GRAY, (*o, snake_block, snake_block), border_radius=3)

def draw_powerup(pos, ptype):
    color = {
        'speed': CYAN,
        'shield': YELLOW,
        'life': RED,
        'random': MAGENTA
    }[ptype]
    pygame.draw.rect(screen, color, (*pos, snake_block, snake_block), border_radius=4)

def start_screen():
    button = pygame.Rect(WIDTH//2 - 80, HEIGHT//2 - 25, 160, 50)
    while True:
        screen.fill(BG_COLOR)
        centered_text("Snake Game", big_font, YELLOW, HEIGHT//3)
        pygame.draw.rect(screen, WHITE, button)
        centered_text("Start", font, BLACK, button.y + 10)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and button.collidepoint(event.pos):
                return

def pause_screen():
    paused = True
    while paused:
        screen.fill(BG_COLOR)
        centered_text("Game Paused", big_font, YELLOW, HEIGHT // 3)
        centered_text("Press P to Resume", font, WHITE, HEIGHT // 2)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                paused = False
                countdown_timer()

def countdown_timer():
    for i in range(3, 0, -1):
        screen.fill(BG_COLOR)
        centered_text(f"Resuming in {i}", big_font, YELLOW, HEIGHT // 2)
        pygame.display.update()
        pygame.time.delay(1000)
    screen.fill(BG_COLOR)
    centered_text("Go!", big_font, YELLOW, HEIGHT // 2)
    pygame.display.update()
    pygame.time.delay(500)

def difficulty_screen():
    while True:
        screen.fill(BG_COLOR)
        centered_text("Select Difficulty", big_font, YELLOW, HEIGHT // 3)
        centered_text("E - Easy    M - Medium    H - Hard", font, WHITE, HEIGHT // 2)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    return 8, []
                elif event.key == pygame.K_m:
                    return 12, generate_obstacles(10), False
                elif event.key == pygame.K_h:
                    return 14, generate_obstacles(10), True

def game_over_screen(reason, score):
    screen.fill(BLACK)

    # Render all text surfaces
    game_over_text = big_font.render("Game Over", True, RED)
    reason_text = font.render(reason, True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    retry_text = font.render("Press R to Retry or Q to Quit", True, WHITE)

    # Get the center positions for layout
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60))
    reason_rect = reason_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
    retry_rect = retry_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))

    # Blit the texts onto the screen
    screen.blit(game_over_text, game_over_rect)
    screen.blit(reason_text, reason_rect)
    screen.blit(score_text, score_rect)
    screen.blit(retry_text, retry_rect)

    pygame.display.update()

    # Wait for user input (no flicker)
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    game_loop()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()





def generate_obstacles(count):
    return [[random.randrange(0, WIDTH, snake_block), random.randrange(0, HEIGHT, snake_block)] for _ in range(count)]

def move_obstacles(obstacles):
    for obs in obstacles:
        dx = random.choice([-snake_block, 0, snake_block])
        dy = random.choice([-snake_block, 0, snake_block])
        obs[0] = (obs[0] + dx) % WIDTH
        obs[1] = (obs[1] + dy) % HEIGHT
    return obstacles

# Main Game
def game_loop():
    global speed_multiplier, shield_active, extra_life_used, effect_timer

    result = difficulty_screen()
    if len(result) == 2:
        base_speed, obstacles = result
        moving = False
    else:
        base_speed, obstacles, moving = result

    speed_multiplier = 1
    shield_active = False
    extra_life_used = False

    snake = [[WIDTH // 2, HEIGHT // 2]]
    dx, dy = 0, 0
    direction = "STOP"
    next_direction = "STOP"
    length = 1
    food = [random.randrange(0, WIDTH, snake_block), random.randrange(0, HEIGHT, snake_block)]

    powerup = None
    powerup_type = None
    powerup_time = 0
    last_ob_move = time.time()
    powerup_spawn = time.time()

    while True:
        screen.fill(BG_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    next_direction = "LEFT"
                elif event.key == pygame.K_RIGHT:
                    next_direction = "RIGHT"
                elif event.key == pygame.K_UP:
                    next_direction = "UP"
                elif event.key == pygame.K_DOWN:
                    next_direction = "DOWN"
                elif event.key == pygame.K_p:
                    pause_screen()

        if next_direction:
            if next_direction == "LEFT":
                dx, dy = -snake_block, 0
            elif next_direction == "RIGHT":
                dx, dy = snake_block, 0
            elif next_direction == "UP":
                dx, dy = 0, -snake_block
            elif next_direction == "DOWN":
                dx, dy = 0, snake_block
            direction = next_direction

        if direction != "STOP":
            head = [snake[-1][0] + dx, snake[-1][1] + dy]

            hit_wall = not (0 <= head[0] < WIDTH and 0 <= head[1] < HEIGHT)
            hit_self = head in snake
            hit_obs = head in obstacles

            if hit_wall or hit_self or hit_obs:
                if shield_active:
                    shield_active = False  # absorb hit
                elif not extra_life_used:
                    extra_life_used = True
                    continue  # skip crash once
                else:
                    if hit_self:
                        reason = "You ate yourself!"
                    elif hit_wall:
                        reason = "You hit the wall!"
                    elif hit_obs:
                        reason = "You crashed into an obstacle!"
                    else:
                        reason = "You died!"
                    game_over_screen(reason, length - 1)
                    return

            snake.append(head)

            if head == food:
                length += 1
                food = [random.randrange(0, WIDTH, snake_block), random.randrange(0, HEIGHT, snake_block)]
            else:
                while len(snake) > length:
                    del snake[0]

            # Power-up eaten
            if powerup and head == powerup:
                apply_powerup(powerup_type)
                powerup = None

        # Handle active effects
        if effect_timer and time.time() - effect_timer > 5:
            speed_multiplier = 1
            effect_timer = 0

        # Power-up logic
        if time.time() - powerup_spawn > 10 and not powerup:
            powerup = [random.randrange(0, WIDTH, snake_block), random.randrange(0, HEIGHT, snake_block)]
            powerup_type = random.choice(['speed', 'shield', 'life', 'random'])
            powerup_time = time.time()

        if powerup and time.time() - powerup_time > 7:
            powerup = None

        if moving and time.time() - last_ob_move > 1:
            obstacles = move_obstacles(obstacles)
            last_ob_move = time.time()

        draw_snake(snake)
        draw_obstacles(obstacles)
        pygame.draw.rect(screen, RED, (*food, snake_block, snake_block), border_radius=6)
        if powerup:
            draw_powerup(powerup, powerup_type)

        # Effects UI
        effect = ""
        if speed_multiplier > 1:
            effect = "Speed Boost"
        elif shield_active:
            effect = "Shield Active"
        elif extra_life_used:
            effect = "Extra Life Used"
        if effect:
            screen.blit(font.render(effect, True, WHITE), (WIDTH - 200, 10))

        score = font.render(f"Score: {length - 1}", True, WHITE)
        screen.blit(score, (10, 10))

        speed = (base_speed + (length // 5)) * speed_multiplier
        pygame.display.update()
        clock.tick(speed)

def apply_powerup(ptype):
    global speed_multiplier, shield_active, extra_life_used, effect_timer
    if ptype == "speed":
        speed_multiplier = 1.5
        effect_timer = time.time()
    elif ptype == "shield":
        shield_active = True
    elif ptype == "life":
        extra_life_used = False
    elif ptype == "random":
        apply_powerup(random.choice(['speed', 'shield', 'life']))

# Run the Game
if __name__ == "__main__":
    start_screen()
    game_loop()
