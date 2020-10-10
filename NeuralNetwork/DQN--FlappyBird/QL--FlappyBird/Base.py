class Base:
    def __init__(self, img, pos_x, pos_y,shift):
        self.img = img
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = img.get_width()
        self.height = img.get_height()
        self.shift = shift
