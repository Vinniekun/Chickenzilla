import pygame
from pygame.rect import Rect

from DebugInfo import DebugInfo
from engine import Point, Scene, GameObject
from engine.Animation import Animation
from engine.TileMap import TileMap
from engine import Physics
from random import randrange

class Beach(Scene):
    def __init__(self):
        Scene.__init__(self, "Beach")
        self.num_onda = 0

    def start(self, game_data):
        # cria e adiciona um gato
        self.game_data = game_data
        self.game_objects.append(Roberto(game_data))
        self.game_objects.append(DebugInfo(game_data))
        for bg in range(1,4):
            background = Background('bg' + str(bg), game_data)
            background.dest.topleft = Point((bg-1) * 1920, 0)
            self.game_objects.append(background)
        self.next_bg = 4
        Scene.start(self, game_data)

        #self.system.camera_target = self.game_objects[-2]
        self.intervalo_tempo = 0


    def update(self):
        self.intervalo_tempo += self.system.delta_time
        self.check_onda()
        Scene.update(self)

    def check_onda(self):
        if self.num_onda < 5:
            self.gera_onda()

    def gera_onda(self):
        time = self.rand_onda()
        type = self.rand_type()
        self.num_onda += 1
        self.game_objects.append(Onda(time, type, self.game_data))
        self.layers.add(self.game_objects[-1])
        self.intervalo_tempo = 0

    def gera_fundo(self, pos_x_excluida):
        pos_x_nova = pos_x_excluida + 3 * 1920
        self.game_objects.append(Background('bg' + str(self.next_bg), self.game_data))
        self.game_objects[-1].dest.x = pos_x_nova
        self.layers.add(self.game_objects[-1])

        if self.next_bg + 1 in range(2, 4):
            self.next_bg += 1
        else:
            self.next_bg = 2

    def rand_onda(self):
        #definir um tempo de intervalo para ondas aparecerem
        time = randrange(1000,6000,1000)
        return time

    def rand_type(self):
        type = randrange(1,3)
        if type is 1:
            return 'onda_pequena'
        #elif type is 2:
            #return 'onda_media'
        else:
            return 'onda_grande'

    def fim_onda(self):
        self.num_onda -= 1

    def render(self):
        Scene.render(self)

class Interface(GameObject):
    def __init__(self, game_data):
        GameObject.__init__(self, None, game_data)

    def render(self):
        self.system.blit(ID='interface_fundo', dest=Rect((self.screen_size.x - 260, 0), (256,128)))
        self.system.blit(ID='interface_frango', dest=Rect((self.screen_size.x - 240, 0), (64, 128)))
        self.system.blit(ID='interface_particula', dest=Rect((self.screen_size.x - 200, 0), (64, 128)))
        self.system.blit(ID='interface_particula', dest=Rect((self.screen_size.x - 160, 0), (64, 128)))
        self.system.blit(ID='interface_particula', dest=Rect((self.screen_size.x - 120, 0), (64, 128)))
        self.system.blit(ID='interface_roberto', dest=Rect((self.screen_size.x - 80, 0), (64, 128)))


class Background(GameObject):
    def __init__(self, type, game_data):
        self.animation_names = ['bg1','bg2','bg3','bg4']
        GameObject.__init__(self, 'cenario' , game_data)
        self.current_animation_name = type
        self._layer = -1
        self.scale = 1
        self.dest.topleft = Point(0, 0)

    def update(self):

        self.dest.topleft += Point(-20, 0)
        if self.rect.right <= 0:
            self.kill()
            self.scene.gera_fundo(self.rect.left)
        GameObject.update(self)

    def render(self):
        GameObject.render(self)


