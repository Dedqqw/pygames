import pygame
import sys
import random
pygame.init()

W, H = 550, 550
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Catch the Falling Blocks")

RED, WHT,BLC = (255, 0, 0), (255, 255, 255), (0,0,0)
# Load images
bg_img = pygame.image.load("Schermafbeelding 2026-02-05 105843.png").convert()
bg_img = pygame.transform.scale(bg_img, (W, H))

block_img = pygame.image.load("Schermafbeelding 2026-02-05 202438.png").convert_alpha()
block_img = pygame.transform.scale(block_img, (100, 100))

paddle_img = pygame.image.load("Schermafbeelding 2026-01-15 204202.png").convert_alpha()
paddle_img = pygame.transform.scale(paddle_img, (120, 120))

paddle = paddle_img.get_rect()
paddle.midbottom = (W // 2, H - 10)

block = block_img.get_rect()
block.x = random.randint(0, W - block.width)
block.y = 0

fall_speed = 5

font = pygame.font.SysFont("new times roman", 40)
score = 0

clock = pygame.time.Clock()
run = True

while run:
    clock.tick(60)

    # draw background first
    screen.blit(bg_img, (0, 0))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        paddle.x -= 9
    if keys[pygame.K_d]:
        paddle.x += 9
    #if keys[pygame.K_w]:
        #paddle.y -= 9
    #if keys[pygame.K_s]:
        #paddle.y += 9

    paddle.x = max(0, min(W - paddle.width, paddle.x))
    paddle.y = max(0, min(H - paddle.height, paddle.y))

    block.y += fall_speed
    
    #if block.y > H:
        #block.y = 0
        #block.x = random.randint(0, W - block.width)

    if block.colliderect(paddle):
        score += 1  # Increase score
        block.y = 0
        block.x = random.randint(0, W - block.width)
        fall_speed += 0.5

    screen.blit(paddle_img, paddle)
    screen.blit(block_img, block)

    if block.y > H:
        game_over = font.render(f"Game Over! Final Score: {score}", True, RED)
        screen.blit(game_over, (W // 2 - 150, H // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        run = False

    score_text = font.render(f"Score: {score}", True, BLC)
    screen.blit(score_text, (10, 10))
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
sys.exit()
