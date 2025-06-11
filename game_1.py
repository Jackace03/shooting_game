import pygame
import sys
import random

# Initialize PyGame
pygame.init()

# Set up the game window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
font = pygame.font.SysFont(None, 36)
pygame.display.set_caption("Simple Shooter Game")
laser_sound = pygame.mixer.Sound("laser_1.mp3")
laser_sound.set_volume(0.5)

# Player settings
player_width = 50
player_height = 60
player_x = screen_width // 2 - player_width // 2
player_y = screen_height - player_height - 10
player_speed = 5

# Bullet settings
bullet_width = 5
bullet_height = 10
bullet_speed = 7
bullets = []

# Power Up settings
powerup_width = 30
powerup_height = 30
powerup_speed = 3
powerups = []

# Normal Enemy settings
enemy_width = 50
enemy_height = 60
enemy_speed = 2
enemy_health = 3
enemies = []
alien_img = pygame.image.load("alien_1.jpg").convert_alpha()
alien_img = pygame.transform.scale(alien_img, (enemy_width, enemy_height))

# Fast Enemy settings
fast_enemy_width = 40
fast_enemy_height = 50
fast_enemy_speed = 5
fast_enemy_health = 1
fast_enemies = []

# Tank Enemy settings
tank_enemy_width = 100
tank_enemy_height = 120
tank_enemy_speed = 1
tank_enemy_health = 10
tank_enemies = []

# Shooting Enemy settings
shooting_enemy_width = 50
shooting_enemy_height = 60
shooting_enemy_speed = 2
shooting_enemy_health = 2
shooting_enemies = []
shooting_enemies_bullets = []

# Spawn an enemy every 2 seconds
enemy_timer = 0
enemy_spawn_time = 2000

# Set the frame rate
clock = pygame.time.Clock()

#health
health = 10

#score
score = 0

#game over
game_over = False

#frame rate
frame_rate = 60
difficulty_frames = 0

#power ups
rapid_fire_end_time = 0
last_shot_time = 0

# Collision detection function
def check_collision(rect1, rect2):
    return rect1.colliderect(rect2)

