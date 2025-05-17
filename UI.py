import pygame, math, SoundPlayer
import Config

pygame.init()

# SET UP #

TitlePixelFont = pygame.font.Font("Assets/Pyxxl.ttf", 35)
PixelFont = pygame.font.Font("Assets/PixelOperator.ttf", 50)
SmallPixelFont = pygame.font.Font("Assets/PixelOperator.ttf", 30)

# CLASSES #

TextsGroup = pygame.sprite.Group()
SlidersGroup = pygame.sprite.Group()
ToggleButtonsGroup = pygame.sprite.Group()
BackgroundsGroup = pygame.sprite.Group()
InstructionTextGroup = pygame.sprite.Group()

class BackgroundFader(pygame.sprite.Sprite):
    def __init__(self, Image, CenterPos):
        super().__init__()
        
        BackgroundsGroup.add(self)

        self.FadeSpeed = Config.BACKGROUND_FADE_SPEED

        self.Background = pygame.image.load(Image).convert()

        self.BackgroundFading = False
        self.BackgroundAlpha = 50
        self.FadeDirection = 1
        self.Background.set_alpha(self.BackgroundAlpha)

        self.BackgroundRect = self.Background.get_rect()
        self.BackgroundRect.center = CenterPos

    def UpdateBackground(self, Screen):
        if self.BackgroundFading:
            self.BackgroundAlpha += self.FadeSpeed * self.FadeDirection

            if self.BackgroundAlpha >= 255:
                self.BackgroundAlpha = 255
                self.FadeDirection = -1
                self.FadeSpeed = 5
            if self.BackgroundAlpha <= 50:
                self.BackgroundAlpha = 50
                self.FadeDirection = 1
                self.FadeSpeed = 30
                self.BackgroundFading = False

        self.Background.set_alpha(self.BackgroundAlpha)

        Screen.blit(self.Background, self.BackgroundRect)

    def update(self, Screen):
        self.UpdateBackground(Screen)

