import pygame

class game_object:
    x = 0
    y = 0

    x_vel = 0
    y_vel = 0

    width = 0
    height = 0

    def __init__(self, pos, width, height):
        self.x = pos[0]
        self.y = pos[1]
        self.width = width
        self.height = height
    
    def center(self):
        return (self.x + self.width//2, self.y + self.height//2)
    
    def update_pos(self):
        self.x += self.x_vel
        self.y += self.y_vel
    
    def is_out_window(self, window):
        right = window.get_width() - self.width
        bottom = window.get_height() - self.height
        return not 0 < self.x < right or not 0 < self.y < bottom

    def fit_in_window(self, window):
        right = window.get_width() - self.width
        bottom = window.get_height() - self.height
        self.x = min(right, max(self.x, 0))
        self.y = min(bottom, max(self.y, 0))

    def update_vel(self, external_forces):
        pass

class direction:
    LEFT = -1
    RIGHT = 1

class player(game_object):
    is_run = 0
    is_falling = 0

    facing = 1
    walk_right = None
    walk_left = None

    move_sequence = None
    sequence_counter = 0
    sprite = None

    move_map = None
    settings = None

    jump_vel = 0

    def __init__(self, pos, width, height):
        return super().__init__(pos, width, height)

    def jump(self):
        self.y_vel = self.jump_vel
        self.y += self.y_vel
        self.is_falling = True

    def update_sequence(self, move_sequence):
        if self.move_sequence != move_sequence:
            self.move_sequence = move_sequence
            self.sequence_counter = 0

        self.sequence_counter += 1
        if self.sequence_counter > len(move_sequence)-1:
            self.sequence_counter = 0

        self.sprite = move_sequence[self.sequence_counter]

    def draw(self, window):
        window.blit(self.sprite, (self.x, self.y))

class projectile(game_object):

    radius = 0
    color = (0, 0, 0)

    def __init__(self, pos, radius):
        self.radius = radius
        return super().__init__(pos, radius, radius)

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)