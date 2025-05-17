import pygame, math, random, threading, VisualFX, SoundPlayer
import Paddle, Config, UI

BallGroup = pygame.sprite.Group()
PaddleGroup = Paddle.PaddleGroup

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        BallGroup.add(self)

        self.rect = pygame.Rect(0, 0, 10, 10)
        self.rect.center = (Config.SCREEN_SIZE_X / 2, Config.SCREEN_SIZE_Y / 2)

        self.pos_x = Config.SCREEN_SIZE_X / 2
        self.pos_y = Config.SCREEN_SIZE_Y / 2

        self.Speed = 3
        self.XSpeed = 0
        self.YSpeed = 0
        self.PaddleCollisionAllowed = True

        self.GetRandomDirection()

    def GetRandomDirection(self):
        self.Speed = 2

        RandomAngle = math.radians(random.choice([45, 135, 225, 315]))

        self.XSpeed = math.sin(RandomAngle)
        self.YSpeed = math.cos(RandomAngle)

    def BallBounceEffectStart(self, AxisToCheck):
        if not Config.SpecialEffectsEnabled: return

        if AxisToCheck == "Y":
            SoundPlayer.PlaySound("WallHit.mp3", 20 + (round(abs(self.XSpeed * self.Speed) + abs(self.YSpeed * self.Speed), 2)) * 2)

            if self.YSpeed > 0: VisualFX.BallBounceEffect(self.rect.center, 360, 20)
            else: VisualFX.BallBounceEffect(self.rect.center, 180, 20)
        else:
            SoundPlayer.PlaySound("BallBounce.mp3", 20 + (round(abs(self.XSpeed * self.Speed) + abs(self.YSpeed * self.Speed), 2)) * 2)

            if self.XSpeed > 0: VisualFX.BallBounceEffect(self.rect.center, 90, 5)
            else: VisualFX.BallBounceEffect(self.rect.center, 270, 5)

        VisualFX.ScreenShakeMax = (round(abs(self.XSpeed * self.Speed) + abs(self.YSpeed * self.Speed), 2)) / 2

    def CheckForCollision(self):
        Collisions = pygame.sprite.groupcollide(BallGroup, PaddleGroup, False, False, pygame.sprite.collide_rect)

        if Collisions:
            PaddleHit = None

            for _, PaddlesHit in Collisions.items():
                for Paddle in PaddlesHit:
                    PaddleHit = Paddle

            if self.PaddleCollisionAllowed:
                self.BallBounceEffectStart("X")

                self.XSpeed *= -1
                self.YSpeed -= PaddleHit.Velocity * 0.1
                self.PaddleCollisionAllowed = False
                self.Speed *= 1.05
        else:
            self.PaddleCollisionAllowed = True

    def CheckForChangeDirection(self):
        self.CheckForCollision()

        if self.rect.centery > 490 or self.rect.centery < 10:
            self.BallBounceEffectStart("Y")

            self.YSpeed *= -1
            self.Speed *= 1.05

    def CheckForBallScored(self, RedBackground, BlueBackground, Score):
        BallWentToLeft = self.rect.centerx < -20
        BallWentToRight = self.rect.centerx > Config.SCREEN_SIZE_X + 20

        if BallWentToLeft or BallWentToRight:
            SoundPlayer.PlaySound("PointEarned.mp3", 100)

            self.XSpeed = 0
            self.YSpeed = 0

            self.pos_x = Config.SCREEN_SIZE_X / 2
            self.pos_y = Config.SCREEN_SIZE_Y / 2
            self.rect.center = (self.pos_x, self.pos_y)

            threading.Timer(1.5, self.GetRandomDirection).start()

        if BallWentToLeft:
            Score.RightScore += 1
            RedBackground.BackgroundFading = True

        if BallWentToRight:
            Score.LeftScore += 1
            BlueBackground.BackgroundFading = True

    def Move(self):
        if Config.GAME_START_INSTRUCTIONS: return

        self.pos_x += self.XSpeed * self.Speed
        self.pos_y += self.YSpeed * self.Speed

        self.rect.center = (int(self.pos_x), int(self.pos_y))

    def Draw(self, Screen):
        pygame.draw.circle(Screen, "WHITE", self.rect.center, 10)

    def update(self):
        self.Move()
        self.CheckForChangeDirection()