class Text(pygame.sprite.Sprite):
    def __init__(self, Screen, Message, Font : pygame.font.Font, CenterPos, Color, Alpha, IsButton, HoverEffect, OnButtonClickedFunction):
        super().__init__()

        TextsGroup.add(self)

        self.OriginalColor = Color
        self.CurrentColor = list(Color)
        self.Message = Message
        self.Font = Font

        self.Text = Font.render(Message, False, Color)
        self.TextRect = self.Text.get_rect()
        self.TextRect.center = CenterPos

        self.Text.set_alpha(Alpha)

        self.IsButton = IsButton
        self.Hovered = False
        self.HoverSoundPlayed = False
        self.HoverEffect = HoverEffect
        self.OnButtonClickedFunction = OnButtonClickedFunction

        self.StartingCenterPos = CenterPos
        self.Pos = pygame.Vector2(CenterPos)

        self.FadeToDirection = False

    def FadeToDirectionTween(self, StartPos, EndPos, Speed):
        self.Pos = StartPos
        self.TextRect.center = self.Pos
        self.FadeToDirectionStartPos = StartPos
        self.FadeToDirectionEndPos = EndPos
        self.FadeToDirection = True
        self.FadeToDirectionSpeed = Speed

    def UpdateColor(self, Screen):
        TargetTextColor = [0, 0, 0] if self.Hovered else self.OriginalColor

        for i in range(3):
            if self.CurrentColor[i] < TargetTextColor[i]:
                self.CurrentColor[i] = min(self.CurrentColor[i] + 40, TargetTextColor[i])
            elif self.CurrentColor[i] > TargetTextColor[i]:
                self.CurrentColor[i] = max(self.CurrentColor[i] - 40, TargetTextColor[i])

        BackgroundBox = pygame.Surface(self.TextRect.inflate(60, 0).size)
        BackgroundBox.fill((255, 255, 255))
        BackgroundBox.set_alpha(255 - self.CurrentColor[0])
        
        Screen.blit(BackgroundBox, self.TextRect.inflate(60, -5))
        self.Text = self.Font.render(self.Message, False, self.CurrentColor)

    def CheckIfHovered(self):
        if Config.TRANSITION_FADING: return

        if self.TextRect.collidepoint(pygame.mouse.get_pos()): 
            self.Hovered = True

            if not self.HoverSoundPlayed: SoundPlayer.PlaySound("ButtonHover.mp3", 20); self.HoverSoundPlayed = True
        else: 
            self.Hovered = False
            self.HoverSoundPlayed = False

        if self.Hovered and pygame.mouse.get_pressed()[0] and Config.LEFT_CLICKABLE:
            if self.OnButtonClickedFunction: self.OnButtonClickedFunction(); SoundPlayer.PlaySound("ButtonClick.mp3", 100)

    def ChangeMessage(self, NewMessage : str):
        self.Message = NewMessage
        self.Text = self.Font.render(self.Message, False, self.CurrentColor)
        self.TextRect = self.Text.get_rect()
        self.TextRect.center = self.StartingCenterPos

    def Draw(self, Screen):
        if self.FadeToDirection:
            MaxDirection : pygame.Vector2 = pygame.Vector2(self.FadeToDirectionStartPos) - pygame.Vector2(self.FadeToDirectionEndPos)
            Direction : pygame.Vector2 = pygame.Vector2(self.TextRect.center) - pygame.Vector2(self.FadeToDirectionEndPos)
            
            if Direction.length() > 0.1:
                Progress = 1 - (Direction.length() / MaxDirection.length())
                self.Text.set_alpha(255 * Progress)

                Direction = Direction.normalize() * (self.FadeToDirectionSpeed * ((Direction.length() + 1) / MaxDirection.length()))
                self.Pos -= Direction
                self.TextRect.center = pygame.Vector2(round(self.Pos.x), round(self.Pos.y))
            else:
                self.Pos = self.FadeToDirectionEndPos
                self.TextRect.center = self.Pos
                self.Text.set_alpha(255)
                self.FadeToDirection = False

        Screen.blit(self.Text, self.TextRect)

    def update(self, Screen):
        if self.IsButton: self.CheckIfHovered()
        if self.HoverEffect: self.UpdateColor(Screen)

        self.Draw(Screen)

