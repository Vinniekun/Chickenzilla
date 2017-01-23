from engine import System
from TestScene import TestScene
from PongScene import PongScene
from TextureTestScene import TextureTestScene
from StartScreen import StartScreen


system = System()
scene = StartScreen()
system.push_scene(scene)
system.run()
