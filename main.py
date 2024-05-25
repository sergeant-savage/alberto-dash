import pygame
import pygame.locals as pyg
from random import randint
from entities import Player, EnemyEasy, EnemyMedium, Bullet

pygame.init()

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1050

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

running = True

ADDENEMY = pygame.USEREVENT + 1

pygame.time.set_timer(ADDENEMY, 750)


enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

all = pygame.sprite.Group()

clock = pygame.time.Clock()

player = Player()
all.add(player)
shooting = False
reload = 0

while running:
    for event in pygame.event.get():
        print(event)
        if event.type == pyg.QUIT:
            running = False
        elif event.type == ADDENEMY:
            if randint(0, 1) == 0:
                new_enemy = EnemyEasy(player.rect.centerx, player.rect.centery)
            else:
                new_enemy = EnemyMedium()

            enemies.add(new_enemy)
            all.add(new_enemy)
        elif event.type == pyg.MOUSEBUTTONDOWN:
            if event.button == 1:
                shooting = True
        elif event.type ==pyg.MOUSEBUTTONUP:
            if event.button == 1:
                shooting = False

    screen.fill((135, 206, 250))
    pressed_keys = pygame.key.get_pressed()

    player.update(pressed_keys)
    bullets.update()
    for enemy in enemies:
        if pygame.sprite.spritecollideany(enemy, bullets):
            enemy.kill()
        if enemy.kind == 1:
            enemy.update()
        elif enemy.kind == 2:
            enemy.update(player.rect.centerx, player.rect.centery)

    if shooting == True:
        if reload == 0:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            new_bullet = Bullet(player.rect.center, mouse_x, mouse_y)
            bullets.add(new_bullet)
            reload = 5
    
    if reload != 0:
        reload -= 1
        

    for bullet in bullets:
        screen.blit(bullet.surf, bullet.rect)

    for sprite in all:
        screen.blit(sprite.surf, sprite.rect)

    if pygame.sprite.spritecollideany(player, enemies):
        running = False


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
