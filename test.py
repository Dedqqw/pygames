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
WHITE = (255, 255, 255)
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

# -------------------- PLAYER --------------------
paddle = paddle_img.get_rect()
paddle.midbottom = (W // 2, H - 10)

# -------------------- BLOCK --------------------
block = good_block_img.get_rect()
block.x = random.randint(0, W - block.width)
block.y = 0

fall_speed = 5
is_bad_block = False

# -------------------- SCORE --------------------
font = pygame.font.SysFont("timesnewroman", 36)
score = 0

# -------------------- GAME LOOP --------------------
run = True
while run:
    clock.tick(FPS)

    # -------- EVENTS --------
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
        if is_bad_block:
            run = False  # GAME OVER
        else:
            score += 1
            fall_speed += 0.4

            block.y = 0
            block.x = random.randint(0, W - block.width)
            is_bad_block = random.random() < 0.25  # 25% chance

    # -------- BLOCK MISSED --------
    if block.y > H:
        block.y = 0
        block.x = random.randint(0, W - block.width)
        is_bad_block = random.random() < 0.25

    # -------- DRAW --------
    screen.blit(bg_img, (0, 0))

    if is_bad_block:
        screen.blit(bad_block_img, block)
    else:
        screen.blit(good_block_img, block)

    screen.blit(paddle_img, paddle)

    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.update()

# -------------------- GAME OVER SCREEN --------------------
screen.fill(BLACK)
game_over = font.render(f"Game Over! Final Score: {score}", True, RED)
screen.blit(game_over, (W // 2 - 200, H // 2))
pygame.display.update()
pygame.time.wait(2000)

pygame.quit()
sys.exit()
