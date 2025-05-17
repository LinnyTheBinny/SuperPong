import pygame, Config

pygame.init()

# VARIABLES #

CurrentMusic = None

# FUNCTIONS #

def PlaySound(SoundFile : str, Volume):
    Sound = pygame.mixer.Sound("Assets/SFX/" + SoundFile)
    Sound.set_volume(Volume / 100 * Config.SFXVolume)
    Sound.play()

def PlayMusic(MusicFile : str):
    global CurrentMusic

    Music = pygame.mixer.Sound("Assets/Music/" + MusicFile)
    Music.set_volume(1 * Config.MusicVolume)
    Music.play(100)
    CurrentMusic = Music

def UpdateMusicVolume():
    global CurrentMusic

    if CurrentMusic != None:
        CurrentMusic.set_volume(0.5 * Config.MusicVolume)

def FadeOutMusic():
    global CurrentMusic

    if CurrentMusic != None:
        CurrentMusic.fadeout(3000)
        CurrentMusic = None