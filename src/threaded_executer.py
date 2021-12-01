
import os
import sys
from front_end import pacman
from optparse import OptionParser

def start_game(args):
    pacman.main(layout=args['layout'],
                num_ghosts=args['ghosts'], 
                frame_time=args['frametime'],
                episodes=args['episodes'],  
                method=args['method'], 
                verbose=args['verbose'], 
                multithreaded=args['multithreaded'])

def do_parse(argv):

    parser = OptionParser()
    usageStr = """
    USAGE:      python pacman.py <options>
    EXAMPLES:   (1) python pacman.py
                    - starts an interactive game
                (2) python pacman.py --layout smallClassic --zoom 2
                OR  python pacman.py -l smallClassic -z 2
                    - starts an interactive game on a smaller board, zoomed in
    """
    parser = OptionParser(usageStr)

    parser.add_option('-l', '--layout', type='string', dest='layout')
    parser.add_option('-e', '--episodes', type='int', dest='episodes')
    parser.add_option('-g', '--ghosts', type='int', dest='ghosts')
    parser.add_option('-f', '--frametime', type='float', dest='frametime')
    parser.add_option('-m', '--method', type='string', dest='method')
    parser.add_option('-v', '--verbose', dest='verbose', default=False)
    parser.add_option('-t', '--multithreaded', dest='multithreaded', default=False)
    
    
    options, otherjunk = parser.parse_args(argv)
    if len(otherjunk) != 0:
        raise Exception('Command line input not understood: ' + str(otherjunk))
    args = dict()

    args['layout'] = options.layout
    args['episodes'] = options.episodes
    args['ghosts'] = options.ghosts
    args['frametime'] = options.frametime
    args['method'] = options.method
    args['verbose'] = bool(options.verbose)
    args['multithreaded'] = bool(options.multithreaded)

    return args

if __name__ == '__main__':

    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)

    args = do_parse(sys.argv[1:] ) # Get game components based on input

    start_game(args)
