class Bird:
    birdIndex = 0
    birdFlapped = False
    BIRD_ACC_Y = 1
    bird_vel_y = 1
    BIRD_MIN_VEL_Y = 1
    BIRD_MAX_VEL_Y = 10

    BIRD_BEGIN = 'begin'
    BIRD_RUNNING = 'running'
    BIRD_DIE = 'die'

    bird_state = BIRD_RUNNING

    def __init__(self, pos_x, pos_y, bird_img):
        self.posX = pos_x
        self.posY = pos_y
        self.birdImg = bird_img
        self.birdImgWidth = bird_img[0].get_width()
        self.birdImgHeight = bird_img[0].get_height()

    def getIcon(self):
        return self.birdImg[0]

    def getBirdImg(self):
        self.birdIndex += 1
        return self.birdImg[self.birdIndex % 3]
