import random

class Cowboy:

    def __init__(self, x, y, hit_status, base_sprite, hit_sprite, spawn_time):
        """
        Constructor.
        param x: A cowboys x position
        param y: A cowboys y position
        param hit_status: Has the cowboy been shot yet?
        param base_sprite: The sprite of a healthy cowboy.
        param hit_sprite:  The sprite of a shot cowboy.
        param spawn_time: When the cowboy spawns in.
        """
        self.x = x
        self.y = y
        self.hit_status = hit_status
        self.base_sprite = base_sprite
        self.hit_sprite = hit_sprite
        self.spawn_time = spawn_time


    def cycle_move_up(self, x, time_left, start_time, pause_time, window):
        """
        The cowboy will move upwards to be shot.
        :param x: The cowboys xcord position
        :param time_left: 60 -> 0, global timer
        :param start_time: When the upwards movemebt starts.
        :param pause_time: when the movement stops
        :param window: the blitting window
        """
        if time_left <= start_time and time_left > pause_time:
            self.x = x
            self.y -= 1
            window.blit(self.base_sprite, (self.x, self.y))
        else:
            self.x = x
            self.y = self.y
            window.blit(self.base_sprite, (self.x, self.y))

    def cycle_move_down(self, x, time_left, start_time, pause_time, window):
        """
        The cowboy will move upwards to be shot.
        :param x: The cowboys xcord position
        :param time_left: 60 -> 0, global timer
        :param start_time: When the downwards movemebt starts.
        :param pause_time: when the movement stops
        :param window: the blitting window
        """
        if time_left <= start_time and time_left > pause_time:
            self.x = x
            self.y += 1
            window.blit(self.base_sprite, (self.x, self.y))
        else:
            self.x = x
            self.y = self.y
            window.blit(self.base_sprite, (self.x, self.y))

    def get_shot(self):
        """
        reflects the hit status and sprite to a shot cowboy
        """
        if not self.hit_status:
            self.base_sprite,self.hit_sprite = self.hit_sprite,self.base_sprite
        self.hit_status = True

    def spawn(self, window):
        """
        Spawns the cowboy.
        :param window: blitting window
        """
        window.blit(self.base_sprite, (self.x, self.y))

