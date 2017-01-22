import pygame
from pygame.rect import Rect

from DebugInfo import DebugInfo
from engine import Point, Scene, GameObject
from engine.Animation import Animation
from engine.TileMap import TileMap
from engine import Physics
from random import randrange
from Beach import Beach
from engine.managers import Sound

class StartScreen(Scene):
    def __init__(self):
        Scene.__init__(self, "StartScreen")


    def start(self, game_data):
        # cria e adiciona um gato
        self.game_data = game_data
        self.game_objects.append(Roberto(game_data))
        self.game_objects.append(DebugInfo(game_data))
        self.game_objects.append(Background('bg1', game_data))
        self.game_objects.append(MarChao(game_data))
        self.game_objects.append(Interface(game_data))
        Sound.play('songintro.wav')
        #self.next_bg = 4

        Scene.start(self, game_data)

class Interface(GameObject):
    def __init__(self, game_data):
        GameObject.__init__(self, None, game_data)
        self.timer = 0

    def render(self):
        self.system.blit(ID='title', dest=Rect((620 , 0), (256, 256)), scale=3)
        self.system.blit(ID='spacetorun', dest=Rect((500 , 750), (128, 24)), scale=8)


class Background(GameObject):
    def __init__(self, type, game_data):
        self.animation_names = ['bg1','bg2','bg3','bg4']
        GameObject.__init__(self, 'cenario' , game_data)
        self.current_animation_name = type
        self._layer = -1
        self.scale = 1
        self.dest.topleft = Point(0, 0)


class MarChao(GameObject):
    def __init__(self, game_data):
        self.animation_names = ['marchao']
        GameObject.__init__(self, 'marchao', game_data)
        self.dest.size = self.animation.get_src_size()
        self.scale = 8
        self.dest.topleft = Point(0 , self.screen_size.y - self.rect.h)
        self._layer = 4

class Foguete(GameObject):
    def __init__(self, type, game_data):
        self.animation_names = ['fogo1', 'fogo2', 'fogo3']
        GameObject.__init__(self, 'foguete', game_data)

        self._layer = 2
        self.current_animation_name = type
        self.animation = self.animation_dict[type]
        self.dest.size = self.animation.get_src_size()
        self.scale = 7
        self.dest.topleft = Point(self.screen_size.x - self.rect.w, self.screen_size.y // 2 - self.rect.h)
        self.animation.num_loops = 1

    def update(self):
        if self.animation.is_finished():
            self.kill()
        GameObject.update(self)

from engine import Physics

class Roberto(GameObject):
    STATE_ON_AIR = 1
    STATE_ON_GROUND = 2
    STATE_DOUBLE_JUMP = 3

    #BUFFS!
    BUFF_GRAPE1 = 1
    BUFF_NO_JUMP = 8
    BUFF_DOUBLE_JUMP = 9

    def __init__(self, game_data):
        self.animation_names = ['running', 'jumping']
        GameObject.__init__(self, 'roberto', game_data)

        self.game_data = game_data

        self.dest.size = self.animation.get_src_size()
        self.scale = 1
        #self.dest.topleft = Point(self.screen_size.x // 3, self.screen_size.y - self.rect.h * 1.3)
        self.dest.topleft = Point(self.screen_size.x // 3, 640)
        self.tags.append('roberto')
        self.state = self.STATE_ON_GROUND
        self.vel_y = Point(0,0)
        self.jump_power = Point(0,-2000)
        self.total_gravity = Point(0, 11000)
        self.in_air = Point(0, 100)
        self.gravity = Point(self.total_gravity)
        self.updatable = True
        self.invencible = 0
        self.invencible_state = False
        self.pontos_para_foguete = 0
        self.num_uvas = 0
        self.soltar_foguetes = 2000

        self.pos_roberto_atual = Point(self.screen_size.x - 80, 0)
        self.pos_roberto = Rect((self.pos_roberto_atual), (64, 128))

    def soltar_foguete(self):
        self.scene.game_objects.append(Foguete('fogo3', self.game_data))
        self.scene.layers.add(self.scene.game_objects[-1])

    def update(self):
        self.soltar_foguetes -= self.system.delta_time
        if self.soltar_foguetes <= 0:
            self.soltar_foguete()
            self.soltar_foguetes = 5000

        for event in self.system.get_events():
            if event.type is pygame.KEYDOWN and event.key is pygame.K_SPACE:
                self.system.push_scene(Beach())
                self.scene.state = self.scene.STATE_PAUSED


        GameObject.update(self)