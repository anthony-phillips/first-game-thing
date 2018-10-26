import pygame

class game_object:
    x = 0
    y = 0

    x_vel = 0
    y_vel = 0

    width = 0
    height = 0

    hit_x_offset = 0
    hit_y_offset = 0
    hit_width = 0
    hit_height = 0
    
    def get_hitbox(self):
        return (self.x + self.hit_x_offset, self.y + self.hit_y_offset, self.hit_width, self.hit_height)

    def __init__(self, pos, width, height):
        self.x = pos[0]
        self.y = pos[1]
        self.width = width
        self.height = height
    
    def hit_center(self):
        return (self.hit_left() + self.hit_width//2, self.hit_top() + self.height//2)
    
    def hit_top(self):
        return self.y + self.hit_y_offset
    
    def hit_bottom(self):
        return self.hit_top() + self.hit_height
    
    def hit_left(self):
        return self.x + self.hit_x_offset
    
    def hit_right(self):
        return self.hit_left() + self.hit_width

    def update_pos(self):
        self.x += self.x_vel
        self.y += self.y_vel
    
    def is_out_window(self, window):
        left = 0 - self.hit_x_offset
        right = window.get_width() - self.hit_x_offset - self.hit_width
        top = 0 - self.hit_y_offset
        bottom = window.get_height() - self.hit_y_offset - self.hit_height
        return not left < self.x < right or not top < self.y < bottom

    def fit_in_window(self, window):
        left = 0 - self.hit_x_offset
        right = window.get_width() - self.hit_x_offset - self.hit_width
        top = 0 - self.hit_y_offset
        bottom = window.get_height() - self.hit_y_offset - self.hit_height
        self.x = min(right, max(self.x, left))
        self.y = min(bottom, max(self.y, top))

    def contains(self, obj):
        return self.hit_left() <= obj.x <= self.hit_right() and self.hit_top() <= obj.y <= self.hit_bottom()

class direction:
    LEFT = -1
    RIGHT = 1

class player(game_object):
    is_run = 0
    is_falling = 0

    projectile_color = (0, 0, 0)
    projectile_hit_sounds = None
    jump_sound = None
    land_sound = None
    attack_sounds = None
    wound_sounds = None
    death_sounds = None

    facing = 1
    walk_right = None
    walk_left = None

    move_sequence = None
    sequence_counter = 0
    sequence_rate = 1
    sprite = None

    move_map = None
    settings = None

    jump_vel = 0
    walk_speed = 0
    run_speed = 0

    health = 1
    damage = 0

    def __init__(self, pos, width, height):
        return super().__init__(pos, width, height)

    def jump(self):
        self.y_vel = self.jump_vel
        self.y += self.y_vel
        self.is_falling = True
        #self.jump_sound.play()

    def update_sequence(self, move_sequence):
        if self.move_sequence != move_sequence:
            self.move_sequence = move_sequence
            self.sequence_counter = 0
        self.sequence_counter += 1
        if self.sequence_counter > len(move_sequence)-1:
            self.sequence_counter = 0
        self.sprite = move_sequence[self.sequence_counter//self.sequence_rate]

    def draw(self, window):
        window.blit(self.sprite, (self.x, self.y))

class projectile(game_object):

    radius = 0
    color = (0, 0, 0)

    damage = 0
    hit_sound = None

    owner = None

    def __init__(self, pos, radius):
        self.radius = radius
        return super().__init__(pos, radius, radius)

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)