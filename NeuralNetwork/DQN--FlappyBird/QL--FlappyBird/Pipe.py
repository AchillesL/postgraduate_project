class Pipe:

    gapY = 120

    isOver = False

    def __init__(self, pipeImg, posX, offsetY, screenH):
        self.pipeImg = pipeImg
        self.posX = posX
        self.offsetY = offsetY
        self.imgWidth = self.pipeImg[0].get_width()
        self.imgHeight = self.pipeImg[0].get_height();

        self.posY = (
            # 上面柱子的坐标的Y值
            0 - int((2 * self.pipeImg[0].get_height() + self.gapY - screenH) / 2) - offsetY,
            # 下面柱子的坐标的Y值
            int((screenH + self.gapY) / 2) - offsetY
        )
