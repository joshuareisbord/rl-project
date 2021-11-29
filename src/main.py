import os
from front_end import pacman

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

# if os.environ.get('DISPLAY','') == '':
#     print('no display found. Using :0.0')
#     os.environ.__setitem__('DISPLAY', ':0.0')

pacman.main(layout='mediumGrid', episodes=3, frame_time=0.001)
