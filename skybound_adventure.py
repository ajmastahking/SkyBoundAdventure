
import math
import random
import sys
import pygame

pygame.init()

# ==========================================
# GAME SETTINGS
# ==========================================
WIDTH = 800
HEIGHT = 440
FPS = 60

GRAVITY = 0.57
MOVE_SPEED = 4.5
JUMP_POWER = -12.5
DOUBLE_JUMP_POWER = -11.5

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Skybound Adventure")
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("arial", 22, bold=True)
SMALL_FONT = pygame.font.SysFont("arial", 16, bold=True)
BIG_FONT = pygame.font.SysFont("arial", 42, bold=True)

WHITE = (255, 255, 255)
DARK = (39, 50, 77)
PINK = (255, 101, 141)
GOLD = (255, 220, 84)
GREEN = (104, 201, 120)

# ==========================================
# LEVEL DATA
# Each platform is (x, y, width)
# ==========================================
LEVELS = [
    {
        "width": 2550,
        "ground": [
            (0, 390, 480),
            (590, 390, 380),
            (1080, 390, 440),
            (1630, 390, 360),
            (2090, 390, 460),
        ],
        "floating": [
            (210, 310, 130),
            (410, 245, 120),
            (670, 305, 120),
            (880, 235, 135),
            (1160, 310, 140),
            (1370, 240, 125),
            (1680, 305, 130),
            (1900, 240, 130),
            (2200, 300, 150),
        ],
        "enemies": [740, 1240, 1750, 2220],
    },
    {
        "width": 2850,
        "ground": [
            (0, 390, 380),
            (500, 390, 330),
            (950, 390, 360),
            (1430, 390, 350),
            (1900, 390, 350),
            (2370, 390, 480),
        ],
        "floating": [
            (160, 300, 110),
            (350, 230, 110),
            (590, 280, 115),
            (800, 210, 125),
            (1040, 290, 100),
            (1240, 215, 115),
            (1490, 300, 115),
            (1710, 225, 120),
            (1980, 290, 110),
            (2200, 210, 110),
            (2450, 285, 130),
            (2650, 225, 110),
        ],
        "enemies": [560, 1030, 1510, 2010, 2470],
    },
    {
        "width": 3100,
        "ground": [
            (0, 390, 340),
            (460, 390, 320),
            (900, 390, 310),
            (1330, 390, 340),
            (1800, 390, 320),
            (2240, 390, 330),
            (2690, 390, 410),
        ],
        "floating": [
            (150, 295, 100),
            (330, 220, 100),
            (520, 290, 105),
            (730, 205, 110),
            (980, 290, 105),
            (1160, 205, 100),
            (1390, 295, 105),
            (1590, 210, 105),
            (1850, 290, 100),
            (2050, 205, 105),
            (2310, 285, 110),
            (2500, 210, 100),
            (2770, 295, 105),
            (2930, 215, 110),
        ],
        "enemies": [520, 1000, 1450, 1860, 2330, 2740],
    },
]


