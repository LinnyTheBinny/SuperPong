import pygame, random, sys, math, threading, VisualFX, SoundPlayer
import Ball, Paddle, UI, Config
import Score

pygame.init()
MainScreen = pygame.display.set_mode((Config.SCREEN_SIZE_X, Config.SCREEN_SIZE_Y))
Screen = pygame.Surface((Config.SCREEN_SIZE_X, Config.SCREEN_SIZE_Y), pygame.SRCALPHA)
pygame.display.set_caption("Pong")

# VARIABLES #

GameState = "MainMenu"
Clock = pygame.time.Clock()

# CLASSES #

TransitionScreen = UI.TransitioningScreen()

ScoreClass = Score.Score()

# GUI STUFF #

MusicVolumeValueText = None
SFXVolumeValueText = None

WControlText = None
SControlText = None
UpControlText= None
DownControlText = None

PausedTitle = None
BackToMenuButton = None
RestartButton = None

# FUNCTIONS #

def CleanPreviousScene():
    UI.TextsGroup.empty()
    Ball.BallGroup.empty()
    Paddle.PaddleGroup.empty()
    UI.BackgroundsGroup.empty()
    UI.InstructionTextGroup.empty()
    UI.ToggleButtonsGroup.empty()
    VisualFX.WhiteSqaresGroup.empty()
    UI.SlidersGroup.empty()

SoundPlayer.PlayMusic("BackgroundMusic.mp3")

def SetUpMainMenu():
    global GameState

    GameState = "MainMenu"
    
    CleanPreviousScene()

    TitleText = UI.Text(Screen, "Super Pong", UI.TitlePixelFont, (Config.SCREEN_SIZE_X / 2, Config.SCREEN_SIZE_Y / 2 - 130), (255, 255, 255), 255, False, False, None)
    if Config.SpecialEffectsEnabled: TitleText.FadeToDirectionTween((Config.SCREEN_SIZE_X / 2 - 200, Config.SCREEN_SIZE_Y / 2 - 130), (Config.SCREEN_SIZE_X / 2, Config.SCREEN_SIZE_Y / 2 - 130), 10)

    def MakeCreditText():
        CreditText = UI.Text(Screen, "By Lin Moon", UI.SmallPixelFont, (Config.SCREEN_SIZE_X / 2, Config.SCREEN_SIZE_Y / 2 - 80), (255, 255, 255), 255, False, False, None)
        if Config.SpecialEffectsEnabled: CreditText.FadeToDirectionTween((Config.SCREEN_SIZE_X / 2 + 200, Config.SCREEN_SIZE_Y / 2 - 80), (Config.SCREEN_SIZE_X / 2, Config.SCREEN_SIZE_Y / 2 - 80), 10)
    
    def MakePlayButton():
        def OnPlayButtonClicked():
            if Config.SpecialEffectsEnabled:

                TransitionScreen.StartFade()
                threading.Timer(TransitionScreen.FadeSpeed / 10, lambda: SetUpPlayerVSPlayer(ScoreClass.LeftScore, ScoreClass.RightScore)).start()
            else:
                SetUpPlayerVSPlayer(ScoreClass.LeftScore, ScoreClass.RightScore)

        PlayButton = UI.Text(Screen, "Play", UI.SmallPixelFont, (Config.SCREEN_SIZE_X / 2, Config.SCREEN_SIZE_Y / 2 + 30), (255, 255, 255), 0, True, True, OnPlayButtonClicked)
        if Config.SpecialEffectsEnabled: PlayButton.FadeToDirectionTween((Config.SCREEN_SIZE_X / 2, Config.SCREEN_SIZE_Y / 2 + 70), (Config.SCREEN_SIZE_X / 2, Config.SCREEN_SIZE_Y / 2 + 30), 3)

    def MakeSettingsButton():
        def OnSettingsButtonClicked():
            if Config.SpecialEffectsEnabled:
                TransitionScreen.StartFade()
                threading.Timer(TransitionScreen.FadeSpeed / 10, SetUpSettings).start()
            else:
                SetUpSettings()

        SettingsButton = UI.Text(Screen, "Settings", UI.SmallPixelFont, (Config.SCREEN_SIZE_X / 2, Config.SCREEN_SIZE_Y / 2 + 80), (255, 255, 255), 0, True, True, OnSettingsButtonClicked)
        if Config.SpecialEffectsEnabled: SettingsButton.FadeToDirectionTween((Config.SCREEN_SIZE_X / 2, Config.SCREEN_SIZE_Y / 2 + 120), (Config.SCREEN_SIZE_X / 2, Config.SCREEN_SIZE_Y / 2 + 80), 3)

    def MakeQuitButton():
        def OnQuitButtonClicked():
            pygame.quit()
            sys.exit()

        QuitButton = UI.Text(Screen, "Quit", UI.SmallPixelFont, (Config.SCREEN_SIZE_X / 2, Config.SCREEN_SIZE_Y / 2 + 130), (255, 255, 255), 0, True, True, OnQuitButtonClicked)
        if Config.SpecialEffectsEnabled: QuitButton.FadeToDirectionTween((Config.SCREEN_SIZE_X / 2, Config.SCREEN_SIZE_Y / 2 + 170), (Config.SCREEN_SIZE_X / 2, Config.SCREEN_SIZE_Y / 2 + 130), 3)

    threading.Timer(0.2, MakeCreditText).start() if Config.SpecialEffectsEnabled else MakeCreditText()
    threading.Timer(0.7, MakePlayButton).start() if Config.SpecialEffectsEnabled else MakePlayButton()
    threading.Timer(0.9, MakeSettingsButton).start() if Config.SpecialEffectsEnabled else MakeSettingsButton()
    threading.Timer(1.1, MakeQuitButton).start() if Config.SpecialEffectsEnabled else MakeQuitButton()

