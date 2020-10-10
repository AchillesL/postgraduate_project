import pygame
import Bird
import Pipe
import Scene
import random

FPS = 45
screen_width = 288
screen_heigh = 512

REMOVE_SPEED = 3

# 地面的Y轴位置
base_y = screen_heigh - 112


def main():
    pygame.init()

    screen = pygame.display.set_mode((screen_width, screen_heigh))
    pygame.display.set_caption('Flappy Bird')

    scene = Scene.Scene(pygame)
    bird = Bird.Bird(int(screen_width * 0.2), int(screen_heigh * 0.4), scene.birdImgs);

    pygame.display.set_icon(bird.getIcon())
    screen.blit(scene.background, (0, 0))

    baseShift = scene.base.get_width() - scene.background.get_width()
    base_x = 0

    pipeList = []
    pipePosX = 0

    for i in range(10):
        pipePosX += screen_width + random.randint(-150, -60)
        pipe = Pipe.Pipe(scene.pipeImg, pipePosX, random.randint(-60, 150), screen_heigh)
        pipeList.append(pipe)

    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE):
                scene.Sounds['wing'].play()
                # 按下空格，小鸟处于“振翅”状态，即需要往上飞
                bird.birdFlapped = True
                # 小鸟最初的速度最大=10，逐步递减
                bird.bird_vel_y = 10

        if bird.bird_state == bird.BIRD_RUNNING:
            screen.blit(scene.background, (0, 0))

            # “振翅”状态，且速度没到最大速度
            if bird.birdFlapped and bird.bird_vel_y > bird.BIRD_MIN_VEL_Y:
                bird.bird_vel_y -= bird.BIRD_ACC_Y
                bird.posY -= bird.bird_vel_y

            # 往上飞到达最大速度，此时应该下降，即脱离“振翅”状态
            if bird.birdFlapped and bird.bird_vel_y <= bird.BIRD_MIN_VEL_Y:
                bird.bird_vel_y = 1
                bird.birdFlapped = False

            # 处于非振翅状态时，小鸟下落
            if not bird.birdFlapped:
                bird.bird_vel_y += bird.BIRD_ACC_Y
                bird.posY += bird.bird_vel_y

            screen.blit(bird.getBirdImg(), (bird.posX, bird.posY))

            # # 显示柱子
            # for p in pipeList:
            #     p.posX -= REMOVE_SPEED
            #     screen.blit(p.pipeImg[0], (p.posX, p.posY[0]))
            #     screen.blit(p.pipeImg[1], (p.posX, p.posY[1]))

            # 在X方向移动地面图片
            base_x = -((-base_x + REMOVE_SPEED) % baseShift)
            screen.blit(scene.base, (base_x, base_y))

            print(pygame.Rect(bird.birdImg[0].get_rect()).colliderect(pygame.Rect(scene.background.get_rect())))

            # if pygame.Rect(bird.birdImg[0].get_rect()).colliderect(pygame.Rect(scene.base.get_rect())):
            #     bird.bird_state = bird.BIRD_DIE

            # if bird.posY > base_y - bird.birdImg[0].get_width():
            #     bird.bird_state = bird.BIRD_DIE

        elif bird.bird_state == bird.BIRD_DIE:
            bird.posY = int(screen_heigh * 0.4)
            bird.bird_vel_y = 1
            bird.bird_state = bird.BIRD_RUNNING

        pygame.display.update()
        pygame.time.Clock().tick(FPS)


if __name__ == '__main__':
    main()