# ==========================================
# PLAYER
# ==========================================
class Player:
    def __init__(self):
        self.rect = pygame.Rect(55, 310, 28, 36)
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.vx = 0
        self.vy = 0
        self.jumps = 0
        self.on_ground = False
        self.invincible = 0
        self.facing = 1

    def jump(self):
        if self.jumps < 2:
            if self.jumps == 0:
                self.vy = JUMP_POWER
            else:
                self.vy = DOUBLE_JUMP_POWER

            self.jumps += 1
            self.on_ground = False

    def update(self, platforms, world_width):
        keys = pygame.key.get_pressed()

        self.vx = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -MOVE_SPEED
            self.facing = -1

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = MOVE_SPEED
            self.facing = 1

        self.x += self.vx
        self.x = max(0, min(world_width - self.rect.width, self.x))
        self.rect.x = round(self.x)

        previous_bottom = self.rect.bottom

        self.vy = min(13, self.vy + GRAVITY)
        self.y += self.vy
        self.rect.y = round(self.y)

        self.on_ground = False

        # Landing on platforms
        for platform in platforms:
            if (
                self.vy >= 0
                and previous_bottom <= platform.rect.top + 8
                and self.rect.bottom >= platform.rect.top
                and self.rect.right > platform.rect.left + 5
                and self.rect.left < platform.rect.right - 5
            ):
                self.rect.bottom = platform.rect.top
                self.y = float(self.rect.y)
                self.vy = 0
                self.jumps = 0
                self.on_ground = True

        if self.invincible > 0:
            self.invincible -= 1

    def draw(self, surface, camera):
        if self.invincible > 0 and self.invincible % 8 >= 4:
            return

        x = self.rect.x - camera
        y = self.rect.y

        # Boots
        pygame.draw.rect(surface, (63, 75, 147), (x + 3, y + 27, 10, 9))
        pygame.draw.rect(surface, (63, 75, 147), (x + 17, y + 27, 10, 9))

        # Head
        pygame.draw.rect(surface, (248, 182, 110), (x + 4, y + 4, 20, 20))

        # Shirt
        pygame.draw.rect(surface, PINK, (x + 1, y + 20, 26, 11))

        # Hat
        pygame.draw.rect(surface, (86, 64, 160), (x + 1, y + 1, 26, 8))
        pygame.draw.rect(surface, (86, 64, 160), (x + 5, y - 3, 18, 6))

        # Eyes
        offset = 0 if self.facing == 1 else -5
        pygame.draw.rect(surface, DARK, (x + 12 + offset, y + 12, 3, 4))
        pygame.draw.rect(surface, DARK, (x + 19 + offset, y + 12, 3, 4))

        # Blush
        pygame.draw.rect(surface, (233, 134, 141), (x + 6, y + 18, 5, 3))


# ==========================================
# PLATFORMS
# ==========================================
class Platform:
    def __init__(self, x, y, width, ground=False):
        self.rect = pygame.Rect(x, y, width, 70 if ground else 18)
        self.ground = ground

    def draw(self, surface, camera):
        rect = self.rect.move(-camera, 0)

        if self.ground:
            pygame.draw.rect(surface, (136, 104, 76), rect)
            pygame.draw.rect(
                surface, GREEN,
                (rect.x, rect.y, rect.width, 10)
            )
            for x in range(rect.x + 20, rect.right, 55):
                pygame.draw.rect(
                    surface, (111, 83, 61),
                    (x, rect.y + 30, 13, 5)
                )
        else:
            pygame.draw.rect(surface, (147, 118, 182), rect)
            pygame.draw.rect(
                surface, (213, 182, 250),
                (rect.x, rect.y, rect.width, 10)
            )


# ==========================================
# COINS
# ==========================================
class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.collected = False

    def update(self, player):
        if self.collected:
            return False

        distance = math.hypot(
            player.rect.centerx - self.x,
            player.rect.centery - self.y
        )

        if distance < 27:
            self.collected = True
            return True

        return False

    def draw(self, surface, camera, frame):
        if self.collected:
            return

        x = int(self.x - camera)
        y = int(self.y + math.sin(frame * 0.07 + self.x) * 4)

        pygame.draw.ellipse(surface, (232, 154, 36), (x - 11, y - 13, 22, 26))
        pygame.draw.ellipse(surface, GOLD, (x - 9, y - 12, 16, 22))
        pygame.draw.rect(surface, (255, 243, 164), (x - 2, y - 7, 3, 13))


# ==========================================
# ENEMIES
# ==========================================
class Slime:
    def __init__(self, x, direction=1):
        self.x = float(x)
        self.rect = pygame.Rect(x, 365, 31, 25)
        self.speed = 1.2 * direction
        self.min_x = x - 65
        self.max_x = x + 75
        self.alive = True

    def update(self):
        if not self.alive:
            return

        self.x += self.speed

        if self.x < self.min_x or self.x > self.max_x:
            self.speed *= -1

        self.rect.x = round(self.x)

    def draw(self, surface, camera):
        if not self.alive:
            return

        x = self.rect.x - camera
        y = self.rect.y

        pygame.draw.ellipse(
            surface, (120, 198, 92),
            (x, y, 31, 25)
        )

        pygame.draw.rect(surface, WHITE, (x + 8, y + 10, 5, 7))
        pygame.draw.rect(surface, WHITE, (x + 20, y + 10, 5, 7))

        pygame.draw.rect(surface, DARK, (x + 10, y + 12, 2, 4))
        pygame.draw.rect(surface, DARK, (x + 22, y + 12, 2, 4))


