# 场景类，包括用到的图片，音乐等等
class Scene:
    def __init__(self, pygame):
        self.birdImgs = (
            pygame.image.load('res/image/redbird-upflap.png').convert_alpha(),
            pygame.image.load('res/image/redbird-midflap.png').convert_alpha(),
            pygame.image.load('res/image/redbird-downflap.png').convert_alpha()
        )
        self.number = (
            pygame.image.load('res/image/0.png').convert_alpha(),
            pygame.image.load('res/image/1.png').convert_alpha(),
            pygame.image.load('res/image/2.png').convert_alpha(),
            pygame.image.load('res/image/3.png').convert_alpha(),
            pygame.image.load('res/image/4.png').convert_alpha(),
            pygame.image.load('res/image/5.png').convert_alpha(),
            pygame.image.load('res/image/6.png').convert_alpha(),
            pygame.image.load('res/image/7.png').convert_alpha(),
            pygame.image.load('res/image/8.png').convert_alpha(),
            pygame.image.load('res/image/9.png').convert_alpha()
        )
        self.base = pygame.image.load('res/image/base.png').convert_alpha()
        self.pipeImg = (
            pygame.transform.flip(pygame.image.load('res/image/pipe-green.png').convert_alpha(), False, True),
            pygame.image.load('res/image/pipe-green.png').convert_alpha()
        )
        self.background = pygame.image.load('res/image/background-day.png').convert_alpha()
        self.Sounds = {
            'die': pygame.mixer.Sound('res/audio/die.wav'),
            'hit': pygame.mixer.Sound('res/audio/hit.wav'),
            'point': pygame.mixer.Sound('res/audio/point.wav'),
            'swoosh': pygame.mixer.Sound('res/audio/swoosh.wav'),
            'wing': pygame.mixer.Sound('res/audio/wing.wav')
        }