class InstructionText(pygame.sprite.Sprite):
    def __init__(self, Screen, Message, Font : pygame.font.Font, CenterPos, Color, Alpha, BorderWidth):
        super().__init__()

        InstructionTextGroup.add(self)

        self.Text = Font.render(Message, False, Color)
        self.TextRect = self.Text.get_rect()
        self.TextRect.center = CenterPos

        self.Text.set_alpha(Alpha)

        self.Message = Message
        self.Font = Font
        self.CurrentColor = Color
        self.BorderWidth = BorderWidth
        self.Pos = pygame.Vector2(CenterPos)

        if self.Font == PixelFont:
            SideSize = 45

        self.BorderBoxRect = pygame.Rect(0, 0, SideSize, SideSize)
        self.BorderBoxRect.center = self.TextRect.center

        self.FadeToDirection = False
        self.FadeDirection = "In"

    def FadeToDirectionTween(self, StartPos, EndPos, Speed, FadeDirection):
        self.Pos = StartPos
        self.TextRect.center = self.Pos
        self.FadeToDirectionStartPos = StartPos
        self.FadeToDirectionEndPos = EndPos
        self.FadeToDirection = True
        self.FadeToDirectionSpeed = Speed
        self.FadeDirection = FadeDirection

    def Draw(self, Screen):
        if self.FadeToDirection:
            MaxDirection : pygame.Vector2 = pygame.Vector2(self.FadeToDirectionStartPos) - pygame.Vector2(self.FadeToDirectionEndPos)
            Direction : pygame.Vector2 = pygame.Vector2(self.TextRect.center) - pygame.Vector2(self.FadeToDirectionEndPos)
            
            if Direction.length() > 0.1:
                Progress = 1 - (Direction.length() / MaxDirection.length())
                self.Text.set_alpha(255 * Progress) if self.FadeDirection == "In" else self.Text.set_alpha(255 - 255 * Progress)

                Direction = Direction.normalize() * (self.FadeToDirectionSpeed * ((Direction.length() + 1) / MaxDirection.length()))
                self.Pos -= Direction
                self.TextRect.center = pygame.Vector2(round(self.Pos.x), round(self.Pos.y))
            else:
                self.Pos = self.FadeToDirectionEndPos
                self.TextRect.center = self.Pos
                self.Text.set_alpha(255) if self.FadeDirection == "In" else self.Text.set_alpha(0)
                self.FadeToDirection = False

        self.BorderBoxRect.center = self.TextRect.center
        TempSurface = pygame.Surface(self.BorderBoxRect.size, pygame.SRCALPHA)

        if self.FadeDirection == "In":
            BorderColor = (*self.CurrentColor, self.Text.get_alpha() if self.Text.get_alpha() else 255)
        else:
            BorderColor = (*self.CurrentColor, self.Text.get_alpha() if self.Text.get_alpha() else 0)

        LocalCenter = pygame.Vector2(self.TextRect.center) - pygame.Vector2(self.BorderBoxRect.topleft)

        if self.Message == "DOWN*ARROW":
            pygame.draw.polygon(TempSurface, BorderColor, [
                LocalCenter + pygame.Vector2(0, self.BorderBoxRect.size[0] / 3),
                LocalCenter + pygame.Vector2(self.BorderBoxRect.size[0] / 4, 0),
                LocalCenter - pygame.Vector2(self.BorderBoxRect.size[0] / 4, 0)
            ])
        elif self.Message == "UP*ARROW":
            pygame.draw.polygon(TempSurface, BorderColor, [
                LocalCenter - pygame.Vector2(0, self.BorderBoxRect.size[0] / 3),
                LocalCenter + pygame.Vector2(self.BorderBoxRect.size[0] / 4, 0),
                LocalCenter - pygame.Vector2(self.BorderBoxRect.size[0] / 4, 0)
            ])
        else:
            Screen.blit(self.Text, self.TextRect)

        pygame.draw.rect(TempSurface, BorderColor, TempSurface.get_rect(), self.BorderWidth, 10)
        Screen.blit(TempSurface, self.BorderBoxRect.topleft)

    def update(self, Screen):
        self.Draw(Screen)

class TransitioningScreen():
    def __init__(self):
        self.Rect = pygame.Rect(0, 0, Config.SCREEN_SIZE_X, Config.SCREEN_SIZE_Y)

        self.Surface = pygame.Surface(self.Rect.size)
        self.Surface.fill((0, 0, 0))
        self.Alpha = 0
        self.Surface.set_alpha(self.Alpha)

        self.FadeSpeed = 7
        self.FadeDirection = "In"

    def StartFade(self):
        Config.TRANSITION_FADING = True

    def Draw(self, Screen):
        if Config.TRANSITION_FADING:
            if self.FadeDirection == "In":
                self.Alpha += self.FadeSpeed

                if self.Alpha >= 400:
                    self.Alpha = 255
                    self.FadeDirection = "Out"
            else:
                self.Alpha -= self.FadeSpeed

                if self.Alpha <= 0:
                    self.Alpha = 0
                    self.FadeDirection = "In"
                    Config.TRANSITION_FADING = False

        self.Surface.set_alpha(self.Alpha)
        Screen.blit(self.Surface, self.Rect)

    def update(self, Screen):
        self.Draw(Screen)

