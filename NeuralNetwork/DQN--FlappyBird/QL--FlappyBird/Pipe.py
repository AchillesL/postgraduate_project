class Pipe:
    gapY = 100

    def __init__(self, pipeImg, posX, offsetY, screenH):
        self.pipeImg = pipeImg
        self.posX = posX
        self.offsetY = offsetY

        self.posY = (
            # 上面柱子的坐标的Y值
            0 - int((2 * self.pipeImg[0].get_height() + self.gapY - screenH) / 2) - offsetY,
            # 下面柱子的坐标的Y值
            int((screenH + self.gapY) / 2) - offsetY
        )
