import pygame
import random
import json
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Tower Defense")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Game variables
enemy_size = 50
tower_size = 50
bullet_speed = 5
score = 0
tower_speed = 5
game_over = False
input_active = False
player_name = ''
high_scores = []
boss_appeared = False

# Fonts
font = pygame.font.SysFont(None, 36)
game_over_font = pygame.font.SysFont(None, 72)

# Load images
enemy_image = pygame.image.load("enemy.png")
enemy2_image = pygame.image.load("enemy2.png")
tower_image = pygame.image.load("tower.png")
boss_image = pygame.image.load("boss.png")
background_image = pygame.image.load("space_background.jpg")

# Resize images
enemy_image = pygame.transform.scale(enemy_image, (enemy_size, enemy_size))
enemy2_image = pygame.transform.scale(enemy2_image, (enemy_size, enemy_size))
tower_image = pygame.transform.scale(tower_image, (tower_size, tower_size))
boss_image = pygame.transform.scale(boss_image, (100, 100))  # Boss size

# Background scrolling
bg_y1 = 0
bg_y2 = -HEIGHT
bg_scroll_speed = 1

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - enemy_size)
        self.rect.y = -enemy_size
        self.health = 1
        self.speed = random.randint(2, 4)  # Different speeds for enemy

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.kill()

class Enemy2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy2_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - enemy_size)
        self.rect.y = -enemy_size
        self.health = 2
        self.speed = random.randint(1, 3)  # Different speeds for enemy2

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.kill()

# Boss class
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = boss_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 100)  # Random initial x position
        self.rect.y = 50  # Constant y position
        self.health = 30
        self.speed = 5  # Boss horizontal speed
        self.direction = 1  # 1 for right, -1 for left

    def update(self):
        self.rect.x += self.speed * self.direction

        # Reverse direction if boss reaches screen edges
        if self.rect.right >= WIDTH or self.rect.left <= 0:
            self.direction *= -1

    def shoot(self):
        if random.randint(1, 20) == 1:  # Boss shooting frequency
            bullet = Bullet(self.rect.centerx, self.rect.bottom, 1)
            all_sprites.add(bullet)
            boss_bullets.add(bullet)

# Tower class
class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = tower_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def move(self, dx):
        self.rect.x += dx
        # Keep tower within screen bounds
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > WIDTH - tower_size:
            self.rect.x = WIDTH - tower_size

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction=-1):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.direction = direction

    def update(self):
        self.rect.y += bullet_speed * self.direction
        if self.rect.y < 0 or self.rect.y > HEIGHT:
            self.kill()

# Function to restart the game
def restart_game():
    global all_sprites, enemies, enemies2, bullets, tower, score, game_over, input_active, player_name, boss, boss_appeared, boss_bullets
    all_sprites.empty()
    enemies.empty()
    enemies2.empty()
    bullets.empty()
    boss_bullets.empty()
    score = 0
    game_over = False
    input_active = False
    player_name = ''
    boss_appeared = False
    tower = Tower(WIDTH // 2 - tower_size // 2, HEIGHT - tower_size)
    all_sprites.add(tower)

# Function to save high scores
def save_high_scores():
    global high_scores
    with open("high_scores.json", "w") as f:
        json.dump(high_scores, f)

# Function to load high scores
def load_high_scores():
    global high_scores
    if os.path.exists("high_scores.json"):
        with open("high_scores.json", "r") as f:
            high_scores = json.load(f)

# Sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
enemies2 = pygame.sprite.Group()
bullets = pygame.sprite.Group()
boss_bullets = pygame.sprite.Group()

# Create a tower
tower = Tower(WIDTH // 2 - tower_size // 2, HEIGHT - tower_size)
all_sprites.add(tower)

# Load high scores
load_high_scores()

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                # Shoot a bullet
                bullet = Bullet(tower.rect.centerx, tower.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
            elif event.key == pygame.K_r and game_over and not input_active:
                restart_game()
            elif event.key == pygame.K_RETURN and game_over and input_active:
                high_scores.append({"name": player_name, "score": score})
                high_scores = sorted(high_scores, key=lambda x: x["score"], reverse=True)[:5]
                save_high_scores()
                input_active = False
            elif event.key == pygame.K_BACKSPACE and input_active:
                player_name = player_name[:-1]
            elif input_active:
                player_name += event.unicode

    if not game_over:
        # Get pressed keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            tower.move(-tower_speed)
        if keys[pygame.K_RIGHT]:
            tower.move(tower_speed)

        # Spawn enemies
        if random.randint(1, 20) == 1:
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)
        if random.randint(1, 40) == 1:
            enemy2 = Enemy2()
            all_sprites.add(enemy2)
            enemies2.add(enemy2)

        # Update sprites
        all_sprites.update()

        # Check for collisions with Enemy
        hits = pygame.sprite.groupcollide(enemies, bullets, False, True)
        for hit in hits:
            hit.health -= 1
            if hit.health <= 0:
                hit.kill()
                score += 1

        # Check for collisions with Enemy2
        hits = pygame.sprite.groupcollide(enemies2, bullets, False, True)
        for hit in hits:
            hit.health -= 1
            if hit.health <= 0:
                hit.kill()
                score += 2  # Enemy2 gives more points

        # Check for boss appearance
        if score >= 50 and not boss_appeared:
            boss = Boss()
            all_sprites.add(boss)
            boss_appeared = True

        # Boss shoots bullets
        if boss_appeared:
            boss.shoot()

        # Check for collisions between enemies and the tower
        if pygame.sprite.spritecollideany(tower, enemies) or pygame.sprite.spritecollideany(tower, enemies2):
            game_over = True
            input_active = True
            tower.kill()  # Kill the tower sprite

        # Check for collisions between boss bullets and tower
        if pygame.sprite.spritecollideany(tower, boss_bullets):
            game_over = True
            input_active = True
            tower.kill()  # Kill the tower sprite

        # Check for collisions between bullets and boss
        if boss_appeared:
            hits = pygame.sprite.spritecollide(boss, bullets, True)
            for hit in hits:
                boss.health -= 1
                if boss.health <= 0:
                    boss.kill()
                    score += 10  # Boss gives more points

    # Draw background
    screen.blit(background_image, (0, bg_y1))
    screen.blit(background_image, (0, bg_y2))

    # Update background position
    bg_y1 += bg_scroll_speed
    bg_y2 += bg_scroll_speed

    # Reset background position
    if bg_y1 >= HEIGHT:
        bg_y1 = -HEIGHT
    if bg_y2 >= HEIGHT:
        bg_y2 = -HEIGHT

    # Draw sprites
    all_sprites.draw(screen)

    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Draw game over
    if game_over:
        game_over_text = game_over_font.render("Game Over", True, RED)
        restart_text = font.render("Press 'R' to Restart", True, WHITE)
        enter_name_text = font.render("Enter Your Name: " + player_name, True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + game_over_text.get_height() // 2 + 10))
        if input_active:
            screen.blit(enter_name_text, (WIDTH // 2 - enter_name_text.get_width() // 2, HEIGHT // 2 + game_over_text.get_height() // 2 + 50))

        # Draw high scores
        high_scores_text = game_over_font.render("High Scores", True, WHITE)
        screen.blit(high_scores_text, (WIDTH // 2 - high_scores_text.get_width() // 2, 50))
        for idx, score_entry in enumerate(high_scores):
            score_entry_text = font.render(f"{score_entry['name']}: {score_entry['score']}", True, WHITE)
            screen.blit(score_entry_text, (WIDTH // 2 - score_entry_text.get_width() // 2, 100 + idx * 30))

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
