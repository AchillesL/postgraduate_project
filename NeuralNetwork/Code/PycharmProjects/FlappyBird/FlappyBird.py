import pygame

window = None
screenW, screenH = 0, 0
bird = None

resourcePath = "C:\\Users\\ZXX-PC\\Desktop\\flappybird\\"

class Bird:
    def __init__(self, x, y):
        self.img = pygame.image.load(resourcePath + "bird0_1.png")
        self.x = x
        self.y = y


def initGame():
    # 初始化
    pygame.init()
    pygame.display.set_caption("Flappy Bird")
    iconImg = pygame.image.load(resourcePath + "bird1_0.png")
    pygame.display.set_icon(iconImg)

    # 设置背景图，初始化画面宽高等
    bgImg = pygame.image.load(resourcePath + "bg_day.png")
    screenW = bgImg.get_size()[0]
    screenH = bgImg.get_size()[1]
    global window
    window = pygame.display.set_mode((screenW, screenH))
    showObject(bgImg, 0, 0)

    # 初始化小鸟
    global bird
    bird = Bird(screenW // 2, screenH // 2)


def showObject(img, x, y):
    window.blit(img, (x, y))


def loopGame():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        showObject(bird.img, bird.x, bird.y)
        pygame.display.update()


if __name__ == '__main__':
    initGame()
    loopGame()
