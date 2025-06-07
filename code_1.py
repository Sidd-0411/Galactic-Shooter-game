import pygame
import random
import sys
import math

pygame.init()

WIDTH, HEIGHT = 600, 700
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("UFO vs Asteroids")

# Load images
bg_img = pygame.image.load("assets/space_bg.jpg")
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

ufo_img = pygame.image.load("assets/ufo.png")
asteroid_img = pygame.image.load("assets/asteroid.png")
laser_img = pygame.image.load("assets/laser.png")
heart_img = pygame.image.load("assets/heart.png")
heart_img = pygame.transform.scale(heart_img, (32, 32))

try:
    SEXY_FONT = pygame.font.Font("assets/ethnocentric.ttf", 32)
except:
    SEXY_FONT = pygame.font.SysFont("Comic Sans MS", 32)

SHIP_SPEED = 10
ASTEROID_SPEED = 2
clock = pygame.time.Clock()
high_score = 0

DIFFICULTIES = {
    "Easy": 2,
    "Medium": 4,
    "Hard": 6
}
difficulty_names = list(DIFFICULTIES.keys())
current_difficulty_index = 1

CHARGE_TIME_FRAMES = 180
NUM_CONE_LASERS = 30
CONE_ANGLE_DEGREES = 90

class ConeLaser:
    def __init__(self, x, y, angle_deg):
        self.x = x
        self.y = y
        self.speed = 12
        self.angle = math.radians(angle_deg)
        self.vx = self.speed * math.sin(self.angle)
        self.vy = -self.speed * math.cos(self.angle)
        self.image = pygame.transform.rotate(laser_img, angle_deg)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.active = True

    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.center = (self.x, self.y)
        if self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT:
            self.active = False

    def draw(self, surface, offset=(0, 0)):
        ox, oy = offset
        surface.blit(self.image, (self.rect.x + ox, self.rect.y + oy))

