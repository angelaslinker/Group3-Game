# Helpful link if pygame doesn't work on your system. https://bobbyhadz.com/blog/python-no-module-named-pygame
# Sound effects .wav
# Music sounds .mp3

import pygame
pygame.init()


class AudioMusic():
    def __init__(self, filepath):
        '''Initializes audio service'''
        self._sound = filepath

    def playMusic(self):
        music = pygame.mixer.music.load(self._sound)
        pygame.mixer.music.play(-1)


# Test AudioMusic class
# play = AudioMusic("game/services/boing.wav")
# for i in range(200):
#     play.playMusic()
