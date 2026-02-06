import pygame
import sys
import random

pygame.init()

# -------------------- SETTINGS --------------------
W, H = 550, 550
FPS = 60

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Catch the Falling Blocks")
clock = pygame.time.Clock()

# -------------------- COLORS --------------------
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# -------------------- LOAD IMAGES --------------------
bg_img = pygame.image.load("Schermafbeelding 2026-02-05 105843.png").convert()
bg_img = pygame.transform.scale(bg_img, (W, H))

paddle_img = pygame.image.load("Schermafbeelding 2026-01-15 204202.png").convert_alpha()
paddle_img = pygame.transform.scale(paddle_img, (120, 120))

good_block_img = pygame.image.load("Schermafbeelding 2026-02-05 202438.png").convert_alpha()
good_block_img = pygame.transform.scale(good_block_img, (100, 100))

bad_block_img = pygame.image.load("afbeelding (2).png").convert_alpha()
bad_block_img = pygame.transform.scale(bad_block_img, (100, 100))

rare_block_img = pygame.image.load("le-bon-bon-lebron-james.png").convert_alpha()
rare_block_img = pygame.transform.scale(rare_block_img, (100, 100))

# -------------------- PLAYER --------------------
paddle = paddle_img.get_rect()
paddle.midbottom = (W // 2, H - 10)

# -------------------- BLOCK --------------------
block = good_block_img.get_rect()
block.x = random.randint(0, W - block.width)
block.y = 0

fall_speed = 5
block_type = "good"  # good / bad / rare

# -------------------- SCORE --------------------
font = pygame.font.SysFont("timesnewroman", 36)
score = 0

# -------------------- BLOCK SPAWN FUNCTION --------------------
def spawn_block():
    global block_type
    r = random.random()

    if r < 0.01:
        block_type = "rare"      # 1%
    elif r < 0.25:
        block_type = "bad"       # 24%
    else:
        block_type = "good"      # 75%

    block.x = random.randint(0, W - block.width)
    block.y = 0

# -------------------- GAME LOOP --------------------
run = True
while run:
    clock.tick(FPS)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False

    # -------- INPUT --------
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        paddle.x -= 8
    if keys[pygame.K_d]:
        paddle.x += 8

    paddle.x = max(0, min(W - paddle.width, paddle.x))

    # -------- BLOCK FALL --------
    block.y += fall_speed

    # -------- COLLISION --------
    if block.colliderect(paddle):
        if block_type == "bad":
            run = False
        elif block_type == "good":
            score += 1
            fall_speed += 0.4
            spawn_block()
        elif block_type == "rare":
            score += 10
            spawn_block()

    # -------- BLOCK MISSED --------
    if block.y > H:
        spawn_block()

    # -------- DRAW --------
    screen.blit(bg_img, (0, 0))

    if block_type == "good":
        screen.blit(good_block_img, block)
    elif block_type == "bad":
        screen.blit(bad_block_img, block)
    elif block_type == "rare":
        screen.blit(rare_block_img, block)

    screen.blit(paddle_img, paddle)

    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.update()

# -------------------- GAME OVER --------------------
screen.fill(BLACK)
game_over = font.render(f"Game Over! Final Score: {score}", True, RED)
screen.blit(game_over, (W // 2 - 200, H // 2))
pygame.display.update()
pygame.time.wait(2000)

pygame.quit()
sys.exit()
