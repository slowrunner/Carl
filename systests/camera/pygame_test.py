#!/usr/bin/env python3

# file: pygame_test.py

from PIL import Image
import numpy as np
from time import sleep
import pygame


pygame.init()
clk = pygame.time.Clock()

im = np.array(Image.open('images/motion_capture.jpg'))
win = pygame.display.set_mode((im.shape[1],im.shape[0]))

img = pygame.image.load('images/motion_capture.jpg')

while True:
    try:
        win.blit(img,(0,0))
        pygame.display.flip()
        clk.tick(3)
        sleep(5)
        exit(0)
    except KeyboardInterrupt:
        print("\nExiting")
        break
