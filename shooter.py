import pygame
import random

# Pygame initialization
pygame.init()

# Game window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simple Shooter")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)

# Game loop
def game_loop():
    # Game settings
    player_size = 50
    player_speed = 2
    enemy_size = 50
    enemy_speed = 2
    enemy_spawn_rate = 60  # Number of frames between enemy spawns
    enemy_spawn_timer = 0
    max_bullets = 5
    bullet_size = 10
    bullet_speed = 10
    player_pos = [screen_width // 2, screen_height - player_size - 10]
    enemy_list = []
    bullet_list = []
    booster_duration = 3000  # Duration of the booster effect in milliseconds (3 seconds)
    booster_cooldown = 6000  # Cooldown time in milliseconds (6 seconds)
    booster_timer = 60000
    booster_cooldown_timer = 30000
    booster_active = False
    score = 0  # Score variable

    # Function to spawn enemies
    def spawn_enemy():
        enemy_pos = [random.randint(0, screen_width - enemy_size), 0]
        enemy_list.append(enemy_pos)

    # Game loop
    game_over = False
    while not game_over:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t and booster_cooldown_timer == 0:
                    booster_active = True
                    booster_timer = pygame.time.get_ticks()
                    booster_cooldown_timer = pygame.time.get_ticks()
                elif event.key == pygame.K_ESCAPE:
                    paused = True
                    while paused:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_ESCAPE:
                                    paused = False
                                elif event.key == pygame.K_q:
                                    game_over = True
                                    paused = False
                        pygame.display.update()

        # Movement handling
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT] and player_pos[0] < screen_width - player_size:
            player_pos[0] += player_speed
        if keys[pygame.K_SPACE]:
            if len(bullet_list) < max_bullets:
                bullet_list.append([player_pos[0] + player_size // 2 - bullet_size // 2, player_pos[1] - bullet_size])
        
        # Updating the game
        screen.fill(black)

        # Updating the player position
        pygame.draw.rect(screen, white, (player_pos[0], player_pos[1], player_size, player_size))

        # Updating the enemy positions
        for enemy_pos in enemy_list.copy():
            if booster_active:
                pygame.draw.rect(screen, red, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size), 3)
            else:
                pygame.draw.rect(screen, red, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))
            enemy_pos[1] += enemy_speed
            if enemy_pos[1] > screen_height:
                enemy_list.remove(enemy_pos)

        # Spawning new enemies
        enemy_spawn_timer += 1
        if enemy_spawn_timer == enemy_spawn_rate:
            enemy_spawn_timer = 0
            spawn_enemy()

        # Updating the bullet positions
        for bullet_pos in bullet_list.copy():
            pygame.draw.rect(screen, white, (bullet_pos[0], bullet_pos[1], bullet_size, bullet_size))
            bullet_pos[1] -= bullet_speed
            if bullet_pos[1] < 0:
                bullet_list.remove(bullet_pos)

        # Collision detection
        for enemy_pos in enemy_list:
            if player_pos[0] < enemy_pos[0] + enemy_size and player_pos[0] + player_size > enemy_pos[0] and player_pos[1] < enemy_pos[1] + enemy_size and player_pos[1] + player_size > enemy_pos[1]:
                if booster_active:
                    enemy_list.remove(enemy_pos)
                    score += 10  # Increase score by 10 points
                else:
                    game_over = True
                break
            for bullet_pos in bullet_list:
                if bullet_pos[0] < enemy_pos[0] + enemy_size and bullet_pos[0] + bullet_size > enemy_pos[0] and bullet_pos[1] < enemy_pos[1] + enemy_size and bullet_pos[1] + bullet_size > enemy_pos[1]:
                    enemy_list.remove(enemy_pos)
                    bullet_list.remove(bullet_pos)
                    score += 10  # Increase score by 10 points
                    break

        # Updating the booster cooldown timer
        if booster_cooldown_timer != 0:
            current_time = pygame.time.get_ticks()
            if current_time - booster_cooldown_timer >= booster_cooldown:
                booster_cooldown_timer = 0

        # Updating the booster timer
        if booster_active:
            current_time = pygame.time.get_ticks()
            if current_time - booster_timer >= booster_duration:
                booster_active = False

        # Drawing the booster rectangle
        if booster_cooldown_timer == 0:
            pygame.draw.rect(screen, green, (10, 10, 20, 20))
        elif booster_active:
            pygame.draw.rect(screen, green, (10, 10, 20, 20), 3)

        # Checking for collision with booster
        if player_pos[0] < 30 and player_pos[1] < 30:
            if booster_cooldown_timer == 0:
                booster_cooldown_timer = pygame.time.get_ticks()

        # Noclip effect if booster is active
        if booster_active:
            pygame.draw.rect(screen, white, (player_pos[0], player_pos[1], player_size, player_size), 3)

        # Drawing the score text
        font = pygame.font.SysFont(None, 30)
        score_text = font.render("Score: " + str(score), True, white)
        screen.blit(score_text, (10, screen_height - 30))

        # Updating the screen
        pygame.display.update()

    # "Game Over" text
    font = pygame.font.SysFont(None, 50)
    text = font.render("Game Over", True, white)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text, text_rect)
    pygame.display.update()

    # Waiting for the "R" key to be pressed to restart the game
    restart = False
    while not restart:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                restart = True

    # Starting the game loop again
    game_loop()

# Starting the game loop
game_loop()

# Quitting Pygame
pygame.quit()