SetUpMainMenu()

def UpdateMainMenu():
    UI.TextsGroup.update(Screen)

def SetUpSettings():
    global GameState, MusicVolumeValueText, SFXVolumeValueText

    GameState = "Settings"
    
    CleanPreviousScene()

    def OnBackButtonClick():
        if Config.SpecialEffectsEnabled:
            TransitionScreen.StartFade()
            threading.Timer(TransitionScreen.FadeSpeed / 10, SetUpMainMenu).start()
        else:
            SetUpMainMenu()

    SettingsText = UI.Text(Screen, "Settings", UI.TitlePixelFont, (Config.SCREEN_SIZE_X / 2, Config.SCREEN_SIZE_Y / 2 - 130), (255, 255, 255), 255, False, False, None)

    MusicVolumeText = UI.Text(Screen, "Music Volume", UI.SmallPixelFont, (Config.SCREEN_SIZE_X / 2 - 135, Config.SCREEN_SIZE_Y / 2 - 50), (255, 255, 255), 255, False, False, None)
    SFXVolumeText = UI.Text(Screen, "SFX Volume", UI.SmallPixelFont, (Config.SCREEN_SIZE_X / 2 - 123, Config.SCREEN_SIZE_Y / 2), (255, 255, 255), 255, False, False, None)

    MusicVolumeSlider = UI.Slider(MusicVolumeText.TextRect.center + pygame.Vector2(200, 0), "MusicVolume")
    SFXVolumeSlider = UI.Slider(SFXVolumeText.TextRect.center + pygame.Vector2(188, 0), "SFXVolume")

    MusicVolumeValueText = UI.Text(Screen, "50", UI.SmallPixelFont, (Config.SCREEN_SIZE_X / 2 + 200, Config.SCREEN_SIZE_Y / 2 - 50), (255, 255, 255), 255, False, False, None)
    SFXVolumeValueText = UI.Text(Screen, "50", UI.SmallPixelFont, (Config.SCREEN_SIZE_X / 2 + 200, Config.SCREEN_SIZE_Y / 2), (255, 255, 255), 255, False, False, None)

    SpecialEffectsText = UI.Text(Screen, "Special Effects", UI.SmallPixelFont, (Config.SCREEN_SIZE_X / 2 - 25, Config.SCREEN_SIZE_Y / 2 + 60), (255, 255, 255), 255, False, False, None)
    SpecialEffectsToggleButton = UI.ToggleButton((Config.SCREEN_SIZE_X / 2 + 100, Config.SCREEN_SIZE_Y / 2 + 60), "SpecialEffects")

    BackButton = UI.Text(Screen, "Back", UI.SmallPixelFont, (Config.SCREEN_SIZE_X / 2, Config.SCREEN_SIZE_Y / 2 + 150), (255, 255, 255), 0, True, True, OnBackButtonClick)

