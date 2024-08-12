"""
Models a high-velocity can of Heinz Beans
"""

class Can:

    def __init__(self,x,y,sp1,sp2,sp3,sp4,list_order):
        """
        Constructor.
        :param x: Cans x_position.
        :param y: Cans y_position.
        :param sp1: Sprite1 (all of these are just the same sprite rotated 90 degrees lmao)
        :param sp2: Sprite2
        :param sp3: Sprite3
        :param sp4: Sprite4
        :param list_order: The order of sprites to cycle through.
        """
        self.x = x
        self.y = y,
        self.png_list = [sp1,sp2,sp3,sp4]
        self.list_order = list_order


    def respawn(self):
        """
        Resets the position of the can for takeoff.
        """
        self.x = -100

    def fly(self, y, frame_counter, window):
        """
        Launches the can eastward at a high speed.
        :param y: The cans randomized height.
        :param frame_counter: The internal frame counter (up to 3600)
        :param window: Thye blitting window.
        """
        self.x += 25
        self.y = y
        window.blit(self.png_list[self.list_order], (self.x, self.y))
        if frame_counter % 10 == 0:
            self.list_order += 1
            if self.list_order == 4:
                self.list_order = 0