def draw_text_center(text, font, color, y):
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(center=(WIDTH // 2, y))
    win.blit(rendered, rect)

def main_menu():
    global current_difficulty_index
    selected = 0
    menu_options = ["New Game", "Difficulty", "Exit"]
    running = True

    while running:
        clock.tick(60)
        win.fill((10, 10, 30))
        draw_text_center(" UFO vs Asteroids ", SEXY_FONT, (255, 255, 0), 150)

        for i, option in enumerate(menu_options):
            color = (255, 255, 255)
            if i == selected:
                color = (255, 150, 0)
            draw_text_center(option, SEXY_FONT, color, 300 + i * 60)

        diff_text = f"Difficulty: {difficulty_names[current_difficulty_index]}"
        draw_text_center(diff_text, SEXY_FONT, (200, 200, 200), 500)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(menu_options)
                elif event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                    if menu_options[selected] == "New Game":
                        running = False
                    elif menu_options[selected] == "Difficulty":
                        current_difficulty_index = (current_difficulty_index + 1) % len(difficulty_names)
                    elif menu_options[selected] == "Exit":
                        pygame.quit()
                        sys.exit()

def draw_game(ufo, lasers, cone_lasers, asteroids, score, lives, shake_offset=(0, 0), charge_progress=0, meteor_shower_active=False):
    offset_x, offset_y = shake_offset

    win.blit(bg_img, (0 + offset_x, 0 + offset_y))
    win.blit(ufo_img, (ufo.x + offset_x, ufo.y + offset_y))

    for laser in lasers:
        win.blit(laser_img, (laser.x + offset_x, laser.y + offset_y))

    for claser in cone_lasers:
        claser.draw(win, shake_offset)

    for asteroid in asteroids:
        win.blit(asteroid_img, (asteroid.x + offset_x, asteroid.y + offset_y))

    score_text = SEXY_FONT.render(f"Score: {score}", True, (255, 255, 255))
    hs_text = SEXY_FONT.render(f"High Score: {high_score}", True, (200, 200, 100))

    win.blit(score_text, (10, 10))
    win.blit(hs_text, (WIDTH // 2 - 110, 10))

    for i in range(lives):
        x_pos = WIDTH - (i + 1) * (heart_img.get_width() + 10) - 10
        win.blit(heart_img, (x_pos, 10))

    if charge_progress > 0.1:
        bar_width = 200
        bar_height = 20
        filled_width = int(bar_width * charge_progress)
        bar_x = WIDTH // 2 - bar_width // 2
        bar_y = HEIGHT - 50
        pygame.draw.rect(win, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)
        pygame.draw.rect(win, (0, 255, 255), (bar_x, bar_y, filled_width, bar_height))

    if meteor_shower_active:
        alert = SEXY_FONT.render("⚠️ METEOR SHOWER ⚠️", True, (255, 80, 80))
        win.blit(alert, (WIDTH // 2 - 170, HEIGHT // 2 - 200))

    pygame.display.update()

def draw_game_over(score):
    win.blit(bg_img, (0, 0))
    game_over_text = SEXY_FONT.render(" GAME OVER ", True, (255, 0, 0))
    retry_text = SEXY_FONT.render("Press [R] to Retry", True, (255, 255, 255))
    your_score = SEXY_FONT.render(f"Your Score: {score}", True, (255, 255, 255))
    best_score = SEXY_FONT.render(f"High Score: {high_score}", True, (255, 255, 100))

    win.blit(game_over_text, (WIDTH // 2 - 170, HEIGHT // 2 - 60))
    win.blit(your_score, (WIDTH // 2 - 150, HEIGHT // 2 - 20))
    win.blit(best_score, (WIDTH // 2 - 150, HEIGHT // 2 + 20))
    win.blit(retry_text, (WIDTH // 2 - 170, HEIGHT // 2 + 60))

    pygame.display.update()

def main():
    global high_score, ASTEROID_SPEED

    ASTEROID_SPEED = DIFFICULTIES[difficulty_names[current_difficulty_index]]

    ufo = ufo_img.get_rect(midbottom=(WIDTH // 2, HEIGHT - 20))
    lasers = []
    cone_lasers = []
    asteroids = []
    score = 0
    lives = 3
    game_over = False
    shake_duration = 0
    shake_magnitude = 8

    charge_frames = 0
    charging = False

    # Meteor shower variables
    meteor_shower_active = False
    meteor_shower_timer = 0
    next_meteor_shower = random.randint(1200, 1800)

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if not game_over:
            if keys[pygame.K_LEFT] and ufo.left > 0:
                ufo.x -= SHIP_SPEED
            if keys[pygame.K_RIGHT] and ufo.right < WIDTH:
                ufo.x += SHIP_SPEED

            if keys[pygame.K_SPACE]:
                if not charging:
                    charging = True
                    charge_frames = 0
                else:
                    charge_frames += 1
            else:
                if charging:
                    charge_ratio = charge_frames / CHARGE_TIME_FRAMES

                    if charge_ratio < 0.5:
                        # Below 50% charge, fire single normal laser
                        if len(lasers) < 5:
                            laser = laser_img.get_rect(midbottom=ufo.midtop)
                            lasers.append(laser)
                    else:
                        # At 50% or more, fire cone lasers starting at 10 up to 20
                        scaled_ratio = (charge_ratio - 0.5) / 0.5  # 0 to 1
                        num_lasers_to_fire = 10 + int(10 * scaled_ratio)  # 10 to 20 lasers

                        cone_lasers.clear()
                        start_angle = -CONE_ANGLE_DEGREES / 2
                        angle_step = CONE_ANGLE_DEGREES / (NUM_CONE_LASERS - 1)
                        step = max(1, NUM_CONE_LASERS // num_lasers_to_fire)
                        for i in range(0, NUM_CONE_LASERS, step):
                            angle = start_angle + i * angle_step
                            cone_lasers.append(ConeLaser(ufo.centerx, ufo.top, angle))

                    charging = False
                    charge_frames = 0

            for laser in lasers[:]:
                laser.y -= 8
                if laser.bottom < 0:
                    lasers.remove(laser)

            for claser in cone_lasers[:]:
                claser.move()
                if not claser.active:
                    cone_lasers.remove(claser)

            # Meteor Shower Logic
            meteor_shower_timer += 1
            if not meteor_shower_active and meteor_shower_timer > next_meteor_shower:
                meteor_shower_active = True
                meteor_shower_timer = 0
                next_meteor_shower = random.randint(1800, 2400)
                shake_duration = 20

            if meteor_shower_active and meteor_shower_timer > 300:
                meteor_shower_active = False
                meteor_shower_timer = 0

            # Asteroid spawning
            spawn_chance = 3 if meteor_shower_active else 30
            if random.randint(1, spawn_chance) == 1:
                asteroid = asteroid_img.get_rect(midtop=(random.randint(0, WIDTH - 50), 0))
                asteroids.append(asteroid)

            for asteroid in asteroids[:]:
                speed = ASTEROID_SPEED + 3 if meteor_shower_active else ASTEROID_SPEED
                asteroid.y += speed
                if asteroid.top > HEIGHT:
                    asteroids.remove(asteroid)
                elif asteroid.colliderect(ufo):
                    asteroids.remove(asteroid)
                    lives -= 1
                    shake_duration = 15
                    if lives <= 0:
                        game_over = True
                        if score > high_score:
                            high_score = score

            for asteroid in asteroids[:]:
                for laser in lasers[:]:
                    if asteroid.colliderect(laser):
                        asteroids.remove(asteroid)
                        lasers.remove(laser)
                        score += 1
                        break

            for claser in cone_lasers:
                for asteroid in asteroids[:]:
                    if claser.rect.colliderect(asteroid):
                        asteroids.remove(asteroid)
                        score += 1

            if shake_duration > 0:
                shake_offset = (
                    random.randint(-shake_magnitude, shake_magnitude),
                    random.randint(-shake_magnitude, shake_magnitude)
                )
                shake_duration -= 1
            else:
                shake_offset = (0, 0)

            charge_progress = min(charge_frames / CHARGE_TIME_FRAMES, 1.0)
            draw_game(ufo, lasers, cone_lasers, asteroids, score, lives, shake_offset, charge_progress, meteor_shower_active)
        else:
            draw_game_over(score)
            if keys[pygame.K_r]:
                main()

if __name__ == "__main__":
    main_menu()
    main()
