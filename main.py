import pygame
import math
import pygame.locals as pyg
from random import randint

pygame.init()

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1050

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

running = True

ADDENEMY = pygame.USEREVENT + 1

pygame.time.set_timer(ADDENEMY, 500)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()

        self.surf = pygame.image.load("./alberto.jpg")
        self.rect = self.surf.get_rect(center=(575, 425))

    def update(self, pressed_keys):
        if pressed_keys[pyg.K_UP] or pressed_keys[pyg.K_w]:
            self.rect.move_ip(0, -10)
        if pressed_keys[pyg.K_DOWN] or pressed_keys[pyg.K_s]:
            self.rect.move_ip(0, 10)

        if pressed_keys[pyg.K_LEFT] or pressed_keys[pyg.K_a]:
            self.rect.move_ip(-10, 0)

        if pressed_keys[pyg.K_RIGHT] or pressed_keys[pyg.K_d]:
            self.rect.move_ip(10, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        if self.rect.top <= 0:
            self.rect.top = 0

        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Enemy(pygame.sprite.Sprite):
    def __init__(self, player_x, player_y):
        super(Enemy, self).__init__()
        # self.surf = pygame.Surface((75, 75))
        self.surf = pygame.image.load("nathan.jpg").convert()
        enemy_x, enemy_y = randint(0, SCREEN_WIDTH), randint(50, 150)
        self.rect = self.surf.get_rect(
            center=(enemy_x, enemy_y)
        )
        self.accel = randint(1, 10)*0.1

        o, a = (player_x-enemy_x, player_y-enemy_y)

        self.angle = math.atan(o/a)  # * (180/math.pi)
        self.speed = randint(5, 10)
        print(self.angle*180/math.pi)
        self.y_vel = (math.cos(self.angle) * self.speed)
        self.x_vel = (math.sin(self.angle) * self.speed)

    def update(self):
        self.rect.move_ip(self.x_vel, self.y_vel)
        if self.rect.bottom > SCREEN_HEIGHT or self.rect.right > SCREEN_WIDTH or self.rect.left < 0:
            self.kill()
        if self.speed < 30:
            self.speed += self.accel
            self.y_vel = (math.cos(self.angle) * (self.speed))
            self.x_vel = (math.sin(self.angle) * (self.speed))


enemies = pygame.sprite.Group()

all = pygame.sprite.Group()

clock = pygame.time.Clock()

player = Player()
all.add(player)

while running:
    for event in pygame.event.get():
        print(event)
        if event.type == pyg.QUIT:
            running = False
        elif event.type == ADDENEMY:
            new_enemy = Enemy(player.rect.centerx, player.rect.centery)
            enemies.add(new_enemy)
            all.add(new_enemy)

    screen.fill((135, 206, 250))
    pressed_keys = pygame.key.get_pressed()

    player.update(pressed_keys)
    enemies.update()

    for sprite in all:
        screen.blit(sprite.surf, sprite.rect)

    if pygame.sprite.spritecollideany(player, enemies):
        running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
