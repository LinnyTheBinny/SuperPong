import pygame
import Config

PaddleGroup = pygame.sprite.Group()

class Paddle(pygame.sprite.Sprite):
    def __init__(self, XPos, UpKey, DownKey):
        super().__init__()

        PaddleGroup.add(self)

        self.MaxVelocity = Config.PADDLE_SPEED
        self.Velocity = 0

        self.YPosition = 250
        self.XPosition = XPos
        self.UpKey = UpKey
        self.DownKey = DownKey

        self.rect = pygame.Rect(0, 0, 8, 100)

    def CheckForMovement(self):
        if Config.GAME_START_INSTRUCTIONS: return

        KeysHeldDown = pygame.key.get_pressed()

        if KeysHeldDown[self.UpKey]:
            self.Velocity = pygame.math.clamp(self.Velocity + 0.4, -self.MaxVelocity, self.MaxVelocity)
        elif KeysHeldDown[self.DownKey]:
            self.Velocity = pygame.math.clamp(self.Velocity - 0.4, -self.MaxVelocity, self.MaxVelocity)
        else:
            if self.Velocity > 0: self.Velocity -= 0.2
            else: self.Velocity += 0.2

        self.YPosition -= self.Velocity

        if pygame.math.clamp(self.YPosition, 50, 450) != self.YPosition: self.Velocity = 0
        self.YPosition = pygame.math.clamp(self.YPosition, 50, 450) # Make sure it stays in boundary

    def Draw(self, Screen):
        self.rect.center = (self.XPosition, self.YPosition)
        pygame.draw.rect(Screen, "WHITE", self.rect)

    def update(self, Screen):
        self.CheckForMovement()
        self.Draw(Screen)