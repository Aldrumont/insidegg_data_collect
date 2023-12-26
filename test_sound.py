from gtts import gTTS
from pydub import AudioSegment
import pygame
import os
import tempfile

def speak_text(text, speed=1.5):  # Speed can be adjusted as needed
    # Convert the text to speech in Brazilian Portuguese
    tts = gTTS(str(text), lang='pt-br')
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    tts.save(temp_file.name)

    # Load the audio file using pydub
    sound = AudioSegment.from_mp3(temp_file.name)
    # Speed up the sound
    sound = speed_change(sound, speed)
    # Save the modified audio
    modified_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    sound.export(modified_file.name, format="mp3")

    # Initialize pygame and play the modified sound
    pygame.mixer.init()
    pygame.mixer.music.load(modified_file.name)
    pygame.mixer.music.play()

    # Wait for the sound to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # Clean up temporary files
    os.unlink(temp_file.name)
    os.unlink(modified_file.name)

def speed_change(sound, speed=1.0):
    # Change the speed of the sound
    return sound.speedup(playback_speed=speed)

# Get user input
text = input("Digite um número: ")
speak_text(text)
