import pygame

FPS = 30
screen_width = 288
screen_heigh = 512

ground_base_y = screen_heigh - 112
IMAGES, SOUNDS = {}, {}


def initImageSound():
    IMAGES['bird_flap'] = (
        pygame.image.load('res/image/redbird-upflap.png').convert_alpha(),
        pygame.image.load('res/image/redbird-midflap.png').convert_alpha(),
        pygame.image.load('res/image/redbird-downflap.png').convert_alpha()
    )

    IMAGES['number'] = (
        pygame.image.load('res/image/0.png').convert_alpha(),
        pygame.image.load('res/image/1.png').convert_alpha(),
        pygame.image.load('res/image/2.png').convert_alpha(),
        pygame.image.load('res/image/3.png').convert_alpha(),
        pygame.image.load('res/image/4.png').convert_alpha(),
        pygame.image.load('res/image/5.png').convert_alpha(),
        pygame.image.load('res/image/6.png').convert_alpha(),
        pygame.image.load('res/image/7.png').convert_alpha(),
        pygame.image.load('res/image/8.png').convert_alpha(),
        pygame.image.load('res/image/9.png').convert_alpha(),
    )

    IMAGES['ground'] = pygame.image.load('res/image/base.png').convert_alpha()
    IMAGES['pipe'] = (
        pygame.image.load('res/image/pipe-green.png').convert_alpha(),
        pygame.transform.flip(pygame.image.load('res/image/pipe-green.png').convert_alpha(), False, True)
    )
    IMAGES['background'] = pygame.image.load('res/image/background-day.png').convert_alpha()

    SOUNDS['die'] = pygame.mixer.Sound('res/audio/die.wav')
    SOUNDS['hit'] = pygame.mixer.Sound('res/audio/hit.wav')
    SOUNDS['point'] = pygame.mixer.Sound('res/audio/point.wav')
    SOUNDS['swoosh'] = pygame.mixer.Sound('res/audio/swoosh.wav')
    SOUNDS['wing'] = pygame.mixer.Sound('res/audio/wing.wav')


def main():
    global screen
    pygame.init()

    screen = pygame.display.set_mode((screen_width, screen_heigh))
    pygame.display.set_caption('Flappy Bird')

    initImageSound()
    pygame.display.set_icon(IMAGES['bird_flap'][0])
    screen.blit(IMAGES['background'], (0, 0))
    screen.blit(IMAGES['ground'], (0, ground_base_y))

    baseShift = IMAGES['ground'].get_width() - IMAGES['background'].get_width()
    basex = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE):
                SOUNDS['wing'].play()

        basex = -((-basex + 2) % baseShift)
        screen.blit(IMAGES['ground'], (basex, ground_base_y))

        pygame.display.update()
        pygame.time.Clock().tick(FPS)


if __name__ == '__main__':
    main()
