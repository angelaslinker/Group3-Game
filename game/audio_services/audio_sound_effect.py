from pygame import mixer
mixer.init()  # Initialize mixer


class AudioSoundEffect():
    def __init__(self):
        '''Initializes audio service'''
        PATH = "audio_services/"
        self._negativeBeeps_sound = mixer.Sound(PATH + "negativeBeeps.wav")
        self._success_sound = mixer.Sound(PATH + "success.wav")

    def playSound(self, type):
        if type == 1:
            self._negativeBeeps_sound.play()
        if type == 2:
            self._success_sound.play()


# Test AudioSoundEffect class
# play = AudioSoundEffect()
# play.playSound(1)
# play.playSound(2)
