import pygame
import sys
import random

pygame.init()

# -------------------- SETTINGS --------------------
W, H = 550, 550
FPS = 60
MAX_LIVES = 3

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Catch the Falling Blocks")
clock = pygame.time.Clock()

# -------------------- COLORS --------------------
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# -------------------- LOAD IMAGES --------------------
bg_img = pygame.image.load("fotos/Petersbg.png").convert()
bg_img = pygame.transform.scale(bg_img, (W, H))

paddle_img = pygame.image.load("fotos/peddle.png").convert_alpha()
paddle_img = pygame.transform.scale(paddle_img, (120, 120))

good_block_img = pygame.image.load("fotos/nota.png").convert_alpha()
good_block_img = pygame.transform.scale(good_block_img, (100, 100))

bad_block_img = pygame.image.load("fotos/penmakers.png").convert_alpha()
bad_block_img = pygame.transform.scale(bad_block_img, (100, 100))

rare_block_img = pygame.image.load("fotos/le-bon-bon-lebron-james.png").convert_alpha()
rare_block_img = pygame.transform.scale(rare_block_img, (100, 100))

heart_img = pygame.image.load("fotos/heart.png").convert_alpha()
heart_img = pygame.transform.scale(heart_img, (32, 32))

broken_heart_img = pygame.image.load("fotos/broken.png").convert_alpha()
broken_heart_img = pygame.transform.scale(broken_heart_img, (32, 32))

# -------------------- PLAYER --------------------
paddle = paddle_img.get_rect()
paddle.midbottom = (W // 2, H - 10)

# -------------------- BLOCK --------------------
block = good_block_img.get_rect()
block_type = "good"
fall_speed = 5

# -------------------- SCORE / LIVES --------------------
font = pygame.font.SysFont("timesnewroman", 32)
score = 0
lives = MAX_LIVES

paused = False
game_over = False

# -------------------- SPAWN BLOCK --------------------
def spawn_block():
    global block_type
    r = random.random()

    if r < 0.01:
        block_type = "rare"   # 1%
    elif r < 0.25:
        block_type = "bad"    # 24%
    else:
        block_type = "good"   # 75%

    block.x = random.randint(0, W - block.width)
    block.y = 0

# -------------------- RESET GAME --------------------
def reset_game():
    global score, lives, fall_speed, paused, game_over
    score = 0
    lives = MAX_LIVES
    fall_speed = 5
    paused = False
    game_over = False
    paddle.midbottom = (W // 2, H - 10)
    spawn_block()

spawn_block()

# -------------------- GAME LOOP --------------------
run = True
while run:
    clock.tick(FPS)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_p and not game_over:
                paused = not paused
            if e.key == pygame.K_r:
                reset_game()

    if not paused and not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            paddle.x -= 8
        if keys[pygame.K_d]:
            paddle.x += 8

        paddle.x = max(0, min(W - paddle.width, paddle.x))

        block.y += fall_speed

        if block.colliderect(paddle):
            if block_type == "bad":
                game_over = True
            elif block_type == "good":
                score += 1
                fall_speed += 0.4
                spawn_block()
            elif block_type == "rare":
                score += 10
                spawn_block()

        if block.y > H:
            if block_type != "bad":
                lives -= 1
                if lives <= 0:
                    game_over = True
            spawn_block()

    # -------------------- DRAW --------------------
    screen.blit(bg_img, (0, 0))

    if block_type == "good":
        screen.blit(good_block_img, block)
    elif block_type == "bad":
        screen.blit(bad_block_img, block)
    elif block_type == "rare":
        screen.blit(rare_block_img, block)

    screen.blit(paddle_img, paddle)

    # Hearts
    for i in range(MAX_LIVES):
        x = 10 + i * 36
        y = 10
        if i < lives:
            screen.blit(heart_img, (x, y))
        else:
            screen.blit(broken_heart_img, (x, y))

    # Score (right side)
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (W - score_text.get_width() - 10, 10))

    if paused:
        pause_text = font.render("PAUSED (P)", True, RED)
        screen.blit(pause_text, (W // 2 - 90, H // 2))

    if game_over:
        over_text = font.render("GAME OVER", True, RED)
        restart_text = font.render("Press R to Restart", True, RED)
        screen.blit(over_text, (W // 2 - 100, H // 2 - 40))
        screen.blit(restart_text, (W // 2 - 160, H // 2))

    pygame.display.update()

pygame.quit()
sys.exit()

