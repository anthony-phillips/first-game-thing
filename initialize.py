import pygame
import json
from game_object import direction, player, projectile

with open('settings.json') as f:
    settings = json.load(f)

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
win = pygame.display.set_mode((852, 480))
pygame.display.set_caption("Doodily Doo")

FRICTION = settings['physics']['friction']
GRAVITY = settings['physics']['gravity']
TERM_VEL = settings['physics']['term_vel']

BACKGROUND_IMG = pygame.image.load('sprites\\new_bg.jpg')
font = pygame.font.SysFont('arial', 30, True)

p1 = player((0, win.get_height()-64), 64, 64)
p1.health = 100
p1.damage = 14
p1.jump_vel = -20
p1.walk_speed = 3
p1.run_speed = 5
p1.walk_right = [pygame.image.load('sprites\R{}.png'.format(i)) for i in range(1, 10)]
p1.walk_left = [pygame.image.load('sprites\L{}.png'.format(i)) for i in range(1, 10)]
p1.facing = direction.RIGHT
p1.sprite = p1.walk_right[0]
p1.projectile_color = (0, 0, 255)
p1.projectile_hit_sounds = [
    pygame.mixer.Sound('sounds\ArrowHitA.wav'),
    pygame.mixer.Sound('sounds\ArrowHitA.wav'),
    pygame.mixer.Sound('sounds\ArrowHitB.wav')
]
p1.attack_sounds = [
    pygame.mixer.Sound('sounds\BowRelease.wav'),
    pygame.mixer.Sound('sounds\BowRelease02.wav'),
    pygame.mixer.Sound('sounds\BowRelease03.wav')
]
p1.wound_sounds = [
    pygame.mixer.Sound('sounds\DwarfMaleWoundA.wav'),
    pygame.mixer.Sound('sounds\DwarfMaleWoundB.wav'),
    pygame.mixer.Sound('sounds\DwarfMaleWoundC.wav')
]
p1.jump_sounds = [pygame.mixer.Sound('sounds\DwarfMaleMainJump.wav')]
p1.land_sounds = [pygame.mixer.Sound('sounds\DwarfMaleMainLand.wav')]
p1.death_sounds = [pygame.mixer.Sound('sounds\DwarfMaleDeathA.wav')]
p1.victory_sounds = [
    pygame.mixer.Sound('sounds\DwarfMaleCheer02.wav'),
    pygame.mixer.Sound('sounds\DwarfMaleCheer03.wav')
]
p1.hit_x_offset = 20
p1.hit_width = 26
p1.hit_y_offset = 15
p1.hit_height = 48
p1.move_map = settings['p1']['move_map']
p1.settings = settings['p1']['settings']

p2 = player((win.get_width()-64, win.get_height()-64), 64, 64)
p2.health = 85
p2.damage = 12
p2.jump_vel = -25
p2.walk_speed = 4
p2.run_speed = 6
p2.walk_right = [pygame.image.load('sprites\R{}E.png'.format(i)) for i in range(1, 12)]
p2.walk_left = [pygame.image.load('sprites\L{}E.png'.format(i)) for i in range(1, 12)]
p2.facing = direction.LEFT
p2.sprite = p2.walk_left[0]
p2.projectile_color = (255, 0, 0)
p2.projectile_hit_sounds = [
    pygame.mixer.Sound('sounds\ArrowHitA.wav'),
    pygame.mixer.Sound('sounds\ArrowHitA.wav'),
    pygame.mixer.Sound('sounds\ArrowHitB.wav')
]
p2.attack_sounds = [
    pygame.mixer.Sound('sounds\BowRelease.wav'),
    pygame.mixer.Sound('sounds\BowRelease02.wav'),
    pygame.mixer.Sound('sounds\BowRelease03.wav')
]
p2.wound_sounds = [
    pygame.mixer.Sound('sounds\OrcMaleWoundA.wav'),
    pygame.mixer.Sound('sounds\OrcMaleWoundB.wav'),
    pygame.mixer.Sound('sounds\OrcMaleWoundC.wav')
]
p2.jump_sounds = [pygame.mixer.Sound('sounds\OrcMaleMainJump.wav')]
p2.land_sounds = [pygame.mixer.Sound('sounds\OrcMaleMainLand.wav')]
p2.death_sounds = [pygame.mixer.Sound('sounds\OrcMaleDeath.wav')]
p2.victory_sounds = [
    pygame.mixer.Sound('sounds\OrcMaleCheer01.wav'),
    pygame.mixer.Sound('sounds\OrcMaleCheer02.wav')
]
p2.hit_x_offset = 18
p2.hit_width = 25
p2.hit_y_offset = 10
p2.hit_height = 48
p2.move_map = settings['p2']['move_map']
p2.settings = settings['p2']['settings']

pygame.mixer.music.load('sounds\\battle05.ogg')
pygame.mixer.music.load('sounds\\battle06.ogg')

players = [p1, p2]
projectiles = []