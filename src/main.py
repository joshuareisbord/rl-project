import os
from front_end import pacman

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)
pacman.main(layout='SmallClassicTest2', episodes=1, frame_time=0.01)
