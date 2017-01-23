from engine import System
from TestScene import TestScene
from PongScene import PongScene
from TextureTestScene import TextureTestScene
from StartScreen import StartScreen
try:
    import pygame_sdl2
    pygame_sdl2.import_as_pygame()
except ImportError:
    pass

system = System()
scene = StartScreen()
system.push_scene(scene)
system.run()
