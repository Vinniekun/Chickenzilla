import pygame
from pygame.rect import Rect

from DebugInfo import DebugInfo
from engine import Point, Scene, GameObject
from engine.Animation import Animation
from engine.TileMap import TileMap
from engine import Physics
from random import randrange
from engine.managers import Sound
try:
    import pygame_sdl2
    pygame_sdl2.import_as_pygame()
except ImportError:
    pass


class GameOver(Scene):
    def __init__(self):
        Scene.__init__(self, "GameOver")


    def start(self, game_data):
        # cria e adiciona um gato
        self.game_data = game_data
        #self.game_objects.append(Roberto(game_data))
        self.game_objects.append(DebugInfo(game_data))
        #self.game_objects.append(Background('bg1', game_data))
        #self.game_objects.append(MarChao(game_data))
        self.game_objects.append(Interface(game_data))
        #Sound.play('songintro.wav')
        #self.next_bg = 4

        Scene.start(self, game_data)

    def update(self):
        Scene.update(self)

    def render(self):
        Scene.render(self)

class Interface(GameObject):
    def __init__(self, game_data):
        GameObject.__init__(self, None, game_data)
        self.timer = 0
        self.surface = pygame.Surface((1920, 1080)).convert_alpha()

    def update(self):
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.system.__del__()
        for event in self.system.get_events():
            if event.type is pygame.KEYDOWN and event.key is pygame.K_SPACE:
                self.system.__del__()
                #self.scene.state = self.scene.STATE_PAUSED
        GameObject.update(self)

    def render(self):
        self.system.screen.blit(self.surface, (0,0))
        self.system.blit(ID='gameover', dest=Rect((300 , 200), (350, 128)), scale=4)
        self.system.blit(ID='spacetorestart', dest=Rect((400 , 750), (150, 24)), scale=8)