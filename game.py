import json
import pygame
from game_object import player, projectile

win = pygame.display.set_mode((852, 480))
pygame.display.set_caption("Doodily Doo")

with open('settings.json') as f:
    settings = json.load(f)

FRICTION = settings['physics']['friction']
GRAVITY = settings['physics']['gravity']
TERM_VEL = settings['physics']['term_vel']

p1 = player(0, win.get_height()-64, 64, 64)
p1.jump_height = 30
p1.jump_duration = 10
p1.jump_vel = -20
p1.walk_right = [pygame.image.load('sprites\R{}.png'.format(i)) for i in range(1, 10)]
p1.walk_left = [pygame.image.load('sprites\L{}.png'.format(i)) for i in range(1, 10)]
p1.facing = 1
p1.sprite = p1.walk_right[0]

bg = pygame.image.load('sprites\\bg.jpg')

projectiles = []
def redraw_frame():
    win.blit(bg, (0, 0))
    p1.draw(win)
    for projectile in projectiles:
        projectile.draw(win)
    pygame.display.update()


clock = pygame.time.Clock()
run = True
fire_pressed = False
jump_pressed = False
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    ground = win.get_height() - p1.height
    right_bound = win.get_width() - p1.width

    # Horizontal movement
    p1.is_run = pygame.key.get_mods() & pygame.KMOD_SHIFT
    if keys[pygame.K_a]:    # If left
        p1.facing = -1
        p1.x_vel = -5 if p1.is_run else -3
        p1.update_sequence(p1.walk_left)
    elif keys[pygame.K_d]:  # If right
        p1.facing = 1
        p1.x_vel = 5 if p1.is_run else 3
        p1.update_sequence(p1.walk_right)
    elif not p1.is_falling and p1.x_vel != 0:   # Friction on the ground
        magnitude = abs(p1.x_vel)               # Get the magnitude of the velocity
        p1.x_vel = max(0, magnitude - FRICTION) # Subtract friction
        p1.x_vel *= p1.facing
        if p1.x_vel == 0:
            if p1.facing == 1:
                p1.sprite = p1.walk_right[0]
            else:
                p1.sprite = p1.walk_left[0]

    p1.x += p1.x_vel
    if p1.x > right_bound:
        p1.x = right_bound
    elif p1.x < 0:
        p1.x = 0

    # Vertical movement
    if keys[pygame.K_w] and not p1.is_falling:
        if settings['controls']['spam_jump'] or not jump_pressed:
            jump_pressed = True
            p1.jump()
    elif p1.is_falling:
            p1.y_vel = min(TERM_VEL, p1.y_vel + GRAVITY) # Terminal velocity
            p1.y = min( p1.y + p1.y_vel, ground) # Update y position
            p1.is_falling = p1.y != ground
    jump_pressed = bool(keys[pygame.K_w])

    win.fill((0,0,0))

    if keys[pygame.K_SPACE]:
        if settings['controls']['spam_fire'] or not fire_pressed:
            fire_pressed = True
            p1x, p1y = p1.center()
            p = projectile(p1x, p1y, 3)
            p.x_vel = 20 * p1.facing
            projectiles.append(p)
    else:
        fire_pressed = False
    
    for p in projectiles:
        p.x += p.x_vel
        p.radius += 1
        p.color = tuple([min(255, c + 10) for c in p.color])
        if p.x > right_bound or p.x < 0:
            projectiles.remove(p)

    redraw_frame()
    clock.tick(60)

pygame.quit()