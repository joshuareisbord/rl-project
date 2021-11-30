import os
from front_end import pacman

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

# Verbose = False will display the GUI. Frame_time lets you control how fast the display is updated.
# Note some small states will cause the game to studder as it is taking longer to calculate A* for that state.
# Verbose = True will just have std output of each game.

pacman.main(layout='smallClassicTest2', episodes=3, frame_time=0.001, method='QLearning', verbose=True)