def UpdateSettingsScreen():
    UI.TextsGroup.update(Screen)
    UI.SlidersGroup.update(Screen)
    UI.ToggleButtonsGroup.update(Screen)

    if MusicVolumeValueText: MusicVolumeValueText.ChangeMessage(str(int(Config.MusicVolume * 100)))
    if SFXVolumeValueText: SFXVolumeValueText.ChangeMessage(str(int(Config.SFXVolume * 100)))

def SetUpPlayerVSPlayer(LeftScore, RightScore):
    global RedBackground, BlueBackground, GameState, ScoreText, SpeedText, MainBall

    Config.GAME_START_INSTRUCTIONS = True

    CleanPreviousScene()

    MainBall = Ball.Ball()

    LeftPaddle = Paddle.Paddle(50, pygame.K_w, pygame.K_s)
    RightPaddle = Paddle.Paddle(750, pygame.K_UP, pygame.K_DOWN)

    RedBackground = UI.BackgroundFader("Assets/red.png", (200, 250))
    BlueBackground = UI.BackgroundFader("Assets/blue.png", (600, 250))

    ScoreText = UI.Text(Screen, "", UI.PixelFont, (400, 50), (255, 255, 255), 255, False, False, None)
    SpeedText = UI.Text(Screen, "", UI.SmallPixelFont, (400, 450), (255, 255, 255), 255, False, False, None)

    def MakeAllInstructionTexts():
        global WControlText, SControlText, UpControlText, DownControlText

        WControlText = UI.InstructionText(Screen, "W", UI.PixelFont, (150, 220), (255, 255, 255), 255, 3)
        if Config.SpecialEffectsEnabled: WControlText.FadeToDirectionTween((300, 220), (150, 220), 10, "In")

        SControlText = UI.InstructionText(Screen, "S", UI.PixelFont, (150, 280), (255, 255, 255), 255, 3)
        if Config.SpecialEffectsEnabled: SControlText.FadeToDirectionTween((300, 280), (150, 280), 10, "In")

        UpControlText = UI.InstructionText(Screen, "UP*ARROW", UI.PixelFont, (650, 220), (255, 255, 255), 255, 3)
        if Config.SpecialEffectsEnabled: UpControlText.FadeToDirectionTween((500, 220), (650, 220), 10, "In")

        DownControlText = UI.InstructionText(Screen, "DOWN*ARROW", UI.PixelFont, (650, 280), (255, 255, 255), 255, 3)
        if Config.SpecialEffectsEnabled: DownControlText.FadeToDirectionTween((500, 280), (650, 280), 10, "In")

    threading.Timer(0.2, MakeAllInstructionTexts).start() if Config.SpecialEffectsEnabled else MakeAllInstructionTexts()

    GameState = "PlayerVSPlayer"

def UpdatePlayerVSPlayerScreen():
    UI.BackgroundsGroup.update(Screen)

    Ball.BallGroup.update()
    Ball.PaddleGroup.update(Screen)

    ScoreText.ChangeMessage(str(ScoreClass.LeftScore) + " : " + str(ScoreClass.RightScore))
    SpeedText.ChangeMessage("Press SPACE to begin" if Config.GAME_START_INSTRUCTIONS else "Speed : " + str(round(abs(MainBall.XSpeed * MainBall.Speed) + abs(MainBall.YSpeed * MainBall.Speed), 2)))

    UI.TextsGroup.update(Screen)
    UI.InstructionTextGroup.update(Screen)

    VisualFX.WhiteSqaresGroup.update(Screen)

    for BallObject in Ball.BallGroup: BallObject.Draw(Screen); BallObject.CheckForBallScored(RedBackground, BlueBackground, ScoreClass)

    VisualFX.UpdateScreenShake()

def RemoveInstructions():
    Config.GAME_START_INSTRUCTIONS = False
    SoundPlayer.PlaySound("EndInstructions.mp3", 100)

    if WControlText: WControlText.FadeToDirectionTween((150, 220), (300, 220), 15, "Out")
    if SControlText: SControlText.FadeToDirectionTween((150, 280), (300, 280), 15, "Out")
    if UpControlText: UpControlText.FadeToDirectionTween((650, 220), (500, 220), 15, "Out")
    if DownControlText: DownControlText.FadeToDirectionTween((650, 280), (500, 280), 15, "Out")

    def EndInstructions():
        UI.InstructionTextGroup.empty()

    threading.Timer(1.0, EndInstructions).start() if Config.SpecialEffectsEnabled else EndInstructions()
    SoundPlayer.FadeOutMusic()