class Enemy:
    def __init__(self, x, y, width, height, health, speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.health = health
        self.speed = speed
        self.shoot_cooldown = random.randint(15, 30)

class PowerUp:
    def __init__(self, x, y, width, height, speed, type):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.type = type

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # laser_sound.play()
                bullet_x = player_x + player_width // 2 - bullet_width // 2
                bullet_y = player_y
                bullets.append(pygame.Rect(bullet_x, bullet_y, bullet_width, bullet_height))

    current_time = pygame.time.get_ticks()
    is_rapid_fire = current_time < rapid_fire_end_time

    keys = pygame.key.get_pressed()

    if is_rapid_fire:
        # Rapid-fire: hold space
        if keys[pygame.K_SPACE] and pygame.time.get_ticks() - last_shot_time > 100:
            bullet_x = player_x + player_width // 2 - bullet_width // 2
            bullet_y = player_y
            bullets.append(pygame.Rect(bullet_x, bullet_y, bullet_width, bullet_height))
            last_shot_time = pygame.time.get_ticks()
        

    # Handle player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
        player_x += player_speed

    # Update bullet positions
    for bullet in bullets:
        bullet.y -= bullet_speed
    bullets = [bullet for bullet in bullets if bullet.y > 0]

    if random.randint(0, 500) == 1:  # 1 in 500 chance per frame
        x = random.randint(0, screen_width - powerup_width)
        y = -powerup_height
        new_powerup = PowerUp(x, y, powerup_width, powerup_height, powerup_speed, random.choice(["health", "rapid_fire"]))
        powerups.append(new_powerup)

    # Update enemy positions and spawn new ones
    current_time = pygame.time.get_ticks()
    if current_time - enemy_timer > enemy_spawn_time:
        enemy_type = random.randint(0, 3)
        if enemy_type == 0:
            enemy_x = random.randint(0, screen_width - enemy_width)
            enemy_y = -enemy_height
            enemies.append(Enemy(enemy_x, enemy_y, enemy_width, enemy_height, enemy_health, enemy_speed))
        elif enemy_type == 1:
            enemy_x = random.randint(0, screen_width - fast_enemy_width)
            enemy_y = -fast_enemy_height
            fast_enemies.append(Enemy(enemy_x, enemy_y, fast_enemy_width, fast_enemy_height, fast_enemy_health, fast_enemy_speed))
        elif enemy_type == 2:
            enemy_x = random.randint(0, screen_width - tank_enemy_width)
            enemy_y = -tank_enemy_height
            tank_enemies.append(Enemy(enemy_x, enemy_y, tank_enemy_width, tank_enemy_height, tank_enemy_health, tank_enemy_speed))
        else:
            enemy_x = random.randint(0, screen_width - shooting_enemy_width)
            enemy_y = -shooting_enemy_height
            shooting_enemies.append(Enemy(enemy_x, enemy_y, shooting_enemy_width, shooting_enemy_height, shooting_enemy_health, shooting_enemy_speed))
        enemy_timer = current_time
    
    player = pygame.Rect(player_x, player_y, player_width, player_height)

    for powerup in powerups[:]:
        powerup.rect.y += powerup.speed

    for enemy in enemies:
        enemy.rect.y += enemy.speed
    
    for fast_enemy in fast_enemies:
        fast_enemy.rect.y += fast_enemy.speed

    for tank_enemy in tank_enemies:
        tank_enemy.rect.y += tank_enemy.speed
    
    for shooting_enemy in shooting_enemies:
        shooting_enemy.rect.y += shooting_enemy.speed
        shooting_enemy.shoot_cooldown -= 1
        if shooting_enemy.shoot_cooldown <= 0:
            bullet_x = shooting_enemy.rect.x + shooting_enemy.rect.width // 2 - bullet_width // 2
            bullet_y = shooting_enemy.rect.y
            shooting_enemies_bullets.append(pygame.Rect(bullet_x, bullet_y, bullet_width, bullet_height))
            shooting_enemy.shoot_cooldown = random.randint(15, 60)  # reset cooldown
    
    for bullet in shooting_enemies_bullets:
        bullet.y += bullet_speed
    shooting_enemies_bullets = [bullet for bullet in shooting_enemies_bullets if bullet.y > 0]



    # Check for collisions
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if check_collision(bullet, enemy.rect):
                bullets.remove(bullet)
                enemy.health -= 1
                if enemy.health <= 0:
                    enemies.remove(enemy)
                    score += 1
                break
        for fast_enemy in fast_enemies[:]:
            if check_collision(bullet, fast_enemy.rect):
                bullets.remove(bullet)
                fast_enemy.health -= 1
                if fast_enemy.health <= 0:
                    fast_enemies.remove(fast_enemy)
                    score += 2
                break
        for tank_enemy in tank_enemies[:]:
            if check_collision(bullet, tank_enemy.rect):
                bullets.remove(bullet)
                tank_enemy.health -= 1
                if tank_enemy.health <= 0:
                    tank_enemies.remove(tank_enemy)
                    score += 3
                break
        for shooting_enemy in shooting_enemies[:]:
            if check_collision(bullet, shooting_enemy.rect):
                bullets.remove(bullet)
                shooting_enemy.health -= 1
                if shooting_enemy.health <= 0:
                    shooting_enemies.remove(shooting_enemy)
                    score += 2
                break

    for powerup in powerups[:]:
        if check_collision(powerup.rect, player):
            if powerup.type == 'rapid_fire':
                rapid_fire_end_time = pygame.time.get_ticks() + 3000
            else:
                health += 2
            powerups.remove(powerup)
    
    for bullet in shooting_enemies_bullets[:]:
        if check_collision(bullet, player):
            shooting_enemies_bullets.remove(bullet)
            health -= 1

    for enemy in enemies[:]:
        if check_collision(player, enemy.rect):
            enemies.remove(enemy)
            health -= 1
    
    for fast_enemy in fast_enemies[:]:
        if check_collision(player, fast_enemy.rect):
            fast_enemies.remove(fast_enemy)
            health -= 1
    
    for tank_enemy in tank_enemies[:]:
        if check_collision(player, tank_enemy.rect):
            tank_enemies.remove(tank_enemy)
            health -= 1

    for shooting_enemy in shooting_enemies[:]:
        if check_collision(player, shooting_enemy.rect):
            shooting_enemies.remove(shooting_enemy)
            health -= 1

    if int(score/10) > difficulty_frames:
        difficulty_frames = int(score/10)

    if health <= 0:
        game_over_font = pygame.font.SysFont(None, 72)
        small_font = pygame.font.SysFont(None, 36)
        game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2 - 30))
        restart_text = small_font.render("Press R to Restart", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(screen_width // 2, screen_height // 2 + 30))

        screen.fill((0, 0, 0))  # Clear screen
        screen.blit(game_over_text, game_over_rect)
        screen.blit(restart_text, restart_rect)
        pygame.display.flip()   # Show Game Over message

        # Wait for user to press a key or quit
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # For example, press R to restart
                        # Reset game state
                        health = 10
                        score = 0
                        enemy_timer = 0
                        enemies.clear()
                        fast_enemies.clear()
                        tank_enemies.clear()
                        shooting_enemies.clear()
                        bullets.clear()
                        shooting_enemies_bullets.clear()
                        powerups.remove()
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

    # Remove enemies that are off the screen
    enemies = [enemy for enemy in enemies if enemy.rect.y < screen_height]
    fast_enemies = [fast_enemy for fast_enemy in fast_enemies if fast_enemy.rect.y < screen_height]
    tank_enemies = [tank_enemy for tank_enemy in tank_enemies if tank_enemy.rect.y < screen_height]
    shooting_enemies = [shooting_enemy for shooting_enemy in shooting_enemies if shooting_enemy.rect.y < screen_height]
    powerups = [powerup for powerup in powerups if powerup.rect.y < screen_height]

    # Fill the screen with black
    screen.fill((0, 0, 0))

    # Draw the player
    pygame.draw.rect(screen, (0, 128, 255), (player_x, player_y, player_width, player_height))

    # Draw the bullets
    for bullet in bullets:
        pygame.draw.rect(screen, (255, 255, 255), bullet)

    for bullet in shooting_enemies_bullets:
        pygame.draw.rect(screen, (255, 255, 0), bullet)

    # Draw the enemies
    for enemy in enemies:
        screen.blit(alien_img, enemy.rect)
    for fast_enemy in fast_enemies:
        pygame.draw.rect(screen, (0, 255, 0), fast_enemy.rect)
    for tank_enemy in tank_enemies:
        pygame.draw.rect(screen, (0, 0, 255), tank_enemy.rect)
    for shooting_enemy in shooting_enemies:
        pygame.draw.rect(screen, (255, 255, 0), shooting_enemy.rect)
    for powerup in powerups:
        if powerup.type == 'rapid_fire':
            pygame.draw.rect(screen, (255, 0, 0), powerup.rect)
        else:
            pygame.draw.rect(screen, (0, 255, 255), powerup.rect)

    # Render the score text
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))  # White text
    screen.blit(score_text, (10, 10))  # Top-left corner (x=10, y=10)

    health_text = font.render(f"Health: {health}", True, (255, 255, 255))  # White text
    health_text_width = health_text.get_width()
    screen.blit(health_text, (screen_width - health_text_width - 10, 10))

    if is_rapid_fire:
        seconds_left = (rapid_fire_end_time - current_time) / 1000
        rapid_fire_time = font.render(f"Rapid Fire: {int(seconds_left) + 1}", True, (255, 255, 255))
        rapid_fire_text_width = rapid_fire_time.get_width()
        screen.blit(rapid_fire_time, (screen_width / 2 - rapid_fire_text_width / 2, 10))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate at 60 FPS
    clock.tick(frame_rate + (difficulty_frames * 10))