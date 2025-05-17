import pygame, Config, random, math

pygame.init()

# VARIABLES #

ScreenShakeMax = 0

ScreenShakeX = 0
ScreenShakeY = 0

# CLASSES #

WhiteSqaresGroup = pygame.sprite.Group()

class WhiteSquareParticle(pygame.sprite.Sprite):
    def __init__(self, StartPos, Direction):
        super().__init__()

        WhiteSqaresGroup.add(self)

        self.StartPos = StartPos
        self.Direction = Direction

        self.SideLength = random.randrange(5, 20)

        self.ParticleSurface = pygame.Surface((self.SideLength, self.SideLength), pygame.SRCALPHA)

        RandomAngle = math.radians(Direction + random.randrange(-90, 90))

        self.XDirection = math.sin(RandomAngle)
        self.YDirection = math.cos(RandomAngle)

        self.XPos = StartPos[0]
        self.YPos = StartPos[1]

        self.ParticleRect = pygame.Rect(0, 0, self.SideLength, self.SideLength)
        self.ParticleRect.center = StartPos

        self.Rotation = 90
        self.Transparency = 255
        self.RotationSpeed = random.randrange(1, 4)
        self.Scale = 1

    def UpdateSurface(self):
        self.XPos += self.XDirection * 2.5
        self.YPos += self.YDirection * 2.5

        self.Rotation += self.RotationSpeed
        self.Scale -= 0.05
        self.Transparency -= 10

        if self.Transparency <= 0: self.kill()

        self.ParticleRect.center = (round(self.XPos), round(self.YPos))
        self.ParticleSurfaceClone = pygame.transform.rotozoom(self.ParticleSurface, self.Rotation, self.Scale)
        self.ParticleSurfaceClone.set_alpha(self.Transparency)

    def Draw(self, Screen):
        self.ParticleSurface.fill("WHITE")
        Screen.blit(self.ParticleSurfaceClone, self.ParticleRect)

    def update(self, Screen):
        if not Config.GAME_PAUSED: self.UpdateSurface()
        self.Draw(Screen)

# FUNCTIONS #

def BallBounceEffect(StartPos, Direction: int, Amount):
    if not Config.SpecialEffectsEnabled: return

    for Index in range(Amount):
        WhiteSquareParticle(StartPos, Direction)

def UpdateScreenShake():
    global ScreenShakeX, ScreenShakeY, ScreenShakeMax

    ScreenShakeMax -= 0.3
    if ScreenShakeMax < 0: ScreenShakeMax = 0
    if round(ScreenShakeMax) == 0: return

    ScreenShakeX = random.randrange(-round(ScreenShakeMax), round(ScreenShakeMax))
    ScreenShakeY = random.randrange(-round(ScreenShakeMax), round(ScreenShakeMax))