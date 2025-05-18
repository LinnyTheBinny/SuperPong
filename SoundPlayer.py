import pygame, Config

pygame.init()

# FUNCTIONS #

def PlaySound(SoundFile : str, Volume):
    Sound = pygame.mixer.Sound("Assets/SFX/" + SoundFile)
    Sound.set_volume(Volume / 100 * Config.SFXVolume)
    Sound.play()

def PlayMusic(MusicFile : str):
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.queue("Assets/Music/" + MusicFile)
    else:
        pygame.mixer.music.load("Assets/Music/" + MusicFile)
    
    pygame.mixer.music.set_volume(0.5 * Config.MusicVolume)
    pygame.mixer.music.play(-1)

def UpdateMusicVolume():
    pygame.mixer.music.set_volume(0.5 * Config.MusicVolume)

def FadeOutMusic():
    pygame.mixer.music.fadeout(3000)