class Frango(GameObject):

    STATE_ADVANCING = 1
    STATE_STOP = 2
    STATE_RETREATING = 3

    def __init__(self, game_data):
        self.animation_names = ['running']
        GameObject.__init__(self, 'frango', game_data)

        self.dest.size = self.animation.get_src_size()
        self.scale = 6
        self._layer = 2
        self.state = self.STATE_ADVANCING
        self.aproximacao_x = Point(10,0)
        self.dest.topleft = Point(-self.rect.w, self.screen_size.y // 4)

    def update(self):
        if self.state == self.STATE_ADVANCING:
            self.dest.topleft += self.aproximacao_x
            if self.dest.topleft[0] >= -100:
                self.state = self.STATE_STOP
        GameObject.update(self)


class Onda(GameObject):
    def __init__(self, time, type, game_data):
        GameObject.__init__(self, type, game_data)
        self.scale = 1
        self.tags.append('onda')
        self._layer = 3
        tamanho_onda = self.image.get_size()[1]
        self.inicio_wave = Point(self.screen_size.x + time, self.screen_size.y // 1.15 - tamanho_onda)
        self.dest.topleft = self.inicio_wave
        self.vel_onda = Point(-20, 0)

    def update(self):
        self.dest.bottomleft += self.vel_onda
        self.check_position()
        GameObject.update(self)

    def render(self):
        GameObject.render(self)

    def check_position(self):
        if self.dest.topright[0] <= 0:
            self.scene.fim_onda()
            self.kill()


from engine import Physics

class Roberto(GameObject):
    STATE_ON_AIR = 1
    STATE_ON_GROUND = 2
    STATE_DOUBLE_JUMP = 3

    #BUFFS!
    BUFF_GRAPE1 = 1
    BUFF_GRAPE2 = 2
    BUFF_GRAPE3 = 3
    BUFF_GRAPE4 = 4
    BUFF_GRAPE5 = 5
    BUFF_GRAPE6 = 6
    BUFF_GRAPE7 = 7
    BUFF_NO_JUMP = 8
    BUFF_DOUBLE_JUMP = 9

    def __init__(self, game_data):
        self.animation_names = ['running', 'jumping']
        GameObject.__init__(self, 'roberto', game_data)

        self.game_data = game_data

        self.dest.size = self.animation.get_src_size()
        self.scale = 1
        self.dest.topleft = Point(self.screen_size.x // 3, self.screen_size.y // 1.8)

        self.state = self.STATE_ON_GROUND
        self.vel_y = Point(0,0)
        self.jump_power = Point(0,-2000)
        self.total_gravity = Point(0, 11000)
        self.in_air = Point(0, 100)
        self.gravity = Point(self.total_gravity)
        self.updatable = True
        self.invencible = 0
        self.invencible_state = False

        #posicao da interface
        self.pos_pontos = [Rect((self.screen_size.x - 200, 0), (64, 128)),
                                Rect((self.screen_size.x - 160, 0), (64, 128)),
                                     Rect((self.screen_size.x - 120, 0), (64, 128))]
        self.vidas = len(self.pos_pontos)
        self.pos_roberto_atual = Point(self.screen_size.x - 80, 0)
        self.pos_roberto = Rect((self.pos_roberto_atual), (64, 128))



    def render_interface(self):
        self.system.blit(ID='interface_fundo', dest=Rect((self.screen_size.x - 260, 0), (256, 128)))
        self.system.blit(ID='interface_frango', dest=Rect((self.screen_size.x - 240, 0), (64, 128)))
        for particulas in self.pos_pontos:
            if particulas is not None:
                self.system.blit(ID='interface_particula', dest=particulas)
        self.system.blit(ID='interface_roberto', dest=Rect((self.pos_roberto_atual), (64, 128)))

    def on_collision(self, obj):
        if obj.has_tag("onda") and self.invencible_state is False:
            self.invencible = 2000
            self.invencible_state = True
            #REDUZ A VIDA
            if self.vidas > 0:
                del self.pos_pontos[-1]
                self.vidas -= 1
                self.pos_roberto_atual += Point(-40,0)
                if self.vidas == 0:
                    self.frango_mode()

    def frango_mode(self):
        print("FRANGO MODE!!!!!")
        self.scene.game_objects.append(Frango(self.game_data))
        self.scene.layers.add(self.scene.game_objects[-1])

    def update(self):
        if self.invencible_state:
            self.invencible -= self.system.delta_time
            if self.invencible // 100 % 2 == 0:
                self.renderable = True
            else:
                self.renderable = False
            if self.invencible <= 0:
                self.invencible_state = False
                self.renderable = True

        if self.state is not self.STATE_ON_GROUND:
            self.current_animation_name = 'jumping'
        else:
            self.current_animation_name = 'running'

        if self.state == self.STATE_ON_GROUND:
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self.state = self.STATE_ON_AIR
                self.vel_y = self.jump_power

        #gravidade
        elif self.state == self.STATE_ON_AIR:
            new_pos, self.vel_y = Physics.mruv(self.dest.topleft, self.vel_y, self.gravity, self.system.delta_time)
            self.dest.topleft = new_pos
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                if self.vel_y[1] <= 0:
                    self.vel_y -= self.in_air
            if self.dest.topleft[1] >= self.screen_size.y // 1.8:
                self.state = self.STATE_ON_GROUND
            #se apertar com keydown
            for event in self.system.get_events():
                if event.type is pygame.KEYDOWN and event.key is pygame.K_SPACE:
                    self.state = self.STATE_DOUBLE_JUMP
                    self.vel_y = self.jump_power
                    print("double jump")

        elif self.state == self.STATE_DOUBLE_JUMP:
            new_pos, self.vel_y = Physics.mruv(self.dest.topleft, self.vel_y, self.gravity,
                                           self.system.delta_time)
            self.dest.topleft = new_pos
            if self.dest.topleft[1] >= self.screen_size.y // 1.8:
                self.state = self.STATE_ON_GROUND

        GameObject.update(self)

    def render(self):
        self.render_interface()
        GameObject.render(self)