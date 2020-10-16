import random
import pygame, sys
import math

pygame.init()
pygame.display.set_caption("打飞机")
w, h = 800, 600
screen = pygame.display.set_mode((w, h))
bImg = pygame.image.load(r"C:\Users\ZXX-PC\Desktop\resource\bg.png")

pygame.mixer.music.load(r"C:\Users\ZXX-PC\Desktop\resource\bg.wav")
pygame.mixer.music.play(-1)

exposeSound = pygame.mixer.Sound(r"C:\Users\ZXX-PC\Desktop\resource\exp.wav")

score = 0
font = pygame.font.Font(None, 32)



def showScore():
    text = f"Score:{score}"
    scoreRender = font.render(text, True, (0, 255, 0))
    screen.blit(scoreRender, (10, 10))


class Player:
    def __init__(self, posX, posY):
        self.img = pygame.image.load(r"C:\Users\ZXX-PC\Desktop\resource\player.png")
        self.posX = posX
        self.posY = posY

    def setPosX(self, posX):
        if posX < 0:
            self.posX = 0
        elif posX > w - 64:
            self.posX = w - 64
        else:
            self.posX = posX

    def setPosY(self, posY):
        if posY < 0:
            self.posY = 0
        elif posY > h - 64:
            self.posY = h - 64
        else:
            self.posY = posY

    def isOver(self):
        for e in enemyList:
            dis = math.sqrt((e.posX - self.posX) * (e.posX - self.posX) + (e.posY - self.posY) * (e.posY - self.posY));
            if dis < 60:
                return True
        return False


class Enemy:
    def __init__(self):
        self.step = 10
        self.posY = random.randint(10, 100)
        self.posX = random.randint(100, w - 100)
        self.img = pygame.image.load(r"C:\Users\ZXX-PC\Desktop\resource\enemy.png")

    def isOver(self):
        return self.posY > h - 50


class Bullet:
    def __init__(self):
        self.step = 15
        self.posX = player.posX + (64 - 32) / 2
        self.posY = player.posY - 15
        self.img = pygame.image.load(r"C:\Users\ZXX-PC\Desktop\resource\bullet.png")

    def hit(self):
        global score
        for e in enemyList:
            dis = math.sqrt((e.posX - self.posX) * (e.posX - self.posX) + (e.posY - self.posY) * (e.posY - self.posY));
            if dis < 30:
                score += 1
                exposeSound.play()
                if self in bulletList:
                    bulletList.remove(self)
                enemyList.remove(e)
                enemyList.append(Enemy())


def showEnemy():
    for e in enemyList:
        screen.blit(e.img, (e.posX, e.posY))
        e.posX += e.step
        if e.posX > w - 64 or e.posX < 0:
            e.step *= -1
            e.posY += 40

isOver = False
player = Player(int(w / 2), int(h - h / 7))
stepX, stepY = 0, 0
enemyNumber = 10
enemyList = []
for i in range(enemyNumber):
    enemyList.append(Enemy())

bulletList = []


def showBullet():
    for b in bulletList:
        screen.blit(b.img, (b.posX, b.posY))
        b.posY -= 10
        if b.posY < 0:
            bulletList.remove(b)
        b.hit()


def checkOverGame():
    global isOver
    if player.isOver():
        isOver = True

    for e in enemyList:
        if e.isOver():
            isOver = True

    if isOver:
        text = "Game over"
        overfont = pygame.font.Font(None, 64)
        scoreRender = overfont.render(text, True, (255, 0, 0))
        screen.blit(scoreRender, (w / 3, h / 2))
        enemyList.clear()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                stepX = 5
            elif event.key == pygame.K_LEFT:
                stepX = -5
            elif event.key == pygame.K_UP:
                stepY = -5
            elif event.key == pygame.K_DOWN:
                stepY = 5
            elif event.key == pygame.K_SPACE:
                bulletList.append(Bullet())

        elif event.type == pygame.KEYUP:
            stepX, stepY = 0, 0

    player.setPosX(player.posX + stepX)
    player.setPosY(player.posY + stepY)

    screen.blit(bImg, (0, 0))
    screen.blit(player.img, (player.posX, player.posY))

    showEnemy()
    showBullet()
    showScore()

    checkOverGame()

    pygame.display.update()
    pygame.time.Clock().tick(60)
