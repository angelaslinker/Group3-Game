# Helpful link if pygame doesn't work on your system. https://bobbyhadz.com/blog/python-no-module-named-pygame
# Sound effects .wav.
# Note: .mp3 does not work.

import time
from pygame import mixer
mixer.init()  # Initialize mixer


class AudioSoundEffect():
    def __init__(self):
        '''Initializes audio service'''
        PATH = "game/audio_services/"
        self._drumroll_sound = mixer.Sound(PATH + "drumroll.wav")
        self._negativeBeeps_sound = mixer.Sound(PATH + "negativeBeeps.wav")
        self._success_sound = mixer.Sound(PATH + "success.wav")

    def playSound(self, type):
        if type == 1:
            self._drumroll_sound.play()
            time.sleep(5)
        if type == 2:
            self._negativeBeeps_sound.play()
            time.sleep(2)
        if type == 3:
            self._success_sound.play()
            time.sleep(2)


# Test AudioSoundEffect class
# play = AudioSoundEffect()
# play.playSound(1)
# play.playSound(2)
# play.playSound(3)
