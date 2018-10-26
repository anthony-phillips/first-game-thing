import pygame
from initialize import *
from game_object import direction, player, projectile
import random

def redraw_frame():
    win.fill((0,0,0))
    win.blit(BACKGROUND_IMG, (0, 0))
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
    if play.is_falling and play.hit_bottom() == win.get_height():
        play.land_sound.play()
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
            proj.damage = play.damage
            proj.color = play.projectile_color
            random.choice(play.attack_sounds).play()
            proj.hit_sound = random.choice(play.projectile_hit_sounds)
            proj.owner = play
            proj.x_vel = 20 * play.facing
            projectiles.append(proj)
    else:
        play.fire_pressed = False

    play.update_pos()
    play.fit_in_window(win)

pygame.mixer.music.play(-1)
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
                play.health = max(play.health - proj.damage, 0)
                proj.hit_sound.play()
                random.choice(play.wound_sounds).play()
                if play.health == 0:
                    random.choice(play.death_sounds).play()
                    players.remove(play)
                print('{} hit {}'.format(id(proj.owner), id(play)))
                projectiles.remove(proj)

    redraw_frame()
    clock.tick(30)

pygame.quit()