class Slider(pygame.sprite.Sprite):
    def __init__(self, CenterPos, VariableToChange):
        super().__init__()

        SlidersGroup.add(self)

        self.SliderLineRect = pygame.Rect(0, 0, 200, 5)
        self.SliderLineRect.center = CenterPos

        self.KnobRect = pygame.Rect(0, 0, 10, 30)
        self.KnobRect.center = CenterPos
        self.KnobRectColor = "WHITE"
        self.KnobSelected = False
        self.VariableToChange = VariableToChange

        self.MinPos = self.SliderLineRect.centerx - self.SliderLineRect.size[0] / 2 + (self.KnobRect.size[0] / 2)
        self.MaxPos = self.SliderLineRect.centerx + self.SliderLineRect.size[0] / 2 - (self.KnobRect.size[0] / 2)

        if self.VariableToChange == "MusicVolume":
            self.KnobRect.centerx = self.MinPos + (self.MaxPos - self.MinPos) * Config.MusicVolume
        elif self.VariableToChange == "SFXVolume":
            self.KnobRect.centerx = self.MinPos + (self.MaxPos - self.MinPos) * Config.SFXVolume

    def CheckForMouse(self):
        if not pygame.mouse.get_pressed()[0]:
            self.KnobSelected = False

        if self.KnobRect.collidepoint(pygame.mouse.get_pos()):
            self.KnobRectColor = (150, 150, 150)
            if pygame.mouse.get_pressed()[0] and Config.LEFT_CLICKABLE: self.KnobSelected = True
        else:
            self.KnobRectColor = "WHITE"

        if self.KnobSelected:
            self.KnobRect.centerx = pygame.math.clamp(pygame.mouse.get_pos()[0], self.MinPos, self.MaxPos)
            self.KnobRectColor = (150, 150, 150)

            if self.VariableToChange == "MusicVolume":
                Config.MusicVolume = round((self.KnobRect.centerx - self.MinPos) / (self.MaxPos - self.MinPos), 2)
            elif self.VariableToChange == "SFXVolume":
                Config.SFXVolume = round((self.KnobRect.centerx - self.MinPos) / (self.MaxPos - self.MinPos), 2)

    def Draw(self, Screen):
        pygame.draw.rect(Screen, "WHITE", self.SliderLineRect)
        pygame.draw.rect(Screen, self.KnobRectColor, self.KnobRect)

    def update(self, Screen):
        self.CheckForMouse()
        self.Draw(Screen)

class ToggleButton(pygame.sprite.Sprite):
    def __init__(self, CenterPos, VariableToCheck):
        super().__init__()

        ToggleButtonsGroup.add(self)

        self.Rect = pygame.Rect(0, 0, 40, 40)
        self.Rect.center = CenterPos

        self.InsideColor = (255, 255, 255)

        self.VariableToCheck = VariableToCheck
        self.Hovered = False

    def CheckIfHovered(self):
        if self.Rect.inflate(-10, -10).collidepoint(pygame.mouse.get_pos()): self.Hovered = True
        else: self.Hovered = False

        if self.Hovered and pygame.mouse.get_pressed()[0] and Config.LEFT_CLICKABLE:
            Config.SpecialEffectsEnabled = not Config.SpecialEffectsEnabled

        if self.VariableToCheck == "SpecialEffects":
            if Config.SpecialEffectsEnabled:
                if self.Hovered: self.InsideColor = (150, 150, 150)
                else: self.InsideColor = (255, 255, 255)
            else:
                if self.Hovered: self.InsideColor = (50, 50, 50)

    def Draw(self, Screen):
        pygame.draw.rect(Screen, "WHITE", self.Rect, 2, 10)

        if self.Hovered or (self.VariableToCheck == "SpecialEffects" and Config.SpecialEffectsEnabled):
            pygame.draw.rect(Screen, self.InsideColor, self.Rect.inflate(-10, -10), 0, 10)

    def update(self, Screen):
        self.CheckIfHovered()
        self.Draw(Screen)