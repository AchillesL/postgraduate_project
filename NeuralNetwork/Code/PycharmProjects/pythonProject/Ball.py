import pygame

pygame.init()
window = pygame.display.set_mode((400,800))

window.fill((255,255,255))

y = 0
while True:
    y+= 1

    pygame.display.update()