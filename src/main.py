from engine import System
from TestScene import TestScene
from PongScene import PongScene
from TextureTestScene import TextureTestScene
#from Beach import Beach
from StartScreen import StartScreen
#from GameOver import GameOver

system = System()
#scene = TestScene()
#scene = PongScene()
#scene = TextureTestScene()
scene = StartScreen()
#scene = Beach()
#scene = GameOver()
system.push_scene(scene)
system.run() # entra no laço principal do jogo
