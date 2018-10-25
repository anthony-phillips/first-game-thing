import json
import pygame
from game_object import direction, player, projectile

clock = pygame.time.Clock()
win = pygame.display.set_mode((852, 480))
pygame.display.set_caption("Doodily Doo")

with open('settings.json') as f:
    settings = json.load(f)

FRICTION = settings['physics']['friction']
GRAVITY = settings['physics']['gravity']
TERM_VEL = settings['physics']['term_vel']

p1 = player((0, win.get_height()-64), 64, 64)
p1.jump_vel = -20
p1.walk_right = [pygame.image.load('sprites\R{}.png'.format(i)) for i in range(1, 10)]
p1.walk_left = [pygame.image.load('sprites\L{}.png'.format(i)) for i in range(1, 10)]
p1.facing = direction.RIGHT
p1.sprite = p1.walk_right[0]
p1.move_map = settings['p1']['move_map']
p1.settings = settings['p1']['settings']

p2 = player((win.get_width()-64, win.get_height()-64), 64, 64)
p2.jump_vel = -25
p2.walk_right = [pygame.image.load('sprites\R{}E.png'.format(i)) for i in range(1, 12)]
p2.walk_left = [pygame.image.load('sprites\L{}E.png'.format(i)) for i in range(1, 12)]
p2.facing = direction.LEFT
p2.sprite = p2.walk_left[0]
p2.move_map = settings['p2']['move_map']
p2.settings = settings['p2']['settings']

print(p1.move_map)
print(p2.move_map)

bg = pygame.image.load('sprites\\bg.jpg')

players = [p1, p2]
projectiles = []
def redraw_frame():
    win.fill((0,0,0))
    win.blit(bg, (0, 0))
    for p in players:
        p.draw(win)
    for p in projectiles:
        p.draw(win)
    pygame.display.update()

def player_update(play, keys):
    # Horizontal movement
    play.is_run = keys[play.move_map['run']]
    if keys[play.move_map['left']]:    # If left
        play.facing = direction.LEFT
        play.x_vel = -5 if play.is_run else -3
        play.update_sequence(play.walk_left)
    elif keys[play.move_map['right']]:  # If right
        play.facing = direction.RIGHT
        play.x_vel = 5 if play.is_run else 3
        play.update_sequence(play.walk_right)
    elif not play.is_falling and play.x_vel != 0:   # Friction on the ground
        magnitude = abs(play.x_vel)               # Get the magnitude of the velocity
        play.x_vel = max(0, magnitude - FRICTION) # Subtract friction
        play.x_vel *= play.facing
        if play.x_vel == 0:
            if play.facing == 1:
                play.sprite = play.walk_right[0]
            else:
                play.sprite = play.walk_left[0]

    # Vertical movement
    if keys[play.move_map['jump']] and not play.is_falling:
        if play.settings['spam_jump'] or not play.jump_pressed:
            play.jump_pressed = True
            play.jump()
    elif play.is_falling:
        ground = win.get_height() - play.height
        play.y_vel = min(TERM_VEL, play.y_vel + GRAVITY) # Terminal velocity
        play.is_falling = play.y != ground
    else:
        play.jump_pressed = bool(keys[pygame.K_w])

    play.update_pos()
    if play.is_out_window(win):
        play.fit_in_window(win)

    if keys[play.move_map['fire']]:
        if play.settings['spam_fire'] or not play.fire_pressed:
            play.fire_pressed = True
            proj = projectile(play.center(), 3)
            proj.x_vel = 20 * play.facing
            projectiles.append(proj)
    else:
        play.fire_pressed = False

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    
    for p in players:
        player_update(p, keys)
    
    for p in projectiles:
        p.update_pos()
        if p.is_out_window(win):
            projectiles.remove(p)

    redraw_frame()
    clock.tick(60)

pygame.quit()