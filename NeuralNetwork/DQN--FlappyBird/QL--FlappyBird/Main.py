import pygame
import Bird
import Pipe
import Scene
import random
import Base

FPS = 30
screen_width = 288
screen_heigh = 512

REMOVE_SPEED = 3


def main():
    pygame.init()

    screen = pygame.display.set_mode((screen_width, screen_heigh))
    pygame.display.set_caption('Flappy Bird')

    scene = Scene.Scene(pygame)
    bird = Bird.Bird(int(screen_width * 0.2), int(screen_heigh * 0.4), scene.birdImgs)

    pygame.display.set_icon(bird.getIcon())
    screen.blit(scene.background, (0, 0))

    base = Base.Base(scene.base, 0, screen_heigh - 112, scene.base.get_width() - scene.background.get_width())

    pipeList = []
    pipePosX = 0

    for i in range(2):
        if i == 0:
            pipePosX = screen_width - 250
        pipePosX += screen_width - 80
        pipe = Pipe.Pipe(scene.pipeImg, pipePosX, random.randint(0, 120), screen_heigh)
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
        if bird.bird_state == bird.BIRD_BEGIN:
            score = 0
            pipePosX = 0
            pipeList.clear()

            for i in range(2):
                if i == 0:
                    pipePosX = screen_width
                pipePosX += screen_width - 50
                pipe = Pipe.Pipe(scene.pipeImg, pipePosX, random.randint(0, 120), screen_heigh)
                pipeList.append(pipe)

            bird.bird_state = bird.BIRD_RUNNING

        elif bird.bird_state == bird.BIRD_RUNNING:
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

            # 显示柱子
            for p in pipeList:
                p.posX -= REMOVE_SPEED

                if pipeList[0].posX + pipeList[0].pipeImg[0].get_width() < 0:
                    newPipe = Pipe.Pipe(scene.pipeImg,
                                        pipeList[len(pipeList) - 1].posX + screen_width - 80,
                                        random.randint(0, 120), screen_heigh)
                    pipeList.append(newPipe)
                    pipeList.remove(p)

                screen.blit(p.pipeImg[0], (p.posX, p.posY[0]))
                screen.blit(p.pipeImg[1], (p.posX, p.posY[1]))

            # 在X方向移动地面图片
            base.pos_x = -((-base.pos_x + REMOVE_SPEED) % base.shift)
            screen.blit(scene.base, (base.pos_x, base.pos_y))

            rect_bird = pygame.Rect(bird.posX, bird.posY, bird.birdImgWidth, bird.birdImgHeight)
            # pygame.draw.rect(screen, (255, 0, 0), rect_bird, 1)

            rect_base = pygame.Rect(base.pos_x, base.pos_y, base.width, base.height)
            # 碰撞检测1：检查是否与地面相碰
            if rect_bird.colliderect(rect_base):
                bird.bird_state = bird.BIRD_DIE
                scene.Sounds['hit'].play()

            # 碰撞检测2：检测是否与当前屏幕显示的柱子碰撞
            cur_pipe = pipeList[0]
            for p in pipeList:
                if p.posX < screen_width and p.isOver == False:
                    cur_pipe = p
                    rect_pipe_up = pygame.Rect(cur_pipe.posX, cur_pipe.posY[0], cur_pipe.imgWidth,
                                               cur_pipe.imgHeight)
                    rect_pipe_down = pygame.Rect(cur_pipe.posX, cur_pipe.posY[1], cur_pipe.imgWidth,
                                                 cur_pipe.imgHeight)

                    # pygame.draw.rect(screen, (255, 0, 0), rect_pipe_up, 1)
                    # pygame.draw.rect(screen, (255, 0, 0), rect_pipe_down, 1)

                    if rect_bird.colliderect(rect_pipe_up):
                        bird.bird_state = bird.BIRD_DIE
                        scene.Sounds['hit'].play()
                        break

                    if rect_bird.colliderect(rect_pipe_down):
                        bird.bird_state = bird.BIRD_DIE
                        scene.Sounds['hit'].play()
                        break
                    break

            # 越过柱子得分+1
            if bird.posX > cur_pipe.posX + cur_pipe.imgWidth:
                scene.Sounds['point'].play()
                score += 1
                cur_pipe.isOver = True

            print('x:', cur_pipe.posX + cur_pipe.imgWidth - bird.posX, 'y:', cur_pipe.posY[1] - bird.posY)

            # 显示分数
            score_digits = [int(x) for x in list(str(score))]
            total_width = 0  # total width of all numbers to be printed

            for digit in score_digits:
                total_width += scene.number[digit].get_width()

            x_offset = (screen_width - total_width) / 2

            for digit in score_digits:
                screen.blit(scene.number[digit], (x_offset, screen_heigh * 0.1))
                x_offset += scene.number[digit].get_width()

        elif bird.bird_state == bird.BIRD_DIE:
            bird.posY = int(screen_heigh * 0.4)
            bird.bird_vel_y = 1
            bird.bird_state = bird.BIRD_BEGIN
            pass

        pygame.display.update()
        pygame.time.Clock().tick(FPS)


if __name__ == '__main__':
    main()
