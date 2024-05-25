import pygame
import pygame.locals as pyg
import math
from random import randint

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1050


class Enemy(pygame.sprite.Sprite):
    def __init__(self, surf):
        super(Enemy, self).__init__()
        self.kind = 0
        # self.surf = pygame.Surface((75, 75))
        self.surf = surf
        enemy_x, enemy_y = randint(0, SCREEN_WIDTH), randint(50, 150)
        self.rect = self.surf.get_rect(center=(enemy_x, enemy_y))

    def set_kind(self, kind):
        self.kind = kind


class EnemyEasy(Enemy):
    def __init__(self, player_x, player_y):
        super().__init__(pygame.image.load("nathan.jpg").convert())
        self.set_kind(1)
        # self.surf = pygame.Surface((75, 75))
        self.accel = randint(1, 20) * 0.1

        o, a = (player_x - self.rect.x, player_y - self.rect.y)

        self.angle = math.atan2(o, a)  # * (180/math.pi)
        self.speed = randint(5, 10)
        self.y_vel = math.cos(self.angle) * self.speed
        self.x_vel = math.sin(self.angle) * self.speed

    def update(self):
        self.rect.move_ip(self.x_vel, self.y_vel)
        if (
            self.rect.bottom > SCREEN_HEIGHT
            or self.rect.right > SCREEN_WIDTH
            or self.rect.left < 0
        ):
            self.kill()
        if self.speed < 30:
            self.speed += self.accel
            self.y_vel = math.cos(self.angle) * (self.speed)
            self.x_vel = math.sin(self.angle) * (self.speed)


# Set up an overarching enemy parent class please
class EnemyMedium(Enemy):
    def __init__(self):
        super().__init__(pygame.image.load("elijah.jpeg").convert())
        self.set_kind(2)
        # not hard coded for sanity's sake
        self.angle = 0
        self.y_vel = 0
        self.x_vel = 0
        self.speed = 8
        self.frames = 150

    def update(self, player_x, player_y):
        if self.frames == 0:
            self.kill()
            return

        o, a = (player_x - self.rect.x, player_y - self.rect.y)

        self.angle = math.atan2(o, a)  # * (180/math.pi)
        self.y_vel = math.cos(self.angle) * self.speed
        self.x_vel = math.sin(self.angle) * self.speed
        self.frames -= 1

        self.rect.move_ip(self.x_vel, self.y_vel)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.kind = 0

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

class Bullet(pygame.sprite.Sprite):
    def __init__(self, player_location, mouse_x, mouse_y):
        super(Bullet,self).__init__()
        self.surf = pygame.Surface((25,25))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect(center=(player_location[0], player_location[1]))
        o, a = (mouse_x - self.rect.x, mouse_y - self.rect.y)
        self.angle = math.atan2(o, a)  # * (180/math.pi)
        self.speed = 15
        self.y_vel = math.cos(self.angle) * self.speed
        self.x_vel = math.sin(self.angle) * self.speed

    def update(self):
        self.rect.move_ip(self.x_vel, self.y_vel)

        if (
            self.rect.bottom > SCREEN_HEIGHT
            or self.rect.right > SCREEN_WIDTH
            or self.rect.left < 0
            or self.rect.top < 0
        ):
            self.kill()
