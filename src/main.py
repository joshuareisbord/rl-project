import multiprocessing
import os
from front_end import pacman
from multiprocessing import Process
import multiprocessing as mp

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

# Verbose = False will display the GUI. Frame_time lets you control how fast the display is updated.
# Note some small states will cause the game to studder as it is taking longer to calculate A* for that state.
# Verbose = True will just have std output of each game.

if __name__ == "__main__":

# for i in range(mp.cpu_count()//2):
    for i in range(2):
        p = multiprocessing.Process(pacman.main('smallClassicTest2', 2, 0.001, 'QLearning', True))
        p.start()

    # with mp.Pool(processes=mp.cpu_count()//2) as pool:
    #     pool.map(pacman.main, ('smallClassicTest2', 5, 0.001, 'QLearning', False))

    # pacman.main(layout='smallClassicTest2', episodes=2, frame_time=0.001, method='QLearning', verbose=True)