def RemovePausedScreen():
    global GameState, PausedTitle

    if PausedTitle: PausedTitle.kill()
    if BackToMenuButton: BackToMenuButton.kill()
    if RestartButton: RestartButton.kill()

    GameState = "PlayerVSPlayer"
    Config.GAME_PAUSED = False

def SetUpPausedScreen():
    global GameState, PausedTitle, BackToMenuButton, RestartButton

    GameState = "Paused"
    Config.GAME_PAUSED = True

    PausedTitle = UI.Text(Screen, "Paused", UI.TitlePixelFont, (Config.SCREEN_SIZE_X / 2, Config.SCREEN_SIZE_Y / 2 - 100), (255, 255, 255), 255, False, False, None)

    def OnBackButtonClicked():
        Config.GAME_PAUSED = False
        if not Config.GAME_START_INSTRUCTIONS: SoundPlayer.PlayMusic("BackgroundMusic.mp3")

        if Config.SpecialEffectsEnabled:

            TransitionScreen.StartFade()
            threading.Timer(TransitionScreen.FadeSpeed / 10, SetUpMainMenu).start()
        else:
            SetUpMainMenu()

    def OnRestartButtonClicked():
        Config.GAME_PAUSED = False
        if not Config.GAME_START_INSTRUCTIONS: SoundPlayer.PlayMusic("BackgroundMusic.mp3")

        if Config.SpecialEffectsEnabled:

            TransitionScreen.StartFade()
            threading.Timer(TransitionScreen.FadeSpeed / 10, lambda: SetUpPlayerVSPlayer(ScoreClass.LeftScore, ScoreClass.RightScore)).start()
        else:
            SetUpPlayerVSPlayer(ScoreClass.LeftScore, ScoreClass.RightScore)


    BackToMenuButton = UI.Text(Screen, "Back To Menu", UI.SmallPixelFont, (Config.SCREEN_SIZE_X / 2, Config.SCREEN_SIZE_Y / 2), (255, 255, 255), 0, True, True, OnBackButtonClicked)
    RestartButton = UI.Text(Screen, "Restart Game", UI.SmallPixelFont, (Config.SCREEN_SIZE_X / 2, Config.SCREEN_SIZE_Y / 2 + 60), (255, 255, 255), 0, True, True, OnRestartButtonClicked)


def UpdatePausedScreen():
    if not Config.TRANSITION_FADING: UI.BackgroundsGroup.update(Screen)
    Paddle.PaddleGroup.update(Screen)
    Ball.BallGroup.update()
    UI.TextsGroup.update(Screen)
    UI.InstructionTextGroup.update(Screen)
    VisualFX.WhiteSqaresGroup.update(Screen)

    for BallObject in Ball.BallGroup: BallObject.Draw(Screen); BallObject.CheckForBallScored(RedBackground, BlueBackground, ScoreClass)

    BlackSurface = pygame.Surface((Config.SCREEN_SIZE_X, Config.SCREEN_SIZE_Y), pygame.SRCALPHA)
    BlackSurface.fill("Black")
    BlackSurface.set_alpha(220)

    Screen.blit(BlackSurface, (0, 0))

    if PausedTitle: PausedTitle.update(Screen)
    if BackToMenuButton: BackToMenuButton.update(Screen)
    if RestartButton: RestartButton.update(Screen)

# GAME LOOP # 

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not Config.GAME_PAUSED:
                if Config.GAME_START_INSTRUCTIONS: RemoveInstructions()
            if event.key == pygame.K_ESCAPE and GameState != "MainMenu" and GameState != "Settings":
                if Config.GAME_PAUSED: RemovePausedScreen()
                else: SetUpPausedScreen(); SoundPlayer.PlaySound("Pause.mp3", 100)

    MainScreen.fill("BLACK")
    Screen.fill("BLACK")
    
    if GameState == "MainMenu":
        UpdateMainMenu()
    elif GameState == "Settings":
        UpdateSettingsScreen()
    elif GameState == "PlayerVSPlayer":
        UpdatePlayerVSPlayerScreen()
    elif GameState == "Paused":
        UpdatePausedScreen()

    SoundPlayer.UpdateMusicVolume()

    TransitionScreen.update(Screen)
    Config.LEFT_CLICKABLE = not pygame.mouse.get_pressed()[0]

    MainScreen.blit(Screen, (VisualFX.ScreenShakeX, VisualFX.ScreenShakeY))
    pygame.display.flip()
    Clock.tick(60)