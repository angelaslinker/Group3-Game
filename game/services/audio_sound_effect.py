# Helpful link if pygame doesn't work on your system. https://bobbyhadz.com/blog/python-no-module-named-pygame
# Sound effects .wav
# Music sounds .mp3

import pygame
pygame.init()


class AudioSoundEffect():
    def __init__(self, filepath):
        '''Initializes audio service'''
        self._sound = filepath

    def playSound(self):
        sound = pygame.mixer.Sound(self._sound)
        sound.play()


# Test AudioSoundEffect class
# play = AudioSoundEffect("game/services/boing.wav")
# for i in range(300):
#     play.playSound()
