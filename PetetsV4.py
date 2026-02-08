import pygame
import sys
import random

pygame.init()

# -------------------- SETTINGS --------------------
W, H = 550, 550
FPS = 60
MAX_LIVES = 3

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

# -------------------- COLORS --------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)

# -------------------- FONTS --------------------
title_font = pygame.font.SysFont("arial", 48)
font = pygame.font.SysFont("arial", 28)

# -------------------- GAME STATES --------------------
MENU = "menu"
GAME = "game"
SHOP = "shop"
state = MENU

# -------------------- MONEY --------------------
money = 0

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

# -------------------- BUTTON CLASS --------------------
class Button:
    def __init__(self, text, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self):
        pygame.draw.rect(screen, GRAY, self.rect)
        txt = font.render(self.text, True, BLACK)
        screen.blit(txt, (self.rect.centerx - txt.get_width()//2,
                          self.rect.centery - txt.get_height()//2))

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

# -------------------- BUTTONS --------------------
play_btn = Button("PLAY", 175, 230, 200, 50)
shop_btn = Button("SHOP", 175, 300, 200, 50)
back_btn = Button("BACK", 20, 20, 120, 40)

# -------------------- GAME OBJECTS --------------------
paddle = paddle_img.get_rect()
block = good_block_img.get_rect()

score = 0
lives = MAX_LIVES
fall_speed = 5
block_type = "good"
game_over = False

# -------------------- FUNCTIONS --------------------
def spawn_block():
    global block_type
    r = random.random()
    if r < 0.01:
        block_type = "rare"
    elif r < 0.25:
        block_type = "bad"
    else:
        block_type = "good"

    block.x = random.randint(0, W - block.width)
    block.y = 0

def reset_game():
    global score, lives, fall_speed, game_over
    score = 0
    lives = MAX_LIVES
    fall_speed = 5
    game_over = False
    paddle.midbottom = (W // 2, H - 10)
    spawn_block()

# -------------------- START GAME INIT --------------------
reset_game()

# -------------------- MAIN LOOP --------------------
run = True
while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # -------- MENU --------
        if state == MENU:
            if play_btn.clicked(event):
                reset_game()
                state = GAME
            if shop_btn.clicked(event):
                state = SHOP

        # -------- SHOP --------
        elif state == SHOP:
            if back_btn.clicked(event):
                state = MENU

        # -------- GAME --------
        elif state == GAME:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                state = MENU

    # ================= LOGIC =================
    if state == GAME and not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            paddle.x -= 8
        if keys[pygame.K_d]:
            paddle.x += 8
        paddle.x = max(0, min(W - paddle.width, paddle.x))

        block.y += fall_speed

        if block.colliderect(paddle):
            if block_type == "bad":
                lives -= 1
                if lives <= 0:
                    game_over = True
                    money += score
                spawn_block()

            elif block_type == "good":
                score += 1
                fall_speed += 0.3
                spawn_block()

            elif block_type == "rare":
                score += 10
                spawn_block()

        if block.y > H:
            if block_type != "bad":
                lives -= 1
                if lives <= 0:
                    game_over = True
                    money += score
            spawn_block()

    # ================= DRAW =================
    screen.fill(WHITE)

    # -------- MENU --------
    if state == MENU:
        title = title_font.render("MY GAME", True, BLACK)
        screen.blit(title, (W//2 - title.get_width()//2, 120))
        play_btn.draw()
        shop_btn.draw()
        screen.blit(font.render(f"Money: {money}", True, BLACK), (10, 10))

    # -------- SHOP --------
    elif state == SHOP:
        screen.blit(title_font.render("SHOP", True, BLACK),
                    (W//2 - 60, 120))
        screen.blit(font.render(f"Money: {money}", True, BLACK), (10, 10))
        screen.blit(font.render("Coming soon...", True, BLACK), (180, 260))
        back_btn.draw()

    # -------- GAME --------
    elif state == GAME:
        screen.blit(bg_img, (0, 0))

        if block_type == "good":
            screen.blit(good_block_img, block)
        elif block_type == "bad":
            screen.blit(bad_block_img, block)
        else:
            screen.blit(rare_block_img, block)

        screen.blit(paddle_img, paddle)

        for i in range(MAX_LIVES):
            img = heart_img if i < lives else broken_heart_img
            screen.blit(img, (10 + i * 36, 10))

        screen.blit(font.render(f"Score: {score}", True, BLACK),
                    (W - 140, 10))

        if game_over:
            screen.blit(font.render("GAME OVER", True, RED),
                        (W//2 - 90, H//2))

    pygame.display.update()

pygame.quit()
sys.exit()

