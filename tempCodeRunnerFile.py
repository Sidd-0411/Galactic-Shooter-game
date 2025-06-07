import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 700
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(" UFO vs Asteroids")

# Load images
bg_img = pygame.image.load("assets/space_bg.jpg")
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

ufo_img = pygame.image.load("assets/ufo.png")
asteroid_img = pygame.image.load("assets/asteroid.png")
laser_img = pygame.image.load("assets/laser.png")

# Game settings
SHIP_SPEED = 10
ASTEROID_SPEED = 2
FONT = pygame.font.SysFont(None, 40)

clock = pygame.time.Clock()
high_score = 0  # Global high score


def draw_game(ufo, lasers, asteroids, score, lives):
    win.blit(bg_img, (0, 0))  # 🌌 Draw space background
    win.blit(ufo_img, ufo)

    for laser in lasers:
        win.blit(laser_img, laser)
    for asteroid in asteroids:
        win.blit(asteroid_img, asteroid)

    # Score
    score_text = FONT.render(f"Score: {score}", True, (255, 255, 255))
    win.blit(score_text, (10, 10))

    # Lives
    lives_text = FONT.render(f"Lives: {lives}", True, (255, 150, 150))
    win.blit(lives_text, (WIDTH - 130, 10))

    # High Score
    hs_text = FONT.render(f"High Score: {high_score}", True, (200, 200, 100))
    win.blit(hs_text, (WIDTH // 2 - 100, 10))

    pygame.display.update()


def draw_game_over(score):
    win.blit(bg_img, (0, 0))  # background behind Game Over screen
    game_over_text = FONT.render("💀 GAME OVER 💀", True, (255, 0, 0))
    retry_text = FONT.render("Press [R] to Retry", True, (255, 255, 255))
    your_score = FONT.render(f"Your Score: {score}", True, (255, 255, 255))
    best_score = FONT.render(f"High Score: {high_score}", True, (255, 255, 100))

    win.blit(game_over_text, (WIDTH // 2 - 120, HEIGHT // 2 - 60))
    win.blit(your_score, (WIDTH // 2 - 110, HEIGHT // 2 - 20))
    win.blit(best_score, (WIDTH // 2 - 110, HEIGHT // 2 + 20))
    win.blit(retry_text, (WIDTH // 2 - 140, HEIGHT // 2 + 60))

    pygame.display.update()


def main():
    global high_score

    # Reset all game state
    ufo = ufo_img.get_rect(midbottom=(WIDTH // 2, HEIGHT - 20))
    lasers = []
    asteroids = []
    score = 0
    lives = 3
    game_over = False

    while True:
        clock.tick(60)

        # Handle quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if not game_over:
            # Ship movement
            if keys[pygame.K_LEFT] and ufo.left > 0:
                ufo.x -= SHIP_SPEED
            if keys[pygame.K_RIGHT] and ufo.right < WIDTH:
                ufo.x += SHIP_SPEED

            # Shoot laser
            if keys[pygame.K_SPACE]:
                if len(lasers) < 5:
                    laser = laser_img.get_rect(midbottom=ufo.midtop)
                    lasers.append(laser)

            # Move lasers
            for laser in lasers[:]:
                laser.y -= 8
                if laser.bottom < 0:
                    lasers.remove(laser)

            # Spawn asteroids
            if random.randint(1, 30) == 1:
                asteroid = asteroid_img.get_rect(midtop=(random.randint(0, WIDTH - 50), 0))
                asteroids.append(asteroid)

            # Move asteroids
            for asteroid in asteroids[:]:
                asteroid.y += ASTEROID_SPEED
                if asteroid.top > HEIGHT:
                    asteroids.remove(asteroid)
                if asteroid.colliderect(ufo):
                    asteroids.remove(asteroid)
                    lives -= 1
                    if lives <= 0:
                        game_over = True
                        if score > high_score:
                            high_score = score

            # Check laser hits
            for asteroid in asteroids[:]:
                for laser in lasers[:]:
                    if asteroid.colliderect(laser):
                        asteroids.remove(asteroid)
                        lasers.remove(laser)
                        score += 1
                        break

            draw_game(ufo, lasers, asteroids, score, lives)

        else:
            draw_game_over(score)
            if keys[pygame.K_r]:
                main()  # Restart game


# Run the game
main()