# ==========================================
# PARTICLE EFFECTS
# ==========================================
class Particle:
    def __init__(self, x, y, color):
        self.x = float(x)
        self.y = float(y)
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-4, 1)
        self.life = 25
        self.color = color

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2
        self.life -= 1

    def draw(self, surface, camera):
        if self.life > 0:
            pygame.draw.rect(
                surface,
                self.color,
                (int(self.x - camera), int(self.y), 5, 5)
            )


# ==========================================
# MAIN GAME
# ==========================================
class Game:
    def __init__(self):
        self.level = 0
        self.lives = 3
        self.state = "menu"
        self.frame = 0
        self.camera = 0
        self.load_level(0)
        self.state = "menu"

    def load_level(self, number):
        self.level = number
        data = LEVELS[number]

        self.world_width = data["width"]
        self.player = Player()

        self.platforms = []

        for x, y, width in data["ground"]:
            self.platforms.append(Platform(x, y, width, True))

        for x, y, width in data["floating"]:
            self.platforms.append(Platform(x, y, width))

        self.coins = []

        for x, y, width in data["floating"]:
            self.coins.append(Coin(x + width // 2, y - 28))

        for x, y, width in data["ground"][1:]:
            self.coins.append(Coin(x + width // 2, y - 34))

        self.enemies = []

        for i, x in enumerate(data["enemies"]):
            direction = 1 if i % 2 else -1
            self.enemies.append(Slime(x, direction))

        self.goal = pygame.Rect(self.world_width - 95, 295, 57, 95)

        self.score = 0
        self.camera = 0
        self.particles = []
        self.state = "playing"

    def restart(self):
        self.lives = 3
        self.load_level(0)

    def burst(self, x, y, color, count=10):
        for _ in range(count):
            self.particles.append(Particle(x, y, color))

    def hurt(self):
        player = self.player

        if player.invincible > 0 or self.state != "playing":
            return

        self.lives -= 1
        self.burst(player.rect.centerx, player.rect.centery, PINK, 15)

        if self.lives <= 0:
            self.state = "game_over"
            return

        player.rect.topleft = (55, 310)
        player.x = 55.0
        player.y = 310.0
        player.vx = 0
        player.vy = 0
        player.jumps = 0
        player.invincible = 90
        self.camera = 0

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

        if event.key == pygame.K_r:
            self.restart()
            return

        if self.state == "menu":
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.restart()

        elif self.state == "playing":
            if event.key in (
                pygame.K_SPACE,
                pygame.K_UP,
                pygame.K_w
            ):
                self.player.jump()

        elif self.state == "level_complete":
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.load_level(self.level + 1)

        elif self.state in ("game_over", "victory"):
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.restart()

    def update(self):
        self.frame += 1

        for particle in self.particles:
            particle.update()

        self.particles = [
            p for p in self.particles if p.life > 0
        ]

        if self.state != "playing":
            return

        player = self.player
        previous_bottom = player.rect.bottom

        player.update(self.platforms, self.world_width)

        if player.rect.top > HEIGHT + 90:
            self.hurt()
            return

        # Collect coins
        for coin in self.coins:
            if coin.update(player):
                self.score += 1
                self.burst(coin.x, coin.y, GOLD)

        # Enemy collision
        for enemy in self.enemies:
            if not enemy.alive:
                continue

            enemy.update()

            if player.rect.colliderect(enemy.rect):
                if player.vy > 1 and previous_bottom < enemy.rect.top + 12:
                    enemy.alive = False
                    player.vy = -9
                    player.on_ground = False

                    self.burst(
                        enemy.rect.centerx,
                        enemy.rect.centery,
                        GREEN,
                        12
                    )
                else:
                    self.hurt()
                    if self.state != "playing":
                        return
                    break

        # Finish flag
        if player.rect.colliderect(self.goal):
            if self.level == len(LEVELS) - 1:
                self.state = "victory"
            else:
                self.state = "level_complete"

        # Smooth camera scrolling
        target = max(
            0,
            min(
                self.world_width - WIDTH,
                player.rect.x - 210
            )
        )

        self.camera += (target - self.camera) * 0.12

    def draw_background(self):
        if self.level == 2:
            top_color = (178, 162, 248)
            bottom_color = (244, 184, 214)
        else:
            top_color = (114, 201, 248)
            bottom_color = (220, 246, 255)

        # Sky gradient
        for y in range(HEIGHT):
            t = y / HEIGHT
            color = tuple(
                int(top_color[i] * (1 - t) + bottom_color[i] * t)
                for i in range(3)
            )
            pygame.draw.line(screen, color, (0, y), (WIDTH, y))

        # Parallax clouds
        for i in range(16):
            x = int((i * 227 + 50 - self.camera * 0.18) % 1020 - 110)
            y = 45 + (i * 71) % 180

            pygame.draw.ellipse(screen, (245, 251, 255), (x, y, 90, 28))
            pygame.draw.ellipse(screen, WHITE, (x + 20, y - 12, 55, 35))
            pygame.draw.ellipse(screen, WHITE, (x - 10, y - 8, 50, 34))

        # Distant hills
        hill_color = (161, 216, 192) if self.level != 2 else (161, 139, 200)

        for i in range(20):
            x = int(i * 180 - self.camera * 0.38)
            pygame.draw.ellipse(
                screen,
                hill_color,
                (x - 120, 285 + (i % 3) * 15, 290, 210)
            )

    def draw_goal(self):
        x = int(self.goal.x - self.camera)
        y = self.goal.y

        pygame.draw.rect(screen, (113, 92, 108), (x, y, 5, 95))

        pygame.draw.polygon(
            screen,
            PINK,
            [(x + 5, y), (x + 57, y + 17), (x + 5, y + 35)]
        )

    def draw_hud(self):
        # Top HUD panel
        panel = pygame.Surface((WIDTH, 46), pygame.SRCALPHA)
        panel.fill((20, 35, 60, 150))
        screen.blit(panel, (0, 0))

        level_text = SMALL_FONT.render(
            f"Level {self.level + 1} / {len(LEVELS)}",
            True, WHITE
        )
        coin_text = SMALL_FONT.render(
            f"Coins: {self.score} / {len(self.coins)}",
            True, GOLD
        )
        lives_text = SMALL_FONT.render(
            f"Lives: {self.lives}",
            True, (255, 140, 165)
        )

        screen.blit(level_text, (18, 14))
        screen.blit(coin_text, (280, 14))
        screen.blit(lives_text, (620, 14))

    def draw_overlay(self, title, subtitle, action):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((15, 23, 42, 190))
        screen.blit(overlay, (0, 0))

        title_surface = BIG_FONT.render(title, True, WHITE)
        subtitle_surface = FONT.render(subtitle, True, WHITE)
        action_surface = SMALL_FONT.render(action, True, GOLD)

        screen.blit(
            title_surface,
            title_surface.get_rect(center=(WIDTH // 2, 155))
        )
        screen.blit(
            subtitle_surface,
            subtitle_surface.get_rect(center=(WIDTH // 2, 225))
        )
        screen.blit(
            action_surface,
            action_surface.get_rect(center=(WIDTH // 2, 290))
        )

    def draw(self):
        self.draw_background()

        for platform in self.platforms:
            platform.draw(screen, self.camera)

        for coin in self.coins:
            coin.draw(screen, self.camera, self.frame)

        for enemy in self.enemies:
            enemy.draw(screen, self.camera)

        self.draw_goal()
        self.player.draw(screen, self.camera)

        for particle in self.particles:
            particle.draw(screen, self.camera)

        self.draw_hud()

        if self.state == "menu":
            self.draw_overlay(
                "Skybound Adventure",
                "Collect coins, dodge slimes, reach the flag!",
                "Press ENTER to Start"
            )

        elif self.state == "level_complete":
            self.draw_overlay(
                "Level Complete!",
                "Great job! Ready for the next challenge?",
                "Press ENTER for Next Level"
            )

        elif self.state == "game_over":
            self.draw_overlay(
                "Game Over!",
                "You ran out of lives!",
                "Press ENTER to Try Again"
            )

        elif self.state == "victory":
            self.draw_overlay(
                "YOU WIN!",
                f"All 3 levels completed! Final level coins: {self.score}",
                "Press ENTER to Play Again"
            )

        pygame.display.flip()


# ==========================================
# MAIN GAME LOOP
# ==========================================
def main():
    game = Game()

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            game.handle_event(event)

        game.update()
        game.draw()


if __name__ == "__main__":
    main()
