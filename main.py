from game.services.audio_sound_effect import AudioSoundEffect
from game.services.audio_music import AudioMusic
import time #For testing

def main():
    playMusic = AudioMusic("game/services/boing.wav")
    for j in range(300):  # Random value to play test sound
        playMusic.playMusic()
    playMusic.stopMusic()

    time.sleep(2)

    playSoundEffect = AudioSoundEffect("game/services/boing.wav")
    for i in range(500): #Random value to play test sound
        playSoundEffect.playSound()


if __name__ == "__main__":
    main()
