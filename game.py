import json
import pygame
from game_object import direction, player, projectile

with open('settings.json') as f:
    settings = json.load(f)

pygame.init()
clock = pygame.time.Clock()
win = pygame.display.set_mode((852, 480))
pygame.display.set_caption("Doodily Doo")

FRICTION = settings['physics']['friction']
GRAVITY = settings['physics']['gravity']
TERM_VEL = settings['physics']['term_vel']

p1 = player((0, win.get_height()-64), 64, 64)
p1.health = 100
p1.jump_vel = -20
p1.walk_speed = 3
p1.run_speed = 5
p1.walk_right = [pygame.image.load('sprites\R{}.png'.format(i)) for i in range(1, 10)]
p1.walk_left = [pygame.image.load('sprites\L{}.png'.format(i)) for i in range(1, 10)]
p1.facing = direction.RIGHT
p1.sprite = p1.walk_right[0]
p1.projectile_color = (0, 0, 255)
p1.hit_x_offset = 20
p1.hit_width = 26
p1.hit_y_offset = 15
p1.hit_height = 48
p1.move_map = settings['p1']['move_map']
p1.settings = settings['p1']['settings']

p2 = player((win.get_width()-64, win.get_height()-64), 64, 64)
p2.health = 85
p2.jump_vel = -25
p2.walk_speed = 4
p2.run_speed = 6
p2.walk_right = [pygame.image.load('sprites\R{}E.png'.format(i)) for i in range(1, 12)]
p2.walk_left = [pygame.image.load('sprites\L{}E.png'.format(i)) for i in range(1, 12)]
p2.facing = direction.LEFT
p2.sprite = p2.walk_left[0]
p2.projectile_color = (255, 0, 0)
p2.hit_x_offset = 18
p2.hit_width = 25
p2.hit_y_offset = 10
p2.hit_height = 48
p2.move_map = settings['p2']['move_map']
p2.settings = settings['p2']['settings']

bg = pygame.image.load('sprites\\bg.jpg')

players = [p1, p2]
projectiles = []
print(pygame.font.get_fonts())
font = pygame.font.SysFont('arial', 30, True)
def redraw_frame():
    win.fill((0,0,0))
    win.blit(bg, (0, 0))
    human_health = font.render('Human: {}'.format(p1.health), 1, (0,0,255))
    orc_health = font.render('Orc: {}'.format(p2.health), 1, (255,0,0))
    win.blit(human_health, (0, 0))
    win.blit(orc_health, (0, 50))
    for play in players:
        play.draw(win)
    for proj in projectiles:
        proj.draw(win)
    pygame.display.update()
    
def player_update(play, keys):
    # Horizontal movement
    play.is_run = keys[play.move_map['run']]
    if keys[play.move_map['left']]:    # If left
        play.facing = direction.LEFT
        if play.is_run:
            play.x_vel = play.run_speed * -1
            play.sequence_rate = 2
        else:
            play.x_vel = play.walk_speed * -1
            play.sequence_rate = 3
        play.update_sequence(play.walk_left)
    elif keys[play.move_map['right']]:  # If right
        play.facing = direction.RIGHT
        if play.is_run:
            play.x_vel = play.run_speed
            play.sequence_rate = 2
        else:
            play.x_vel = play.walk_speed
            play.sequence_rate = 3
        play.update_sequence(play.walk_right)
    elif not play.is_falling and play.x_vel != 0: # Friction on the ground
        magnitude = abs(play.x_vel)               # Get the magnitude of the velocity
        play.x_vel = max(0, magnitude - FRICTION) # Subtract friction
        play.x_vel *= play.facing
        if play.x_vel == 0:
            if play.facing == 1:
                play.sprite = play.walk_right[0]
            else:
                play.sprite = play.walk_left[0]

    # Vertical movement
    play.is_falling = play.hit_bottom() < win.get_height()
    if (keys[play.move_map['jump']] and not play.is_falling) and (play.settings['spam_jump'] or not play.jump_pressed):
        play.jump_pressed = True
        play.jump()
    elif play.is_falling:
        play.y_vel = min(TERM_VEL, play.y_vel + GRAVITY) # Terminal velocity
    else:
        play.jump_pressed = bool(keys[pygame.K_w])

    # Fire
    if keys[play.move_map['fire']]:
        if play.settings['spam_fire'] or not play.fire_pressed:
            play.fire_pressed = True
            proj = projectile(play.hit_center(), 3)
            proj.color = play.projectile_color
            proj.owner = play
            proj.x_vel = 20 * play.facing
            projectiles.append(proj)
    else:
        play.fire_pressed = False

    play.update_pos()
    play.fit_in_window(win)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Process player moves
    keys = pygame.key.get_pressed()
    for play in players:
        player_update(play, keys)

    # Update projectile positions and process hits
    for proj in projectiles:
        proj.update_pos()
        if proj.is_out_window(win):
            projectiles.remove(proj)
            continue
        for play in players:
            if proj.owner is not play and play.contains(proj):
                play.x += proj.x_vel
                play.fit_in_window(win)
                play.health -= proj.damage
                print('{} hit {}'.format(id(proj.owner), id(play)))
                projectiles.remove(proj)

    redraw_frame()
    clock.tick(30)

pygame.quit()