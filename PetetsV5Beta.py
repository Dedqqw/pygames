import pygame
import sys
import random
import json
import os

pygame.init()

# ---------------- SETTINGS ----------------
W, H = 550, 550
FPS = 60
MAX_LIVES = 3
SAVE_FILE = "save.json"

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

# ---------------- COLORS ----------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)

# ---------------- FONTS ----------------
title_font = pygame.font.SysFont("arial", 48)
font = pygame.font.SysFont("arial", 26)

# ---------------- STATES ----------------
MENU = "menu"
GAME = "game"
SHOP = "shop"
state = MENU

# ---------------- LOAD IMAGES ----------------
bg_img = pygame.transform.scale(
    pygame.image.load("Schermafbeelding 2026-02-05 105843.png"), (W, H)
)

good_block_img = pygame.transform.scale(
    pygame.image.load("Schermafbeelding 2026-02-05 202438.png"), (100, 100)
)

bad_block_img = pygame.transform.scale(
    pygame.image.load("afbeelding (2).png"), (100, 100)
)

rare_block_img = pygame.transform.scale(
    pygame.image.load("le-bon-bon-lebron-james.png"), (100, 100)
)

heart_img = pygame.transform.scale(
    pygame.image.load("heart.png"), (32, 32)
)

broken_heart_img = pygame.transform.scale(
    pygame.image.load("broken_heart.png"), (32, 32)
)

# ---------------- SKINS ----------------
paddle_skins = {
    "default": {
        "img": pygame.transform.scale(
            pygame.image.load("Schermafbeelding 2026-01-15 204202.png").convert_alpha(),
            (120, 120)
        ),
        "price": 0
    },
    "red": {
        "img": pygame.transform.scale(
            pygame.image.load("paddle_red.png").convert_alpha(),
            (120, 120)
        ),
        "price": 50
    },
    "blue": {
        "img": pygame.transform.scale(
            pygame.image.load("paddle_blue.png").convert_alpha(),
            (120, 120)
        ),
        "price": 100
    }
}

# ---------------- SAVE / LOAD ----------------
def load_save():
    if not os.path.exists(SAVE_FILE):
        return {
            "money": 0,
            "current_skin": "default",
            "owned_skins": ["default"]
        }
    with open(SAVE_FILE, "r") as f:
        return json.load(f)

def save_game():
    data = {
        "money": money,
        "current_skin": current_skin,
        "owned_skins": owned_skins
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

save_data = load_save()
money = save_data["money"]
current_skin = save_data["current_skin"]
owned_skins = save_data["owned_skins"]

# ---------------- BUTTON CLASS ----------------
class Button:
    def __init__(self, text, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self):
        pygame.draw.rect(screen, GRAY, self.rect)
        txt = font.render(self.text, True, BLACK)
        screen.blit(txt, (self.rect.centerx - txt.get_width() // 2,
                          self.rect.centery - txt.get_height() // 2))

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

# ---------------- BUTTONS ----------------
play_btn = Button("PLAY", 175, 230, 200, 50)
shop_btn = Button("SHOP", 175, 300, 200, 50)
back_btn = Button("BACK", 20, 20, 120, 40)

# ---------------- GAME OBJECTS ----------------
paddle = paddle_skins[current_skin]["img"].get_rect()
block = good_block_img.get_rect()

score = 0
lives = MAX_LIVES
fall_speed = 5
block_type = "good"
game_over = False

# ---------------- FUNCTIONS ----------------
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

reset_game()

# ---------------- MAIN LOOP ----------------
run = True
while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_game()
            run = False

        # MENU
        if state == MENU:
            if play_btn.clicked(event):
                reset_game()
                state = GAME
            if shop_btn.clicked(event):
                state = SHOP

        # SHOP
        elif state == SHOP:
            if back_btn.clicked(event):
                save_game()
                state = MENU

            if event.type == pygame.MOUSEBUTTONDOWN:
                y = 220
                for name, skin in paddle_skins.items():
                    rect = pygame.Rect(120, y, 300, 30)
                    if rect.collidepoint(event.pos):
                        if name in owned_skins:
                            current_skin = name
                        else:
                            if money >= skin["price"]:
                                money -= skin["price"]
                                owned_skins.append(name)
                                current_skin = name
                                save_game()
                    y += 40

        # GAME
        elif state == GAME:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                state = MENU

    # GAME LOGIC
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
                    save_game()
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
                    save_game()
            spawn_block()

    # DRAW
    screen.fill(WHITE)

    if state == MENU:
        screen.blit(title_font.render("MY GAME", True, BLACK),
                    (W // 2 - 110, 120))
        play_btn.draw()
        shop_btn.draw()
        screen.blit(font.render(f"Money: {money}", True, BLACK), (10, 10))

    elif state == SHOP:
        screen.blit(title_font.render("SHOP", True, BLACK),
                    (W // 2 - 60, 120))
        screen.blit(font.render(f"Money: {money}", True, BLACK), (10, 10))

        y = 220
        for name, skin in paddle_skins.items():
            text = f"{name.upper()} - "
            text += "OWNED" if name in owned_skins else f"{skin['price']} coins"
            screen.blit(font.render(text, True, BLACK), (120, y))
            y += 40

        back_btn.draw()

    elif state == GAME:
        screen.blit(bg_img, (0, 0))

        img = paddle_skins[current_skin]["img"]
        screen.blit(img, paddle)

        if block_type == "good":
            screen.blit(good_block_img, block)
        elif block_type == "bad":
            screen.blit(bad_block_img, block)
        else:
            screen.blit(rare_block_img, block)

        for i in range(MAX_LIVES):
            heart = heart_img if i < lives else broken_heart_img
            screen.blit(heart, (10 + i * 36, 10))

        screen.blit(font.render(f"Score: {score}", True, BLACK),
                    (W - 140, 10))

        if game_over:
            screen.blit(font.render("GAME OVER", True, RED),
                        (W // 2 - 90, H // 2))

    pygame.display.update()

pygame.quit()
sys.exit()
